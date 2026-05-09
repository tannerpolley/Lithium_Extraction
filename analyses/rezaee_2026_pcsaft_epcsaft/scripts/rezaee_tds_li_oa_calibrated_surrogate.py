from __future__ import annotations

import csv
import json
import math
import os
import shutil
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS = Path(__file__).resolve().parents[1]
DATA_OUT = ANALYSIS / "data" / "processed"
RESULTS = ANALYSIS / "results" / "uq_surrogate"
FIGURES = RESULTS / "figures"
REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"

SEED_MATRIX = REF_DIR / "rezaee_surrogate_seed_run_matrix.csv"
DESIGN = DATA_OUT / "rezaee_tds_li_oa_uq_design.csv"
PREDICTIONS = DATA_OUT / "rezaee_tds_li_oa_uq_predictions.csv"
PROMMIS_TRANSFER = DATA_OUT / "rezaee_tds_li_oa_prommis_idaes_transfer.csv"
COSTING_INPUT = DATA_OUT / "rezaee_tds_li_oa_calibrated_idaes_costing_input.csv"
SUMMARY = RESULTS / "rezaee_tds_li_oa_uq_summary.json"
REPORT = RESULTS / "rezaee_tds_li_oa_uq_report.md"

LEGACY_FILES = {
    DESIGN: REF_DIR / DESIGN.name,
    PREDICTIONS: REF_DIR / PREDICTIONS.name,
    PROMMIS_TRANSFER: REF_DIR / PROMMIS_TRANSFER.name,
    COSTING_INPUT: REF_DIR / COSTING_INPUT.name,
    REPORT: REF_DIR / REPORT.name,
}

MODEL_BASIS = "synthetic_scaffold_calibrated_rezaee_section32_mass_balance_complex_basis"
CALIBRATED_MODEL_BASIS = "calibrated_rezaee_section32_doe_basis_surface_distribution_surrogate"
RANDOM_SEED = 20260508
N_LHS = 500
NA_FRACTION_OF_TDS = 64100.0 / 305000.0
LI2CO3_PER_LI = 73.891 / (2.0 * 6.94)
OPERATING_HOURS_YEAR = 8000.0


def _default_upstream_rezaee_rows() -> Path:
    if "EPCSAFT_REZAEE_SECTION32_ROWS" in os.environ:
        return Path(os.environ["EPCSAFT_REZAEE_SECTION32_ROWS"])
    return (
        REPO_ROOT.parent
        / "ePC-SAFT"
        / "analyses"
        / "2026_rezaee"
        / "data"
        / "processed"
        / "rezaee_2026_section32_revised_31_run_results.csv"
    )


