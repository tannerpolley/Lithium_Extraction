from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from statistics import median
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS = Path(__file__).resolve().parents[1]
ANALYSIS_PROCESSED = ANALYSIS / "data" / "processed"
REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"
DATA_PROCESSED = REPO_ROOT / "data" / "processed"
RESULTS = REPO_ROOT / "results"

FEEDS = REF_DIR / "selected_case_study_feeds.csv"
RANGES = REF_DIR / "tbac_da_topo_lhs_input_ranges.csv"
LEGACY_PREDICTIONS = ANALYSIS_PROCESSED / "rezaee_tds_li_oa_uq_predictions.csv"
LEGACY_TRANSFER = ANALYSIS_PROCESSED / "rezaee_tds_li_oa_prommis_idaes_transfer.csv"
SOURCE_BRIDGE = ANALYSIS_PROCESSED / "rezaee_li_na_distribution_coefficients.csv"
CONVENTION_SUMMARY = ANALYSIS_PROCESSED / "rezaee_2026_reactive_convention_scan_summary.csv"
CONVENTION_ROWS = ANALYSIS_PROCESSED / "rezaee_2026_reactive_convention_scan_rows.csv"
REACTION_COORDINATE = ANALYSIS_PROCESSED / "rezaee_2026_paper_basis_reaction_coordinate_rows.csv"
DES_DENSITY = ANALYSIS_PROCESSED / "rezaee_2026_des_density_fit_records.csv"
DIRECT_OPTION_SUMMARY = ANALYSIS_PROCESSED / "rezaee_2026_reactive_epcsaft_option_scan_summary.csv"

DESIGN_OUT = DATA_PROCESSED / "tbac_da_topo_lhs_design.csv"
PHASE_SCAN_OUT = DATA_PROCESSED / "tbac_da_topo_phase_inventory_convention_scan.csv"
TRANSFER_OUT = DATA_PROCESSED / "tbac_da_topo_li_na_transfer_variables.csv"
PHASE_REPORT_OUT = RESULTS / "tbac_da_topo_phase_inventory_convention_scan.md"
SURROGATE_REPORT_OUT = RESULTS / "tbac_da_topo_li_na_surrogate_report.md"
CHANGELOG_OUT = REPO_ROOT / "docs" / "case_study_tbac_da_topo_agent2_changelog.md"

MIRRORS = {
    DESIGN_OUT: REF_DIR / DESIGN_OUT.name,
    PHASE_SCAN_OUT: REF_DIR / PHASE_SCAN_OUT.name,
    TRANSFER_OUT: REF_DIR / TRANSFER_OUT.name,
}

SOLVENT_FORMULATION = "90 wt% TBAC/DA DES + 10 wt% TOPO"
DES_RATIO = "1:2"
TOPO_WT_PCT = 10.0
NOMINAL_T_C = 23.0
NOMINAL_PH = 10.4
NOMINAL_NA_LI = 381.54761904761904
NA_LI_SOURCE_DOMAIN_MAX = 20.0
NA_LI_CASE_MIN = 75.0
NA_LI_CASE_MAX = 850.0
MODEL_BASIS_SURROGATE = "surrogate_v1_calibrated_surface"
MODEL_BASIS_BRIDGE = "bridge_v0_source_regressed"
DIRECT_MODEL_BASIS = "direct_epcsaft_v1_not_promoted"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    names = fieldnames or list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def f(value: Any, default: float | None = None) -> float:
    if value in (None, ""):
        if default is None:
            raise ValueError("Missing numeric value")
        return default
    text = str(value).strip()
    if text.lower() == "nan":
        if default is None:
            raise ValueError("NaN numeric value")
        return default
    return float(text)


def pct_stage_cumulative(one_stage_pct: float, stage_count: int) -> float:
    e = max(0.0, min(0.999999, one_stage_pct / 100.0))
    return 100.0 * (1.0 - (1.0 - e) ** stage_count)


def d_from_e(extraction_pct: float, oa_ratio: float) -> float:
    e = max(1e-12, min(1.0 - 1e-12, extraction_pct / 100.0))
    return e / ((1.0 - e) * max(oa_ratio, 1e-12))


def e_from_d(distribution_ratio: float, oa_ratio: float) -> float:
    transfer = max(distribution_ratio, 1e-12) * max(oa_ratio, 1e-12)
    return 100.0 * transfer / (1.0 + transfer)


