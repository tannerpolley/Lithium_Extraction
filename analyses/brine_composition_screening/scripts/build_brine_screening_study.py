from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS = Path(__file__).resolve().parents[1]
DATA_DIR = ANALYSIS / "data" / "processed"
RESULTS_DIR = ANALYSIS / "results"
FIG_DIR = RESULTS_DIR / "figures"
REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"

BRINE_TABLE = DATA_DIR / "brine_composition_screening_table.csv"
SCORES = DATA_DIR / "produced_water_rezaee_candidate_scores.csv"
SOURCES = DATA_DIR / "brine_screening_source_log.csv"
REPORT = RESULTS_DIR / "brine_composition_screening_report.md"

LEGACY_REPORT = REF_DIR / "brine_composition_screening_report_2026_05_08.md"
LEGACY_TABLE = REF_DIR / "brine_composition_screening_table_2026_05_08.csv"
LEGACY_SCORES = REF_DIR / "produced_water_rezaee_candidate_scores_2026_05_08.csv"


SOURCE_LOG = [
    {
        "source_id": "USGS_PWDB_v23",
        "status": "public database",
        "title": "USGS National Produced Waters Geochemical Database v2.3",
        "url": "https://data.usgs.gov/datacatalog/data/USGS%3A59d25d63e4b05fe04cc235f9",
        "use": "Produced-water context, trace-element coverage, and database scope.",
    },
    {
        "source_id": "USGS_Smackover_2024",
        "status": "USGS report",
        "title": "Lithium resource in the Smackover Formation brines of Southern Arkansas",
        "url": "https://www.usgs.gov/publications/lithium-resource-smackover-formation-brines-southern-arkansas",
        "use": "Smackover resource context and southern Arkansas produced-water source rationale.",
    },
    {
        "source_id": "Local_Smackover_clean_rows",
        "status": "local cleaned source table derived from USGS southern Arkansas brines",
        "title": "Clean Smackover composition rows",
        "url": "internal curated data product",
        "use": "Low, base, and high Smackover composition cases.",
    },
    {
        "source_id": "Mackey_2024_Marcellus",
        "status": "peer-reviewed article",
        "title": "Estimates of lithium mass yields from produced water sourced from the Devonian-aged Marcellus Shale",
        "url": "https://www.nature.com/articles/s41598-024-58887-x",
        "use": "Marcellus Li, Mg, TDS, Mg/Li, and regional produced-water variability.",
    },
    {
        "source_id": "Jakaria_2025_Bakken",
        "status": "peer-reviewed article",
        "title": "Lithium and Salt Extraction from the Bakken Produced Water",
        "url": "https://link.springer.com/article/10.1007/s13202-025-02012-9",
        "use": "Bakken TDS, Na, Sr, K, Rb, critical-element context, and high-Li county signals.",
    },
    {
        "source_id": "Permian_valorization_2026",
        "status": "peer-reviewed article",
        "title": "Surrogate-Assisted Techno-Economic Optimization to Reduce Saltwater Disposal via Produced-Water Valorization",
        "url": "https://www.mdpi.com/2073-4441/18/6/739",
        "use": "Delaware and Midland Basin Li ranges and median TDS context from public abstract/snippet.",
    },
    {
        "source_id": "Miranda_2022_PW_review",
        "status": "peer-reviewed review",
        "title": "Treatment and Recovery of High-Value Elements from Produced Water",
        "url": "https://www.mdpi.com/2073-4441/14/6/880",
        "use": "Broad produced-water ranges for Na, Ca, Mg, K, Ba, Sr, Li, and REE/critical-mineral framing.",
    },
    {
        "source_id": "Salton_Nature_2025",
        "status": "peer-reviewed article",
        "title": "Electro-driven direct lithium extraction from geothermal brines to generate battery-grade lithium hydroxide",
        "url": "https://www.nature.com/articles/s41467-025-56071-x",
        "use": "Salton Sea synthetic geothermal brine compositions in mM, converted to mg/L.",
    },
    {
        "source_id": "USGS_Lithium_brines_2015",
        "status": "USGS report",
        "title": "Lithium brines: A global perspective",
        "url": "https://www.usgs.gov/publications/lithium-brines-a-global-perspective",
        "use": "Global brine-class framework and salar deposit controls.",
    },
    {
        "source_id": "Rezaee_2025_RSM",
        "status": "peer-reviewed article in local library",
        "title": "Application of Response Surface Methodology for Selective Extraction of Lithium Using a Hydrophobic Deep Eutectic Solvent",
        "url": "https://doi.org/10.1021/acs.iecr.4c03496",
        "use": "90 wt pct TBAC(1):DA(2) DES plus 10 wt pct TOPO optimum, extraction, selectivity, and model-brine composition.",
    },
    {
        "source_id": "Rezaee_2026_SI",
        "status": "supporting information in local library",
        "title": "Supplementary material for thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents",
        "url": "https://doi.org/10.1016/j.fluid.2026.114737",
        "use": "DES/TOPO/RLi/RNa thermodynamic-supporting inputs and density evidence.",
    },
]