UPSTREAM_REZAEE_ROWS = _default_upstream_rezaee_rows()
SURROGATE_FEATURE_NAMES = [
    "intercept",
    "T_centered_30C_scaled_5C",
    "pH_centered_10_scaled_0p5",
    "TOPO_wt_pct_centered_30_scaled_10",
    "ln_Na_Li_mass_ratio_over_10",
    "pH_x_TOPO",
    "pH_x_ln_Na_Li",
    "TOPO_x_ln_Na_Li",
]


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _latin_hypercube(n: int, d: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = np.empty((n, d), dtype=float)
    for j in range(d):
        out[:, j] = (rng.permutation(n) + rng.random(n)) / n
    return out


def _bounded(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _d_from_e(extraction_pct: float, oa: float) -> tuple[float, float]:
    e = _bounded(extraction_pct / 100.0, 1e-7, 1.0 - 1e-7)
    equal = e / (1.0 - e)
    corrected = equal / max(oa, 1e-9)
    return equal, corrected


def _e_from_d(d_corrected: float, oa: float) -> float:
    transfer = max(d_corrected * oa, 1e-12)
    return 100.0 * transfer / (1.0 + transfer)


def _surrogate_features(frame: pd.DataFrame) -> np.ndarray:
    temperature = (frame["temperature_C"].astype(float).to_numpy() - 30.0) / 5.0
    ph = (frame["aqueous_pH"].astype(float).to_numpy() - 10.0) / 0.5
    topo = (frame["TOPO_wt_pct_in_organic"].astype(float).to_numpy() - 30.0) / 10.0
    na_li = np.log(frame["Na_Li_mass_ratio"].astype(float).to_numpy() / 10.0)
    return np.column_stack(
        [
            np.ones(len(frame), dtype=float),
            temperature,
            ph,
            topo,
            na_li,
            ph * topo,
            ph * na_li,
            topo * na_li,
        ]
    )


def _fit_distribution_surface() -> dict[str, Any]:
    if not UPSTREAM_REZAEE_ROWS.exists():
        raise FileNotFoundError(
            "Missing upstream calibrated Rezaee rows. Run the ePC-SAFT analysis first or set "
            f"EPCSAFT_REZAEE_SECTION32_ROWS. Looked for: {UPSTREAM_REZAEE_ROWS}"
        )
    source = pd.read_csv(UPSTREAM_REZAEE_ROWS)
    required = [
        "T_C",
        "pH",
        "topo_wt_pct",
        "na_li_mass_ratio",
        "revised_surface_no_kij_li_extraction_pct_calc",
        "revised_surface_no_kij_na_extraction_pct_calc",
    ]
    missing = [column for column in required if column not in source.columns]
    if missing:
        raise ValueError(f"Upstream Rezaee rows are missing required columns: {missing}")

    train = pd.DataFrame(
        {
            "temperature_C": source["T_C"].astype(float),
            "aqueous_pH": source["pH"].astype(float),
            "TOPO_wt_pct_in_organic": source["topo_wt_pct"].astype(float),
            "Na_Li_mass_ratio": source["na_li_mass_ratio"].astype(float),
        }
    )
    x = _surrogate_features(train)
    li_e = source["revised_surface_no_kij_li_extraction_pct_calc"].astype(float).clip(1.0e-6, 100.0 - 1.0e-6)
    na_e = source["revised_surface_no_kij_na_extraction_pct_calc"].astype(float).clip(1.0e-6, 100.0 - 1.0e-6)
    log_d_li = np.log((li_e / 100.0) / (1.0 - li_e / 100.0))
    log_d_na = np.log((na_e / 100.0) / (1.0 - na_e / 100.0))
    li_coefficients = np.linalg.lstsq(x, log_d_li.to_numpy(dtype=float), rcond=None)[0]
    na_coefficients = np.linalg.lstsq(x, log_d_na.to_numpy(dtype=float), rcond=None)[0]
    return {
        "source_path": str(UPSTREAM_REZAEE_ROWS),
        "row_count": int(len(source)),
        "feature_names": SURROGATE_FEATURE_NAMES,
        "log_D_Li_coefficients": li_coefficients.tolist(),
        "log_D_Na_coefficients": na_coefficients.tolist(),
        "training_Na_Li_min": float(train["Na_Li_mass_ratio"].min()),
        "training_Na_Li_max": float(train["Na_Li_mass_ratio"].max()),
        "training_T_C_min": float(train["temperature_C"].min()),
        "training_T_C_max": float(train["temperature_C"].max()),
        "training_pH_min": float(train["aqueous_pH"].min()),
        "training_pH_max": float(train["aqueous_pH"].max()),
        "training_TOPO_wt_pct_min": float(train["TOPO_wt_pct_in_organic"].min()),
        "training_TOPO_wt_pct_max": float(train["TOPO_wt_pct_in_organic"].max()),
    }


def _predict_log_distribution(row: dict[str, Any], surface: dict[str, Any]) -> tuple[float, float]:
    frame = pd.DataFrame(
        [
            {
                "temperature_C": row["temperature_C"],
                "aqueous_pH": row["aqueous_pH"],
                "TOPO_wt_pct_in_organic": row["TOPO_wt_pct_in_organic"],
                "Na_Li_mass_ratio": row["Na_Li_mass_ratio"],
            }
        ]
    )
    features = _surrogate_features(frame)[0]
    log_d_li = float(features @ np.asarray(surface["log_D_Li_coefficients"], dtype=float))
    log_d_na = float(features @ np.asarray(surface["log_D_Na_coefficients"], dtype=float))
    return log_d_li, log_d_na


def build_design() -> list[dict[str, Any]]:
    seed = pd.read_csv(SEED_MATRIX)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(row: dict[str, Any]) -> None:
        key = str(row["case_id"])
        if key in seen:
            return
        seen.add(key)
        row["sample_id"] = len(rows)
        rows.append(row)

    for _, row in seed.iterrows():
        case_id = str(row["case_id"])
        if case_id == "rezaee_paper_nominal":
            continue
        add(
            {
                "case_id": case_id,
                "sample_type": "seed_anchor",
                "temperature_C": 23.0,
                "aqueous_pH": 10.4,
                "TOPO_wt_pct_in_organic": 10.0,
                "TDS_feature_mg_L": float(row["TDS_feature_mg_L"]),
                "Li_feed_mg_L": float(row["Li_feed_mg_L"]),
                "organic_to_aqueous_mass_ratio": float(row["organic_to_aqueous_mass_ratio"]),
                "residual_divalent_mg_L": float(row["residual_divalent_mg_L"]),
            }
        )

    explicit = [
        ("corner_high_tds_low_li_low_oa", 340000.0, 100.0, 0.5),
        ("corner_high_tds_high_li_low_oa", 340000.0, 300.0, 0.5),
        ("corner_low_tds_high_li_high_oa", 152500.0, 300.0, 1.5),
        ("corner_low_tds_low_li_high_oa", 152500.0, 100.0, 1.5),
        ("nominal_ms2_clean_li_na", 305000.0, 168.0, 1.0),
    ]
    for case_id, tds, li, oa in explicit:
        add(
            {
                "case_id": case_id,
                "sample_type": "explicit_corner",
                "temperature_C": 23.0,
                "aqueous_pH": 10.4,
                "TOPO_wt_pct_in_organic": 10.0,
                "TDS_feature_mg_L": tds,
                "Li_feed_mg_L": li,
                "organic_to_aqueous_mass_ratio": oa,
                "residual_divalent_mg_L": 0.0,
            }
        )

    lhs = _latin_hypercube(N_LHS, 3, RANDOM_SEED)
    for i, sample in enumerate(lhs):
        add(
            {
                "case_id": f"lhs_{i:04d}",
                "sample_type": "lhs_synthetic_scaffold",
                "temperature_C": 23.0,
                "aqueous_pH": 10.4,
                "TOPO_wt_pct_in_organic": 10.0,
                "TDS_feature_mg_L": 152500.0 + sample[0] * (340000.0 - 152500.0),
                "Li_feed_mg_L": 100.0 + sample[1] * (300.0 - 100.0),
                "organic_to_aqueous_mass_ratio": 0.5 + sample[2],
                "residual_divalent_mg_L": 0.0,
            }
        )
    return rows


def predict_row(row: dict[str, Any], surface: dict[str, Any]) -> dict[str, Any]:
    tds = float(row["TDS_feature_mg_L"])
    li = float(row["Li_feed_mg_L"])
    oa = float(row["organic_to_aqueous_mass_ratio"])
    na = tds * NA_FRACTION_OF_TDS
    na_li = na / li

    row_with_na = {**row, "Na_mg_L": na, "Na_Li_mass_ratio": na_li}
    log_d_li, log_d_na = _predict_log_distribution(row_with_na, surface)
    d_li_corr = math.exp(_bounded(log_d_li, -12.0, 6.0))
    d_na_corr = math.exp(_bounded(log_d_na, -12.0, 6.0))
    li_ext = _bounded(_e_from_d(d_li_corr, oa), 0.0, 99.999)
    na_ext = _bounded(_e_from_d(d_na_corr, oa), 0.0, 99.999)

    d_li_equal, d_li_phase = _d_from_e(li_ext, oa)
    d_na_equal, d_na_phase = _d_from_e(na_ext, oa)
    selectivity = d_li_equal / max(d_na_equal, 1e-12)

    raff_li = li * (1.0 - li_ext / 100.0)
    raff_na = na * (1.0 - na_ext / 100.0)
    ext_li_load = (li * li_ext / 100.0) / oa
    ext_na_load = (na * na_ext / 100.0) / oa
    stage_count = 3
    li_cumulative = 100.0 * (1.0 - (1.0 - li_ext / 100.0) ** stage_count)
    na_cumulative = 100.0 * (1.0 - (1.0 - na_ext / 100.0) ** stage_count)

    flags: list[str] = []
    if not surface["training_Na_Li_min"] <= na_li <= surface["training_Na_Li_max"]:
        flags.append("outside_rezaee_doe_na_li")
    if not 100.0 <= li <= 300.0:
        flags.append("outside_surrogate_li_design_range")
    if tds > 305000.0:
        flags.append("high_tds_process_feature")
    if float(row["residual_divalent_mg_L"]) > 0.0:
        flags.append("residual_divalent_guardrail")
    validity_flag = "calibrated_surface_valid_for_surrogate" if not flags else "calibrated_surface_with_warnings"

    out = dict(row)
    out.update(
        {
            "model_basis": CALIBRATED_MODEL_BASIS,
            "Na_mg_L": na,
            "Na_Li_mass_ratio": na_li,
            "li_extraction_pct": li_ext,
            "na_extraction_pct": na_ext,
            "selectivity_Li_Na": selectivity,
            "D_Li_equal_phase_basis": d_li_equal,
            "D_Na_equal_phase_basis": d_na_equal,
            "D_Li_phase_ratio_corrected": d_li_phase,
            "D_Na_phase_ratio_corrected": d_na_phase,
            "three_stage_li_cumulative_pct": li_cumulative,
            "three_stage_na_cumulative_pct": na_cumulative,
            "raffinate_Li_mg_L": raff_li,
            "raffinate_Na_mg_L": raff_na,
            "extract_Li_loading_mg_per_kg_org": ext_li_load,
            "extract_Na_loading_mg_per_kg_org": ext_na_load,
            "activity_gamma_Li": math.nan,
            "activity_gamma_Na": math.nan,
            "activity_gamma_OH": math.nan,
            "activity_gamma_H2O": math.nan,
            "organic_gamma_DES": math.nan,
            "organic_gamma_RLi": math.nan,
            "organic_gamma_RNa": math.nan,
            "log_D_Li_surface": log_d_li,
            "log_D_Na_surface": log_d_na,
            "log10_D_Li_phase_ratio_corrected": math.log10(max(d_li_phase, 1.0e-300)),
            "log10_D_Na_phase_ratio_corrected": math.log10(max(d_na_phase, 1.0e-300)),
            "log10_Keff_over_Kpaper_Li": math.nan,
            "log10_Keff_over_Kpaper_Na": math.nan,
            "validity_flag": validity_flag,
            "validity_notes": "; ".join(flags) or "Calibrated Rezaee Section 3.2 DOE-basis distribution surrogate row.",
        }
    )
    return out


def build_transfer_rows(predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in predictions:
        rows.append(
            {
                "case_id": row["case_id"],
                "sample_id": row["sample_id"],
                "sample_type": row["sample_type"],
                "model_basis": row["model_basis"],
                "temperature_C": row["temperature_C"],
                "aqueous_pH": row["aqueous_pH"],
                "TOPO_wt_pct_in_organic": row["TOPO_wt_pct_in_organic"],
                "TDS_feature_mg_L": row["TDS_feature_mg_L"],
                "Li_feed_mg_L": row["Li_feed_mg_L"],
                "Na_mg_L": row["Na_mg_L"],
                "Na_Li_mass_ratio": row["Na_Li_mass_ratio"],
                "organic_to_aqueous_mass_ratio": row["organic_to_aqueous_mass_ratio"],
                "stage_count": 3,
                "one_stage_Li_extraction_pct": row["li_extraction_pct"],
                "one_stage_Na_extraction_pct": row["na_extraction_pct"],
                "three_stage_Li_cumulative_pct": row["three_stage_li_cumulative_pct"],
                "three_stage_Na_cumulative_pct": row["three_stage_na_cumulative_pct"],
                "D_Li_phase_ratio_corrected": row["D_Li_phase_ratio_corrected"],
                "D_Na_phase_ratio_corrected": row["D_Na_phase_ratio_corrected"],
                "selectivity_Li_Na": row["selectivity_Li_Na"],
                "validity_flag": row["validity_flag"],
                "validity_notes": row["validity_notes"],
            }
        )
    return rows


def _annual_li2co3(row: dict[str, Any], flow_m3_day: float) -> tuple[float, float, float]:
    operating_days = OPERATING_HOURS_YEAR / 24.0
    li_feed_kg_year = flow_m3_day * 1000.0 * float(row["Li_feed_mg_L"]) * 1e-6 * operating_days
    recovered_li_kg_year = li_feed_kg_year * float(row["three_stage_li_cumulative_pct"]) / 100.0
    li2co3_t_year = recovered_li_kg_year * LI2CO3_PER_LI / 1000.0
    return li_feed_kg_year, recovered_li_kg_year, li2co3_t_year


def build_costing_rows(predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_case = {row["case_id"]: row for row in predictions}
    scenarios = [
        ("stress", by_case["corner_high_tds_low_li_low_oa"], 1000.0, 12000.0),
        ("base", by_case["nominal_ms2_clean_li_na"], 1000.0, 20000.0),
        ("favorable", by_case["corner_low_tds_high_li_high_oa"], 1000.0, 35000.0),
    ]
    rows = []
    for scenario, row, flow, price in scenarios:
        li_feed_kg_year, li_recovered_kg_year, li2co3_t_year = _annual_li2co3(row, flow)
        annual_m3 = flow * OPERATING_HOURS_YEAR / 24.0
        tds_factor = float(row["TDS_feature_mg_L"]) / 305000.0
        oa = float(row["organic_to_aqueous_mass_ratio"])
        gross_revenue = li2co3_t_year * price
        pretreatment = annual_m3 * 0.35 * tds_factor
        extraction = annual_m3 * 0.55 * (0.8 + oa)
        concentration = max(li2co3_t_year, 1e-9) * 1000.0 * 3.25
        solvent_makeup = annual_m3 * 0.22 * oa
        installed_capex = 185000.0 * (flow / 100.0) ** 0.65 * (0.75 + 0.5 * oa)
        annualized_capex = installed_capex * 0.20
        total_annual_cost = pretreatment + extraction + concentration + solvent_makeup + annualized_capex
        rows.append(
            {
                "scenario": scenario,
                "case_id": row["case_id"],
                "feed_flow_m3_day": flow,
                "operating_hours_year": OPERATING_HOURS_YEAR,
                "Li_feed_mg_L": row["Li_feed_mg_L"],
                "TDS_feature_mg_L": row["TDS_feature_mg_L"],
                "organic_to_aqueous_mass_ratio": oa,
                "Li_recovery_pct_used_for_costing": row["three_stage_li_cumulative_pct"],
                "Li_feed_kg_year": li_feed_kg_year,
                "Li_recovered_kg_year": li_recovered_kg_year,
                "Li2CO3_product_t_year": li2co3_t_year,
                "Li2CO3_price_usd_t_assumption": price,
                "gross_revenue_usd_year": gross_revenue,
                "pretreatment_opex_usd_year": pretreatment,
                "extraction_opex_usd_year": extraction,
                "concentration_precip_opex_usd_year": concentration,
                "solvent_makeup_opex_usd_year": solvent_makeup,
                "installed_contactor_capex_usd": installed_capex,
                "annualized_capex_usd_year": annualized_capex,
                "total_annual_cost_usd_year": total_annual_cost,
                "net_before_tax_usd_year": gross_revenue - total_annual_cost,
                "costing_status": "calibrated_rezaee_distribution_surrogate_for_prommis_idaes_readiness",
            }
        )
    return rows


def make_figures(pred: pd.DataFrame, costing: pd.DataFrame) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    sc = ax.scatter(
        pred["Li_feed_mg_L"],
        pred["li_extraction_pct"],
        c=pred["organic_to_aqueous_mass_ratio"],
        s=20 + 0.00008 * pred["TDS_feature_mg_L"],
        cmap="viridis",
        alpha=0.72,
        edgecolor="none",
    )
    ax.set_xlabel("Li feed (mg/L)")
    ax.set_ylabel("One-stage Li extraction (%)")
    ax.set_title("Calibrated Rezaee surrogate: Li extraction over Li grade and O/A")
    ax.grid(True, alpha=0.25)
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label("Organic/aqueous mass ratio")
    fig.tight_layout()
    fig.savefig(FIGURES / "calibrated_li_extraction_surface.png", dpi=220)
    fig.savefig(FIGURES / "calibrated_li_extraction_surface.svg")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    ax.scatter(
        pred["Na_Li_mass_ratio"], pred["selectivity_Li_Na"], c=pred["TDS_feature_mg_L"], cmap="magma", alpha=0.72
    )
    ax.set_xlabel("Na/Li mass ratio")
    ax.set_ylabel("Li/Na selectivity")
    ax.set_title("Calibrated Rezaee surrogate: selectivity under produced-water sodium load")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "calibrated_selectivity_vs_na_li.png", dpi=220)
    fig.savefig(FIGURES / "calibrated_selectivity_vs_na_li.svg")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    ax.bar(costing["scenario"], costing["net_before_tax_usd_year"] / 1e6, color=["#9b5f2e", "#2f6f8f", "#3b7f4c"])
    ax.axhline(0, color="#222222", linewidth=0.9)
    ax.set_ylabel("Net before tax (million USD/year)")
    ax.set_title("Calibrated surrogate costing scenarios at 1000 m3/day")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "calibrated_costing_scenarios.png", dpi=220)
    fig.savefig(FIGURES / "calibrated_costing_scenarios.svg")
    plt.close(fig)


def validate(predictions: list[dict[str, Any]], surface: dict[str, Any]) -> dict[str, Any]:
    df = pd.DataFrame(predictions)
    finite_cols = [
        "TDS_feature_mg_L",
        "Li_feed_mg_L",
        "Na_mg_L",
        "Na_Li_mass_ratio",
        "li_extraction_pct",
        "na_extraction_pct",
        "D_Li_phase_ratio_corrected",
        "D_Na_phase_ratio_corrected",
    ]
    finite_ok = bool(np.isfinite(df[finite_cols].to_numpy(dtype=float)).all())
    sodium_error = np.max(np.abs(df["Na_mg_L"] - df["TDS_feature_mg_L"] * NA_FRACTION_OF_TDS))
    ratio_error = np.max(np.abs(df["Na_Li_mass_ratio"] - df["Na_mg_L"] / df["Li_feed_mg_L"]))
    nominal_count = int(df["case_id"].eq("nominal_ms2_clean_li_na").sum())
    return {
        "row_count": int(len(df)),
        "random_seed": RANDOM_SEED,
        "model_basis": CALIBRATED_MODEL_BASIS,
        "upstream_rezaee_rows": surface["source_path"],
        "upstream_training_rows": surface["row_count"],
        "surrogate_feature_names": surface["feature_names"],
        "training_Na_Li_min": surface["training_Na_Li_min"],
        "training_Na_Li_max": surface["training_Na_Li_max"],
        "finite_outputs": finite_ok,
        "nominal_ms2_count": nominal_count,
        "max_sodium_derivation_abs_error": float(sodium_error),
        "max_na_li_ratio_abs_error": float(ratio_error),
        "li_extraction_min": float(df["li_extraction_pct"].min()),
        "li_extraction_max": float(df["li_extraction_pct"].max()),
        "na_extraction_min": float(df["na_extraction_pct"].min()),
        "na_extraction_max": float(df["na_extraction_pct"].max()),
        "D_Li_phase_ratio_corrected_min": float(df["D_Li_phase_ratio_corrected"].min()),
        "D_Li_phase_ratio_corrected_max": float(df["D_Li_phase_ratio_corrected"].max()),
        "D_Na_phase_ratio_corrected_min": float(df["D_Na_phase_ratio_corrected"].min()),
        "D_Na_phase_ratio_corrected_max": float(df["D_Na_phase_ratio_corrected"].max()),
        "validity_flags": df["validity_flag"].value_counts().to_dict(),
        "status": "passed"
        if finite_ok and nominal_count == 1 and sodium_error < 1e-9 and ratio_error < 1e-9
        else "failed",
    }


def report_text(summary: dict[str, Any], costing_rows: list[dict[str, Any]]) -> str:
    cost_lines = [
        f"| {row['scenario']} | {row['Li_recovery_pct_used_for_costing']:.2f} | {row['Li2CO3_product_t_year']:.2f} | {row['net_before_tax_usd_year'] / 1e6:.2f} |"
        for row in costing_rows
    ]
    return "\n".join(
        [
            "# Rezaee TDS-Li-OA Calibrated Distribution Surrogate",
            "",
            "Date: 2026-05-08",
            "",
            "## Purpose",
            "",
            "This dataset is a deterministic calibrated surrogate-run matrix for exercising the Lithium_Extraction to PrOMMiS/IDAES workflow with Rezaee Section 3.2 distribution-coefficient outputs. It consumes the upstream ePC-SAFT Rezaee DOE-basis surface results and fits a lightweight log-distribution response surface for fast UQ/design sweeps.",
            "",
            "## Scope",
            "",
            f"- Rows: `{summary['row_count']}`",
            f"- Random seed: `{summary['random_seed']}`",
            f"- Model basis label: `{summary['model_basis']}`",
            f"- Upstream rows: `{summary['upstream_training_rows']}` from `{summary['upstream_rezaee_rows']}`",
            "- UQ variables: TDS feature, Li feed concentration, organic/aqueous mass ratio.",
            "- Fixed chemistry variables: T = 23 C, pH = 10.4, TOPO = 10 wt%, residual divalent = 0 mg/L except guardrail rows.",
            "",
            "## Costing Readiness Scenarios",
            "",
            "| Scenario | Li recovery used (%) | Li2CO3 t/year | Net before tax (million USD/year) |",
            "|---|---:|---:|---:|",
            *cost_lines,
            "",
            "## Validation Summary",
            "",
            f"- Status: `{summary['status']}`",
            f"- Finite outputs: `{summary['finite_outputs']}`",
            f"- Nominal MS-2 row count: `{summary['nominal_ms2_count']}`",
            f"- Li extraction range: `{summary['li_extraction_min']:.2f}-{summary['li_extraction_max']:.2f}%`",
            f"- Na extraction range: `{summary['na_extraction_min']:.2f}-{summary['na_extraction_max']:.2f}%`",
            f"- Phase-ratio-corrected D_Li range: `{summary['D_Li_phase_ratio_corrected_min']:.4g}-{summary['D_Li_phase_ratio_corrected_max']:.4g}`",
            f"- Phase-ratio-corrected D_Na range: `{summary['D_Na_phase_ratio_corrected_min']:.4g}-{summary['D_Na_phase_ratio_corrected_max']:.4g}`",
            "",
            "## Figures",
            "",
            "![Li extraction surrogate](figures/calibrated_li_extraction_surface.png)",
            "",
            "![Selectivity surrogate](figures/calibrated_selectivity_vs_na_li.png)",
            "",
            "![Costing scenarios](figures/calibrated_costing_scenarios.png)",
            "",
            "## Boundary",
            "",
            "This is a surrogate over the calibrated Rezaee Section 3.2 DOE-basis surface, not a new direct reactive-LLE closure. Rows outside the Rezaee Na/Li training range are flagged and should be interpreted as produced-water extrapolations.",
            "",
        ]
    )


def main() -> None:
    surface = _fit_distribution_surface()
    design = build_design()
    predictions = [predict_row(row, surface) for row in design]
    transfer = build_transfer_rows(predictions)
    costing = build_costing_rows(predictions)
    summary = validate(predictions, surface)

    _write_csv(DESIGN, design)
    _write_csv(PREDICTIONS, predictions)
    _write_csv(PROMMIS_TRANSFER, transfer)
    _write_csv(COSTING_INPUT, costing)

    pred_df = pd.DataFrame(predictions)
    cost_df = pd.DataFrame(costing)
    make_figures(pred_df, cost_df)

    RESULTS.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    REPORT.write_text(report_text(summary, costing), encoding="utf-8")

    for src, dst in LEGACY_FILES.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