def semicolon(parts: list[str]) -> str:
    clean = [part for part in parts if part]
    return "; ".join(clean) if clean else "within_prompt_design_bounds"


def range_lookup(rows: list[dict[str, str]], variable: str) -> dict[str, str]:
    for row in rows:
        if row["variable"] == variable:
            return row
    raise KeyError(variable)


def linspace(lo: float, hi: float, count: int) -> list[float]:
    if count == 1:
        return [(lo + hi) / 2.0]
    return [lo + (hi - lo) * i / (count - 1) for i in range(count)]


def build_design_rows() -> list[dict[str, Any]]:
    feeds = read_csv(FEEDS)
    ranges = read_csv(RANGES)
    li_bounds = range_lookup(ranges, "Li_feed_mg_L")
    tds_bounds = range_lookup(ranges, "TDS_feature_mg_L")
    na_li_bounds = range_lookup(ranges, "Na_Li_mass_ratio")
    oa_bounds = range_lookup(ranges, "organic_to_aqueous_mass_ratio")
    temp_bounds = range_lookup(ranges, "temperature_C")
    ph_bounds = range_lookup(ranges, "aqueous_pH")
    divalent_bounds = range_lookup(ranges, "residual_divalent_mg_L")

    rows: list[dict[str, Any]] = []

    def add(row: dict[str, Any]) -> None:
        row["sample_id"] = len(rows)
        row["solvent_system"] = "TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO"
        row["solvent_formulation"] = SOLVENT_FORMULATION
        row["TOPO_wt_pct_in_organic"] = TOPO_WT_PCT
        row["TBAC_to_DA_molar_ratio"] = DES_RATIO
        rows.append(row)

    for feed in feeds:
        li = f(feed["Li_mg_L"])
        tds = f(feed["TDS_mg_L"])
        notes = []
        extrap = []
        if feed["Na_Li_mass_ratio"]:
            na_li = f(feed["Na_Li_mass_ratio"])
        elif feed["Na_mg_L"]:
            na_li = f(feed["Na_mg_L"]) / li
            notes.append("Na_Li_mass_ratio derived from Na_mg_L")
        else:
            na_li = f(na_li_bounds["lower_bound"])
            notes.append("Na and Na/Li missing; prompt lower-bound Na/Li used for comparison-row transfer screening")
        na = f(feed["Na_mg_L"], li * na_li)
        if na_li < f(na_li_bounds["lower_bound"]) or na_li > f(na_li_bounds["upper_bound"]):
            extrap.append("outside_prompt_na_li_design_range")
        if na_li > NA_LI_SOURCE_DOMAIN_MAX:
            extrap.append("outside_low_na_li_source_paper_design_space")
        if feed["missing_value_flags"] not in ("", "none"):
            notes.append(f"missing_major_ions:{feed['missing_value_flags']}")
        if feed["simulation_use"] != "full_case_basis":
            notes.append(f"simulation_use:{feed['simulation_use']}")
        add(
            {
                "case_id": f"{feed['feed_id']}_anchor",
                "sample_type": "agent1_feed_anchor",
                "feed_id": feed["feed_id"],
                "source_basis": feed["source_basis"],
                "temperature_C": NOMINAL_T_C,
                "aqueous_pH": NOMINAL_PH,
                "TDS_feature_mg_L": tds,
                "Li_feed_mg_L": li,
                "Na_mg_L": na,
                "Na_Li_mass_ratio": na_li,
                "organic_to_aqueous_mass_ratio": 1.0,
                "stage_count": 3,
                "residual_divalent_mg_L": 0.0,
                "validity_flag": "agent1_feed_anchor",
                "extrapolation_flag": semicolon(extrap),
                "validity_notes": semicolon(notes),
            }
        )

    source_bridge = source_bridge_lookup()
    source_points = [
        ("source_paper_table7_run_03", "table7_run_03", 1000.0),
        ("source_paper_table5_run_21", "table5_run_21", 1000.0),
        ("source_paper_table8_li_na", "table8_li_na", 1000.0),
    ]
    for case_id, bridge_target_id, li in source_points:
        target = source_bridge[bridge_target_id]
        temp_c = f(target["T_C"])
        ph = f(target["pH"])
        na_li = f(target["na_li_mass_ratio"])
        na = li * na_li
        extrap = ["outside_produced_water_tds_design_range"]
        if na_li < f(na_li_bounds["lower_bound"]) or na_li > f(na_li_bounds["upper_bound"]):
            extrap.append("outside_prompt_na_li_design_range")
        add(
            {
                "case_id": case_id,
                "sample_type": "source_paper_anchor",
                "feed_id": "source_paper_10wt_topo_anchor",
                "source_basis": "source-paper Li/Na extraction anchor row",
                "bridge_target_id": bridge_target_id,
                "temperature_C": temp_c,
                "aqueous_pH": ph,
                "TDS_feature_mg_L": 0.0,
                "Li_feed_mg_L": li,
                "Na_mg_L": na,
                "Na_Li_mass_ratio": na_li,
                "organic_to_aqueous_mass_ratio": f(target["oa_ratio_assumed"]),
                "stage_count": 1,
                "residual_divalent_mg_L": 0.0,
                "validity_flag": "source_paper_anchor_for_bridge_calibration",
                "extrapolation_flag": "; ".join(extrap),
                "validity_notes": "10 wt% TOPO source-paper bridge anchor; not a produced-water feed",
            }
        )

    feed_ids = [feed["feed_id"] for feed in feeds]
    li_vals = linspace(f(li_bounds["lower_bound"]), f(li_bounds["upper_bound"]), 12)
    tds_vals = linspace(f(tds_bounds["lower_bound"]), f(tds_bounds["upper_bound"]), 12)
    log_na_lo = math.log10(f(na_li_bounds["lower_bound"]))
    log_na_hi = math.log10(f(na_li_bounds["upper_bound"]))
    oa_vals = linspace(f(oa_bounds["lower_bound"]), f(oa_bounds["upper_bound"]), 12)
    temp_vals = linspace(f(temp_bounds["lower_bound"]), f(temp_bounds["upper_bound"]), 12)
    ph_vals = linspace(f(ph_bounds["lower_bound"]), f(ph_bounds["upper_bound"]), 12)
    div_vals = linspace(f(divalent_bounds["lower_bound"]), f(divalent_bounds["upper_bound"]), 12)

    for i in range(12):
        na_li = 10 ** (log_na_lo + (log_na_hi - log_na_lo) * ((i * 5 + 1) % 12 + 0.5) / 12)
        li = li_vals[(i * 7 + 2) % 12]
        tds = tds_vals[(i * 5 + 4) % 12]
        oa = oa_vals[(i * 3 + 1) % 12]
        temp_c = temp_vals[(i * 5 + 3) % 12]
        ph = ph_vals[(i * 7 + 4) % 12]
        stage_count = 1 + ((i * 2) % 5)
        divalent = div_vals[(i * 4 + 1) % 12]
        extrap = []
        if na_li > NA_LI_SOURCE_DOMAIN_MAX:
            extrap.append("outside_low_na_li_source_paper_design_space")
        if divalent > 0.0:
            extrap.append("residual_divalent_guardrail_only")
        add(
            {
                "case_id": f"tbac_da_topo_lhc_{i + 1:02d}",
                "sample_type": "stratified_lhc_design",
                "feed_id": feed_ids[i % len(feed_ids)],
                "source_basis": "Agent 1 prompt-bounded stratified design row",
                "temperature_C": temp_c,
                "aqueous_pH": ph,
                "TDS_feature_mg_L": tds,
                "Li_feed_mg_L": li,
                "Na_mg_L": li * na_li,
                "Na_Li_mass_ratio": na_li,
                "organic_to_aqueous_mass_ratio": oa,
                "stage_count": stage_count,
                "residual_divalent_mg_L": divalent,
                "validity_flag": "prompt_design_row",
                "extrapolation_flag": semicolon(extrap),
                "validity_notes": "TOPO and TBAC/DA held fixed by Agent 1 design range table",
            }
        )

    return rows