def _salton_mM(li: float, na: float, ca: float, k: float, mg: float | None = None) -> dict[str, float | None]:
    return {
        "Li_mg_L": li * 6.94,
        "Na_mg_L": na * 22.989769,
        "Ca_mg_L": ca * 40.078,
        "K_mg_L": k * 39.0983,
        "Mg_mg_L": None if mg is None else mg * 24.305,
    }


def brine_rows() -> list[dict[str, Any]]:
    salton_a = _salton_mM(30, 2300, 690, 430, 1.5)
    salton_b = _salton_mM(42, 3100, 1070, 540, None)
    return [
        {
            "group": "produced water",
            "candidate": "Smackover AR low observed",
            "region_or_source": "Southern Arkansas Smackover",
            "Li_mg_L": 11.7,
            "TDS_mg_L": 156000,
            "Na_mg_L": 37100,
            "K_mg_L": 351,
            "Mg_mg_L": 2250,
            "Ca_mg_L": 13900,
            "Sr_mg_L": 907,
            "Ba_mg_L": 7.47,
            "B_mg_L": 47.5,
            "Br_mg_L": 1650,
            "REE_status": "not reported in clean local source set",
            "source_id": "Local_Smackover_clean_rows",
            "source_status": "source-backed local clean row",
            "notes": "Unfavorable clean Smackover bound; low Li but complete major-ion context.",
        },
        {
            "group": "produced water",
            "candidate": "Smackover AR MS-2 base",
            "region_or_source": "Southern Arkansas Smackover",
            "Li_mg_L": 168,
            "TDS_mg_L": 305000,
            "Na_mg_L": 64100,
            "K_mg_L": 2300,
            "Mg_mg_L": 3310,
            "Ca_mg_L": 36900,
            "Sr_mg_L": 1940,
            "Ba_mg_L": 8.39,
            "B_mg_L": 163,
            "Br_mg_L": 2700,
            "REE_status": "not reported in clean local source set",
            "source_id": "Local_Smackover_clean_rows",
            "source_status": "source-backed local clean row",
            "notes": "Base produced-water candidate: high Li, high TDS, high Ca/Sr pretreatment burden.",
        },
        {
            "group": "produced water",
            "candidate": "Smackover AR high observed",
            "region_or_source": "Southern Arkansas Smackover",
            "Li_mg_L": 252,
            "TDS_mg_L": 340000,
            "Na_mg_L": 70800,
            "K_mg_L": 3160,
            "Mg_mg_L": 3130,
            "Ca_mg_L": 39900,
            "Sr_mg_L": 2490,
            "Ba_mg_L": 26.1,
            "B_mg_L": 212,
            "Br_mg_L": 5510,
            "REE_status": "not reported in clean local source set",
            "source_id": "Local_Smackover_clean_rows",
            "source_status": "source-backed local clean row",
            "notes": "Highest Li and TDS clean Smackover row in the local set.",
        },
        {
            "group": "produced water",
            "candidate": "Marcellus NE PA median",
            "region_or_source": "Appalachian Basin / Marcellus",
            "Li_mg_L": 205,
            "TDS_mg_L": 100000,
            "Na_mg_L": None,
            "K_mg_L": None,
            "Mg_mg_L": 1000,
            "Ca_mg_L": None,
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "B_mg_L": None,
            "Br_mg_L": None,
            "REE_status": "not emphasized in source; produced-water database may contain trace data",
            "source_id": "Mackey_2024_Marcellus",
            "source_status": "peer-reviewed regional median",
            "notes": "High Li and low Mg/Li relative to SW PA; TDS shown as literature lower-bound class.",
        },
        {
            "group": "produced water",
            "candidate": "Marcellus SW PA median",
            "region_or_source": "Appalachian Basin / Marcellus",
            "Li_mg_L": 127,
            "TDS_mg_L": 100000,
            "Na_mg_L": None,
            "K_mg_L": None,
            "Mg_mg_L": 2300,
            "Ca_mg_L": None,
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "B_mg_L": None,
            "Br_mg_L": None,
            "REE_status": "not emphasized in source; produced-water database may contain trace data",
            "source_id": "Mackey_2024_Marcellus",
            "source_status": "peer-reviewed regional median",
            "notes": "Lower Li and higher Mg/Li than NE PA but larger produced-water volume per well.",
        },
        {
            "group": "produced water",
            "candidate": "Bakken high-Li county signal",
            "region_or_source": "Williston Basin / Bakken",
            "Li_mg_L": 103,
            "TDS_mg_L": 258193,
            "Na_mg_L": 79415,
            "K_mg_L": 11730,
            "Mg_mg_L": None,
            "Ca_mg_L": None,
            "Sr_mg_L": 1631.66,
            "Ba_mg_L": None,
            "B_mg_L": None,
            "Br_mg_L": None,
            "REE_status": "REE recovery discussed; specific REE values not used here",
            "source_id": "Jakaria_2025_Bakken",
            "source_status": "peer-reviewed article; mixed figure/table extraction",
            "notes": "High salinity, high Na, high Sr/Rb; Li from highest reported county average.",
        },
        {
            "group": "produced water",
            "candidate": "Permian Delaware typical",
            "region_or_source": "Permian Basin / Delaware",
            "Li_mg_L": 12,
            "TDS_mg_L": 71600,
            "Na_mg_L": None,
            "K_mg_L": None,
            "Mg_mg_L": None,
            "Ca_mg_L": None,
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "B_mg_L": None,
            "Br_mg_L": None,
            "REE_status": "trace critical minerals possible; not a strong Li case",
            "source_id": "Permian_valorization_2026",
            "source_status": "peer-reviewed article; public abstract/snippet values",
            "notes": "High water volume and treatment relevance; lower Li grade than Smackover/Marcellus.",
        },
        {
            "group": "produced water",
            "candidate": "Permian Midland typical",
            "region_or_source": "Permian Basin / Midland",
            "Li_mg_L": 20,
            "TDS_mg_L": 122000,
            "Na_mg_L": None,
            "K_mg_L": None,
            "Mg_mg_L": None,
            "Ca_mg_L": None,
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "B_mg_L": None,
            "Br_mg_L": None,
            "REE_status": "trace critical minerals possible; not a strong Li case",
            "source_id": "Permian_valorization_2026",
            "source_status": "peer-reviewed article; public abstract/snippet values",
            "notes": "Midland Li range is above Delaware but still low for DES/TOPO flagship screening.",
        },
        {
            "group": "geothermal brine",
            "candidate": "Salton Sea wellhead synthetic A",
            "region_or_source": "Imperial Valley geothermal",
            "Li_mg_L": salton_a["Li_mg_L"],
            "TDS_mg_L": 300000,
            "Na_mg_L": salton_a["Na_mg_L"],
            "K_mg_L": salton_a["K_mg_L"],
            "Mg_mg_L": salton_a["Mg_mg_L"],
            "Ca_mg_L": salton_a["Ca_mg_L"],
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "B_mg_L": None,
            "Br_mg_L": None,
            "REE_status": "critical metals possible; REE not central in cited test",
            "source_id": "Salton_Nature_2025",
            "source_status": "peer-reviewed synthetic brine converted from mM",
            "notes": "High Li and very high Ca/K/Na; geothermal, not produced water.",
        },
        {
            "group": "geothermal brine",
            "candidate": "Salton Sea Simbol synthetic B",
            "region_or_source": "Imperial Valley geothermal",
            "Li_mg_L": salton_b["Li_mg_L"],
            "TDS_mg_L": 300000,
            "Na_mg_L": salton_b["Na_mg_L"],
            "K_mg_L": salton_b["K_mg_L"],
            "Mg_mg_L": None,
            "Ca_mg_L": salton_b["Ca_mg_L"],
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "B_mg_L": None,
            "Br_mg_L": None,
            "REE_status": "critical metals possible; Fe/Mn are explicit competitors",
            "source_id": "Salton_Nature_2025",
            "source_status": "peer-reviewed synthetic brine converted from mM",
            "notes": "High Li and extreme Ca/Na plus Fe/Mn in original test; not the produced-water focus.",
        },
        {
            "group": "salar brine",
            "candidate": "Salar de Atacama core",
            "region_or_source": "Chile salar",
            "Li_mg_L": 1500,
            "TDS_mg_L": 250000,
            "Na_mg_L": None,
            "K_mg_L": None,
            "Mg_mg_L": None,
            "Ca_mg_L": None,
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "B_mg_L": 850,
            "Br_mg_L": None,
            "REE_status": "not treated as REE brine; Li/B/K resource context",
            "source_id": "USGS_Lithium_brines_2015",
            "source_status": "USGS/global literature screening value",
            "notes": "Benchmark high-grade salar; useful comparator, not produced water.",
        },
        {
            "group": "salar brine",
            "candidate": "Salar de Uyuni typical",
            "region_or_source": "Bolivia salar",
            "Li_mg_L": 550,
            "TDS_mg_L": 250000,
            "Na_mg_L": None,
            "K_mg_L": None,
            "Mg_mg_L": None,
            "Ca_mg_L": None,
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "B_mg_L": None,
            "Br_mg_L": None,
            "REE_status": "not treated as REE brine",
            "source_id": "USGS_Lithium_brines_2015",
            "source_status": "literature screening range midpoint",
            "notes": "High Li but generally more Mg/process difficulty than Atacama.",
        },
        {
            "group": "seawater",
            "candidate": "Open ocean seawater",
            "region_or_source": "global seawater",
            "Li_mg_L": 0.17,
            "TDS_mg_L": 35000,
            "Na_mg_L": 10770,
            "K_mg_L": 399,
            "Mg_mg_L": 1290,
            "Ca_mg_L": 412,
            "Sr_mg_L": 8,
            "Ba_mg_L": 0.03,
            "B_mg_L": 4.5,
            "Br_mg_L": 65,
            "REE_status": "REE ultra-trace; not a practical DES/TOPO target",
            "source_id": "USGS_Lithium_brines_2015",
            "source_status": "screening reference",
            "notes": "Useful lower-bound comparator; Li is too dilute for this case-study solvent train.",
        },
        {
            "group": "model brine",
            "candidate": "Rezaee Iran-source synthetic",
            "region_or_source": "southern Iran source-model brine",
            "Li_mg_L": 40.2,
            "TDS_mg_L": 276000,
            "Na_mg_L": 47705.2,
            "K_mg_L": 2610.1,
            "Mg_mg_L": 2811.6,
            "Ca_mg_L": 755.4,
            "Sr_mg_L": 63.17,
            "Ba_mg_L": None,
            "B_mg_L": 58.32,
            "Br_mg_L": None,
            "REE_status": "not reported",
            "source_id": "Rezaee_2025_RSM",
            "source_status": "peer-reviewed model-brine experiment",
            "notes": "Direct solvent benchmark: 90 wt pct DES plus 10 wt pct TOPO gave 51.63 pct Li extraction from the synthetic brine.",
        },
    ]


