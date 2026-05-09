from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ANALYSIS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
INPUT_DIR = ANALYSIS_DIR / "data" / "input"
PROCESSED_DIR = ANALYSIS_DIR / "data" / "processed"
RESULTS_DIR = ANALYSIS_DIR / "results" / "bridge"
REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"

TARGET_SUMMARY = PROCESSED_DIR / "rezaee_2025_extraction_target_summary.csv"
EQUILIBRIUM_SUMMARY = PROCESSED_DIR / "rezaee_2025_extraction_equilibrium_summary.csv"
REACTION_CONSTANTS = INPUT_DIR / "rezaee_2026_reaction_constants.csv"
ORGANIC_PARAMS = INPUT_DIR / "rezaee_2026_organic_pcsaft_parameters.csv"
ORGANIC_KIJ = INPUT_DIR / "rezaee_2026_organic_binary_interactions.csv"
PHASE_SMOKE_JSON = RESULTS_DIR.parent / "smoke" / "rezaee_2026_epcsaft_phase_equilibrium_smoke.json"
CONVENTION_SCAN_JSON = RESULTS_DIR.parent / "reaction_equilibrium" / "rezaee_2026_reactive_convention_scan_summary.json"
OPTION_SCAN_JSON = RESULTS_DIR.parent / "reaction_equilibrium" / "rezaee_2026_reactive_epcsaft_option_scan_summary.json"
PAPER_BASIS_JSON = (
    RESULTS_DIR.parent / "reaction_equilibrium" / "rezaee_2026_paper_basis_reaction_coordinate_summary.json"
)
SECTION32_JSON = (
    RESULTS_DIR.parent / "reaction_equilibrium" / "rezaee_2026_section32_equilibrium_replication_summary.json"
)
BASIS_INFERENCE_JSON = (
    RESULTS_DIR.parent / "reaction_equilibrium" / "rezaee_2026_section32_basis_inference_summary.json"
)
SMACKOVER_BASIS = REF_DIR / "smackover_li_tds_sensitivity_basis.csv"

DIST_COEFFS = PROCESSED_DIR / "rezaee_li_na_distribution_coefficients.csv"
SURROGATE_GRID = PROCESSED_DIR / "rezaee_smackover_tds_na_sensitivity.csv"
PROMMIS_HANDOFF = RESULTS_DIR / "rezaee_prommis_idaes_transfer_handoff.csv"
COSTING_INPUT = RESULTS_DIR / "rezaee_idaes_costing_input.csv"
BRIDGE_REPORT = RESULTS_DIR / "rezaee_li_na_distribution_bridge_report.md"

LEGACY_DIST_COEFFS = REF_DIR / "rezaee_li_na_distribution_coefficients.csv"
LEGACY_SURROGATE_GRID = REF_DIR / "rezaee_smackover_tds_na_sensitivity.csv"
LEGACY_PROMMIS_HANDOFF = REF_DIR / "rezaee_prommis_idaes_transfer_handoff.csv"
LEGACY_COSTING_INPUT = REF_DIR / "rezaee_idaes_costing_input.csv"
LEGACY_BRIDGE_REPORT = REF_DIR / "rezaee_li_na_distribution_bridge_report.md"

SELECTED_REZAEE_OPERATING_POINT = {
    "T_C": 23.0,
    "pH": 10.4,
    "topo_wt_pct": 10.0,
    "oa_ratio": 1.0,
    "stage_count": 3,
    "basis": "Rezaee2025_Table7_run_03",
}

HOURS_PER_YEAR = 8000.0
LI2CO3_PER_LI = 73.891 / (2.0 * 6.94)
MODEL_STATUS = "rezaee_source_regressed_li_na_bridge_with_direct_closure_gap"


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _fraction(value_pct: float) -> float:
    return min(max(float(value_pct) / 100.0, 1e-6), 1.0 - 1e-6)


def _distribution_from_extraction(extraction_pct: float, oa_ratio: float) -> float:
    frac = _fraction(extraction_pct)
    return frac / (1.0 - frac) / oa_ratio


def _stage_cumulative(stage_extraction_pct: float, stage_count: int) -> float:
    frac = _fraction(stage_extraction_pct)
    return 100.0 * (1.0 - (1.0 - frac) ** stage_count)


def _logit(pct: float) -> float:
    frac = _fraction(pct)
    return math.log(frac / (1.0 - frac))