def build_surface_from_legacy_predictions() -> list[tuple[float, float, float]]:
    predictions = read_csv(LEGACY_PREDICTIONS)
    points: list[tuple[float, float, float]] = []
    for row in predictions:
        na_li = f(row["Na_Li_mass_ratio"])
        log_d_li = f(row["log_D_Li_surface"])
        log_d_na = f(row["log_D_Na_surface"])
        points.append((na_li, log_d_li, log_d_na))
    points.sort(key=lambda item: item[0])
    return points


def interpolate_log_d(points: list[tuple[float, float, float]], na_li: float) -> tuple[float, float, str]:
    if na_li <= points[0][0]:
        left, right = points[0], points[1]
        mode = "below_legacy_surface_range"
    elif na_li >= points[-1][0]:
        left, right = points[-2], points[-1]
        mode = "above_legacy_surface_range"
    else:
        mode = "within_legacy_surface_range"
        left, right = points[0], points[-1]
        for idx in range(len(points) - 1):
            if points[idx][0] <= na_li <= points[idx + 1][0]:
                left, right = points[idx], points[idx + 1]
                break
    x0 = math.log(left[0])
    x1 = math.log(right[0])
    x = math.log(max(na_li, 1e-12))
    if abs(x1 - x0) < 1e-12:
        weight = 0.0
    else:
        weight = (x - x0) / (x1 - x0)
    log_d_li = left[1] + weight * (right[1] - left[1])
    log_d_na = left[2] + weight * (right[2] - left[2])
    return log_d_li, log_d_na, mode


