from __future__ import annotations

import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analyses.hbta_topo_case_study.scripts.hbta_topo_reactive_stage_solve import (
    TABLE4_CUMULATIVE_LI_PCT,
    fit_reactive_parameters,
    run_reactive_crossflow,
)

REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"
SENSITIVITY_INPUT = REF_DIR / "smackover_li_tds_sensitivity_basis.csv"
TRANSFER_OUT = REF_DIR / "smackover_ms2_transfer_sensitivity.csv"
HANDOFF_OUT = REF_DIR / "smackover_prommis_transfer_handoff.csv"
COSTING_OUT = REF_DIR / "phase8_costing_scenarios_skeleton.csv"
REPORT_OUT = REF_DIR / "phase6_8_smackover_skeleton_report.md"

BASE_CASE_ID = "smackover_clean_median_tds_proxy"
OA_VALUES = [0.5, 1.0, 1.5]
HBTA_MOL_L = 0.015
TOPO_MOL_L = 0.015
STAGE_COUNT = 3
HOURS_PER_YEAR = 8000.0
LI2CO3_PER_LI = 73.891 / (2.0 * 6.94)
MODEL_STATUS = "source_regressed_li_na_predictive_stage_model_limited_epcsaft"


@dataclass
class FeedCase:
    case_id: str
    basis_type: str
    site_id: str
    li_mg_L: float
    na_mg_L: float
    k_mg_L: float
    mg_mg_L: float
    ca_mg_L: float
    sr_mg_L: float
    ba_mg_L: float
    cl_mg_L: float
    br_mg_L: float
    so4_mg_L: float
    b_mg_L: float
    tds_mg_L: float
    source_policy: str


def _num(value, default: float | None = None) -> float | None:
    if value is None:
        return default
    if isinstance(value, float) and math.isnan(value):
        return default
    text = str(value).strip()
    if text in {"", "not_reported", "not_applicable"}:
        return default
    return float(text)


def _load_feed_cases() -> list[FeedCase]:
    df = pd.read_csv(SENSITIVITY_INPUT)
    base = df.loc[df["case_id"].eq(BASE_CASE_ID)].iloc[0]
    base_tds = float(base["TDS_mg_L"])
    ion_cols = ["Na", "K", "Mg", "Ca", "Sr", "Ba", "Cl", "Br", "SO4", "B"]

    cases: list[FeedCase] = []
    for _, row in df.iterrows():
        tds = float(row["TDS_mg_L"])
        scale = tds / base_tds
        values: dict[str, float] = {}
        source_policy = "reported_source_row"
        for ion in ion_cols:
            col = f"{ion}_mg_L"
            value = _num(row[col])
            if value is None:
                value = float(base[col]) * scale
                source_policy = "base_major_ions_scaled_to_tds"
            values[ion] = float(value)

        cases.append(
            FeedCase(
                case_id=str(row["case_id"]),
                basis_type=str(row["basis_type"]),
                site_id=str(row["site_id"]),
                li_mg_L=float(row["Li_mg_L"]),
                na_mg_L=values["Na"],
                k_mg_L=values["K"],
                mg_mg_L=values["Mg"],
                ca_mg_L=values["Ca"],
                sr_mg_L=values["Sr"],
                ba_mg_L=values["Ba"],
                cl_mg_L=values["Cl"],
                br_mg_L=values["Br"],
                so4_mg_L=values["SO4"],
                b_mg_L=values["B"],
                tds_mg_L=tds,
                source_policy=source_policy,
            )
        )
    return cases


def _trust_label(feed: FeedCase, oa_ratio: float) -> str:
    if feed.source_policy == "base_major_ions_scaled_to_tds":
        return "extrapolative_scaling_major_ions"
    in_li = 30.0 <= feed.li_mg_L <= 90.0
    in_na = 0.0 <= feed.na_mg_L <= 20000.0
    in_oa = 0.25 <= oa_ratio <= 1.8
    if in_li and in_na and in_oa:
        return "inside_existing_showcase_envelope"
    if in_oa:
        return "source_regressed_extrapolated_to_smackover"
    return "outside_existing_oa_sweep"


