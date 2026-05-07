from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"
PARAM_DIR = REPO_ROOT / "data" / "pcsaft_parameters" / "gando_2025"

SOURCE_SUMMARY = REF_DIR / "non_ionic_case_study_process_summary.csv"
SENSITIVITY_INPUT = REF_DIR / "smackover_li_tds_sensitivity_basis.csv"

FIT_JSON = PARAM_DIR / "hbta_topo_reactive_fit.json"
FIT_CSV = REF_DIR / "hbta_topo_reactive_fit_parameters.csv"
STAGE_CSV = REF_DIR / "hbta_topo_reactive_stage_results.csv"
PROMMIS_CSV = REF_DIR / "hbta_topo_reactive_prommis_stage_table.csv"
COST_ASSUMPTIONS_CSV = REF_DIR / "hbta_topo_formal_costing_assumptions.csv"
COST_RESULTS_CSV = REF_DIR / "hbta_topo_formal_costing_results.csv"
REPORT_MD = REF_DIR / "hbta_topo_reactive_model_report.md"

BASE_CASE_ID = "smackover_clean_median_tds_proxy"
TABLE4_CUMULATIVE_LI_PCT = np.asarray([54.95, 85.60, 97.17], dtype=float)
REFERENCE_SELECTIVITY_LI_NA = 2100.0
REFERENCE_LI_FEED_MG_L = 60.0
REFERENCE_NA_FEED_MG_L = 10900.0
REFERENCE_HBTA_MOL_L = 0.015
REFERENCE_TOPO_MOL_L = 0.015
REFERENCE_OA_RATIO = 1.0
REFERENCE_STAGE_COUNT = 3

HOURS_PER_YEAR = 8000.0
LI2CO3_PER_LI = 73.891 / (2.0 * 6.94)

MW_KG_MOL = {
    "Li+": 6.94e-3,
    "Na+": 22.98976928e-3,
    "Cl-": 35.45e-3,
}


@dataclass(frozen=True)
class ReactiveFit:
    log10_beta_li: float
    log10_beta_na: float
    log10_capacity_factor: float
    saltout_gain: float
    saltout_ref_mol_L: float = 10.0
    hbta_stoich_per_li: float = 2.0
    topo_stoich_per_li: float = 1.0
    activity_model: str = "epcsaft_aqueous_gamma_when_available"
    model_status: str = "calibrated_reactive_hbta_topo_not_full_predictive_epcsaft"

    @property
    def beta_li(self) -> float:
        return 10.0 ** self.log10_beta_li

    @property
    def beta_na(self) -> float:
        return 10.0 ** self.log10_beta_na

    @property
    def capacity_factor(self) -> float:
        return 10.0 ** self.log10_capacity_factor


@dataclass(frozen=True)
class ReactiveStageResult:
    stage: int
    li_feed_mol_L: float
    na_feed_mol_L: float
    li_raffinate_mol_L: float
    na_raffinate_mol_L: float
    li_extract_mol_L_org: float
    na_extract_mol_L_org: float
    li_stage_extraction_pct: float
    na_stage_extraction_pct: float
    li_cumulative_extraction_pct: float
    na_cumulative_extraction_pct: float
    d_li: float
    d_na: float
    selectivity_li_na: float
    hbta_consumed_mol_L_org: float
    topo_consumed_mol_L_org: float
    gamma_li: float
    gamma_na: float
    gamma_source: str
    model_status: str


def mg_L_to_mol_L(value_mg_L: float, species: str) -> float:
    return float(value_mg_L) * 1e-6 / MW_KG_MOL[species]


def mol_L_to_mg_L(value_mol_L: float, species: str) -> float:
    return float(value_mol_L) * MW_KG_MOL[species] * 1e6


def _safe_ratio(numerator: float, denominator: float) -> float:
    return float(numerator) / max(float(denominator), 1e-30)