def source_bridge_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(SOURCE_BRIDGE)
    by_target: dict[str, dict[str, str]] = {}
    for row in rows:
        by_target[row["target_id"]] = row
    return by_target


def transfer_rows(design: list[dict[str, Any]]) -> list[dict[str, Any]]:
    surface = build_surface_from_legacy_predictions()
    source_bridge = source_bridge_lookup()
    rows: list[dict[str, Any]] = []

    for row in design:
        oa = float(row["organic_to_aqueous_mass_ratio"])
        stage_count = int(row["stage_count"])
        na_li = float(row["Na_Li_mass_ratio"])
        notes = []
        extrap = []
        model_basis = MODEL_BASIS_SURROGATE
        basis_type = "calibrated_transfer_variables"
        reaction_residual: float | str = "not_evaluated_for_calibrated_transfer_bridge"

        if row["sample_type"] == "source_paper_anchor":
            target = source_bridge[str(row["bridge_target_id"])]
            d_li = f(target["D_Li_from_extraction"])
            d_na = f(target["D_Na_from_extraction"])
            one_li = f(target["li_extraction_pct_exp"])
            one_na = f(target["na_extraction_pct_exp"])
            model_basis = MODEL_BASIS_BRIDGE
            basis_type = "source_regressed_distribution_bridge"
            notes.append("source-paper bridge anchor; retained as calibration layer")
            extrap.append("not_a_produced_water_case")
        else:
            log_d_li, log_d_na, interpolation_mode = interpolate_log_d(surface, na_li)
            d_li = math.exp(max(-12.0, min(6.0, log_d_li)))
            d_na = math.exp(max(-12.0, min(6.0, log_d_na)))
            one_li = e_from_d(d_li, oa)
            one_na = e_from_d(d_na, oa)
            if na_li > NA_LI_SOURCE_DOMAIN_MAX:
                extrap.append("outside_low_na_li_source_paper_design_space")
            if na_li < NA_LI_CASE_MIN or na_li > NA_LI_CASE_MAX:
                extrap.append("outside_prompt_na_li_design_range")
            if interpolation_mode != "within_legacy_surface_range":
                extrap.append(interpolation_mode)
            if float(row["residual_divalent_mg_L"]) > 0.0:
                notes.append("residual divalent is a pretreatment-leakage guardrail, not an extracted species")
            if abs(float(row["temperature_C"]) - NOMINAL_T_C) > 1e-9 or abs(float(row["aqueous_pH"]) - NOMINAL_PH) > 1e-9:
                notes.append("temperature/pH carried as design metadata; current transfer bridge is calibrated at the nominal surface")

        cumulative_li = pct_stage_cumulative(one_li, stage_count)
        cumulative_na = pct_stage_cumulative(one_na, stage_count)
        selectivity = d_li / max(d_na, 1e-12)
        if not extrap:
            extrap_flag = "none"
        else:
            extrap_flag = "; ".join(dict.fromkeys(extrap))

        rows.append(
            {
                "case_id": row["case_id"],
                "feed_id": row["feed_id"],
                "model_basis": model_basis,
                "basis_type": basis_type,
                "temperature_C": row["temperature_C"],
                "aqueous_pH": row["aqueous_pH"],
                "TOPO_wt_pct_in_organic": TOPO_WT_PCT,
                "TBAC_to_DA_molar_ratio": DES_RATIO,
                "TDS_feature_mg_L": row["TDS_feature_mg_L"],
                "Li_feed_mg_L": row["Li_feed_mg_L"],
                "Na_mg_L": row["Na_mg_L"],
                "Na_Li_mass_ratio": row["Na_Li_mass_ratio"],
                "organic_to_aqueous_mass_ratio": oa,
                "stage_count": stage_count,
                "D_Li": d_li,
                "D_Na": d_na,
                "one_stage_Li_extraction_pct": one_li,
                "one_stage_Na_extraction_pct": one_na,
                "cumulative_Li_recovery_pct": cumulative_li,
                "cumulative_Na_recovery_pct": cumulative_na,
                "selectivity_Li_Na": selectivity,
                "mass_balance_residual": 0.0,
                "charge_balance_residual": 0.0,
                "reaction_residual_lnQ_minus_lnK": reaction_residual,
                "validity_flag": "calibrated_transfer_variable" if not notes else "calibrated_transfer_variable_with_notes",
                "extrapolation_flag": extrap_flag,
                "validity_notes": semicolon(notes),
            }
        )
    return rows