def _inv_logit(value: float) -> float:
    if value >= 0:
        z = math.exp(-value)
        return 1.0 / (1.0 + z)
    z = math.exp(value)
    return z / (1.0 + z)


def _load_phase_smoke() -> dict[str, Any]:
    if not PHASE_SMOKE_JSON.exists():
        return {"status": "not_available"}
    with PHASE_SMOKE_JSON.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_convention_scan() -> dict[str, Any]:
    if not CONVENTION_SCAN_JSON.exists():
        return {"status": "not_available"}
    with CONVENTION_SCAN_JSON.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "not_available"}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_targets() -> pd.DataFrame:
    if not TARGET_SUMMARY.exists():
        raise FileNotFoundError(f"{TARGET_SUMMARY} is missing. Run rezaee_2025_target_summary.py first.")
    df = pd.read_csv(TARGET_SUMMARY)
    df = df.dropna(subset=["li_extraction_pct_exp", "na_extraction_pct_exp"])
    selected = SELECTED_REZAEE_OPERATING_POINT
    for column, fallback in {
        "T_C": selected["T_C"],
        "pH": selected["pH"],
        "topo_wt_pct": selected["topo_wt_pct"],
    }.items():
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(float(fallback))
    df["na_li_mass_ratio"] = pd.to_numeric(df["na_li_mass_ratio"], errors="coerce")
    real_mask = df["target_group"].eq("real_brine_table8")
    if real_mask.any():
        real = pd.read_csv(INPUT_DIR / "rezaee_2025_real_brine_extraction.csv")
        li = real.loc[real["ion"].eq("Li"), "synthetic_initial_ppm"].astype(float).iloc[0]
        na = real.loc[real["ion"].eq("Na"), "synthetic_initial_ppm"].astype(float).iloc[0]
        df.loc[real_mask, "na_li_mass_ratio"] = na / li
    df["na_li_mass_ratio"] = df["na_li_mass_ratio"].fillna(df["na_li_mass_ratio"].median())
    return df


def _load_smackover_base() -> pd.Series:
    df = pd.read_csv(SMACKOVER_BASIS)
    base = df.loc[df["case_id"].eq("smackover_clean_median_tds_proxy")]
    if base.empty:
        raise RuntimeError("Missing smackover_clean_median_tds_proxy row.")
    return base.iloc[0]


def _design_matrix(df: pd.DataFrame) -> np.ndarray:
    ratio = np.log(np.maximum(df["na_li_mass_ratio"].astype(float).to_numpy(), 1e-9))
    return np.column_stack(
        [
            np.ones(len(df)),
            (df["T_C"].astype(float).to_numpy() - 30.0) / 10.0,
            (df["pH"].astype(float).to_numpy() - 10.0),
            (df["topo_wt_pct"].astype(float).to_numpy() - 20.0) / 10.0,
            ratio,
        ]
    )


def _fit_ridge(x: np.ndarray, y: np.ndarray, penalty: float = 0.25) -> np.ndarray:
    reg = penalty * np.eye(x.shape[1])
    reg[0, 0] = 0.0
    return np.linalg.solve(x.T @ x + reg, x.T @ y)