def aqueous_activity_coefficients(li_mol_L: float, na_mol_L: float, cl_mol_L: float) -> tuple[float, float, str]:
    """Return aqueous Li/Na activity coefficients from ePC-SAFT when the local package can evaluate them."""
    try:
        import epcsaft
        from data.epcsaft_properties import pcsaft_prop

        species = ["H2O", "Li+", "Na+", "Cl-"]
        keys = ["H2O-Salt-2001", "Li+", "Na+", "Cl-"]
        fields = ["m", "s", "e", "e_assoc", "vol_a", "assoc_scheme", "z", "dielc", "d_born", "MW", "f_solv"]
        params: dict[str, Any] = {}
        for field in fields:
            values: list[Any] = []
            for key in keys:
                value = pcsaft_prop[key].get(field, 0.0)
                values.append(value(298.15) if callable(value) else value)
            params[field] = values if field == "assoc_scheme" else np.asarray(values, dtype=float)

        h2o_mol_L = 55.34
        charge_balanced_cl = max(float(cl_mol_L), float(li_mol_L) + float(na_mol_L), 1e-12)
        moles = np.asarray([h2o_mol_L, max(li_mol_L, 0.0), max(na_mol_L, 0.0), charge_balanced_cl], dtype=float)
        x = moles / np.sum(moles)
        mix = epcsaft.ePCSAFTMixture.from_params(params, species=species)
        state = mix.state(T=298.15, P=101325.0, x=x, phase="liq")
        gamma = state.activity_coefficient(species=species)
        gamma_li = float(np.clip(gamma["Li+"], 0.05, 20.0))
        gamma_na = float(np.clip(gamma["Na+"], 0.05, 20.0))
        return gamma_li, gamma_na, "epcsaft_from_local_runtime_params"
    except Exception as exc:
        return 1.0, 1.0, f"ideal_fallback_after_{type(exc).__name__}"


def solve_reactive_stage(
    *,
    li_mol_L: float,
    na_mol_L: float,
    cl_mol_L: float,
    hbta_mol_L: float,
    topo_mol_L: float,
    oa_ratio: float,
    fit: ReactiveFit,
    stage: int,
    initial_li_mol_L: float,
    initial_na_mol_L: float,
) -> ReactiveStageResult:
    li = max(float(li_mol_L), 0.0)
    na = max(float(na_mol_L), 0.0)
    oa = max(float(oa_ratio), 1e-30)
    gamma_li, gamma_na, gamma_source = aqueous_activity_coefficients(li, na, cl_mol_L)

    ligand_capacity = min(
        max(float(hbta_mol_L), 0.0) / fit.hbta_stoich_per_li,
        max(float(topo_mol_L), 0.0) / fit.topo_stoich_per_li,
    )
    capacity_mol = fit.capacity_factor * ligand_capacity * oa

    normalized_na = math.log1p(na / max(fit.saltout_ref_mol_L, 1e-30))
    anchor_na = math.log1p(mg_L_to_mol_L(REFERENCE_NA_FEED_MG_L, "Na+") / max(fit.saltout_ref_mol_L, 1e-30))
    saltout_factor = 1.0 + fit.saltout_gain * _safe_ratio(normalized_na, anchor_na)
    saltout_factor = float(np.clip(saltout_factor, 0.05, 20.0))

    # This is a fitted mass-action stage law with explicit 2 HBTA : 1 TOPO : 1 Li
    # capacity accounting. Full organic ePC-SAFT parameters are still absent.
    w_li = fit.beta_li * gamma_li * saltout_factor * li
    w_na = fit.beta_na * gamma_na * na
    denom = 1.0 + w_li + w_na
    li_extracted = min(li * 0.999999, capacity_mol * w_li / denom)
    capacity_left = max(0.0, capacity_mol - li_extracted)
    na_extracted = min(na * 0.999999, capacity_left * w_na / max(1.0 + w_na, 1e-30))

    li_raff = max(li - li_extracted, 0.0)
    na_raff = max(na - na_extracted, 0.0)
    li_d = _safe_ratio(li_extracted / oa, li_raff)
    na_d = _safe_ratio(na_extracted / oa, na_raff)
    selectivity = _safe_ratio(li_d, na_d)

    return ReactiveStageResult(
        stage=stage,
        li_feed_mol_L=li,
        na_feed_mol_L=na,
        li_raffinate_mol_L=li_raff,
        na_raffinate_mol_L=na_raff,
        li_extract_mol_L_org=li_extracted / oa,
        na_extract_mol_L_org=na_extracted / oa,
        li_stage_extraction_pct=100.0 * _safe_ratio(li_extracted, li),
        na_stage_extraction_pct=100.0 * _safe_ratio(na_extracted, na),
        li_cumulative_extraction_pct=100.0 * (1.0 - _safe_ratio(li_raff, initial_li_mol_L)),
        na_cumulative_extraction_pct=100.0 * (1.0 - _safe_ratio(na_raff, initial_na_mol_L)),
        d_li=li_d,
        d_na=na_d,
        selectivity_li_na=selectivity,
        hbta_consumed_mol_L_org=fit.hbta_stoich_per_li * li_extracted / oa,
        topo_consumed_mol_L_org=fit.topo_stoich_per_li * li_extracted / oa,
        gamma_li=gamma_li,
        gamma_na=gamma_na,
        gamma_source=gamma_source,
        model_status=fit.model_status,
    )


