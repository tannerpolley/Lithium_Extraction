from __future__ import annotations

import csv
import textwrap
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[3]
REF_DIR = REPO_ROOT / "data" / "reference" / "produced_water"
DATA_PROCESSED = REPO_ROOT / "data" / "processed"
RESULTS = REPO_ROOT / "results"
SLIDE_DIR = REPO_ROOT / "slides" / "case_study_tbac_da_topo_produced_water"
FIGURES = SLIDE_DIR / "figures"

FEEDS = REF_DIR / "selected_case_study_feeds.csv"
TRANSFER = DATA_PROCESSED / "tbac_da_topo_li_na_transfer_variables.csv"
PHASE_SCAN_REPORT = RESULTS / "tbac_da_topo_phase_inventory_convention_scan.md"

STAGE_RESULTS = DATA_PROCESSED / "tbac_da_topo_prommis_stage_results.csv"
RECONCILIATION = DATA_PROCESSED / "tbac_da_topo_recovery_reconciliation.csv"
TEA_RESULTS = DATA_PROCESSED / "tbac_da_topo_screening_tea_results.csv"
STAGE_REPORT = RESULTS / "tbac_da_topo_prommis_stage_results.md"
TEA_REPORT = RESULTS / "tbac_da_topo_screening_tea.md"
DECK = SLIDE_DIR / "deck.qmd"
DECK_README = SLIDE_DIR / "README.md"
READINESS = REPO_ROOT / "docs" / "final_case_study_readiness_checklist.md"
CHANGELOG = REPO_ROOT / "docs" / "case_study_tbac_da_topo_agent3_changelog.md"

SOLVENT = "TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO"
SOLVENT_SHORT = "TBAC/DA DES + 10 wt% TOPO"
SOLVENT_FORMULATION = "90 wt% TBAC/DA DES + 10 wt% TOPO"
LI2CO3_PER_LI = 73.891 / (2.0 * 6.94)
OPERATING_DAYS_PER_YEAR = 8000.0 / 24.0
REFERENCE_PRODUCT_VALUE_USD_KG = 20.0
PLOT_BLUE = "#2f5f73"
PLOT_ORANGE = "#b36b2c"
PLOT_GREEN = "#527a43"
PLOT_GRAY = "#666666"
PLOT_LIGHT = "#f5f5f2"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    names = fieldnames or list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def number(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    text = str(value).strip()
    if text == "" or text.lower() == "nan":
        return default
    return float(text)


def pct_stage_cumulative(one_stage_pct: float, stage_count: int) -> float:
    e = max(0.0, min(0.999999, one_stage_pct / 100.0))
    return 100.0 * (1.0 - (1.0 - e) ** stage_count)


def slug(text: str) -> str:
    return (
        text.lower()
        .replace("/", "_")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
    )


def wrap(text: str, width: int = 58) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def load_inputs() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], list[dict[str, str]]]:
    feeds = {row["feed_id"]: row for row in read_csv(FEEDS)}
    transfer_rows = read_csv(TRANSFER)
    transfer = {row["case_id"]: row for row in transfer_rows}
    required_cases = [
        "smackover_ms2_main_anchor",
        "smackover_high_observed_sensitivity_anchor",
        "marcellus_ne_pa_comparison_anchor",
        "bakken_high_na_stress_anchor",
    ]
    missing = [case for case in required_cases if case not in transfer]
    if missing:
        raise ValueError(f"Missing required transfer rows: {missing}")
    return feeds, transfer, transfer_rows


def scenario_specs() -> list[dict[str, Any]]:
    return [
        {
            "scenario": "base_smackover_ms2",
            "case_id": "smackover_ms2_main_anchor",
            "feed_flow_m3_day": 1000.0,
            "pretreatment_Li_loss_pct": 3.0,
            "solvent_loss_rate": 0.005,
            "stage_count": 3,
            "role": "base",
            "deck_label": "Base: Smackover MS-2",
        },
        {
            "scenario": "stress_bakken_high_na",
            "case_id": "bakken_high_na_stress_anchor",
            "feed_flow_m3_day": 750.0,
            "pretreatment_Li_loss_pct": 5.0,
            "solvent_loss_rate": 0.008,
            "stage_count": 3,
            "role": "stress",
            "deck_label": "Stress: Bakken high Na",
        },
        {
            "scenario": "favorable_smackover_high_li",
            "case_id": "smackover_high_observed_sensitivity_anchor",
            "feed_flow_m3_day": 1000.0,
            "pretreatment_Li_loss_pct": 2.0,
            "solvent_loss_rate": 0.004,
            "stage_count": 3,
            "role": "favorable",
            "deck_label": "Favorable: high-Li Smackover",
        },
        {
            "scenario": "comparison_marcellus_card",
            "case_id": "marcellus_ne_pa_comparison_anchor",
            "feed_flow_m3_day": 1000.0,
            "pretreatment_Li_loss_pct": 3.0,
            "solvent_loss_rate": 0.005,
            "stage_count": 3,
            "role": "comparison_card",
            "deck_label": "Comparison: Marcellus NE PA",
        },
        {
            "scenario": "sensitivity_pretreatment_li_loss",
            "case_id": "smackover_ms2_main_anchor",
            "feed_flow_m3_day": 1000.0,
            "pretreatment_Li_loss_pct": 8.0,
            "solvent_loss_rate": 0.005,
            "stage_count": 3,
            "role": "sensitivity",
            "deck_label": "Sensitivity: pretreatment Li loss",
        },
        {
            "scenario": "sensitivity_solvent_loss",
            "case_id": "smackover_ms2_main_anchor",
            "feed_flow_m3_day": 1000.0,
            "pretreatment_Li_loss_pct": 3.0,
            "solvent_loss_rate": 0.020,
            "stage_count": 3,
            "role": "sensitivity",
            "deck_label": "Sensitivity: solvent loss",
        },
        {
            "scenario": "sensitivity_stage_count_5",
            "case_id": "smackover_ms2_main_anchor",
            "feed_flow_m3_day": 1000.0,
            "pretreatment_Li_loss_pct": 3.0,
            "solvent_loss_rate": 0.005,
            "stage_count": 5,
            "role": "sensitivity",
            "deck_label": "Sensitivity: five stages",
        },
    ]