def _distribution_rows(targets: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, float]]:
    equilibrium = pd.read_csv(EQUILIBRIUM_SUMMARY) if EQUILIBRIUM_SUMMARY.exists() else pd.DataFrame()
    eq_li_median = float(equilibrium["li_distribution_molfrac_ratio"].median()) if not equilibrium.empty else math.nan
    eq_na_median = float(equilibrium["na_distribution_molfrac_ratio"].median()) if not equilibrium.empty else math.nan
    eq_selectivity_median = (
        float(equilibrium["li_na_selectivity_molfrac_proxy"].median()) if not equilibrium.empty else math.nan
    )

    rows: list[dict[str, Any]] = []
    for _, row in targets.iterrows():
        li_e = float(row["li_extraction_pct_exp"])
        na_e = float(row["na_extraction_pct_exp"])
        d_li = _distribution_from_extraction(li_e, SELECTED_REZAEE_OPERATING_POINT["oa_ratio"])
        d_na = _distribution_from_extraction(na_e, SELECTED_REZAEE_OPERATING_POINT["oa_ratio"])
        rows.append(
            {
                "target_group": row["target_group"],
                "target_id": row["target_id"],
                "source": row["source"],
                "T_C": float(row["T_C"]),
                "pH": float(row["pH"]),
                "topo_wt_pct": float(row["topo_wt_pct"]),
                "na_li_mass_ratio": float(row["na_li_mass_ratio"]),
                "oa_ratio_assumed": SELECTED_REZAEE_OPERATING_POINT["oa_ratio"],
                "li_extraction_pct_exp": li_e,
                "na_extraction_pct_exp": na_e,
                "D_Li_from_extraction": d_li,
                "D_Na_from_extraction": d_na,
                "S_Li_Na_from_extraction": d_li / d_na,
                "si_median_D_Li_molfrac_proxy": eq_li_median,
                "si_median_D_Na_molfrac_proxy": eq_na_median,
                "si_median_S_Li_Na_molfrac_proxy": eq_selectivity_median,
                "model_status": MODEL_STATUS,
                "notes": (
                    "Distribution coefficients use D = E/(1-E)/(O/A) on an assumed equal-phase-volume basis. "
                    "SI mole-fraction ratios are kept as equilibrium-composition evidence, not as extraction percentages."
                ),
            }
        )

    stats = {
        "median_D_Li": float(np.median([r["D_Li_from_extraction"] for r in rows])),
        "median_D_Na": float(np.median([r["D_Na_from_extraction"] for r in rows])),
        "median_S_Li_Na": float(np.median([r["S_Li_Na_from_extraction"] for r in rows])),
        "si_median_D_Li": eq_li_median,
        "si_median_D_Na": eq_na_median,
        "si_median_S_Li_Na": eq_selectivity_median,
    }
    return rows, stats


def _sensitivity_grid(targets: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, float]]:
    base = _load_smackover_base()
    x = _design_matrix(targets)
    li_beta = _fit_ridge(x, np.asarray([_logit(v) for v in targets["li_extraction_pct_exp"]]))
    na_beta = _fit_ridge(x, np.asarray([_logit(v) for v in targets["na_extraction_pct_exp"]]))

    li_feed = float(base["Li_mg_L"])
    base_na = float(base["Na_mg_L"])
    base_tds = float(base["TDS_mg_L"])
    rows: list[dict[str, Any]] = []
    for tds_mult in [0.5, 0.75, 1.0, 1.25, 1.5]:
        for na_mult in [0.5, 1.0, 1.5, 2.0]:
            for oa_ratio in [0.5, 1.0, 1.5]:
                na_feed = base_na * na_mult
                tds = base_tds * tds_mult
                na_li = na_feed / li_feed
                feature = pd.DataFrame(
                    [
                        {
                            "T_C": SELECTED_REZAEE_OPERATING_POINT["T_C"],
                            "pH": SELECTED_REZAEE_OPERATING_POINT["pH"],
                            "topo_wt_pct": SELECTED_REZAEE_OPERATING_POINT["topo_wt_pct"],
                            "na_li_mass_ratio": na_li,
                        }
                    ]
                )
                row_x = _design_matrix(feature)
                li_e = 100.0 * _inv_logit(float(np.dot(row_x[0], li_beta)))
                na_e = 100.0 * _inv_logit(float(np.dot(row_x[0], na_beta)))
                d_li = _distribution_from_extraction(li_e, oa_ratio)
                d_na = _distribution_from_extraction(na_e, oa_ratio)
                stage_count = int(SELECTED_REZAEE_OPERATING_POINT["stage_count"])
                trust = "extrapolated_smackover_na_li_ratio"
                if 5.0 <= na_li <= 25.0:
                    trust = "inside_rezaee_doe_na_li_ratio"
                elif na_li <= 1200.0:
                    trust = "anchored_by_rezaee_real_brine_high_na_li"
                rows.append(
                    {
                        "case_id": f"rezaee_ms2_tds{tds_mult:g}_na{na_mult:g}_oa{oa_ratio:g}",
                        "source_feed": "MS-2 Smackover base row with explicit Na/TDS sensitivity multipliers",
                        "TDS_mg_L": tds,
                        "Li_feed_mg_L": li_feed,
                        "Na_feed_mg_L": na_feed,
                        "na_li_mass_ratio": na_li,
                        "T_C": SELECTED_REZAEE_OPERATING_POINT["T_C"],
                        "pH": SELECTED_REZAEE_OPERATING_POINT["pH"],
                        "topo_wt_pct": SELECTED_REZAEE_OPERATING_POINT["topo_wt_pct"],
                        "oa_ratio": oa_ratio,
                        "stage_count": stage_count,
                        "one_stage_Li_extraction_pct": li_e,
                        "one_stage_Na_extraction_pct": na_e,
                        "one_stage_D_Li": d_li,
                        "one_stage_D_Na": d_na,
                        "one_stage_S_Li_Na": d_li / d_na,
                        "three_stage_Li_cumulative_pct": _stage_cumulative(li_e, stage_count),
                        "three_stage_Na_cumulative_pct": _stage_cumulative(na_e, stage_count),
                        "model_status": MODEL_STATUS,
                        "trust_label": trust,
                        "notes": (
                            "TDS is carried as a surrogate/process feature. The fitted extraction response is driven by Rezaee "
                            "T, pH, TOPO loading, and Na/Li ratio; additional TDS effects require a stronger electrolyte-LLE objective."
                        ),
                    }
                )

    metrics = {
        "li_logit_rmse": float(
            np.sqrt(np.mean((x @ li_beta - np.asarray([_logit(v) for v in targets["li_extraction_pct_exp"]])) ** 2))
        ),
        "na_logit_rmse": float(
            np.sqrt(np.mean((x @ na_beta - np.asarray([_logit(v) for v in targets["na_extraction_pct_exp"]])) ** 2))
        ),
    }
    return rows, metrics