def run_reactive_crossflow(
    *,
    li_mg_L: float,
    na_mg_L: float,
    cl_mg_L: float,
    hbta_mol_L: float,
    topo_mol_L: float,
    oa_ratio: float,
    stage_count: int,
    fit: ReactiveFit,
) -> list[ReactiveStageResult]:
    li_initial = mg_L_to_mol_L(li_mg_L, "Li+")
    na_initial = mg_L_to_mol_L(na_mg_L, "Na+")
    cl_mol_L = mg_L_to_mol_L(cl_mg_L, "Cl-")
    li_remaining = li_initial
    na_remaining = na_initial
    stages: list[ReactiveStageResult] = []
    for stage in range(1, int(stage_count) + 1):
        result = solve_reactive_stage(
            li_mol_L=li_remaining,
            na_mol_L=na_remaining,
            cl_mol_L=cl_mol_L,
            hbta_mol_L=hbta_mol_L,
            topo_mol_L=topo_mol_L,
            oa_ratio=oa_ratio,
            fit=fit,
            stage=stage,
            initial_li_mol_L=li_initial,
            initial_na_mol_L=na_initial,
        )
        stages.append(result)
        li_remaining = result.li_raffinate_mol_L
        na_remaining = result.na_raffinate_mol_L
    return stages


def fit_reactive_parameters() -> ReactiveFit:
    target_stage1_li = TABLE4_CUMULATIVE_LI_PCT[0] / 100.0
    target_d_li = target_stage1_li / max(1.0 - target_stage1_li, 1e-30)
    target_d_na = target_d_li / REFERENCE_SELECTIVITY_LI_NA
    target_stage1_na = target_d_na / (1.0 + target_d_na)

    def unpack(x: np.ndarray) -> ReactiveFit:
        return ReactiveFit(
            log10_beta_li=float(x[0]),
            log10_beta_na=float(x[1]),
            log10_capacity_factor=float(x[2]),
            saltout_gain=float(x[3]),
        )

    def residuals(x: np.ndarray) -> np.ndarray:
        fit = unpack(x)
        stages = run_reactive_crossflow(
            li_mg_L=REFERENCE_LI_FEED_MG_L,
            na_mg_L=REFERENCE_NA_FEED_MG_L,
            cl_mg_L=47220.0,
            hbta_mol_L=REFERENCE_HBTA_MOL_L,
            topo_mol_L=REFERENCE_TOPO_MOL_L,
            oa_ratio=REFERENCE_OA_RATIO,
            stage_count=REFERENCE_STAGE_COUNT,
            fit=fit,
        )
        calc_cum = np.asarray([stage.li_cumulative_extraction_pct / 100.0 for stage in stages], dtype=float)
        res = list(2.0 * (calc_cum - TABLE4_CUMULATIVE_LI_PCT / 100.0))
        res.append(8.0 * (stages[0].na_stage_extraction_pct / 100.0 - target_stage1_na))
        res.append(0.5 * (math.log10(max(stages[0].selectivity_li_na, 1e-30)) - math.log10(REFERENCE_SELECTIVITY_LI_NA)))
        return np.asarray(res, dtype=float)

    sol = least_squares(
        residuals,
        x0=np.asarray([2.0, -0.7, 0.0, 1.5], dtype=float),
        bounds=([-3.0, -6.0, -2.0, 0.0], [8.0, 4.0, 1.0, 10.0]),
        xtol=1e-11,
        ftol=1e-11,
        gtol=1e-11,
        max_nfev=400,
    )
    return unpack(sol.x)


