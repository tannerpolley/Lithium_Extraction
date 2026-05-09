from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS = Path(__file__).resolve().parents[1]
DATA_IN = ANALYSIS / "data" / "input"
DATA_OUT = ANALYSIS / "data" / "processed"
RESULTS = ANALYSIS / "results" / "surrogate_input_space"
FIGURES = RESULTS / "figures"
REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"

CLEAN_FEED = DATA_OUT / "rezaee_clean_li_na_pretreated_feed_basis.csv"
VARIABLE_RANGES = DATA_OUT / "rezaee_surrogate_input_variable_ranges.csv"
SEED_RUNS = DATA_OUT / "rezaee_surrogate_seed_run_matrix.csv"
REPORT = RESULTS / "rezaee_clean_li_na_surrogate_input_space.md"
FIGURE = FIGURES / "rezaee_surrogate_input_ranges.png"

LEGACY_CLEAN_FEED = REF_DIR / "rezaee_clean_li_na_pretreated_feed_basis.csv"
LEGACY_VARIABLE_RANGES = REF_DIR / "rezaee_surrogate_input_variable_ranges.csv"
LEGACY_SEED_RUNS = REF_DIR / "rezaee_surrogate_seed_run_matrix.csv"
LEGACY_REPORT = REF_DIR / "rezaee_clean_li_na_surrogate_input_space.md"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_clean_feed() -> list[dict[str, Any]]:
    source = pd.read_csv(REF_DIR / "smackover_li_tds_sensitivity_basis.csv")
    base = source.loc[source["case_id"].eq("smackover_clean_median_tds_proxy")].iloc[0]
    divalent_cols = ["Mg_mg_L", "Ca_mg_L", "Sr_mg_L", "Ba_mg_L"]
    divalent_load = sum(float(base[col]) for col in divalent_cols)
    li = float(base["Li_mg_L"])
    na = float(base["Na_mg_L"])
    tds = float(base["TDS_mg_L"])
    rows = []
    for removal in [0.95, 0.99, 0.999]:
        rows.append(
            {
                "case_id": f"ms2_clean_li_na_divalent_removal_{removal:.3f}".replace(".", "p"),
                "source_site_id": base["site_id"],
                "source_field": base["field"],
                "starting_basis": "post_pretreatment_clean_li_na_stream",
                "Li_mg_L": li,
                "Na_mg_L": na,
                "Na_Li_mass_ratio": na / li,
                "source_TDS_mg_L": tds,
                "TDS_feature_mg_L": tds,
                "pretreatment_removal_target_fraction": removal,
                "removed_Mg_mg_L": float(base["Mg_mg_L"]) * removal,
                "removed_Ca_mg_L": float(base["Ca_mg_L"]) * removal,
                "removed_Sr_mg_L": float(base["Sr_mg_L"]) * removal,
                "removed_Ba_mg_L": float(base["Ba_mg_L"]) * removal,
                "residual_divalent_mg_L": divalent_load * (1.0 - removal),
                "residual_divalent_Li_mass_ratio": divalent_load * (1.0 - removal) / li,
                "modeling_note": (
                    "Li and Na are the extraction feed species. TDS is retained as a salinity/process feature "
                    "until a concrete pretreatment mass-balance script updates chloride, alkalinity, and reagent addition."
                ),
            }
        )
    return rows