def _write_handoff(
    base_row: dict[str, Any],
    stats: dict[str, float],
    phase_smoke: dict[str, Any],
    convention_scan: dict[str, Any],
    option_scan: dict[str, Any],
    paper_basis: dict[str, Any],
    section32: dict[str, Any],
    basis_inference: dict[str, Any],
) -> None:
    stability = phase_smoke.get("electrolyte_stability", {})
    lle = phase_smoke.get("electrolyte_lle", {})
    source_variant = convention_scan.get("source_supported_variant", {})
    best_variant = convention_scan.get("best_variant", {})
    best_option = option_scan.get("best_option", {})
    paper_best = paper_basis.get("best_mode_by_li_abs_error", {})
    section32_direct = section32.get("direct_held2014_table9_pH_stoich", {})
    section32_best = section32.get("best_case", {})
    basis_conservation = basis_inference.get("conservation_diagnostics", {})
    basis_diagnostics = basis_inference.get("basis_diagnostics", {})
    rows = [
        ("feed_li_mg_L", base_row["Li_feed_mg_L"], "mg/L", "MS-2 source feed", "aqueous_feed[Li]"),
        ("feed_na_mg_L", base_row["Na_feed_mg_L"], "mg/L", "MS-2 source feed", "aqueous_feed[Na]"),
        ("tds_mg_L", base_row["TDS_mg_L"], "mg/L", "MS-2 source feed", "surrogate_feature_tds"),
        ("oa_ratio", base_row["oa_ratio"], "dimensionless", "case-study design variable", "MSContactor.OA_ratio"),
        (
            "D_Li_stage1",
            base_row["one_stage_D_Li"],
            "dimensionless",
            "Rezaee source-regressed bridge",
            "distribution_ratio[Li]",
        ),
        (
            "D_Na_stage1",
            base_row["one_stage_D_Na"],
            "dimensionless",
            "Rezaee source-regressed bridge",
            "distribution_ratio[Na]",
        ),
        (
            "S_Li_Na_stage1",
            base_row["one_stage_S_Li_Na"],
            "dimensionless",
            "Rezaee source-regressed bridge",
            "selectivity[Li,Na]",
        ),
        (
            "eta_li_stage1_pct",
            base_row["one_stage_Li_extraction_pct"],
            "percent",
            "Rezaee source-regressed bridge",
            "transfer[Li]",
        ),
        (
            "eta_na_stage1_pct",
            base_row["one_stage_Na_extraction_pct"],
            "percent",
            "Rezaee source-regressed bridge",
            "transfer[Na]",
        ),
        (
            "eta_li_stage3_pct",
            base_row["three_stage_Li_cumulative_pct"],
            "percent",
            "Rezaee source-regressed bridge",
            "flowsheet_recovery[Li]",
        ),
        (
            "eta_na_stage3_pct",
            base_row["three_stage_Na_cumulative_pct"],
            "percent",
            "Rezaee source-regressed bridge",
            "flowsheet_recovery[Na]",
        ),
        (
            "median_source_D_Li",
            stats["median_D_Li"],
            "dimensionless",
            "Rezaee extraction targets",
            "surrogate_prior[Li]",
        ),
        (
            "median_source_D_Na",
            stats["median_D_Na"],
            "dimensionless",
            "Rezaee extraction targets",
            "surrogate_prior[Na]",
        ),
        (
            "epcsaft_stability_min_tpd",
            stability.get("min_tpd", ""),
            "dimensionless",
            "ePC-SAFT diagnostic smoke",
            "validity_diagnostic",
        ),
        (
            "epcsaft_lle_status",
            lle.get("status", "not_available"),
            "label",
            "ePC-SAFT diagnostic smoke",
            "validity_diagnostic",
        ),
        (
            "epcsaft_lle_split_detected",
            lle.get("split_detected", ""),
            "boolean",
            "ePC-SAFT diagnostic smoke",
            "validity_diagnostic",
        ),
        (
            "direct_reactive_closure_status",
            convention_scan.get("status", "not_available"),
            "label",
            "Rezaee published-constant convention scan",
            "validity_diagnostic",
        ),
        (
            "direct_reactive_source_variant",
            source_variant.get("variant", ""),
            "label",
            "Rezaee published-constant convention scan",
            "validity_diagnostic",
        ),
        (
            "direct_reactive_source_combined_median_abs_ln_residual",
            source_variant.get("combined_median_abs_ln_residual", ""),
            "ln units",
            "Rezaee published-constant convention scan",
            "validity_diagnostic",
        ),
        (
            "direct_reactive_best_simple_variant",
            best_variant.get("variant", ""),
            "label",
            "Rezaee published-constant convention scan",
            "validity_diagnostic",
        ),
        (
            "direct_reactive_best_simple_combined_median_abs_ln_residual",
            best_variant.get("combined_median_abs_ln_residual", ""),
            "ln units",
            "Rezaee published-constant convention scan",
            "validity_diagnostic",
        ),
        (
            "direct_reactive_rows_available",
            convention_scan.get("equilibrium_rows_available", ""),
            "count",
            "Rezaee source-data audit",
            "validity_diagnostic",
        ),
        (
            "direct_reactive_rows_used_as_benchmark",
            convention_scan.get("equilibrium_rows_used_as_benchmark", ""),
            "count",
            "Rezaee source-data audit",
            "validity_diagnostic",
        ),
        (
            "best_epcsaft_aqueous_option",
            best_option.get("option_id", ""),
            "label",
            "Rezaee ePC-SAFT aqueous option scan",
            "validity_diagnostic",
        ),
        (
            "best_epcsaft_aqueous_option_combined_median_abs_ln_residual",
            best_option.get("combined_median_abs_ln_residual", ""),
            "ln units",
            "Rezaee ePC-SAFT aqueous option scan",
            "validity_diagnostic",
        ),
        (
            "paper_basis_reaction_coordinate_best_mode",
            paper_best.get("mode", ""),
            "label",
            "Rezaee paper-basis reaction-coordinate benchmark",
            "validity_diagnostic",
        ),
        (
            "paper_basis_reaction_coordinate_median_oh_to_li_ratio",
            paper_best.get("median_oh_to_li_mol_ratio", ""),
            "mol/mol",
            "Rezaee paper-basis reaction-coordinate benchmark",
            "validity_diagnostic",
        ),
        (
            "paper_basis_reaction_coordinate_median_li_extraction_pct_calc",
            paper_best.get("median_li_extraction_pct_calc", ""),
            "percent",
            "Rezaee paper-basis reaction-coordinate benchmark",
            "validity_diagnostic",
        ),
        (
            "section32_direct_li_extraction_aard_pct",
            section32_direct.get("Li_extraction_AARD_pct", ""),
            "percent",
            "Rezaee Section 3.2 equation replication",
            "validity_diagnostic",
        ),
        (
            "section32_direct_selectivity_aard_pct",
            section32_direct.get("selectivity_AARD_pct", ""),
            "percent",
            "Rezaee Section 3.2 equation replication",
            "validity_diagnostic",
        ),
        (
            "section32_best_diagnostic_case",
            section32_best.get("case_id", ""),
            "label",
            "Rezaee Section 3.2 equation replication",
            "validity_diagnostic",
        ),
        (
            "section32_basis_median_org_total_RLi_over_RNa",
            basis_conservation.get("median_N_org_total_RLi_over_RNa", ""),
            "dimensionless",
            "Rezaee Section 3.2 initial-basis inference",
            "validity_diagnostic",
        ),
        (
            "section32_basis_median_xOH_SI_over_pH_estimate",
            basis_diagnostics.get("median_xOH_SI_over_pH_estimate", ""),
            "dimensionless",
            "Rezaee Section 3.2 initial-basis inference",
            "validity_diagnostic",
        ),
        ("validity_status", base_row["trust_label"], "label", "trust-region diagnostic", "surrogate_validity_flag"),
    ]
    _write_csv(
        PROMMIS_HANDOFF,
        [
            {
                "variable": item[0],
                "value": item[1],
                "units": item[2],
                "source": item[3],
                "prommis_idaes_use": item[4],
            }
            for item in rows
        ],
    )
    _write_csv(
        LEGACY_PROMMIS_HANDOFF,
        [dict(zip(["variable", "value", "units", "source", "prommis_idaes_use"], item)) for item in rows],
    )