def _load_feed_cases() -> pd.DataFrame:
    return pd.read_csv(SENSITIVITY_INPUT)


def _case_value(row: pd.Series, field: str, fallback: float) -> float:
    value = row.get(field)
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return fallback
    text = str(value).strip()
    if text in {"", "not_reported", "not_applicable"}:
        return fallback
    return float(text)


def _trust_label(row: pd.Series, oa_ratio: float) -> str:
    if str(row.get("basis_type")) == "screening_case":
        return "extrapolative_scaling_major_ions"
    if 0.25 <= oa_ratio <= 1.5:
        return "calibrated_reactive_extrapolated_to_smackover"
    return "outside_reactive_fit_oa_sweep"


def _stage_trust_label(row: pd.Series, oa_ratio: float, stage: ReactiveStageResult) -> str:
    if stage.li_cumulative_extraction_pct >= 99.0:
        return "outside_literature_capacity_envelope_near_total_transfer"
    return _trust_label(row, oa_ratio)


def write_fit_artifacts(fit: ReactiveFit) -> None:
    PARAM_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": "hbta_topo_2_to_1_to_1_calibrated_reactive_stage",
        "status": fit.model_status,
        "fit_basis": {
            "primary_stage_targets": TABLE4_CUMULATIVE_LI_PCT.tolist(),
            "primary_stage_source": "Shan/Gando 2025 Table 4, DOI 10.3390/W17152258",
            "stoichiometry_source": "Zhang et al. 2017, DOI 10.1016/j.seppur.2017.07.028",
            "stoichiometry": "2 HBTA : 1 TOPO : 1 Li complex from slope analysis",
            "li_na_selectivity_target": REFERENCE_SELECTIVITY_LI_NA,
        },
        "parameters": asdict(fit),
        "boundary": (
            "This is a calibrated reactive stage law with ePC-SAFT aqueous activity corrections where available. "
            "It is not a full predictive reactive ePC-SAFT LLE model because HBTA, TOPO, diluent, and complex "
            "PC-SAFT parameters are still not available."
        ),
    }
    FIT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    pd.DataFrame(
        [
            {"parameter": key, "value": value, "units": "various", "source": "least_squares_fit"}
            for key, value in asdict(fit).items()
        ]
    ).to_csv(FIT_CSV, index=False)