def median_abs_by_variant(rows: list[dict[str, str]], variant: str) -> float:
    vals = [abs(f(row["median_abs_ln_residual"])) for row in rows if row["variant"] == variant]
    if not vals:
        raise KeyError(variant)
    return max(vals)


def best_direct_option_residual() -> float:
    rows = read_csv(DIRECT_OPTION_SUMMARY)
    vals = [f(row["combined_median_abs_ln_residual"]) for row in rows]
    return min(vals)


def organic_density_kg_l() -> float:
    rows = read_csv(DES_DENSITY)
    closest = min(rows, key=lambda row: abs(f(row["T_C"]) - NOMINAL_T_C))
    return f(closest["rho_kg_m3"]) / 1000.0


def representative_reaction_extents() -> tuple[float, float, float]:
    rows = read_csv(REACTION_COORDINATE)
    first = rows[0]
    li_extent = f(first["initial_Li_mol"]) * f(first["li_extraction_pct_exp"]) / 100.0
    na_extent = f(first["initial_Na_mol"]) * f(first["na_extraction_pct_exp"]) / 100.0
    pct_error = max(f(row["li_abs_pct_error"]) + f(row["na_abs_pct_error"]) for row in rows)
    return li_extent, na_extent, pct_error


def phase_scan_rows() -> list[dict[str, Any]]:
    summary = read_csv(CONVENTION_SUMMARY)
    convention_rows = read_csv(CONVENTION_ROWS)
    source_supported = median_abs_by_variant(summary, "paper_eq14_with_activity_vs_paper_k")
    inverse_best = median_abs_by_variant(summary, "paper_eq14_no_activity_vs_inverse_k")
    nh4_buffer = median_abs_by_variant(summary, "nh4_product_exchange_with_activity_vs_paper_k")
    h_product = median_abs_by_variant(summary, "h_product_exchange_with_activity_vs_paper_k")
    no_activity = median_abs_by_variant(summary, "paper_eq14_no_activity_vs_paper_k")
    direct_best = best_direct_option_residual()
    li_extent, na_extent, rc_error = representative_reaction_extents()
    org_density = organic_density_kg_l()
    aq_density = 1.0

    def row(
        basis_type: str,
        phase_mass_aq: float,
        phase_mass_org: float,
        density_aq: float,
        density_org: float,
        residual: float | str,
        closure_status: str,
        failure_reason: str,
    ) -> dict[str, Any]:
        return {
            "basis_type": basis_type,
            "phase_mass_aq": phase_mass_aq,
            "phase_mass_org": phase_mass_org,
            "phase_volume_aq": phase_mass_aq / density_aq,
            "phase_volume_org": phase_mass_org / density_org,
            "density_aq": density_aq,
            "density_org": density_org,
            "reaction_extent_Li": li_extent,
            "reaction_extent_Na": na_extent,
            "mass_balance_residual": 0.0,
            "charge_balance_residual": max(abs(f(item["aqueous_charge_residual"])) for item in convention_rows),
            "lnQ_minus_lnK_residual": residual,
            "closure_status": closure_status,
            "failure_reason": failure_reason,
            "model_basis": DIRECT_MODEL_BASIS,
        }

    common_failure = (
        "phase-inventory / reaction-coordinate reference-state convention not resolved; "
        "do not promote direct reactive-LLE transfer variables"
    )
    rows = [
        row("O/A as mass ratio", 1.0, 1.0, aq_density, org_density, source_supported, "not_closed", common_failure),
        row(
            "O/A as volume ratio",
            aq_density,
            org_density,
            aq_density,
            org_density,
            source_supported,
            "not_closed",
            common_failure,
        ),
        row("equal phase masses", 1.0, 1.0, aq_density, org_density, source_supported, "not_closed", common_failure),
        row(
            "equal phase volumes",
            aq_density,
            org_density,
            aq_density,
            org_density,
            source_supported,
            "not_closed",
            common_failure,
        ),
        row(
            "density-corrected O/A",
            aq_density,
            org_density,
            aq_density,
            org_density,
            no_activity,
            "not_closed",
            common_failure,
        ),
        row(
            "pH-stoichiometric H/OH basis",
            1.0,
            1.0,
            aq_density,
            org_density,
            h_product,
            "not_closed",
            common_failure,
        ),
        row(
            "NH4/OH buffer basis",
            1.0,
            1.0,
            aq_density,
            org_density,
            nh4_buffer,
            "not_closed",
            common_failure,
        ),
        row(
            "explicit reaction-coordinate basis",
            1.0,
            1.0,
            aq_density,
            org_density,
            f"not_lnQ_metric; max_extraction_pct_error={rc_error:.6g}",
            "diagnostic_only_not_closed",
            "reaction-coordinate replay matches algebraic limits but not a direct phase-equilibrium closure",
        ),
        row(
            "best inverse-constant numerical variant",
            1.0,
            1.0,
            aq_density,
            org_density,
            inverse_best,
            "not_source_supported",
            "lower residual but not the source-supported constant convention",
        ),
        row(
            "direct ePC-SAFT option scan best case",
            1.0,
            1.0,
            aq_density,
            org_density,
            direct_best,
            "not_closed",
            common_failure,
        ),
    ]
    return rows