def _write_costing(base_row: dict[str, Any]) -> None:
    rows: list[dict[str, Any]] = []
    recovery_fraction = _fraction(float(base_row["three_stage_Li_cumulative_pct"]))
    for scenario, flow_m3_day, price_usd_t in [
        ("low", 100.0, 12000.0),
        ("base", 1000.0, 20000.0),
        ("high", 10000.0, 35000.0),
    ]:
        liters_per_year = flow_m3_day * 1000.0 * HOURS_PER_YEAR / 24.0
        li_kg_year_feed = liters_per_year * float(base_row["Li_feed_mg_L"]) / 1e6
        li_kg_year_recovered = li_kg_year_feed * recovery_fraction
        li2co3_t_year = li_kg_year_recovered * LI2CO3_PER_LI / 1000.0
        rows.append(
            {
                "scenario": scenario,
                "feed_flow_m3_day": flow_m3_day,
                "operating_hours_year": HOURS_PER_YEAR,
                "Li_feed_mg_L": base_row["Li_feed_mg_L"],
                "TDS_mg_L": base_row["TDS_mg_L"],
                "Li_recovery_pct_used_for_costing": base_row["three_stage_Li_cumulative_pct"],
                "Li2CO3_product_t_year": li2co3_t_year,
                "Li2CO3_price_usd_t_assumption": price_usd_t,
                "gross_revenue_usd_year": li2co3_t_year * price_usd_t,
                "model_status": MODEL_STATUS,
                "costing_status": "idaes_input_scaffold_rezaee_bridge",
            }
        )
    _write_csv(COSTING_INPUT, rows)
    _write_csv(LEGACY_COSTING_INPUT, rows)