def write_stage_and_handoff_artifacts(fit: ReactiveFit) -> list[dict[str, Any]]:
    feeds = _load_feed_cases()
    base = feeds.loc[feeds["case_id"].eq(BASE_CASE_ID)].iloc[0]
    fallback_major = {
        "Na_mg_L": float(base["Na_mg_L"]),
        "Cl_mg_L": float(base["Cl_mg_L"]),
    }
    rows: list[dict[str, Any]] = []
    for _, row in feeds.iterrows():
        for oa_ratio in (0.5, 1.0, 1.5):
            stages = run_reactive_crossflow(
                li_mg_L=float(row["Li_mg_L"]),
                na_mg_L=_case_value(row, "Na_mg_L", fallback_major["Na_mg_L"]),
                cl_mg_L=_case_value(row, "Cl_mg_L", fallback_major["Cl_mg_L"]),
                hbta_mol_L=REFERENCE_HBTA_MOL_L,
                topo_mol_L=REFERENCE_TOPO_MOL_L,
                oa_ratio=oa_ratio,
                stage_count=REFERENCE_STAGE_COUNT,
                fit=fit,
            )
            for stage in stages:
                rows.append(
                    {
                        "case_id": row["case_id"],
                        "basis_type": row["basis_type"],
                        "site_id": row["site_id"],
                        "oa_ratio": oa_ratio,
                        "stage": stage.stage,
                        "stage_count": REFERENCE_STAGE_COUNT,
                        "Li_feed_mg_L": row["Li_mg_L"],
                        "Na_feed_mg_L": _case_value(row, "Na_mg_L", fallback_major["Na_mg_L"]),
                        "Cl_feed_mg_L": _case_value(row, "Cl_mg_L", fallback_major["Cl_mg_L"]),
                        "TDS_mg_L": row["TDS_mg_L"],
                        "li_stage_extraction_pct": stage.li_stage_extraction_pct,
                        "na_stage_extraction_pct": stage.na_stage_extraction_pct,
                        "li_cumulative_extraction_pct": stage.li_cumulative_extraction_pct,
                        "na_cumulative_extraction_pct": stage.na_cumulative_extraction_pct,
                        "D_Li": stage.d_li,
                        "D_Na": stage.d_na,
                        "S_Li_Na": stage.selectivity_li_na,
                        "Li_raffinate_mg_L": mol_L_to_mg_L(stage.li_raffinate_mol_L, "Li+"),
                        "Na_raffinate_mg_L": mol_L_to_mg_L(stage.na_raffinate_mol_L, "Na+"),
                        "Li_extract_mg_L_org": mol_L_to_mg_L(stage.li_extract_mol_L_org, "Li+"),
                        "Na_extract_mg_L_org": mol_L_to_mg_L(stage.na_extract_mol_L_org, "Na+"),
                        "HBTA_consumed_mol_L_org": stage.hbta_consumed_mol_L_org,
                        "TOPO_consumed_mol_L_org": stage.topo_consumed_mol_L_org,
                        "gamma_Li": stage.gamma_li,
                        "gamma_Na": stage.gamma_na,
                        "gamma_source": stage.gamma_source,
                        "trust_label": _stage_trust_label(row, oa_ratio, stage),
                        "model_status": stage.model_status,
                    }
                )
    pd.DataFrame(rows).to_csv(STAGE_CSV, index=False)

    base_rows = [
        row
        for row in rows
        if row["case_id"] == BASE_CASE_ID and abs(float(row["oa_ratio"]) - 1.0) < 1e-12
    ]
    with PROMMIS_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["stage", "variable", "value", "units", "prommis_idaes_use", "status"])
        for row in base_rows:
            for variable, units, use in (
                ("li_stage_extraction_pct", "percent", "MSContactor.transfer[Li,stage]"),
                ("na_stage_extraction_pct", "percent", "MSContactor.transfer[Na,stage]"),
                ("li_cumulative_extraction_pct", "percent", "flowsheet.recovery[Li]"),
                ("D_Li", "dimensionless", "distribution_ratio[Li]"),
                ("S_Li_Na", "dimensionless", "selectivity[Li,Na]"),
                ("Li_raffinate_mg_L", "mg/L", "stage.raffinate[Li]"),
                ("Li_extract_mg_L_org", "mg/L organic", "stage.extract[Li]"),
            ):
                writer.writerow(
                    [
                        row["stage"],
                        variable,
                        row[variable],
                        units,
                        use,
                        row["model_status"],
                    ]
                )
    return rows