def build_variable_ranges(clean_feed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = clean_feed[1]
    return [
        {
            "variable": "temperature_C",
            "unit": "deg C",
            "paper_tested_min": 20.0,
            "paper_tested_max": 40.0,
            "recommended_surrogate_min": 20.0,
            "recommended_surrogate_max": 35.0,
            "nominal": 23.0,
            "source_basis": "Rezaee 2025 RSM DOE",
            "effect_summary": "Temperature was the strongest reported selectivity factor; lower temperature favored selectivity.",
            "surrogate_priority": "high",
        },
        {
            "variable": "aqueous_pH",
            "unit": "pH",
            "paper_tested_min": 9.0,
            "paper_tested_max": 11.0,
            "recommended_surrogate_min": 9.5,
            "recommended_surrogate_max": 10.8,
            "nominal": 10.4,
            "source_basis": "Rezaee 2025 RSM DOE and optimum-neighborhood rows",
            "effect_summary": "pH was the strongest reported lithium-extraction factor; pH above 11 caused third phase/emulsion risk.",
            "surrogate_priority": "very_high",
        },
        {
            "variable": "TOPO_wt_pct_in_organic",
            "unit": "wt pct",
            "paper_tested_min": 10.0,
            "paper_tested_max": 50.0,
            "recommended_surrogate_min": 10.0,
            "recommended_surrogate_max": 30.0,
            "nominal": 10.0,
            "source_basis": "Rezaee 2025 RSM DOE, coextractant screen, and final economic selection",
            "effect_summary": "TOPO has a weak but nonzero response effect; 10 wt pct was selected to reduce TOPO cost while retaining Li extraction.",
            "surrogate_priority": "high",
        },
        {
            "variable": "Na_Li_mass_ratio",
            "unit": "mass ratio",
            "paper_tested_min": 5.0,
            "paper_tested_max": 15.0,
            "recommended_surrogate_min": 190.0,
            "recommended_surrogate_max": 575.0,
            "nominal": float(base["Na_Li_mass_ratio"]),
            "source_basis": "Rezaee 2025 DOE and clean MS-2 Smackover Li/Na stream",
            "effect_summary": "Rezaee reported weak Li-extraction response in the paper domain; produced water forces a high-Na extrapolation that must be mapped explicitly.",
            "surrogate_priority": "very_high",
        },
        {
            "variable": "Li_feed_mg_L",
            "unit": "mg/L",
            "paper_tested_min": 50.0,
            "paper_tested_max": 1000.0,
            "recommended_surrogate_min": 100.0,
            "recommended_surrogate_max": 300.0,
            "nominal": float(base["Li_mg_L"]),
            "source_basis": "Rezaee 2025 initial-lithium test and produced-water screening",
            "effect_summary": "Extraction percentage was stable across 50-1000 ppm in Rezaee; produced-water candidate ranking is strongly tied to Li grade.",
            "surrogate_priority": "high",
        },
        {
            "variable": "organic_to_aqueous_mass_ratio",
            "unit": "mass ratio",
            "paper_tested_min": 0.5,
            "paper_tested_max": 2.0,
            "recommended_surrogate_min": 0.5,
            "recommended_surrogate_max": 1.5,
            "nominal": 1.0,
            "source_basis": "Rezaee 2025 aqueous-to-organic ratio discussion and current bridge grid",
            "effect_summary": "Higher aqueous-to-organic ratio decreased extraction; O/A controls stage capacity and distribution-coefficient interpretation.",
            "surrogate_priority": "very_high",
        },
        {
            "variable": "TDS_feature_mg_L",
            "unit": "mg/L",
            "paper_tested_min": "",
            "paper_tested_max": "",
            "recommended_surrogate_min": 152500.0,
            "recommended_surrogate_max": 340000.0,
            "nominal": float(base["TDS_feature_mg_L"]),
            "source_basis": "Smackover clean low/base/high rows and current Rezaee bridge sensitivity",
            "effect_summary": "TDS is not a fitted Rezaee response variable yet; keep it as a salinity and costing/process feature until direct LLE or activity-based surrogate rows are generated.",
            "surrogate_priority": "medium",
        },
        {
            "variable": "residual_divalent_mg_L",
            "unit": "mg/L",
            "paper_tested_min": 0.0,
            "paper_tested_max": "",
            "recommended_surrogate_min": 0.0,
            "recommended_surrogate_max": 430.0,
            "nominal": 0.0,
            "source_basis": "Pretreatment assumption from selected produced-water basis",
            "effect_summary": "Not an active extraction variable; carry as a validation flag and pretreatment-cost variable so divalent leakage does not silently enter the Li/Na model.",
            "surrogate_priority": "guardrail",
        },
    ]


def build_seed_runs(ranges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    values = {row["variable"]: row for row in ranges}
    base = {
        "temperature_C": 23.0,
        "aqueous_pH": 10.4,
        "TOPO_wt_pct_in_organic": 10.0,
        "Na_Li_mass_ratio": values["Na_Li_mass_ratio"]["nominal"],
        "Li_feed_mg_L": values["Li_feed_mg_L"]["nominal"],
        "organic_to_aqueous_mass_ratio": 1.0,
        "TDS_feature_mg_L": values["TDS_feature_mg_L"]["nominal"],
        "residual_divalent_mg_L": 0.0,
    }
    rows: list[dict[str, Any]] = []

    def add(case_id: str, note: str, **overrides: float) -> None:
        row = dict(base)
        row.update(overrides)
        row.update({"case_id": case_id, "purpose": note})
        rows.append(row)

    add("rezaee_paper_nominal", "Paper selected operating point on the clean Li/Na basis.", Na_Li_mass_ratio=5.0, Li_feed_mg_L=1000.0, TDS_feature_mg_L=0.0)
    add("ms2_clean_li_na_nominal", "Selected Smackover MS-2 clean Li/Na base case.")
    for variable in [
        "temperature_C",
        "aqueous_pH",
        "TOPO_wt_pct_in_organic",
        "Na_Li_mass_ratio",
        "Li_feed_mg_L",
        "organic_to_aqueous_mass_ratio",
        "TDS_feature_mg_L",
    ]:
        low = float(values[variable]["recommended_surrogate_min"])
        high = float(values[variable]["recommended_surrogate_max"])
        add(f"{variable}_low", f"One-factor low bound for {variable}.", **{variable: low})
        add(f"{variable}_high", f"One-factor high bound for {variable}.", **{variable: high})
    add(
        "stress_high_na_high_tds_low_oa",
        "Produced-water stress point for high sodium, high salinity, and low solvent inventory.",
        Na_Li_mass_ratio=575.0,
        TDS_feature_mg_L=340000.0,
        organic_to_aqueous_mass_ratio=0.5,
    )
    add(
        "best_practical_selectivity_corner",
        "Lower-temperature, controlled-pH, nominal TOPO corner for selectivity.",
        temperature_C=20.0,
        aqueous_pH=10.4,
        TOPO_wt_pct_in_organic=10.0,
        organic_to_aqueous_mass_ratio=1.5,
    )
    add(
        "pretreatment_leakage_guardrail",
        "Same Li/Na basis with residual divalent leakage carried only as a guardrail.",
        residual_divalent_mg_L=430.0,
    )
    return rows


def plot_ranges(ranges: list[dict[str, Any]]) -> None:
    rows = [row for row in ranges if row["surrogate_priority"] != "guardrail"]
    labels = [row["variable"].replace("_", " ") for row in rows]
    y = range(len(rows))
    fig, ax = plt.subplots(figsize=(11.0, 6.2))
    for i, row in enumerate(rows):
        xmin = float(row["recommended_surrogate_min"])
        xmax = float(row["recommended_surrogate_max"])
        nominal = float(row["nominal"])
        if row["paper_tested_min"] != "":
            pmin = float(row["paper_tested_min"])
            pmax = float(row["paper_tested_max"])
            scale_min = min(xmin, pmin, nominal)
            scale_max = max(xmax, pmax, nominal)
        else:
            pmin = pmax = None
            scale_min = min(xmin, nominal)
            scale_max = max(xmax, nominal)
        span = scale_max - scale_min or 1.0

        def norm(value: float) -> float:
            return 0.12 + 0.55 * ((value - scale_min) / span)

        ax.plot([norm(xmin), norm(xmax)], [i, i], color="#2f6f8f", linewidth=8, solid_capstyle="round")
        if row["paper_tested_min"] != "":
            assert pmin is not None and pmax is not None
            ax.plot([norm(pmin), norm(pmax)], [i + 0.18, i + 0.18], color="#e08b2c", linewidth=3, solid_capstyle="round")
        ax.scatter([norm(nominal)], [i], s=70, color="#111111", zorder=3)
        ax.text(0.71, i, f"recommended {xmin:g} to {xmax:g} {row['unit']}", va="center", fontsize=8)
        if row["paper_tested_min"] != "":
            ax.text(0.71, i + 0.22, f"paper {pmin:g} to {pmax:g}", va="center", fontsize=7, color="#9a5a12")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks([])
    ax.set_xlabel("Each row is scaled to that variable's combined paper and produced-water range")
    ax.set_title("Recommended clean Li+Na surrogate input ranges")
    ax.grid(True, axis="y", alpha=0.15)
    fig.tight_layout()
    FIGURES.mkdir(parents=True, exist_ok=True)
    for suffix in ["png", "svg"]:
        fig.savefig(FIGURES / f"rezaee_surrogate_input_ranges.{suffix}", dpi=220)
    plt.close(fig)


def report_text(clean_feed: list[dict[str, Any]], ranges: list[dict[str, Any]], runs: list[dict[str, Any]]) -> str:
    base = clean_feed[1]
    top_vars = [row for row in ranges if row["surrogate_priority"] in {"very_high", "high"}]
    range_lines = [
        f"| {row['variable']} | {row['recommended_surrogate_min']} to {row['recommended_surrogate_max']} {row['unit']} | {row['nominal']} | {row['surrogate_priority']} | {row['effect_summary']} |"
        for row in top_vars
    ]
    return "\n".join(
        [
            "# Rezaee Clean Li/Na Surrogate Input Space",
            "",
            "Date: 2026-05-08",
            "",
            "## Basis",
            "",
            "The selected produced-water site is treated as a source-backed Smackover feed followed by an upstream pretreatment block. The extraction model starts after divalent removal, with lithium and sodium as the active aqueous cations. Calcium, magnesium, strontium, and barium remain pretreatment-cost and validation-guardrail variables, not active extraction species.",
            "",
            f"Nominal clean-stream basis: Li `{base['Li_mg_L']:.1f} mg/L`, Na `{base['Na_mg_L']:.1f} mg/L`, Na/Li mass ratio `{base['Na_Li_mass_ratio']:.1f}`, source TDS feature `{base['TDS_feature_mg_L']:.0f} mg/L`.",
            "",
            "## High-Priority Variables",
            "",
            "| Variable | Recommended range | Nominal | Priority | Why it matters |",
            "|---|---:|---:|---|---|",
            *range_lines,
            "",
            "## Figure",
            "",
            "![Recommended clean Li+Na surrogate input ranges](figures/rezaee_surrogate_input_ranges.png)",
            "",
            "## Seed Run Matrix",
            "",
            f"The generated seed matrix contains `{len(runs)}` rows. It is not the final surrogate dataset. It is the input contract for the pending concrete script that will run the ePC-SAFT/Rezaee bridge over these variables and return distribution coefficients, extraction percentages, validity flags, and PrOMMiS/IDAES transfer variables.",
            "",
            "## Waiting Point",
            "",
            "The next phase should not fabricate surrogate response data. Until the concrete run script exists, the honest completion state is: feed basis, variable bounds, seed points, and downstream handoff schema are ready; response surfaces and optimizer-ready surrogate coefficients are pending the actual model-run generator.",
            "",
        ]
    )


def main() -> None:
    clean_feed = build_clean_feed()
    ranges = build_variable_ranges(clean_feed)
    runs = build_seed_runs(ranges)

    write_csv(CLEAN_FEED, clean_feed)
    write_csv(VARIABLE_RANGES, ranges)
    write_csv(SEED_RUNS, runs)
    plot_ranges(ranges)
    RESULTS.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report_text(clean_feed, ranges, runs), encoding="utf-8")

    for src, dst in [
        (CLEAN_FEED, LEGACY_CLEAN_FEED),
        (VARIABLE_RANGES, LEGACY_VARIABLE_RANGES),
        (SEED_RUNS, LEGACY_SEED_RUNS),
        (REPORT, LEGACY_REPORT),
    ]:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())

    for path in [CLEAN_FEED, VARIABLE_RANGES, SEED_RUNS, REPORT, FIGURE]:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