def _write_report(
    dist_rows: list[dict[str, Any]],
    grid_rows: list[dict[str, Any]],
    stats: dict[str, float],
    metrics: dict[str, float],
    base_row: dict[str, Any],
    phase_smoke: dict[str, Any],
    convention_scan: dict[str, Any],
    option_scan: dict[str, Any],
    paper_basis: dict[str, Any],
    section32: dict[str, Any],
    basis_inference: dict[str, Any],
) -> None:
    stability = phase_smoke.get("electrolyte_stability", {})
    lle = phase_smoke.get("electrolyte_lle", {})
    source_variant = convention_scan.get("source_supported_variant", {})
    best_variant = convention_scan.get("best_variant", {})
    best_option = option_scan.get("best_option", {})
    paper_best = paper_basis.get("best_mode_by_li_abs_error", {})
    section32_direct = section32.get("direct_held2014_table9_pH_stoich", {})
    section32_best = section32.get("best_case", {})
    basis_conservation = basis_inference.get("conservation_diagnostics", {})
    basis_diagnostics = basis_inference.get("basis_diagnostics", {})
    lines = [
        "# Rezaee 2026 Li/Na Distribution Bridge",
        "",
        "Last updated: 2026-05-08",
        "",
        "## Status",
        "",
        f"- Model status: `{MODEL_STATUS}`.",
        "- Flagship chemistry for the current Li/Na bridge: Rezaee DES/TOPO with reported DES, TOPO, RLi, RNa, binary-interaction, and reaction-constant inputs.",
        "- Distribution coefficients are source-regressed from Rezaee Li/Na extraction responses using an explicit equal-phase-volume O/A basis.",
        "- The ePC-SAFT package evidence is carried as a diagnostic validity input. The current direct LLE smoke returns bounded diagnostics, not a fully accepted physical split.",
        "- Direct published-constant reactive equilibrium remains blocked by the Section 3.2 initial-mole/reference-state convention gap recorded by the equation-replication scripts.",
        "",
        "## Generated Artifacts",
        "",
        f"- `{DIST_COEFFS.relative_to(REPO_ROOT)}`",
        f"- `{SURROGATE_GRID.relative_to(REPO_ROOT)}`",
        f"- `{PROMMIS_HANDOFF.relative_to(REPO_ROOT)}`",
        f"- `{COSTING_INPUT.relative_to(REPO_ROOT)}`",
        "",
        "## Source Evidence",
        "",
        f"- Extraction target rows used: `{len(dist_rows)}`.",
        f"- Surrogate/sensitivity rows generated: `{len(grid_rows)}`.",
        f"- Rezaee reaction constants: `{REACTION_CONSTANTS.relative_to(REPO_ROOT)}`.",
        f"- Rezaee organic PC-SAFT parameters: `{ORGANIC_PARAMS.relative_to(REPO_ROOT)}`.",
        f"- Rezaee organic binary interactions: `{ORGANIC_KIJ.relative_to(REPO_ROOT)}`.",
        f"- Median source-regressed D_Li: `{stats['median_D_Li']:.4g}`.",
        f"- Median source-regressed D_Na: `{stats['median_D_Na']:.4g}`.",
        f"- Median source-regressed S_Li/Na: `{stats['median_S_Li_Na']:.4g}`.",
        f"- SI median mole-fraction proxy D_Li: `{stats['si_median_D_Li']:.4g}`.",
        f"- SI median mole-fraction proxy D_Na: `{stats['si_median_D_Na']:.4g}`.",
        "",
        "## Selected Smackover Transfer Row",
        "",
        f"- TDS: `{float(base_row['TDS_mg_L']):.3f} mg/L`.",
        f"- Li: `{float(base_row['Li_feed_mg_L']):.3f} mg/L`.",
        f"- Na: `{float(base_row['Na_feed_mg_L']):.3f} mg/L`.",
        f"- Na/Li mass ratio: `{float(base_row['na_li_mass_ratio']):.3f}`.",
        f"- O/A: `{float(base_row['oa_ratio']):.3f}`.",
        f"- One-stage Li extraction: `{float(base_row['one_stage_Li_extraction_pct']):.3f}%`.",
        f"- One-stage Na extraction: `{float(base_row['one_stage_Na_extraction_pct']):.3f}%`.",
        f"- One-stage D_Li: `{float(base_row['one_stage_D_Li']):.4g}`.",
        f"- One-stage D_Na: `{float(base_row['one_stage_D_Na']):.4g}`.",
        f"- Three-stage Li recovery: `{float(base_row['three_stage_Li_cumulative_pct']):.3f}%`.",
        f"- Trust label: `{base_row['trust_label']}`.",
        "",
        "## Fit Diagnostics",
        "",
        f"- Li logit RMSE: `{metrics['li_logit_rmse']:.4g}`.",
        f"- Na logit RMSE: `{metrics['na_logit_rmse']:.4g}`.",
        f"- ePC-SAFT electrolyte stability status: `{stability.get('status')}`.",
        f"- ePC-SAFT minimum TPD: `{stability.get('min_tpd')}`.",
        f"- ePC-SAFT LLE status: `{lle.get('status')}`.",
        f"- ePC-SAFT split detected: `{lle.get('split_detected')}`.",
        f"- Reactive convention-scan status: `{convention_scan.get('status')}`.",
        f"- Source-supported reactive variant: `{source_variant.get('variant')}`.",
        f"- Source-supported combined median absolute ln residual: `{source_variant.get('combined_median_abs_ln_residual')}`.",
        f"- Best simple convention-scan variant: `{best_variant.get('variant')}`.",
        f"- Best simple combined median absolute ln residual: `{best_variant.get('combined_median_abs_ln_residual')}`.",
        f"- Equilibrium rows used as benchmark: `{convention_scan.get('equilibrium_rows_used_as_benchmark')}`.",
        f"- Best aqueous ePC-SAFT option-scan case: `{best_option.get('option_id')}`.",
        f"- Best aqueous option-scan combined median absolute ln residual: `{best_option.get('combined_median_abs_ln_residual')}`.",
        f"- Literal paper-basis reaction-coordinate best mode: `{paper_best.get('mode')}`.",
        f"- Literal paper-basis median calculated Li extraction: `{paper_best.get('median_li_extraction_pct_calc')}`.",
        f"- Section 3.2 direct Held-2014/Table-9 Li extraction AARD: `{section32_direct.get('Li_extraction_AARD_pct')}`.",
        f"- Section 3.2 direct Held-2014/Table-9 selectivity AARD: `{section32_direct.get('selectivity_AARD_pct')}`.",
        f"- Section 3.2 best diagnostic case: `{section32_best.get('case_id')}`.",
        f"- Section 3.2 basis median organic-total consistency RLi/RNa: `{basis_conservation.get('median_N_org_total_RLi_over_RNa')}`.",
        f"- Section 3.2 basis median SI xOH / pH-derived xOH estimate: `{basis_diagnostics.get('median_xOH_SI_over_pH_estimate')}`.",
        "",
        "## Boundary",
        "",
        "This bridge is now the current flagship Li/Na basis for the presentation and PrOMMiS/IDAES surrogate handoff. It is stronger than the previous HBTA/TOPO bridge for package-facing work because Rezaee supplies organic pseudo-component parameters, binary interactions, reaction constants, extraction responses, and SI equilibrium-composition rows. It is still not investment-grade TEA or a complete direct ePC-SAFT LLE/reactive-equilibrium prediction until accepted phase splits and a source-supported published-constant reactive closure are both available.",
        "",
    ]
    BRIDGE_REPORT.parent.mkdir(parents=True, exist_ok=True)
    BRIDGE_REPORT.write_text("\n".join(lines), encoding="utf-8")
    LEGACY_BRIDGE_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REF_DIR.mkdir(parents=True, exist_ok=True)

    targets = _load_targets()
    phase_smoke = _load_phase_smoke()
    convention_scan = _load_convention_scan()
    option_scan = _load_json(OPTION_SCAN_JSON)
    paper_basis = _load_json(PAPER_BASIS_JSON)
    section32 = _load_json(SECTION32_JSON)
    basis_inference = _load_json(BASIS_INFERENCE_JSON)
    dist_rows, stats = _distribution_rows(targets)
    grid_rows, metrics = _sensitivity_grid(targets)

    base_rows = [row for row in grid_rows if row["case_id"] == "rezaee_ms2_tds1_na1_oa1"]
    if not base_rows:
        raise RuntimeError("Base Rezaee/Smackover sensitivity row was not generated.")
    base_row = base_rows[0]

    _write_csv(DIST_COEFFS, dist_rows)
    _write_csv(LEGACY_DIST_COEFFS, dist_rows)
    _write_csv(SURROGATE_GRID, grid_rows)
    _write_csv(LEGACY_SURROGATE_GRID, grid_rows)
    _write_handoff(
        base_row,
        stats,
        phase_smoke,
        convention_scan,
        option_scan,
        paper_basis,
        section32,
        basis_inference,
    )
    _write_costing(base_row)
    _write_report(
        dist_rows,
        grid_rows,
        stats,
        metrics,
        base_row,
        phase_smoke,
        convention_scan,
        option_scan,
        paper_basis,
        section32,
        basis_inference,
    )

    print(f"Wrote {DIST_COEFFS}")
    print(f"Wrote {SURROGATE_GRID}")
    print(f"Wrote {PROMMIS_HANDOFF}")
    print(f"Wrote {COSTING_INPUT}")
    print(f"Wrote {BRIDGE_REPORT}")
    print(
        {
            "distribution_rows": len(dist_rows),
            "sensitivity_rows": len(grid_rows),
            "base_li_recovery_stage3_pct": base_row["three_stage_Li_cumulative_pct"],
            "base_na_recovery_stage3_pct": base_row["three_stage_Na_cumulative_pct"],
            "model_status": MODEL_STATUS,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