def write_costing(rows: list[dict[str, Any]]) -> None:
    base = next(
        row
        for row in rows
        if row["case_id"] == BASE_CASE_ID and abs(float(row["oa_ratio"]) - 1.0) < 1e-12 and int(row["stage"]) == 3
    )
    assumptions = [
        ("Li2CO3_price_low_usd_kg", 12.0, "USD/kg", "scenario assumption, not market quote"),
        ("Li2CO3_price_base_usd_kg", 20.0, "USD/kg", "scenario assumption, not market quote"),
        ("Li2CO3_price_high_usd_kg", 35.0, "USD/kg", "scenario assumption, not market quote"),
        ("pretreatment_low_usd_m3", 2.0, "USD/m3 feed", "placeholder for Ca/Mg removal"),
        ("pretreatment_base_usd_m3", 5.0, "USD/m3 feed", "placeholder for Ca/Mg removal"),
        ("pretreatment_high_usd_m3", 10.0, "USD/m3 feed", "placeholder for Ca/Mg removal"),
        ("extraction_opex_base_usd_m3", 3.0, "USD/m3 feed", "contacting, pumping, phase disengagement placeholder"),
        ("concentration_precip_base_usd_m3", 6.0, "USD/m3 feed", "stripping/concentration/Li2CO3 precipitation placeholder"),
        ("solvent_makeup_low_usd_m3", 0.5, "USD/m3 feed", "low loss scenario"),
        ("solvent_makeup_base_usd_m3", 2.0, "USD/m3 feed", "base loss scenario"),
        ("solvent_makeup_high_usd_m3", 6.0, "USD/m3 feed", "high loss scenario"),
        ("annual_charge_factor", 0.20, "1/year", "conceptual annualized capex factor"),
        ("contactor_capex_usd_per_m3_day", 15000.0, "USD/(m3/day)", "Class-5 placeholder"),
    ]
    pd.DataFrame(assumptions, columns=["assumption", "value", "units", "notes"]).to_csv(COST_ASSUMPTIONS_CSV, index=False)

    scenarios = [
        ("low", 100.0, 12.0, 2.0, 0.5, 0.75),
        ("base", 1000.0, 20.0, 5.0, 2.0, 1.0),
        ("high", 10000.0, 35.0, 10.0, 6.0, 1.5),
    ]
    cost_rows: list[dict[str, Any]] = []
    model_li_recovery_pct = float(base["li_cumulative_extraction_pct"])
    costing_li_recovery_pct = min(model_li_recovery_pct, float(TABLE4_CUMULATIVE_LI_PCT[-1]))
    li_recovery = costing_li_recovery_pct / 100.0
    for scenario, flow_m3_day, price, pretreat, solvent, capex_multiplier in scenarios:
        liters_year = flow_m3_day * 1000.0 * HOURS_PER_YEAR / 24.0
        feed_m3_year = flow_m3_day * HOURS_PER_YEAR / 24.0
        li_feed_kg_year = liters_year * float(base["Li_feed_mg_L"]) / 1e6
        li_recovered_kg_year = li_feed_kg_year * li_recovery
        li2co3_t_year = li_recovered_kg_year * LI2CO3_PER_LI / 1000.0
        revenue = li2co3_t_year * 1000.0 * price
        extraction_opex = feed_m3_year * 3.0
        concentration_opex = feed_m3_year * 6.0
        pretreat_opex = feed_m3_year * pretreat
        solvent_opex = feed_m3_year * solvent
        capex = flow_m3_day * 15000.0 * capex_multiplier
        annualized_capex = capex * 0.20
        total_annual_cost = extraction_opex + concentration_opex + pretreat_opex + solvent_opex + annualized_capex
        cost_rows.append(
            {
                "scenario": scenario,
                "feed_flow_m3_day": flow_m3_day,
                "Li_feed_mg_L": base["Li_feed_mg_L"],
                "TDS_mg_L": base["TDS_mg_L"],
                "Li_recovery_pct_model": model_li_recovery_pct,
                "Li_recovery_pct_used_for_costing": costing_li_recovery_pct,
                "Li_recovery_costing_basis": "min(model_result, Shan/Gando Table 4 97.17 pct anchor)",
                "Li_feed_kg_year": li_feed_kg_year,
                "Li_recovered_kg_year": li_recovered_kg_year,
                "Li2CO3_product_t_year": li2co3_t_year,
                "Li2CO3_price_usd_kg": price,
                "gross_revenue_usd_year": revenue,
                "pretreatment_opex_usd_year": pretreat_opex,
                "extraction_opex_usd_year": extraction_opex,
                "concentration_precip_opex_usd_year": concentration_opex,
                "solvent_makeup_opex_usd_year": solvent_opex,
                "installed_contactor_capex_usd": capex,
                "annualized_capex_usd_year": annualized_capex,
                "total_annual_cost_usd_year": total_annual_cost,
                "net_before_tax_usd_year": revenue - total_annual_cost,
                "cost_status": "formal_class5_placeholder_not_vendor_quote",
            }
        )
    pd.DataFrame(cost_rows).to_csv(COST_RESULTS_CSV, index=False)