def _write_transfer_rows(cases: list[FeedCase]) -> list[dict[str, object]]:
    fit = fit_reactive_parameters()
    rows: list[dict[str, object]] = []
    for feed in cases:
        for oa_ratio in OA_VALUES:
            stages = run_reactive_crossflow(
                li_mg_L=feed.li_mg_L,
                na_mg_L=feed.na_mg_L,
                cl_mg_L=feed.cl_mg_L,
                hbta_mol_L=HBTA_MOL_L,
                topo_mol_L=TOPO_MOL_L,
                oa_ratio=oa_ratio,
                stage_count=STAGE_COUNT,
                fit=fit,
            )
            one = stages[0]
            three = stages[-1]
            trust_label = _trust_label(feed, oa_ratio)
            if three.li_cumulative_extraction_pct >= 99.0:
                trust_label = "outside_literature_capacity_envelope_near_total_transfer"
            rows.append(
                {
                    "case_id": feed.case_id,
                    "basis_type": feed.basis_type,
                    "site_id": feed.site_id,
                    "source_policy": feed.source_policy,
                    "oa_ratio": oa_ratio,
                    "stage_count": STAGE_COUNT,
                    "Li_feed_mg_L": feed.li_mg_L,
                    "Na_feed_mg_L": feed.na_mg_L,
                    "K_feed_mg_L": feed.k_mg_L,
                    "Mg_feed_mg_L": feed.mg_mg_L,
                    "Ca_feed_mg_L": feed.ca_mg_L,
                    "Sr_feed_mg_L": feed.sr_mg_L,
                    "Ba_feed_mg_L": feed.ba_mg_L,
                    "Cl_feed_mg_L": feed.cl_mg_L,
                    "Br_feed_mg_L": feed.br_mg_L,
                    "SO4_feed_mg_L": feed.so4_mg_L,
                    "B_feed_mg_L": feed.b_mg_L,
                    "TDS_mg_L": feed.tds_mg_L,
                    "one_stage_Li_extraction_pct": one.li_stage_extraction_pct,
                    "one_stage_Na_extraction_pct": one.na_stage_extraction_pct,
                    "one_stage_D_Li": one.d_li,
                    "one_stage_S_Li_Na": one.selectivity_li_na,
                    "three_stage_Li_cumulative_pct": three.li_cumulative_extraction_pct,
                    "three_stage_Na_cumulative_pct": three.na_cumulative_extraction_pct,
                    "three_stage_D_Li_final": three.d_li,
                    "three_stage_S_Li_Na_final": three.selectivity_li_na,
                    "HBTA_consumed_mol_L_org_stage3": three.hbta_consumed_mol_L_org,
                    "TOPO_consumed_mol_L_org_stage3": three.topo_consumed_mol_L_org,
                    "gamma_source_stage3": three.gamma_source,
                    "trust_label": trust_label,
                    "model_status": fit.model_status,
                }
            )
    with TRANSFER_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def _write_handoff(base_row: dict[str, object]) -> None:
    rows = [
        ("feed_li_mg_L", base_row["Li_feed_mg_L"], "mg/L", "MS-2 source feed", "aqueous_feed[Li]"),
        ("feed_na_mg_L", base_row["Na_feed_mg_L"], "mg/L", "MS-2 source feed", "aqueous_feed[Na]"),
        ("feed_ca_mg_L", base_row["Ca_feed_mg_L"], "mg/L", "MS-2 source feed", "pretreatment_feed[Ca]"),
        ("feed_mg_mg_L", base_row["Mg_feed_mg_L"], "mg/L", "MS-2 source feed", "pretreatment_feed[Mg]"),
        ("tds_mg_L", base_row["TDS_mg_L"], "mg/L", "MS-2 source feed", "surrogate_feature_tds"),
        ("oa_ratio", base_row["oa_ratio"], "dimensionless", "case-study design variable", "MSContactor.OA_ratio"),
        (
            "eta_li_stage1_pct",
            base_row["one_stage_Li_extraction_pct"],
            "percent",
            "source-regressed Li/Na HBTA/TOPO stage model",
            "transfer[Li]",
        ),
        (
            "eta_na_stage1_pct",
            base_row["one_stage_Na_extraction_pct"],
            "percent",
            "source-regressed Li/Na HBTA/TOPO stage model",
            "transfer[Na]",
        ),
        (
            "D_li_stage1",
            base_row["one_stage_D_Li"],
            "dimensionless",
            "source-regressed Li/Na HBTA/TOPO stage model",
            "distribution_ratio[Li]",
        ),
        (
            "S_li_na_stage1",
            base_row["one_stage_S_Li_Na"],
            "dimensionless",
            "source-regressed Li/Na HBTA/TOPO stage model",
            "selectivity[Li,Na]",
        ),
        (
            "eta_li_stage3_pct",
            base_row["three_stage_Li_cumulative_pct"],
            "percent",
            "source-regressed Li/Na HBTA/TOPO stage model",
            "flowsheet_recovery[Li]",
        ),
        (
            "eta_na_stage3_pct",
            base_row["three_stage_Na_cumulative_pct"],
            "percent",
            "source-regressed Li/Na HBTA/TOPO stage model",
            "flowsheet_recovery[Na]",
        ),
        ("validity_status", base_row["trust_label"], "label", "trust-region diagnostic", "surrogate_validity_flag"),
    ]
    with HANDOFF_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["variable", "value", "units", "source", "prommis_idaes_use"])
        writer.writerows(rows)