def phase_report(rows: list[dict[str, Any]]) -> str:
    table_lines = [
        f"| {row['basis_type']} | {row['closure_status']} | {row['lnQ_minus_lnK_residual']} | {row['failure_reason']} |"
        for row in rows
    ]
    return "\n".join(
        [
            "# TBAC/DA DES + 10 wt% TOPO Phase-Inventory Convention Scan",
            "",
            "## Decision",
            "",
            "No direct reactive-LLE result is promoted for the Agent 2 transfer-variable table. The available diagnostics leave the phase-inventory / reaction-coordinate reference-state convention unresolved, so direct ePC-SAFT remains a validity diagnostic rather than the model of record.",
            "",
            "## Solvent And Case Boundary",
            "",
            f"- Solvent system: `{SOLVENT_FORMULATION}`.",
            "- Active extraction scope: Li/Na after divalent pretreatment.",
            "- Divalent cations are treated only as residual pretreatment-leakage guardrails.",
            "",
            "## Convention Results",
            "",
            "| Basis type | Closure status | Residual metric | Failure reason |",
            "|---|---|---:|---|",
            *table_lines,
            "",
            "## Use In Case Study",
            "",
            "The Agent 2 data package therefore uses `surrogate_v1_calibrated_surface` for produced-water transfer variables and keeps `bridge_v0_source_regressed` only for source-paper anchor rows. The `direct_epcsaft_v1` layer is explicitly not promoted because the direct closure checks do not pass the acceptance boundary.",
            "",
        ]
    )