def write_report(fit: ReactiveFit, rows: list[dict[str, Any]]) -> None:
    base_rows = [
        row
        for row in rows
        if row["case_id"] == BASE_CASE_ID and abs(float(row["oa_ratio"]) - 1.0) < 1e-12
    ]
    lines = [
        "# HBTA/TOPO Reactive Stage Model And Costing",
        "",
        "## What Changed",
        "",
        "The old Smackover Phase 6-8 path used a selective wrapper. This artifact adds a calibrated reactive-stage model with the literature-supported `2 HBTA : 1 TOPO : 1 Li` complex stoichiometry and ePC-SAFT aqueous activity coefficients when the local runtime can evaluate them.",
        "",
        "## Scientific Boundary",
        "",
        "This is still not a full predictive reactive ePC-SAFT LLE calculation. HBTA, TOPO, sulfonated kerosene/diluent, Li-complex, and competing divalent-complex ePC-SAFT parameters remain unresolved. The new model is a better bridge because its chemistry is explicit and fitted to source-backed stage data, but it is still a calibrated stage law.",
        "",
        "## Sources Used",
        "",
        "- Shan/Gando 2025, DOI `10.3390/W17152258`: Table 4 three-stage lithium extraction after impurity removal.",
        "- Zhang et al. 2017, DOI `10.1016/j.seppur.2017.07.028`: HBTA/TOPO slope-analysis stoichiometry and Li/Na selectivity anchor.",
        "- Zhang et al. 2018, DOI `10.1016/j.hydromet.2017.10.029`: HBTA/TOPO/kerosene process support.",
        "",
        "## Fitted Parameters",
        "",
        f"- `log10_beta_li = {fit.log10_beta_li:.8f}`",
        f"- `log10_beta_na = {fit.log10_beta_na:.8f}`",
        f"- `log10_capacity_factor = {fit.log10_capacity_factor:.8f}`",
        f"- `saltout_gain = {fit.saltout_gain:.8f}`",
        "",
        "## MS-2 Base Case, O/A = 1",
        "",
        "| Stage | Li stage (%) | Li cumulative (%) | Na stage (%) | Selectivity | Raffinate Li (mg/L) |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in base_rows:
        lines.append(
            f"| {int(row['stage'])} | {float(row['li_stage_extraction_pct']):.4f} | "
            f"{float(row['li_cumulative_extraction_pct']):.4f} | {float(row['na_stage_extraction_pct']):.6f} | "
            f"{float(row['S_Li_Na']):.2f} | {float(row['Li_raffinate_mg_L']):.4f} |"
        )
    lines.extend(
        [
            "",
            "For formal costing, lithium recovery is capped at the source-backed `97.17%` Shan/Gando three-stage anchor when the extrapolated Smackover stage model predicts near-total transfer.",
            "",
            "## Generated Files",
            "",
            f"- `{FIT_JSON.relative_to(REPO_ROOT)}`",
            f"- `{FIT_CSV.relative_to(REPO_ROOT)}`",
            f"- `{STAGE_CSV.relative_to(REPO_ROOT)}`",
            f"- `{PROMMIS_CSV.relative_to(REPO_ROOT)}`",
            f"- `{COST_ASSUMPTIONS_CSV.relative_to(REPO_ROOT)}`",
            f"- `{COST_RESULTS_CSV.relative_to(REPO_ROOT)}`",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    fit = fit_reactive_parameters()
    write_fit_artifacts(fit)
    rows = write_stage_and_handoff_artifacts(fit)
    write_costing(rows)
    write_report(fit, rows)
    print(f"Saved fit: {FIT_JSON}")
    print(f"Saved stage results: {STAGE_CSV}")
    print(f"Saved PrOMMiS/IDAES table: {PROMMIS_CSV}")
    print(f"Saved costing: {COST_RESULTS_CSV}")
    print(f"Saved report: {REPORT_MD}")


if __name__ == "__main__":
    main()