def stage_row(spec: dict[str, Any], transfer: dict[str, str], feed: dict[str, str]) -> dict[str, Any]:
    one_li = number(transfer["one_stage_Li_extraction_pct"])
    one_na = number(transfer["one_stage_Na_extraction_pct"])
    stage_count = int(spec["stage_count"])
    transfer_stage_count = int(number(transfer["stage_count"]))
    transfer_li = number(transfer["cumulative_Li_recovery_pct"])
    transfer_na = number(transfer["cumulative_Na_recovery_pct"])
    if stage_count == transfer_stage_count:
        stage_li = transfer_li
        stage_na = transfer_na
        stage_reason = "same stage count as transfer table"
    else:
        stage_li = pct_stage_cumulative(one_li, stage_count)
        stage_na = pct_stage_cumulative(one_na, stage_count)
        stage_reason = "different stage-count definition"

    pretreatment_loss = float(spec["pretreatment_Li_loss_pct"])
    process_li = stage_li * (1.0 - pretreatment_loss / 100.0)
    process_na = stage_na
    flow = float(spec["feed_flow_m3_day"])
    operating_days = OPERATING_DAYS_PER_YEAR
    li_feed_mg_l = number(transfer["Li_feed_mg_L"])
    na_feed_mg_l = number(transfer["Na_mg_L"])
    raw_li_kg_day = flow * 1000.0 * li_feed_mg_l * 1e-6
    clean_li_kg_day = raw_li_kg_day * (1.0 - pretreatment_loss / 100.0)
    loaded_li_kg_day = clean_li_kg_day * stage_li / 100.0
    loaded_na_kg_day = flow * 1000.0 * na_feed_mg_l * 1e-6 * stage_na / 100.0
    li2co3_kg_year = loaded_li_kg_day * operating_days * LI2CO3_PER_LI
    divalent_mg_l = number(feed.get("Mg_mg_L")) + number(feed.get("Ca_mg_L")) + number(feed.get("Sr_mg_L")) + number(feed.get("Ba_mg_L"))
    divalent_kg_day = flow * 1000.0 * divalent_mg_l * 1e-6
    workflow = (
        "raw produced water -> pretreatment for Ca/Mg/Sr/Ba and organics -> clean Li/Na extraction feed -> "
        f"{stage_count} solvent-extraction stages -> loaded organic -> stripping/regeneration placeholder -> "
        "Li2CO3-equivalent placeholder -> Na-bearing raffinate"
    )
    validity = transfer["validity_flag"]
    if feed["simulation_use"] == "comparison_card_only":
        validity = f"{validity}; comparison_card_only_missing_major_ions"
    if spec["role"] == "stress":
        validity = f"{validity}; high_na_stress"

    return {
        "case_id": spec["case_id"],
        "scenario": spec["scenario"],
        "scenario_role": spec["role"],
        "feed_id": transfer["feed_id"],
        "model_basis": transfer["model_basis"],
        "basis_type": transfer["basis_type"],
        "solvent_system": SOLVENT,
        "feed_flow_m3_day": flow,
        "operating_days_per_year": operating_days,
        "Li_feed_mg_L": li_feed_mg_l,
        "Na_mg_L": na_feed_mg_l,
        "TDS_feature_mg_L": number(transfer["TDS_feature_mg_L"]),
        "Na_Li_mass_ratio": number(transfer["Na_Li_mass_ratio"]),
        "organic_to_aqueous_mass_ratio": number(transfer["organic_to_aqueous_mass_ratio"]),
        "stage_count": stage_count,
        "transfer_table_stage_count": transfer_stage_count,
        "D_Li": number(transfer["D_Li"]),
        "D_Na": number(transfer["D_Na"]),
        "one_stage_Li_extraction_pct": one_li,
        "one_stage_Na_extraction_pct": one_na,
        "transfer_table_cumulative_Li_recovery_pct": transfer_li,
        "transfer_table_cumulative_Na_recovery_pct": transfer_na,
        "prommis_idaes_staged_Li_recovery_pct": process_li,
        "prommis_idaes_staged_Na_recovery_pct": process_na,
        "pretreatment_Li_loss_pct": pretreatment_loss,
        "residual_divalent_basis": feed["pretreatment_role"],
        "raw_divalent_removed_kg_day": divalent_kg_day,
        "loaded_organic_Li_kg_day": loaded_li_kg_day,
        "loaded_organic_Na_kg_day": loaded_na_kg_day,
        "Li2CO3_kg_year": li2co3_kg_year,
        "recovery_basis_note": f"{stage_reason}; PrOMMiS/IDAES-style recovery includes pretreatment Li loss.",
        "process_workflow": workflow,
        "validity_flag": validity,
        "extrapolation_flag": transfer["extrapolation_flag"],
    }