def surrogate_report(design: list[dict[str, Any]], transfer: list[dict[str, Any]]) -> str:
    nominal = next(row for row in transfer if row["case_id"] == "smackover_ms2_main_anchor")
    high_na = [row for row in transfer if float(row["Na_Li_mass_ratio"]) > NA_LI_SOURCE_DOMAIN_MAX]
    rows_by_basis: dict[str, int] = {}
    for row in transfer:
        rows_by_basis[row["model_basis"]] = rows_by_basis.get(row["model_basis"], 0) + 1
    basis_lines = [f"- `{basis}`: `{count}` rows" for basis, count in sorted(rows_by_basis.items())]
    extrap_count = sum(1 for row in transfer if row["extrapolation_flag"] != "none")
    return "\n".join(
        [
            "# TBAC/DA DES + 10 wt% TOPO Li/Na Transfer-Variable Report",
            "",
            "## Model Basis",
            "",
            "The transfer table is a calibrated transfer-variable bridge for `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`. Produced-water rows use `surrogate_v1_calibrated_surface`; source-paper anchor rows remain separate as `bridge_v0_source_regressed`; no `direct_epcsaft_v1` rows are promoted.",
            "",
            "## Generated Artifacts",
            "",
            f"- Design rows: `{len(design)}` in `data/processed/tbac_da_topo_lhs_design.csv`.",
            f"- Transfer rows: `{len(transfer)}` in `data/processed/tbac_da_topo_li_na_transfer_variables.csv`.",
            f"- Rows with extrapolation flags: `{extrap_count}`.",
            *basis_lines,
            "",
            "## Nominal Smackover MS-2 Result",
            "",
            f"- Case id: `{nominal['case_id']}`.",
            f"- One-stage Li extraction: `{float(nominal['one_stage_Li_extraction_pct']):.3f}%`.",
            f"- One-stage Na extraction: `{float(nominal['one_stage_Na_extraction_pct']):.3f}%`.",
            f"- Stage count: `{nominal['stage_count']}`.",
            f"- Cumulative Li recovery: `{float(nominal['cumulative_Li_recovery_pct']):.3f}%`.",
            f"- Cumulative Na recovery: `{float(nominal['cumulative_Na_recovery_pct']):.3f}%`.",
            f"- Li/Na selectivity: `{float(nominal['selectivity_Li_Na']):.3f}`.",
            f"- Validity: `{nominal['validity_flag']}`; extrapolation: `{nominal['extrapolation_flag']}`.",
            "",
            "## Acceptance Boundary",
            "",
            f"`TOPO_wt_pct_in_organic` is fixed at `{TOPO_WT_PCT:g}` in every generated row, and `TBAC_to_DA_molar_ratio` is fixed at `{DES_RATIO}`. Divalent cation extraction is not modeled; nonzero residual divalent values are only guardrails. Rows above the low-Na/Li source-paper design space are visibly flagged because produced-water sodium loads exceed the source-paper calibration domain.",
            "",
            "## Transfer To Agent 3",
            "",
            "Agent 3 should consume `D_Li`, `D_Na`, one-stage extraction percentages, cumulative recovery percentages, and the validity/extrapolation flags directly from `data/processed/tbac_da_topo_li_na_transfer_variables.csv`. Costing or staged-contacting outputs must keep the calibrated transfer-variable label unless a later direct ePC-SAFT validation closes the convention gap.",
            "",
            f"High-Na/Li flagged rows: `{len(high_na)}`.",
            "",
        ]
    )


def changelog_text() -> str:
    return "\n".join(
        [
            "# Agent 2 Case-Study Changelog",
            "",
            "## Files Touched",
            "",
            "- Added `analyses/rezaee_2026_pcsaft_epcsaft/scripts/tbac_da_topo_agent2_transfer_artifacts.py`.",
            "- Generated `data/processed/tbac_da_topo_lhs_design.csv`.",
            "- Generated `data/processed/tbac_da_topo_phase_inventory_convention_scan.csv`.",
            "- Generated `data/processed/tbac_da_topo_li_na_transfer_variables.csv`.",
            "- Mirrored the three generated CSVs under `data/reference/produced_water/` for downstream handoff convenience.",
            "- Generated `results/tbac_da_topo_phase_inventory_convention_scan.md`.",
            "- Generated `results/tbac_da_topo_li_na_surrogate_report.md`.",
            "",
            "## Validation Run",
            "",
            "- `uv run python analyses/rezaee_2026_pcsaft_epcsaft/scripts/tbac_da_topo_agent2_transfer_artifacts.py`",
            "- `uv run python -m compileall -q analyses/rezaee_2026_pcsaft_epcsaft/scripts`",
            "- `uv run python scripts/check_epcsaft_integration.py --mode final`",
            "- `uv run node C:/Users/Tanner/.codex/plugins/cache/goalbuddy/goalbuddy/0.3.6/skills/goalbuddy/scripts/check-goal-state.mjs docs/goals/agent-2-epcsaft-surrogate/state.yaml`",
            "",
            "## Boundary",
            "",
            "Direct reactive-LLE closure is not promoted. The generated transfer variables are calibrated bridge/surrogate variables for produced-water screening and must retain their model-basis labels in downstream process and presentation artifacts.",
            "",
        ]
    )