def _write_costing(base_row: dict[str, object]) -> None:
    flow_m3_day_values = [100.0, 1000.0, 10000.0]
    recovery_fraction = min(float(base_row["three_stage_Li_cumulative_pct"]), float(TABLE4_CUMULATIVE_LI_PCT[-1])) / 100.0
    rows: list[dict[str, object]] = []
    for flow_m3_day in flow_m3_day_values:
        liters_per_year = flow_m3_day * 1000.0 * HOURS_PER_YEAR / 24.0
        li_kg_year_feed = liters_per_year * float(base_row["Li_feed_mg_L"]) / 1e6
        li_kg_year_recovered = li_kg_year_feed * recovery_fraction
        li2co3_t_year = li_kg_year_recovered * LI2CO3_PER_LI / 1000.0
        rows.append(
            {
                "scenario": f"flow_{int(flow_m3_day)}_m3_day",
                "feed_flow_m3_day": flow_m3_day,
                "operating_hours_year": HOURS_PER_YEAR,
                "Li_feed_mg_L": base_row["Li_feed_mg_L"],
                "TDS_mg_L": base_row["TDS_mg_L"],
                "Li_recovery_pct_used": base_row["three_stage_Li_cumulative_pct"],
                "Li_recovery_pct_costing_capped": recovery_fraction * 100.0,
                "Li_feed_kg_year": li_kg_year_feed,
                "Li_recovered_kg_year": li_kg_year_recovered,
                "Li2CO3_product_t_year": li2co3_t_year,
                "cost_status": "missing_prices_and_capex",
                "notes": "Skeleton throughput only; not a TEA until prices, solvent loss, reagent doses, and equipment sizing are approved.",
            }
        )
    pd.DataFrame(rows).to_csv(COSTING_OUT, index=False)


def _write_report(base_row: dict[str, object]) -> None:
    lines = [
        "# Phase 6-8 Smackover Reactive-Stage Outputs",
        "",
        "## Scope",
        "",
        "These outputs use the source-regressed Li/Na HBTA/TOPO reactive-stage model with 2 HBTA : 1 TOPO : 1 Li stoichiometry and ePC-SAFT aqueous activity coefficients when available. They assume divalent pretreatment and are transfer-variable and costing scaffold artifacts, not full organic-phase HBTA/TOPO ePC-SAFT LLE predictions.",
        "",
        "## Generated Files",
        "",
        f"- `{TRANSFER_OUT.relative_to(REPO_ROOT)}`",
        f"- `{HANDOFF_OUT.relative_to(REPO_ROOT)}`",
        f"- `{COSTING_OUT.relative_to(REPO_ROOT)}`",
        "",
        "## Selected Base Result",
        "",
        f"- Case: `{base_row['case_id']}`",
        f"- O/A ratio: `{base_row['oa_ratio']}`",
        f"- Li feed: `{float(base_row['Li_feed_mg_L']):.3f} mg/L`",
        f"- Na feed: `{float(base_row['Na_feed_mg_L']):.3f} mg/L`",
        f"- TDS: `{float(base_row['TDS_mg_L']):.3f} mg/L`",
        f"- One-stage Li extraction: `{float(base_row['one_stage_Li_extraction_pct']):.4f}%`",
        f"- One-stage Na extraction: `{float(base_row['one_stage_Na_extraction_pct']):.4f}%`",
        f"- Three-stage Li extraction: `{float(base_row['three_stage_Li_cumulative_pct']):.5f}%` (near-total extrapolated model result)",
        f"- Three-stage Na extraction: `{float(base_row['three_stage_Na_cumulative_pct']):.4f}%`",
        f"- Trust label: `{base_row['trust_label']}`",
        "",
        "## Boundary",
        "",
        "The high Smackover salinity and lithium concentration are outside the original Shan/Gando showcase calibration envelope. These rows are useful for process skeletons and reactive-stage surrogate design, but they must be labeled as extrapolative until the HBTA/TOPO organic-phase parameter and complex-parameter gaps are closed.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    cases = _load_feed_cases()
    rows = _write_transfer_rows(cases)
    base_rows = [
        row for row in rows if row["case_id"] == BASE_CASE_ID and abs(float(row["oa_ratio"]) - 1.0) < 1e-12
    ]
    if not base_rows:
        raise RuntimeError("Base O/A=1 row was not generated.")
    base_row = base_rows[0]
    _write_handoff(base_row)
    _write_costing(base_row)
    _write_report(base_row)
    print(f"Saved transfer sensitivity: {TRANSFER_OUT}")
    print(f"Saved PrOMMiS handoff: {HANDOFF_OUT}")
    print(f"Saved costing skeleton: {COSTING_OUT}")
    print(f"Saved report: {REPORT_OUT}")


if __name__ == "__main__":
    main()