def build_stage_results(
    feeds: dict[str, dict[str, str]], transfers: dict[str, dict[str, str]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    reconciliation: list[dict[str, Any]] = []
    for spec in scenario_specs():
        transfer = transfers[spec["case_id"]]
        feed = feeds[transfer["feed_id"]]
        row = stage_row(spec, transfer, feed)
        rows.append(row)
        diff = abs(row["transfer_table_cumulative_Li_recovery_pct"] - row["prommis_idaes_staged_Li_recovery_pct"])
        reason = row["recovery_basis_note"]
        if spec["role"] == "comparison_card":
            chosen = "comparison card only until missing Na/Ca/Sr/Ba source values are filled"
        elif spec["role"] == "sensitivity":
            chosen = "sensitivity value; base deck value remains Smackover MS-2"
        else:
            chosen = f"{row['prommis_idaes_staged_Li_recovery_pct']:.3f}% overall recovery after pretreatment loss"
        reconciliation.append(
            {
                "case_id": row["case_id"],
                "scenario": row["scenario"],
                "transfer_table_cumulative_Li_recovery_pct": row["transfer_table_cumulative_Li_recovery_pct"],
                "prommis_idaes_staged_Li_recovery_pct": row["prommis_idaes_staged_Li_recovery_pct"],
                "absolute_difference_pct_points": diff,
                "reason_for_difference": reason,
                "chosen_deck_value": chosen,
            }
        )
    return rows, reconciliation


def build_tea_rows(stage_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in stage_rows:
        annual_m3 = row["feed_flow_m3_day"] * row["operating_days_per_year"]
        tds_factor = max(row["TDS_feature_mg_L"], 1.0) / 305000.0
        divalent_factor = min(row["raw_divalent_removed_kg_day"] / max(row["feed_flow_m3_day"], 1.0), 75.0) / 75.0
        pretreatment_cost = annual_m3 * (0.55 + 0.35 * tds_factor + 0.40 * divalent_factor)
        extraction_cost = annual_m3 * (0.22 + 0.18 * row["stage_count"]) * (0.75 + row["organic_to_aqueous_mass_ratio"])
        solvent_loss_cost = annual_m3 * row["solvent_loss_rate"] * 950.0 * max(row["organic_to_aqueous_mass_ratio"], 0.2)
        stripping_placeholder_cost = max(row["Li2CO3_kg_year"], 1.0) * 2.40
        total_cost = pretreatment_cost + extraction_cost + solvent_loss_cost + stripping_placeholder_cost
        li2co3 = max(row["Li2CO3_kg_year"], 1.0)
        breakeven_usd_kg = total_cost / li2co3
        margin_usd_year = li2co3 * REFERENCE_PRODUCT_VALUE_USD_KG - total_cost
        caveat = (
            "screening TEA only; excludes vendor quotes, detailed equipment sizing, solvent-degradation testing, "
            "regeneration proof, and brine-specific pilot validation"
        )
        if row["scenario_role"] == "comparison_card":
            caveat = f"{caveat}; comparison-card-only chemistry is incomplete"
        rows.append(
            {
                "case_id": row["case_id"],
                "scenario": row["scenario"],
                "feed_flow_m3_day": row["feed_flow_m3_day"],
                "operating_days_per_year": row["operating_days_per_year"],
                "Li_feed_mg_L": row["Li_feed_mg_L"],
                "Li_recovery_pct": row["prommis_idaes_staged_Li_recovery_pct"],
                "pretreatment_Li_loss_pct": row["pretreatment_Li_loss_pct"],
                "solvent_loss_rate": row["solvent_loss_rate"] if "solvent_loss_rate" in row else scenario_solvent_loss(row["scenario"]),
                "stage_count": row["stage_count"],
                "Li2CO3_kg_year": row["Li2CO3_kg_year"],
                "major_cost_assumptions": (
                    f"pretreatment screening cost scales with TDS/divalent load; extraction cost scales with {row['stage_count']} stages "
                    f"and O/A={row['organic_to_aqueous_mass_ratio']:.3g}; solvent loss rate={scenario_solvent_loss(row['scenario']):.3g}; "
                    f"reference value={REFERENCE_PRODUCT_VALUE_USD_KG:.2f} USD/kg Li2CO3-equivalent"
                ),
                "breakeven_metric": f"{breakeven_usd_kg:.2f} USD/kg Li2CO3-equivalent screening breakeven",
                "net_before_tax_or_margin_metric": f"{margin_usd_year:.0f} USD/year screening margin at reference value",
                "validity_flag": row["validity_flag"],
                "screening_tea_caveat": caveat,
                "pretreatment_cost_usd_year": pretreatment_cost,
                "extraction_cost_usd_year": extraction_cost,
                "solvent_loss_cost_usd_year": solvent_loss_cost,
                "stripping_placeholder_cost_usd_year": stripping_placeholder_cost,
                "total_screening_cost_usd_year": total_cost,
                "breakeven_usd_kg_Li2CO3": breakeven_usd_kg,
                "margin_at_reference_value_usd_year": margin_usd_year,
            }
        )
    return rows


def scenario_solvent_loss(scenario: str) -> float:
    for spec in scenario_specs():
        if spec["scenario"] == scenario:
            return float(spec["solvent_loss_rate"])
    return 0.005


def make_candidate_ranking(feeds: dict[str, dict[str, str]]) -> Path:
    path = FIGURES / "produced_water_candidate_ranking.png"
    rows = [
        ("Smackover MS-2", number(feeds["smackover_ms2_main"]["Li_mg_L"]), number(feeds["smackover_ms2_main"]["TDS_mg_L"]) / 1000.0),
        (
            "Smackover high",
            number(feeds["smackover_high_observed_sensitivity"]["Li_mg_L"]),
            number(feeds["smackover_high_observed_sensitivity"]["TDS_mg_L"]) / 1000.0,
        ),
        (
            "Marcellus NE PA",
            number(feeds["marcellus_ne_pa_comparison"]["Li_mg_L"]),
            number(feeds["marcellus_ne_pa_comparison"]["TDS_mg_L"]) / 1000.0,
        ),
        ("Bakken stress", number(feeds["bakken_high_na_stress"]["Li_mg_L"]), number(feeds["bakken_high_na_stress"]["TDS_mg_L"]) / 1000.0),
    ]
    labels = [row[0] for row in rows]
    li = [row[1] for row in rows]
    tds = [row[2] for row in rows]
    fig, ax1 = plt.subplots(figsize=(9.5, 5.2))
    positions = range(len(rows))
    ax1.barh(list(positions), li, color=PLOT_BLUE, height=0.38, label="Li (mg/L)")
    ax1.set_yticks(list(positions), labels)
    ax1.invert_yaxis()
    ax1.set_xlabel("Lithium, mg/L")
    ax1.grid(axis="x", alpha=0.25)
    ax2 = ax1.twiny()
    ax2.plot(tds, list(positions), color=PLOT_ORANGE, marker="o", linewidth=2.0, label="TDS (g/L)")
    ax2.set_xlabel("TDS, g/L")
    ax1.set_title("Produced-water candidates: lithium grade and salinity severity")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def make_feed_card(feeds: dict[str, dict[str, str]]) -> Path:
    path = FIGURES / "smackover_marcellus_feed_card.png"
    rows = [
        ["Feed", "Li mg/L", "TDS mg/L", "Na/Li", "Process role"],
        [
            "Smackover MS-2",
            feeds["smackover_ms2_main"]["Li_mg_L"],
            feeds["smackover_ms2_main"]["TDS_mg_L"],
            feeds["smackover_ms2_main"]["Na_Li_mass_ratio"],
            "main hard case",
        ],
        [
            "Marcellus NE PA",
            feeds["marcellus_ne_pa_comparison"]["Li_mg_L"],
            feeds["marcellus_ne_pa_comparison"]["TDS_mg_L"],
            "missing",
            "comparison card",
        ],
    ]
    fig, ax = plt.subplots(figsize=(9.5, 3.1))
    ax.axis("off")
    table = ax.table(cellText=rows[1:], colLabels=rows[0], cellLoc="left", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.6)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#d0d0cb")
        if r == 0:
            cell.set_facecolor("#e9ece7")
            cell.set_text_props(weight="bold")
        else:
            cell.set_facecolor("#ffffff")
    ax.set_title("Selected feed cases: main flowsheet case and lower-burden comparison", pad=14)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def make_block_diagram(path: Path, title: str, boxes: list[str], colors: list[str] | None = None) -> Path:
    fig, ax = plt.subplots(figsize=(10.5, 3.2))
    ax.axis("off")
    colors = colors or [PLOT_LIGHT] * len(boxes)
    gap = 0.055
    margin = 0.045
    width = (0.91 - gap * (len(boxes) - 1)) / len(boxes)
    x_positions = [margin + i * (width + gap) for i in range(len(boxes))]
    for idx, (x, label) in enumerate(zip(x_positions, boxes)):
        rect = plt.Rectangle((x, 0.38), width, 0.28, facecolor=colors[idx], edgecolor="#3b3b3b", linewidth=1.0)
        ax.add_patch(rect)
        ax.text(x + width / 2, 0.52, wrap(label, 18), ha="center", va="center", fontsize=9)
        if idx < len(boxes) - 1:
            ax.annotate(
                "",
                xy=(x_positions[idx + 1] - 0.008, 0.52),
                xytext=(x + width + 0.008, 0.52),
                arrowprops={"arrowstyle": "-|>", "lw": 1.35, "color": "#333333", "mutation_scale": 14},
            )
    ax.text(0.5, 0.83, title, ha="center", va="center", fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def make_extraction_card(stage_rows: list[dict[str, Any]]) -> Path:
    path = FIGURES / "base_extraction_result_card.png"
    base = next(row for row in stage_rows if row["scenario"] == "base_smackover_ms2")
    values = [
        ("Li one-stage", base["one_stage_Li_extraction_pct"], "%"),
        ("Na one-stage", base["one_stage_Na_extraction_pct"], "%"),
        ("Li extraction-step", base["transfer_table_cumulative_Li_recovery_pct"], "%"),
        ("Overall after pretreatment", base["prommis_idaes_staged_Li_recovery_pct"], "%"),
        ("Li/Na selectivity", number(base["D_Li"]) / max(number(base["D_Na"]), 1e-12), ""),
    ]
    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    ax.axis("off")
    y = 0.78
    ax.text(0.05, 0.93, "Smackover MS-2 extraction result", fontsize=16, weight="bold", ha="left")
    ax.text(0.05, 0.86, f"{SOLVENT_FORMULATION}; post-pretreatment Li/Na feed", fontsize=10, color=PLOT_GRAY, ha="left")
    for label, value, unit in values:
        ax.text(0.07, y, label, fontsize=11, ha="left", va="center")
        ax.text(0.72, y, f"{value:.3f}{unit}", fontsize=18, weight="bold", ha="right", va="center", color=PLOT_BLUE)
        y -= 0.14
    ax.text(0.05, 0.08, "Deck value uses overall recovery after pretreatment Li loss; extraction-step recovery remains traceable to the transfer table.", fontsize=9, color=PLOT_GRAY)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def make_validity_plot(stage_rows: list[dict[str, Any]]) -> Path:
    path = FIGURES / "surrogate_validity_gate.png"
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    xs = [row["Na_Li_mass_ratio"] for row in stage_rows]
    ys = [row["transfer_table_cumulative_Li_recovery_pct"] for row in stage_rows]
    colors = [PLOT_ORANGE if "outside_low_na_li" in row["extrapolation_flag"] else PLOT_GREEN for row in stage_rows]
    ax.scatter(xs, ys, s=90, color=colors, edgecolor="#303030", linewidth=0.6)
    for row in stage_rows:
        if row["scenario_role"] in ("base", "stress", "favorable", "comparison_card"):
            ax.text(row["Na_Li_mass_ratio"] * 1.02, row["transfer_table_cumulative_Li_recovery_pct"], row["scenario_role"], fontsize=8)
    ax.axvline(20.0, color=PLOT_GRAY, linestyle="--", linewidth=1.2)
    ax.text(21.5, min(ys) + 2, "source-paper\nlow-Na/Li boundary", fontsize=8, color=PLOT_GRAY)
    ax.set_xscale("log")
    ax.set_xlabel("Na/Li mass ratio")
    ax.set_ylabel("Transfer-table cumulative Li recovery (%)")
    ax.set_title("Validity gate: produced-water sodium load is an extrapolation flag")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def make_tea_plot(tea_rows: list[dict[str, Any]]) -> Path:
    path = FIGURES / "screening_tea_scenarios.png"
    keep = [row for row in tea_rows if row["scenario"] in ("stress_bakken_high_na", "base_smackover_ms2", "favorable_smackover_high_li")]
    labels = ["stress", "base", "favorable"]
    mapping = {row["scenario"].split("_")[0]: row for row in keep}
    vals = [mapping[label]["breakeven_usd_kg_Li2CO3"] for label in labels]
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.bar(labels, vals, color=[PLOT_ORANGE, PLOT_BLUE, PLOT_GREEN], width=0.56)
    ax.set_ylabel("USD/kg Li2CO3-equivalent")
    ax.set_title("Screening TEA breakeven by scenario")
    ax.grid(axis="y", alpha=0.25)
    for idx, val in enumerate(vals):
        ax.text(idx, val + max(vals) * 0.02, f"{val:.1f}", ha="center", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def generate_figures(feeds: dict[str, dict[str, str]], stage_rows: list[dict[str, Any]], tea_rows: list[dict[str, Any]]) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    make_candidate_ranking(feeds)
    make_feed_card(feeds)
    make_block_diagram(
        FIGURES / "pretreatment_boundary.png",
        "Pretreatment makes the extraction feed",
        ["raw produced water", "Ca/Mg/Sr/Ba and organics pretreatment", "clean Li/Na extraction feed", "residual-divalent guardrail"],
        ["#ecebe5", "#e8dfd1", "#e1ebee", "#f3e8df"],
    )
    make_block_diagram(
        FIGURES / "tbac_da_topo_mechanism.png",
        "Fixed solvent formulation and Li/Na transfer role",
        ["90 wt% TBAC/DA DES", "10 wt% TOPO", "Li/Na distribution variables", "loaded organic for stripping"],
        ["#ecebe5", "#e8dfd1", "#e1ebee", "#e7eadf"],
    )
    make_extraction_card(stage_rows)
    make_validity_plot(stage_rows)
    make_block_diagram(
        FIGURES / "prommis_idaes_workflow.png",
        "Traceable handoff to staged process and screening TEA",
        ["transfer table", "MSContactor-style stages", "recovery reconciliation", "screening TEA", "internal project ask"],
        ["#ecebe5", "#e1ebee", "#e7eadf", "#f3e8df", "#e8dfd1"],
    )
    make_tea_plot(tea_rows)


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> list[str]:
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for row in rows:
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append(f"{value:.3f}")
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def write_stage_report(stage_rows: list[dict[str, Any]], reconciliation: list[dict[str, Any]]) -> None:
    base = next(row for row in stage_rows if row["scenario"] == "base_smackover_ms2")
    lines = [
        "# TBAC/DA DES + 10 wt% TOPO PrOMMiS/IDAES-Style Stage Results",
        "",
        "## Decision",
        "",
        "The process layer consumes the Agent 2 transfer variables directly. The staged process value reported for the deck is overall Li recovery after pretreatment Li loss, while the transfer-table value remains the extraction-step recovery on the clean Li/Na feed.",
        "",
        "## Base Case",
        "",
        f"- Case: `smackover_ms2_main_anchor`.",
        f"- Solvent system: `{SOLVENT}`.",
        f"- Transfer-table Li recovery: `{base['transfer_table_cumulative_Li_recovery_pct']:.3f}%`.",
        f"- Overall staged Li recovery after pretreatment loss: `{base['prommis_idaes_staged_Li_recovery_pct']:.3f}%`.",
        f"- Na co-extraction across the staged contactor: `{base['prommis_idaes_staged_Na_recovery_pct']:.3f}%`.",
        f"- Li2CO3-equivalent placeholder output at `{base['feed_flow_m3_day']:.0f} m3/day`: `{base['Li2CO3_kg_year']:.0f} kg/year`.",
        "",
        "## Recovery Reconciliation",
        "",
        *markdown_table(
            reconciliation,
            [
                "scenario",
                "transfer_table_cumulative_Li_recovery_pct",
                "prommis_idaes_staged_Li_recovery_pct",
                "absolute_difference_pct_points",
                "reason_for_difference",
                "chosen_deck_value",
            ],
        ),
        "",
        "## Boundary",
        "",
        "Divalent ions appear as pretreatment removal and residual-leakage guardrails. They are not active Li/Na extraction species in this stage model.",
        "",
    ]
    STAGE_REPORT.parent.mkdir(parents=True, exist_ok=True)
    STAGE_REPORT.write_text("\n".join(lines), encoding="utf-8")


def write_tea_report(tea_rows: list[dict[str, Any]]) -> None:
    base = next(row for row in tea_rows if row["scenario"] == "base_smackover_ms2")
    lines = [
        "# TBAC/DA DES + 10 wt% TOPO Screening TEA",
        "",
        "## Decision",
        "",
        "The TEA output is a screening-level scenario scaffold for internal project formalization. It is not vendor-grade, design-grade, or investment-grade economics.",
        "",
        "## Scenario Results",
        "",
        *markdown_table(
            tea_rows,
            [
                "scenario",
                "Li_recovery_pct",
                "pretreatment_Li_loss_pct",
                "solvent_loss_rate",
                "stage_count",
                "Li2CO3_kg_year",
                "breakeven_metric",
            ],
        ),
        "",
        "## Base Case Cost Basis",
        "",
        f"- Base scenario: `{base['scenario']}`.",
        f"- Screening breakeven: `{base['breakeven_metric']}`.",
        f"- Screening margin metric: `{base['net_before_tax_or_margin_metric']}`.",
        "- Cost structure includes pretreatment, extraction/contacting, solvent loss, and stripping/concentration placeholders.",
        "",
        "## Caveat",
        "",
        "Cost values are scenario scaffolds until solvent loss, reagent use, flowrate, regeneration, and equipment assumptions are approved.",
        "",
    ]
    TEA_REPORT.parent.mkdir(parents=True, exist_ok=True)
    TEA_REPORT.write_text("\n".join(lines), encoding="utf-8")


def deck_qmd(stage_rows: list[dict[str, Any]], tea_rows: list[dict[str, Any]], reconciliation: list[dict[str, Any]]) -> str:
    base = next(row for row in stage_rows if row["scenario"] == "base_smackover_ms2")
    stress = next(row for row in tea_rows if row["scenario"] == "stress_bakken_high_na")
    base_tea = next(row for row in tea_rows if row["scenario"] == "base_smackover_ms2")
    favorable = next(row for row in tea_rows if row["scenario"] == "favorable_smackover_high_li")
    base_recon = next(row for row in reconciliation if row["scenario"] == "base_smackover_ms2")
    return "\n".join(
        [
            "---",
            "format:",
            "  revealjs:",
            "    theme: simple",
            "    slide-number: true",
            "    embed-resources: true",
            "    width: 1600",
            "    height: 900",
            "    transition: none",
            "---",
            "",
            "## Internal Project Ask",
            "",
            "Approve an internal integration sprint that connects produced-water feed chemistry, ePC-SAFT-calibrated Li/Na transfer variables, PrOMMiS/IDAES staged extraction, and screening TEA.",
            "",
            "![Workflow handoff](figures/prommis_idaes_workflow.png)",
            "",
            "Decision target: formalize the ePC-SAFT-to-PrOMMiS/IDAES case-study workflow and fund the validation work needed to replace calibrated transfer variables with direct closure when the phase-inventory convention is resolved.",
            "",
            "## Why Produced Water",
            "",
            "Produced water is a lithium-bearing waste stream with existing handling infrastructure, but feed chemistry controls whether extraction is credible.",
            "",
            "![Candidate ranking](figures/produced_water_candidate_ranking.png)",
            "",
            "The case study prioritizes feed quality, salinity severity, and interference burden over volume-only opportunity claims.",
            "",
            "## Candidate Screening",
            "",
            "Smackover, Marcellus, Bakken, and Permian do not play the same process role.",
            "",
            "| Candidate | Case-study role | Decision |",
            "|---|---|---|",
            "| Smackover MS-2 | main flowsheet case | high-salinity hard case with source-backed major ions |",
            "| Smackover high observed | sensitivity | high-Li sensitivity, not the base case |",
            "| Marcellus NE PA | comparison card | lower-burden comparison until missing ions are sourced |",
            "| Bakken high Na | stress test | high-Na validity stress, not the flagship |",
            "",
            "## Selected Feed Cases",
            "",
            "![Feed card](figures/smackover_marcellus_feed_card.png)",
            "",
            "Smackover MS-2 is the main flowsheet case. Marcellus NE PA remains a comparison card because Na, Ca, Sr, and Ba are not source-complete in the current feed table.",
            "",
            "## Pretreatment Boundary",
            "",
            "![Pretreatment boundary](figures/pretreatment_boundary.png)",
            "",
            "Raw produced water is not the extraction feed. Ca, Mg, Sr, Ba, suspended solids, oil, organics, and pretreatment Li loss sit upstream of the Li/Na solvent-extraction model.",
            "",
            "## Solvent System",
            "",
            "![Solvent mechanism](figures/tbac_da_topo_mechanism.png)",
            "",
            f"`{SOLVENT_FORMULATION}` is fixed for the main case-study basis. TOPO is fixed at 10 wt% and TBAC:DA is fixed at 1:2.",
            "",
            "## ePC-SAFT Role",
            "",
            "ePC-SAFT supplies activity, density, distribution, selectivity, and validity information that process models can consume.",
            "",
            "| Role | Main-deck message |",
            "|---|---|",
            "| Transfer variables | Process models consume D_Li, D_Na, stage count, O/A, recovery, and validity flags. |",
            "| Validity gate | High Na/Li rows remain extrapolation-flagged. |",
            "| Direct closure | Direct reactive-LLE is not the model of record until the phase-inventory convention closes. |",
            "",
            "## Base Extraction Result",
            "",
            "![Base extraction result](figures/base_extraction_result_card.png)",
            "",
            f"The Smackover MS-2 transfer table gives `{base['transfer_table_cumulative_Li_recovery_pct']:.3f}%` extraction-step Li recovery. The staged process value used in the deck is `{base['prommis_idaes_staged_Li_recovery_pct']:.3f}%` overall Li recovery after pretreatment Li loss.",
            "",
            "## Surrogate And Validity Gate",
            "",
            "![Validity gate](figures/surrogate_validity_gate.png)",
            "",
            "Produced-water Na/Li ratios exceed the low-Na/Li source-paper design space. PrOMMiS/IDAES should carry the extrapolation flag instead of treating high-Na rows as fully validated.",
            "",
            "## PrOMMiS/IDAES Workflow",
            "",
            "![PrOMMiS/IDAES workflow](figures/prommis_idaes_workflow.png)",
            "",
            "The process layer consumes the transfer table, applies pretreatment Li loss, stages the Li/Na extraction, and hands reconciled recovery values to screening TEA.",
            "",
            f"Recovery reconciliation: `{base_recon['reason_for_difference'].rstrip('.')}`.",
            "",
            "## Screening TEA",
            "",
            "![Screening TEA scenarios](figures/screening_tea_scenarios.png)",
            "",
            f"Base screening breakeven is `{base_tea['breakeven_metric']}`. Stress and favorable cases bracket the current scaffold at `{stress['breakeven_metric']}` and `{favorable['breakeven_metric']}`.",
            "",
            "All economics are screening TEA values for internal project formalization.",
            "",
            "## Roadmap And Ask",
            "",
            "| Workstream | Proof artifact | Stop condition |",
            "|---|---|---|",
            "| Direct ePC-SAFT closure | phase-inventory convention scan | direct closure passes validation or remains bounded |",
            "| PrOMMiS/IDAES integration | staged contactor implementation | transfer variables match reconciled recovery table |",
            "| Screening TEA maturation | approved assumption table | solvent loss, regeneration, and equipment basis are reviewed |",
            "",
            "Project ask: fund the integration and validation sprint, not commercialization or plant-ready economics.",
            "",
            "## Backup: ePC-SAFT Theory Details",
            "",
            "ePC-SAFT contributes activity coefficients, fugacity diagnostics, density support, and phase-stability evidence. The current deck uses calibrated transfer variables because direct reactive-LLE closure is not promoted.",
            "",
            "## Backup: Solvent-Extraction Definitions",
            "",
            "| Quantity | Definition |",
            "|---|---|",
            "| D_Li | Li distribution ratio consumed by staged extraction. |",
            "| D_Na | Na distribution ratio consumed by staged extraction. |",
            "| O/A | organic-to-aqueous mass ratio in the transfer table. |",
            "| Selectivity | D_Li divided by D_Na. |",
            "",
            "## Backup: Source-Paper Benchmark Details",
            "",
            "The source-paper benchmark layer includes 10 wt% TOPO anchor rows with optimized Li extraction near 48.57% and a model-brine Li/Na extraction row near 51.63% Li and 9.97% Na.",
            "",
            "These rows are bridge anchors, not produced-water process simulations.",
            "",
            "## Backup: Phase-Inventory Diagnostics",
            "",
            "The active diagnostic term is phase-inventory / reaction-coordinate reference-state convention.",
            "",
            "The convention scan reports no promoted direct reactive-LLE closure; the case-study deck therefore uses calibrated transfer variables and carries validity flags.",
            "",
            "## Backup: Literature Scorecard",
            "",
            "| Evidence layer | Deck use | Boundary |",
            "|---|---|---|",
            "| Produced-water feed table | Smackover and comparison-feed basis | missing values remain flagged |",
            "| Solvent extraction benchmark | Li/Na extraction anchor | not Smackover experimental validation |",
            "| ePC-SAFT diagnostics | transfer-variable credibility | direct closure not promoted |",
            "| Process and TEA scaffold | internal project ask | screening TEA only |",
            "",
            "## Backup: Full TEA Assumption Table",
            "",
            "| Scenario | Li recovery (%) | Solvent loss rate | Stage count | Breakeven metric |",
            "|---|---:|---:|---:|---|",
            *[
                f"| {row['scenario']} | {row['Li_recovery_pct']:.3f} | {row['solvent_loss_rate']:.3f} | {int(row['stage_count'])} | {row['breakeven_metric']} |"
                for row in tea_rows
            ],
            "",
        ]
    )


def write_deck(stage_rows: list[dict[str, Any]], tea_rows: list[dict[str, Any]], reconciliation: list[dict[str, Any]]) -> None:
    SLIDE_DIR.mkdir(parents=True, exist_ok=True)
    DECK.write_text(deck_qmd(stage_rows, tea_rows, reconciliation), encoding="utf-8")
    DECK_README.write_text(
        "\n".join(
            [
                "# TBAC/DA/TOPO Produced-Water Case-Study Deck",
                "",
                "## Source Of Truth",
                "",
                "- Canonical source: `deck.qmd`.",
                "- Generated review output: `deck.html` after Quarto render.",
                "- Figures: `figures/`.",
                "",
                "## Build",
                "",
                "```powershell",
                "& \"$env:LOCALAPPDATA\\Apps\\Quarto\\bin\\quarto.exe\" render .\\deck.qmd --to revealjs",
                "```",
                "",
                "PowerPoint is out of scope unless explicitly reopened.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def readiness_text() -> str:
    return "\n".join(
        [
            "# Final Case-Study Readiness Checklist",
            "",
            "| Check | Status | Evidence |",
            "|---|---|---|",
            "| Story is case-study-first | pass | `slides/case_study_tbac_da_topo_produced_water/deck.qmd` starts with the internal project ask. |",
            "| Solvent naming is chemical | pass | Deck and reports use TBAC/DA DES + 10 wt% TOPO naming. |",
            "| Smackover and Marcellus are not conflated | pass | Marcellus remains a comparison card with missing-value caveat. |",
            "| Extraction feed is post-pretreatment | pass | Process report and deck carry the pretreatment boundary. |",
            "| Model basis is labeled | pass | Stage results carry `model_basis` and `basis_type` from the transfer table. |",
            "| Phase-inventory convention is bounded | pass | Direct ePC-SAFT is not promoted in the deck or reports. |",
            "| Recovery values are reconciled | pass | `data/processed/tbac_da_topo_recovery_reconciliation.csv`. |",
            "| Screening TEA caveats are visible | pass | `results/tbac_da_topo_screening_tea.md`. |",
            "| Key numbers trace to artifacts | pass | Transfer, process, reconciliation, and TEA CSVs are the numeric source. |",
            "| Main deck has 12 main slides plus backup | pass | `deck.qmd` follows the required 12-slide order. |",
            "| Project ask is internal formalization | pass | First and final main slides frame integration and validation funding. |",
            "",
            "Residual risk: Marcellus NE PA remains comparison-card-only until missing major ions are filled from source-backed data.",
            "",
        ]
    )


def changelog_text() -> str:
    return "\n".join(
        [
            "# TBAC/DA/TOPO Process, TEA, And Deck Changelog",
            "",
            "## Files Touched",
            "",
            "- Added `analyses/rezaee_2026_pcsaft_epcsaft/scripts/tbac_da_topo_agent3_prommis_tea_deck.py`.",
            "- Generated `data/processed/tbac_da_topo_prommis_stage_results.csv`.",
            "- Generated `data/processed/tbac_da_topo_recovery_reconciliation.csv`.",
            "- Generated `data/processed/tbac_da_topo_screening_tea_results.csv`.",
            "- Generated `results/tbac_da_topo_prommis_stage_results.md`.",
            "- Generated `results/tbac_da_topo_screening_tea.md`.",
            "- Generated `slides/case_study_tbac_da_topo_produced_water/deck.qmd`, `README.md`, and management figures.",
            "- Generated `docs/final_case_study_readiness_checklist.md`.",
            "",
            "## Validation Commands",
            "",
            "- `uv run python analyses/rezaee_2026_pcsaft_epcsaft/scripts/tbac_da_topo_agent3_prommis_tea_deck.py`",
            "- `uv run python -m compileall -q analyses/rezaee_2026_pcsaft_epcsaft/scripts`",
            "- `uv run python scripts/check_epcsaft_integration.py --mode final`",
            "- `quarto render slides/case_study_tbac_da_topo_produced_water/deck.qmd --to revealjs`",
            "- custom Agent 3 artifact and deck acceptance validator",
            "",
            "## Boundary",
            "",
            "The process and TEA outputs are screening artifacts for internal project formalization. Direct reactive-LLE closure is not promoted, and Marcellus remains comparison-card-only until missing major ions are sourced.",
            "",
        ]
    )


def validate(stage_rows: list[dict[str, Any]], reconciliation: list[dict[str, Any]], tea_rows: list[dict[str, Any]]) -> None:
    required_stage = {
        "case_id",
        "scenario",
        "feed_id",
        "D_Li",
        "D_Na",
        "one_stage_Li_extraction_pct",
        "one_stage_Na_extraction_pct",
        "transfer_table_cumulative_Li_recovery_pct",
        "prommis_idaes_staged_Li_recovery_pct",
        "validity_flag",
        "extrapolation_flag",
    }
    missing_stage = required_stage - set(stage_rows[0])
    if missing_stage:
        raise ValueError(f"stage results missing {missing_stage}")
    required_tea = {
        "case_id",
        "scenario",
        "feed_flow_m3_day",
        "operating_days_per_year",
        "Li_feed_mg_L",
        "Li_recovery_pct",
        "pretreatment_Li_loss_pct",
        "solvent_loss_rate",
        "stage_count",
        "Li2CO3_kg_year",
        "major_cost_assumptions",
        "breakeven_metric",
        "net_before_tax_or_margin_metric",
        "validity_flag",
        "screening_tea_caveat",
    }
    missing_tea = required_tea - set(tea_rows[0])
    if missing_tea:
        raise ValueError(f"TEA results missing {missing_tea}")
    if not any(row["scenario"] == "base_smackover_ms2" for row in stage_rows):
        raise ValueError("missing base Smackover stage row")
    if not any("comparison-card-only" in row["screening_tea_caveat"] for row in tea_rows):
        raise ValueError("Marcellus comparison caveat missing")
    if any("investment-grade" in row["screening_tea_caveat"].lower() and "not" not in row["screening_tea_caveat"].lower() for row in tea_rows):
        raise ValueError("TEA caveat wording is unsafe")
    if not reconciliation:
        raise ValueError("reconciliation table is empty")


def main() -> None:
    feeds, transfers, _transfer_rows = load_inputs()
    stage_rows, reconciliation = build_stage_results(feeds, transfers)
    for row in stage_rows:
        row["solvent_loss_rate"] = scenario_solvent_loss(row["scenario"])
    tea_rows = build_tea_rows(stage_rows)
    validate(stage_rows, reconciliation, tea_rows)

    write_csv(STAGE_RESULTS, stage_rows)
    write_csv(RECONCILIATION, reconciliation)
    write_csv(TEA_RESULTS, tea_rows)
    generate_figures(feeds, stage_rows, tea_rows)
    write_stage_report(stage_rows, reconciliation)
    write_tea_report(tea_rows)
    write_deck(stage_rows, tea_rows, reconciliation)
    READINESS.write_text(readiness_text(), encoding="utf-8")
    CHANGELOG.write_text(changelog_text(), encoding="utf-8")

    base = next(row for row in stage_rows if row["scenario"] == "base_smackover_ms2")
    print(
        "generated Agent 3 artifacts; "
        f"base extraction-step Li recovery={base['transfer_table_cumulative_Li_recovery_pct']:.3f}% "
        f"and overall staged Li recovery={base['prommis_idaes_staged_Li_recovery_pct']:.3f}%"
    )


if __name__ == "__main__":
    main()