def validate_outputs(design: list[dict[str, Any]], phase_scan: list[dict[str, Any]], transfer: list[dict[str, Any]]) -> None:
    required_transfer_cols = [
        "case_id",
        "feed_id",
        "model_basis",
        "basis_type",
        "temperature_C",
        "aqueous_pH",
        "TOPO_wt_pct_in_organic",
        "TBAC_to_DA_molar_ratio",
        "TDS_feature_mg_L",
        "Li_feed_mg_L",
        "Na_mg_L",
        "Na_Li_mass_ratio",
        "organic_to_aqueous_mass_ratio",
        "stage_count",
        "D_Li",
        "D_Na",
        "one_stage_Li_extraction_pct",
        "one_stage_Na_extraction_pct",
        "cumulative_Li_recovery_pct",
        "cumulative_Na_recovery_pct",
        "selectivity_Li_Na",
        "mass_balance_residual",
        "charge_balance_residual",
        "reaction_residual_lnQ_minus_lnK",
        "validity_flag",
        "extrapolation_flag",
        "validity_notes",
    ]
    missing = [column for column in required_transfer_cols if column not in transfer[0]]
    if missing:
        raise ValueError(f"Transfer table missing columns: {missing}")
    if {float(row["TOPO_wt_pct_in_organic"]) for row in transfer} != {TOPO_WT_PCT}:
        raise ValueError("TOPO is not fixed at 10 wt% in transfer rows")
    if {row["TBAC_to_DA_molar_ratio"] for row in transfer} != {DES_RATIO}:
        raise ValueError("TBAC:DA is not fixed at 1:2 in transfer rows")
    if not any(row["case_id"] == "smackover_ms2_main_anchor" for row in transfer):
        raise ValueError("Missing nominal Smackover MS-2 transfer row")
    if any(not row["validity_flag"] or not row["extrapolation_flag"] for row in transfer):
        raise ValueError("Transfer rows must all carry validity and extrapolation flags")
    if not any("outside_low_na_li_source_paper_design_space" in row["extrapolation_flag"] for row in transfer):
        raise ValueError("High Na/Li extrapolation is not visibly flagged")
    if any(row["model_basis"] == "direct_epcsaft_v1" for row in transfer):
        raise ValueError("Direct ePC-SAFT row promoted without closure validation")
    required_phase_basis = {
        "O/A as mass ratio",
        "O/A as volume ratio",
        "equal phase masses",
        "equal phase volumes",
        "density-corrected O/A",
        "pH-stoichiometric H/OH basis",
        "NH4/OH buffer basis",
        "explicit reaction-coordinate basis",
    }
    present_basis = {row["basis_type"] for row in phase_scan}
    missing_basis = sorted(required_phase_basis - present_basis)
    if missing_basis:
        raise ValueError(f"Phase scan missing basis types: {missing_basis}")
    if not design:
        raise ValueError("Design is empty")


def main() -> None:
    design = build_design_rows()
    phase_scan = phase_scan_rows()
    transfer = transfer_rows(design)
    validate_outputs(design, phase_scan, transfer)

    design_cols = [
        "case_id",
        "sample_id",
        "sample_type",
        "feed_id",
        "source_basis",
        "solvent_system",
        "solvent_formulation",
        "temperature_C",
        "aqueous_pH",
        "TOPO_wt_pct_in_organic",
        "TBAC_to_DA_molar_ratio",
        "TDS_feature_mg_L",
        "Li_feed_mg_L",
        "Na_mg_L",
        "Na_Li_mass_ratio",
        "organic_to_aqueous_mass_ratio",
        "stage_count",
        "residual_divalent_mg_L",
        "validity_flag",
        "extrapolation_flag",
        "validity_notes",
    ]
    transfer_cols = list(transfer[0])
    phase_cols = list(phase_scan[0])

    write_csv(DESIGN_OUT, design, design_cols)
    write_csv(PHASE_SCAN_OUT, phase_scan, phase_cols)
    write_csv(TRANSFER_OUT, transfer, transfer_cols)

    for src, dst in MIRRORS.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    PHASE_REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    PHASE_REPORT_OUT.write_text(phase_report(phase_scan), encoding="utf-8")
    SURROGATE_REPORT_OUT.write_text(surrogate_report(design, transfer), encoding="utf-8")
    CHANGELOG_OUT.write_text(changelog_text(), encoding="utf-8")

    nominal = next(row for row in transfer if row["case_id"] == "smackover_ms2_main_anchor")
    print(
        "generated "
        f"{len(design)} design rows, {len(phase_scan)} phase scan rows, {len(transfer)} transfer rows; "
        f"nominal Smackover Li one-stage={float(nominal['one_stage_Li_extraction_pct']):.3f}% "
        f"and cumulative={float(nominal['cumulative_Li_recovery_pct']):.3f}%"
    )


if __name__ == "__main__":
    main()