def _num(value: Any) -> float | None:
    if value is None:
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(value):
        return None
    return value


def add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["Na_mg_L", "K_mg_L", "Mg_mg_L", "Ca_mg_L", "Sr_mg_L", "Ba_mg_L"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Li_mg_L"] = pd.to_numeric(df["Li_mg_L"], errors="coerce")
    df["TDS_mg_L"] = pd.to_numeric(df["TDS_mg_L"], errors="coerce")
    df["Na_Li_mass_ratio"] = df["Na_mg_L"] / df["Li_mg_L"]
    df["Mg_Li_mass_ratio"] = df["Mg_mg_L"] / df["Li_mg_L"]
    df["Ca_Li_mass_ratio"] = df["Ca_mg_L"] / df["Li_mg_L"]
    df["Divalent_Li_mass_ratio"] = (df["Mg_mg_L"].fillna(0) + df["Ca_mg_L"].fillna(0) + df["Sr_mg_L"].fillna(0) + df["Ba_mg_L"].fillna(0)) / df["Li_mg_L"]
    return df


def score_candidates(df: pd.DataFrame) -> pd.DataFrame:
    produced = df[df["group"].eq("produced water")].copy()
    rows: list[dict[str, Any]] = []
    for _, row in produced.iterrows():
        li = _num(row["Li_mg_L"]) or 0.0
        tds = _num(row["TDS_mg_L"]) or 0.0
        na_li = _num(row["Na_Li_mass_ratio"])
        div_li = _num(row["Divalent_Li_mass_ratio"])
        data_score = 18 if row["source_status"].startswith("source-backed") else 14
        li_score = min(30.0, 30.0 * li / 200.0)
        tds_score = 15.0 if 100000 <= tds <= 350000 else 8.0
        na_score = 15.0 if na_li is not None and na_li <= 1200 else 10.0 if na_li is not None else 8.0
        div_score = 15.0 if div_li is not None and div_li <= 80 else 9.0 if div_li is not None and div_li <= 300 else 5.0
        ree_penalty = 0.0 if "not reported" not in row["REE_status"] else -2.0
        score = li_score + tds_score + na_score + div_score + data_score + ree_penalty
        rows.append(
            {
                "rank_basis": row["candidate"],
                "region_or_source": row["region_or_source"],
                "Li_mg_L": li,
                "TDS_mg_L": tds,
                "Na_Li_mass_ratio": na_li,
                "Divalent_Li_mass_ratio": div_li,
                "source_status": row["source_status"],
                "score_100": round(score, 1),
                "candidate_class": (
                    "primary candidate"
                    if score >= 75
                    else "secondary candidate"
                    if score >= 60
                    else "screening only"
                ),
                "why": row["notes"],
            }
        )
    return pd.DataFrame(rows).sort_values(["score_100", "Li_mg_L"], ascending=False)


def write_csv(path: Path, rows: list[dict[str, Any]] | pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(rows, pd.DataFrame):
        rows.to_csv(path, index=False)
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_scatter(df: pd.DataFrame) -> None:
    colors = {
        "produced water": "#1f77b4",
        "geothermal brine": "#d62728",
        "salar brine": "#2ca02c",
        "seawater": "#17becf",
        "model brine": "#9467bd",
    }
    label_offsets = {
        "Smackover AR MS-2 base": (-8, -10, "right"),
        "Smackover AR high observed": (-8, 10, "right"),
        "Marcellus NE PA median": (6, 6, "left"),
        "Rezaee Iran-source synthetic": (8, 6, "left"),
        "Salton Sea Simbol synthetic B": (-8, 16, "right"),
        "Salar de Atacama core": (6, 6, "left"),
        "Open ocean seawater": (6, 6, "left"),
    }
    fig, ax = plt.subplots(figsize=(10.4, 6.1))
    for group, sub in df.groupby("group"):
        ax.scatter(
            sub["TDS_mg_L"],
            sub["Li_mg_L"],
            s=90,
            color=colors.get(group, "#777777"),
            label=group,
            alpha=0.85,
            edgecolor="white",
            linewidth=0.7,
        )
        for _, row in sub.iterrows():
            if row["candidate"] in label_offsets:
                x_offset, y_offset, horizontal_align = label_offsets[row["candidate"]]
                ax.annotate(
                    row["candidate"].replace(" synthetic", ""),
                    (row["TDS_mg_L"], row["Li_mg_L"]),
                    xytext=(x_offset, y_offset),
                    textcoords="offset points",
                    fontsize=8,
                    ha=horizontal_align,
                    bbox={"boxstyle": "round,pad=0.12", "fc": "white", "ec": "none", "alpha": 0.65},
                )
    ax.axhspan(40, 260, color="#ffe8a3", alpha=0.2, label="Rezaee-tested / produced-water target band")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("TDS (mg/L, log scale)")
    ax.set_ylabel("Lithium (mg/L, log scale)")
    ax.set_title("Lithium grade versus salinity across common brine classes")
    ax.set_xlim(2.0e4, 5.2e5)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    for suffix in ["png", "svg"]:
        fig.savefig(FIG_DIR / f"brine_li_tds_scatter.{suffix}", dpi=220)
    plt.close(fig)


def plot_interference(scores: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9.4, 5.6))
    top = scores.sort_values("score_100", ascending=True)
    labels = [x.replace("Smackover AR ", "Smackover ") for x in top["rank_basis"]]
    ax.barh(labels, top["score_100"], color="#2f6f8f")
    ax.set_xlim(0, 100)
    ax.set_xlabel("DES/TOPO screening score (0-100)")
    ax.set_title("Produced-water candidates for Rezaee 90 wt% DES + 10 wt% TOPO")
    for i, value in enumerate(top["score_100"]):
        ax.text(value + 1, i, f"{value:.1f}", va="center", fontsize=8)
    fig.tight_layout()
    for suffix in ["png", "svg"]:
        fig.savefig(FIG_DIR / f"produced_water_candidate_scores.{suffix}", dpi=220)
    plt.close(fig)


def report_text(df: pd.DataFrame, scores: pd.DataFrame) -> str:
    top_rows = scores.head(5)
    lines = [
        "# Brine Composition Screening For Rezaee DES/TOPO Lithium Extraction",
        "",
        "Date: 2026-05-08",
        "",
        "## Executive Finding",
        "",
        "Produced water is the most relevant brine family for the current case study because it combines high lithium in several basins with existing water-handling infrastructure and a severe sodium/divalent-ion background. For the Rezaee solvent system, the selected workflow assumes upstream pretreatment removes divalent cations first, so the extraction model starts from a clean Li+Na stream. The best near-term candidates are produced waters that have lithium in the same order of magnitude as the Rezaee model brine, high enough salinity to justify a thermodynamic model, and manageable divalent pretreatment risk.",
        "",
        "The top produced-water candidates from this screening are:",
        "",
    ]
    for _, row in top_rows.iterrows():
        lines.append(
            f"- **{row['rank_basis']}**: score `{row['score_100']}/100`, Li `{row['Li_mg_L']:.1f} mg/L`, "
            f"TDS `{row['TDS_mg_L']:.0f} mg/L`, class `{row['candidate_class']}`."
        )
    lines += [
        "",
        "## Why Rezaee 90 wt% DES + 10 wt% TOPO Is The Screening Lens",
        "",
        "Rezaee's optimized condition uses TBAC(1):decanoic-acid(2) hydrophobic DES with 10 wt% TOPO at 23 C and pH 10.4. The reported one-stage optimum is 48.57% lithium extraction with Li/Na selectivity of 4.41. Their multi-cation model brine contains Li, Na, K, Mg, and Ca, and the reported extraction efficiencies are 51.63% for Li, 9.97% for Na, 3.11% for K, 4.38% for Mg, and 2.29% for Ca.",
        "",
        "That means the solvent is not a magic lithium-only separator. It is a Li-over-Na and Li-over-alkaline-earth candidate that still needs pretreatment and process modeling when Ca, Mg, Sr, or Ba are extreme.",
        "",
        "## Composition Landscape",
        "",
        "![Lithium grade versus salinity](figures/brine_li_tds_scatter.png)",
        "",
        "Produced waters occupy the practical middle of the chart: lower lithium than elite salars, but much higher lithium than seawater and often embedded in existing handling infrastructure. Smackover and Marcellus are the most relevant produced-water clusters for this DES/TOPO case because they sit near or above 100 mg/L Li. Bakken can reach attractive Li in some high-Li counties but is extremely saline and sodium-rich. Permian produced water is important for volume and operations, but the public screening ranges are lower in Li.",
        "",
        "## Produced-Water Candidate Ranking",
        "",
        "![Produced-water candidate scores](figures/produced_water_candidate_scores.png)",
        "",
        "| Rank | Candidate | Li mg/L | TDS mg/L | Na/Li | Divalent/Li | Score | Interpretation |",
        "|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for idx, (_, row) in enumerate(scores.iterrows(), start=1):
        na = "" if pd.isna(row["Na_Li_mass_ratio"]) else f"{row['Na_Li_mass_ratio']:.1f}"
        div = "" if pd.isna(row["Divalent_Li_mass_ratio"]) else f"{row['Divalent_Li_mass_ratio']:.1f}"
        lines.append(
            f"| {idx} | {row['rank_basis']} | {row['Li_mg_L']:.1f} | {row['TDS_mg_L']:.0f} | {na} | {div} | {row['score_100']:.1f} | {row['candidate_class']} |"
        )
    lines += [
        "",
        "## Engineering Interpretation",
        "",
        "1. **Smackover is the best produced-water presentation basis.** It has high lithium, high TDS, bromine/brine infrastructure context, and source-backed major-ion rows. The main issue is Ca/Sr pretreatment, not lithium grade.",
        "2. **Marcellus NE is chemically attractive.** It has high lithium and comparatively low Mg/Li among Marcellus regions. Missing sodium/calcium detail in the screening table should be filled before process simulation.",
        "3. **Marcellus SW is operationally attractive but chemically harder.** It has lower lithium and higher Mg/Li than NE PA, but higher produced-water volumes per well in the cited study.",
        "4. **Bakken is a high-salinity stress test.** It has high Na, Sr, K, Rb, and TDS; it is useful for critical-mineral recovery framing, but likely needs stronger pretreatment before DES extraction.",
        "5. **Permian is a process-volume candidate, not the best Li-grade candidate.** It should remain in the comparison set because produced-water volumes are large, but Li grades are lower.",
        "",
        "## Critical Minerals And REE Caveat",
        "",
        "Lithium is a critical mineral, but it is not a rare earth element. Produced-water literature often discusses Li and REE together because both can occur in unconventional aqueous resources. For this case study, REE should be treated as a screening and future-data issue unless a specific brine source reports REE concentrations. The current clean Smackover source table reports several trace metals with censoring, but REE are not reported.",
        "",
        "## Study Workflow",
        "",
        "```mermaid",
        "flowchart LR",
        '  A["Brine composition sources"] --> B["Normalize Li, TDS, Na, K, Mg, Ca, Sr, Ba"]',
        '  B --> C["Compute Na/Li and divalent/Li interference ratios"]',
        '  C --> D["Screen produced-water candidates"]',
        '  D --> E["Rezaee DES/TOPO extraction basis"]',
        '  E --> F["Surrogate and PrOMMiS/IDAES handoff"]',
        '  C --> G["REE and critical-mineral caveats"]',
        "```",
        "",
        "## Recommended Next Data Pulls",
        "",
        "- Add sodium, calcium, strontium, and barium distributions for Marcellus NE/SW from the underlying data release.",
        "- Pull basin-scale rows from the USGS Produced Waters Database for Smackover, Marcellus, Bakken, and Permian using the same censoring and charge-balance rules.",
        "- Add REE only where the source reports measured REE values; do not infer REE from generic critical-mineral language.",
        "- For the DES/TOPO model, prioritize candidates with Li above 100 mg/L, Na/Li within the Rezaee-tested or Rezaee-real-brine extrapolation envelope, and divalent pretreatment that can be explicitly costed.",
        "",
        "## Source Log",
        "",
        "| Source | Status | Use |",
        "|---|---|---|",
    ]
    for source in SOURCE_LOG:
        lines.append(
            f"| [{source['source_id']}]({source['url']}) | {source['status']} | {source['use']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    REF_DIR.mkdir(parents=True, exist_ok=True)

    df = add_metrics(pd.DataFrame(brine_rows()))
    scores = score_candidates(df)

    write_csv(BRINE_TABLE, df)
    write_csv(SCORES, scores)
    write_csv(SOURCES, SOURCE_LOG)
    plot_scatter(df)
    plot_interference(scores)
    REPORT.write_text(report_text(df, scores), encoding="utf-8")

    shutil.copyfile(REPORT, LEGACY_REPORT)
    shutil.copyfile(BRINE_TABLE, LEGACY_TABLE)
    shutil.copyfile(SCORES, LEGACY_SCORES)

    print(f"Wrote {BRINE_TABLE}")
    print(f"Wrote {SCORES}")
    print(f"Wrote {SOURCES}")
    print(f"Wrote {REPORT}")
    print(f"Wrote {FIG_DIR / 'brine_li_tds_scatter.png'}")
    print(f"Wrote {FIG_DIR / 'produced_water_candidate_scores.png'}")
    print({"rows": len(df), "produced_water_candidates": len(scores)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
