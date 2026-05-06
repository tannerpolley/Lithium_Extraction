from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts.gando_2025_pcsaft_repro.gando_2025_selective_model import (
    DEFAULT_CONFIG_JSON,
    MW,
    load_payload,
    load_selective_config,
    mg_L_to_mol_L,
    solve_selective_stage,
)

OUT_DIR = REPO_ROOT / "data" / "multiphase" / "gando_2025_slide_assets"
TABLE4_CUM = np.array([54.95, 85.60, 97.17], dtype=float)
FIG3_NA_MG_L = np.array([0.0, 2000.0, 4000.0, 6000.0, 8000.0, 10900.0], dtype=float)
FIG3_LI_TARGET = np.array([49.82, np.nan, np.nan, np.nan, np.nan, 51.82], dtype=float)
LI_FEED_MG_L = 60.0
NA_FEED_MG_L = 10900.0
TOP_MOL_L = 0.015
OA_RATIO = 1.0

BG = "#f6f1e8"
TEXT = "#182028"
GRID = "#aab3bb"
LI_COLOR = "#0b7a75"
NA_COLOR = "#d95f02"
PAPER_COLOR = "#2f3e46"
SELECTIVITY_COLOR = "#8c564b"
RATIO_COLOR = "#3b5b92"
ACCENT = "#f0c34e"


@dataclass
class StageRow:
    stage: int
    li_feed_mg_L: float
    na_feed_mg_L: float
    li_raffinate_mg_L: float
    na_raffinate_mg_L: float
    li_stage_pct: float
    li_cumulative_pct: float
    na_stage_pct: float
    na_cumulative_pct: float
    li_distribution_ratio: float
    li_na_selectivity: float
    paper_li_cumulative_pct: float


@dataclass
class SweepRow:
    na_mg_L: float
    paper_li_stage_pct: float
    calc_li_stage_pct: float
    calc_na_stage_pct: float
    calc_li_distribution_ratio: float
    calc_li_na_selectivity: float
    saltout_factor: float


def _mol_L_to_mg_L(value_mol_L: float, species: str) -> float:
    return float(value_mol_L) * MW[species] * 1e6


def _style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor(BG)
    ax.grid(axis="y", color=GRID, alpha=0.45, linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=TEXT, labelsize=11)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)


def _annotate_bar_values(ax: plt.Axes, bars, fmt: str = "{:.2f}") -> None:
    for bar in bars:
        height = float(bar.get_height())
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 1.1,
            fmt.format(height),
            ha="center",
            va="bottom",
            fontsize=10,
            color=TEXT,
            fontweight="bold",
        )


def _compute_stage_rows(config) -> list[StageRow]:
    li_remaining = mg_L_to_mol_L(LI_FEED_MG_L, "Li+")
    na_remaining = mg_L_to_mol_L(NA_FEED_MG_L, "Na+")
    li_initial = li_remaining
    na_initial = na_remaining

    rows: list[StageRow] = []
    for idx in range(3):
        li_feed_now = _mol_L_to_mg_L(li_remaining, "Li+")
        na_feed_now = _mol_L_to_mg_L(na_remaining, "Na+")

        stage = solve_selective_stage(
            li_mol_L=li_remaining,
            na_mol_L=na_remaining,
            top_mol_L=TOP_MOL_L,
            o_to_a_ratio=OA_RATIO,
            config=config,
        )

        li_remaining = max(li_remaining - stage.li_extracted_mol, 0.0)
        na_remaining = max(na_remaining - stage.na_extracted_mol, 0.0)

        rows.append(
            StageRow(
                stage=idx + 1,
                li_feed_mg_L=li_feed_now,
                na_feed_mg_L=na_feed_now,
                li_raffinate_mg_L=_mol_L_to_mg_L(li_remaining, "Li+"),
                na_raffinate_mg_L=_mol_L_to_mg_L(na_remaining, "Na+"),
                li_stage_pct=stage.li_extraction_pct,
                li_cumulative_pct=100.0 * (1.0 - li_remaining / max(li_initial, 1e-30)),
                na_stage_pct=stage.na_extraction_pct,
                na_cumulative_pct=100.0 * (1.0 - na_remaining / max(na_initial, 1e-30)),
                li_distribution_ratio=stage.li_distribution_ratio,
                li_na_selectivity=stage.li_na_selectivity,
                paper_li_cumulative_pct=float(TABLE4_CUM[idx]),
            )
        )

    return rows


def _compute_sweep_rows(config) -> list[SweepRow]:
    rows: list[SweepRow] = []
    li_mol_L = mg_L_to_mol_L(LI_FEED_MG_L, "Li+")
    for na_mg_L, li_target in zip(FIG3_NA_MG_L, FIG3_LI_TARGET, strict=True):
        stage = solve_selective_stage(
            li_mol_L=li_mol_L,
            na_mol_L=mg_L_to_mol_L(float(na_mg_L), "Na+"),
            top_mol_L=TOP_MOL_L,
            o_to_a_ratio=OA_RATIO,
            config=config,
        )
        rows.append(
            SweepRow(
                na_mg_L=float(na_mg_L),
                paper_li_stage_pct=float(li_target),
                calc_li_stage_pct=stage.li_extraction_pct,
                calc_na_stage_pct=stage.na_extraction_pct,
                calc_li_distribution_ratio=stage.li_distribution_ratio,
                calc_li_na_selectivity=stage.li_na_selectivity,
                saltout_factor=stage.saltout_factor,
            )
        )
    return rows


def _write_stage_summary_csv(rows: list[StageRow], out_dir: Path) -> Path:
    path = out_dir / "gando_2025_stage_summary.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "stage",
                "paper_li_cumulative_pct",
                "calc_li_stage_pct",
                "calc_li_cumulative_pct",
                "calc_na_stage_pct",
                "calc_na_cumulative_pct",
                "calc_li_distribution_ratio",
                "calc_li_na_selectivity",
                "li_feed_mg_L",
                "li_raffinate_mg_L",
                "na_feed_mg_L",
                "na_raffinate_mg_L",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.stage,
                    row.paper_li_cumulative_pct,
                    row.li_stage_pct,
                    row.li_cumulative_pct,
                    row.na_stage_pct,
                    row.na_cumulative_pct,
                    row.li_distribution_ratio,
                    row.li_na_selectivity,
                    row.li_feed_mg_L,
                    row.li_raffinate_mg_L,
                    row.na_feed_mg_L,
                    row.na_raffinate_mg_L,
                ]
            )
    return path


def _write_sweep_csv(rows: list[SweepRow], out_dir: Path) -> Path:
    path = out_dir / "gando_2025_na_sweep.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "na_mg_L",
                "paper_li_stage_pct",
                "calc_li_stage_pct",
                "calc_na_stage_pct",
                "calc_li_distribution_ratio",
                "calc_li_na_selectivity",
                "saltout_factor",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.na_mg_L,
                    row.paper_li_stage_pct,
                    row.calc_li_stage_pct,
                    row.calc_na_stage_pct,
                    row.calc_li_distribution_ratio,
                    row.calc_li_na_selectivity,
                    row.saltout_factor,
                ]
            )
    return path


def _write_kpi_csv(rows: list[StageRow], sweep_rows: list[SweepRow], out_dir: Path) -> Path:
    path = out_dir / "gando_2025_kpis.csv"
    final = rows[-1]
    nominal = sweep_rows[-1]
    kpis = [
        ("Nominal one-stage Li extraction (%)", nominal.calc_li_stage_pct),
        ("Nominal one-stage Na extraction (%)", nominal.calc_na_stage_pct),
        ("Stage 3 cumulative Li extraction (%)", final.li_cumulative_pct),
        ("Stage 3 cumulative Na extraction (%)", final.na_cumulative_pct),
        ("Stage 3 Li/Na selectivity", final.li_na_selectivity),
        ("Stage 3 Li distribution ratio", final.li_distribution_ratio),
        ("Stage 3 Li remaining in raffinate (mg/L)", final.li_raffinate_mg_L),
        ("Stage 3 Na remaining in raffinate (mg/L)", final.na_raffinate_mg_L),
        ("Stage 3 Li minus paper (pct-pts)", final.li_cumulative_pct - final.paper_li_cumulative_pct),
        ("Nominal salt-out factor", nominal.saltout_factor),
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        writer.writerows(kpis)
    return path


def _render_table_png(
    title: str,
    columns: list[str],
    rows: list[list[str]],
    out_path: Path,
    *,
    width: float = 13.33,
    row_height: float = 0.58,
    title_height: float = 1.2,
    font_size: int = 12,
) -> Path:
    fig_height = max(2.6, title_height + row_height * (len(rows) + 1))
    fig, ax = plt.subplots(figsize=(width, fig_height), dpi=180)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.text(
        0.0,
        1.03,
        title,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=20,
        fontweight="bold",
        color=TEXT,
    )

    table = ax.table(
        cellText=rows,
        colLabels=columns,
        loc="upper left",
        cellLoc="center",
        bbox=[0.0, 0.02, 1.0, 0.90],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)

    for (row_idx, col_idx), cell in table.get_celld().items():
        cell.set_edgecolor("#d7d1c3")
        cell.set_linewidth(0.8)
        if row_idx == 0:
            cell.set_facecolor(PAPER_COLOR)
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("#fffdf8" if row_idx % 2 else "#f2ece1")
            if col_idx == 0:
                cell.set_text_props(weight="bold", color=TEXT)
            else:
                cell.set_text_props(color=TEXT)

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return out_path


def _plot_cumulative(rows: list[StageRow], out_dir: Path) -> Path:
    path = out_dir / "gando_2025_cumulative_extraction_wide.png"
    stages = np.array([row.stage for row in rows], dtype=float)
    li_cum = np.array([row.li_cumulative_pct for row in rows], dtype=float)
    na_cum = np.array([row.na_cumulative_pct for row in rows], dtype=float)
    paper = np.array([row.paper_li_cumulative_pct for row in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    ax.plot(stages, paper, color=PAPER_COLOR, linewidth=2.4, marker="o", markersize=8, label="Paper Li cumulative")
    ax.plot(stages, li_cum, color=LI_COLOR, linewidth=3.0, marker="o", markersize=9, label="Model Li cumulative")
    ax.plot(stages, na_cum, color=NA_COLOR, linewidth=2.6, marker="s", markersize=7, label="Model Na cumulative")
    ax.fill_between(stages, 0.0, li_cum, color=LI_COLOR, alpha=0.08)
    ax.set_xlim(0.8, 3.2)
    ax.set_ylim(0.0, 105.0)
    ax.set_xticks(stages)
    ax.set_xlabel("Crossflow stage", fontsize=13, fontweight="bold")
    ax.set_ylabel("Cumulative extraction (%)", fontsize=13, fontweight="bold")
    ax.set_title("Gando 2025 selective showcase keeps Li high and Na low", fontsize=22, fontweight="bold", pad=18)
    ax.legend(frameon=False, fontsize=12, loc="lower right")
    ax.text(3.03, li_cum[-1], f"{li_cum[-1]:.2f}%", color=LI_COLOR, fontsize=12, fontweight="bold", va="center")
    ax.text(3.03, na_cum[-1], f"{na_cum[-1]:.2f}%", color=NA_COLOR, fontsize=12, fontweight="bold", va="center")
    ax.text(3.03, paper[-1] - 2.5, f"{paper[-1]:.2f}%", color=PAPER_COLOR, fontsize=11, fontweight="bold", va="center")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _plot_stage_bars(rows: list[StageRow], out_dir: Path) -> Path:
    path = out_dir / "gando_2025_stagewise_extraction_bars.png"
    stages = np.array([row.stage for row in rows], dtype=float)
    li_stage = np.array([row.li_stage_pct for row in rows], dtype=float)
    na_stage = np.array([row.na_stage_pct for row in rows], dtype=float)
    width = 0.34

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    li_bars = ax.bar(stages - width / 2.0, li_stage, width=width, color=LI_COLOR, label="Li stage extraction")
    na_bars = ax.bar(stages + width / 2.0, na_stage, width=width, color=NA_COLOR, label="Na stage extraction")
    _annotate_bar_values(ax, li_bars)
    _annotate_bar_values(ax, na_bars)
    ax.set_xticks(stages)
    ax.set_ylim(0.0, 100.0)
    ax.set_xlabel("Crossflow stage", fontsize=13, fontweight="bold")
    ax.set_ylabel("Stage extraction (%)", fontsize=13, fontweight="bold")
    ax.set_title("Each stage remains strongly lithium-selective", fontsize=22, fontweight="bold", pad=18)
    ax.legend(frameon=False, fontsize=12, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _plot_selectivity(rows: list[StageRow], out_dir: Path) -> Path:
    path = out_dir / "gando_2025_selectivity_profile.png"
    stages = np.array([row.stage for row in rows], dtype=float)
    selectivity = np.array([row.li_na_selectivity for row in rows], dtype=float)
    d_li = np.array([row.li_distribution_ratio for row in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    bars = ax.bar(stages, selectivity, width=0.52, color=SELECTIVITY_COLOR, alpha=0.88, label="Li/Na selectivity")
    _annotate_bar_values(ax, bars, "{:.1f}")
    ax.set_xticks(stages)
    ax.set_xlabel("Crossflow stage", fontsize=13, fontweight="bold")
    ax.set_ylabel("Li/Na selectivity", fontsize=13, fontweight="bold")
    ax.set_title("Selectivity intensifies as the raffinate is polished", fontsize=22, fontweight="bold", pad=18)

    ax2 = ax.twinx()
    ax2.set_facecolor("none")
    for spine in ax2.spines.values():
        spine.set_visible(False)
    ax2.tick_params(colors=TEXT, labelsize=11)
    ax2.set_ylabel("Li distribution ratio", fontsize=13, fontweight="bold", color=TEXT)
    ax2.plot(stages, d_li, color=RATIO_COLOR, linewidth=2.8, marker="o", markersize=8, label="$D_{Li}$")
    ax2.text(3.08, d_li[-1], f"$D_{{Li}}$ = {d_li[-1]:.2f}", color=RATIO_COLOR, fontsize=12, fontweight="bold", va="center")

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, frameon=False, fontsize=12, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _plot_nominal_spotlight(rows: list[StageRow], sweep_rows: list[SweepRow], out_dir: Path) -> Path:
    path = out_dir / "gando_2025_nominal_spotlight.png"
    nominal = sweep_rows[-1]
    final = rows[-1]

    fig, axes = plt.subplots(1, 2, figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)

    for ax in axes:
        _style_axes(ax)

    left_values = [nominal.calc_li_stage_pct, nominal.calc_na_stage_pct]
    left_labels = ["Li", "Na"]
    left_colors = [LI_COLOR, NA_COLOR]
    bars_left = axes[0].bar(left_labels, left_values, color=left_colors, width=0.56)
    _annotate_bar_values(axes[0], bars_left)
    axes[0].set_ylim(0.0, 60.0)
    axes[0].set_ylabel("Single-stage extraction (%)", fontsize=13, fontweight="bold")
    axes[0].set_title("Nominal one-stage result", fontsize=18, fontweight="bold", pad=14)
    axes[0].text(
        0.03,
        0.92,
        f"Na feed = {NA_FEED_MG_L:,.0f} mg/L\nTOP = {TOP_MOL_L:.3f} mol/L",
        transform=axes[0].transAxes,
        ha="left",
        va="top",
        fontsize=11,
        color=TEXT,
        bbox=dict(facecolor="#fffdf8", edgecolor="#d7d1c3", boxstyle="round,pad=0.35"),
    )

    right_values = [final.li_cumulative_pct, final.na_cumulative_pct]
    right_labels = ["Li cumulative", "Na cumulative"]
    bars_right = axes[1].bar(right_labels, right_values, color=[LI_COLOR, NA_COLOR], width=0.56)
    _annotate_bar_values(axes[1], bars_right)
    axes[1].set_ylim(0.0, 105.0)
    axes[1].set_ylabel("Three-stage cumulative extraction (%)", fontsize=13, fontweight="bold")
    axes[1].set_title("Three-stage finish", fontsize=18, fontweight="bold", pad=14)
    axes[1].text(
        0.03,
        0.92,
        f"Li/Na selectivity = {final.li_na_selectivity:.1f}\nLi remaining = {final.li_raffinate_mg_L:.2f} mg/L",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=11,
        color=TEXT,
        bbox=dict(facecolor="#fffdf8", edgecolor="#d7d1c3", boxstyle="round,pad=0.35"),
    )

    fig.suptitle("Slide-ready spotlight on the nominal selective case", fontsize=22, fontweight="bold", color=TEXT, y=0.98)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _plot_na_sweep(sweep_rows: list[SweepRow], out_dir: Path) -> Path:
    path = out_dir / "gando_2025_na_sweep_wide.png"
    x = np.array([row.na_mg_L for row in sweep_rows], dtype=float)
    y_li = np.array([row.calc_li_stage_pct for row in sweep_rows], dtype=float)
    y_na = np.array([row.calc_na_stage_pct for row in sweep_rows], dtype=float)
    y_sel = np.array([row.calc_li_na_selectivity for row in sweep_rows], dtype=float)

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    ax.plot(x, y_li, color=LI_COLOR, linewidth=3.0, marker="o", markersize=8, label="Li extraction")
    ax.plot(x, y_na, color=NA_COLOR, linewidth=2.6, marker="s", markersize=7, label="Na extraction")
    finite = ~np.isnan(FIG3_LI_TARGET)
    ax.scatter(
        x[finite],
        FIG3_LI_TARGET[finite],
        facecolors="white",
        edgecolors=PAPER_COLOR,
        s=80,
        linewidths=1.6,
        label="Paper Li points",
        zorder=4,
    )
    ax.set_xlabel("Na concentration in aqueous feed (mg/L)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Single-stage extraction (%)", fontsize=13, fontweight="bold")
    ax.set_ylim(0.0, 60.0)
    ax.set_title("Na-rich feed preserves Li extraction while Na stays low", fontsize=22, fontweight="bold", pad=18)

    ax2 = ax.twinx()
    ax2.set_facecolor("none")
    for spine in ax2.spines.values():
        spine.set_visible(False)
    ax2.tick_params(colors=TEXT, labelsize=11)
    ax2.plot(x, y_sel, color=ACCENT, linewidth=2.4, linestyle="--", marker="D", markersize=6, label="Li/Na selectivity")
    ax2.set_ylabel("Li/Na selectivity", fontsize=13, fontweight="bold", color=TEXT)

    nominal_idx = len(sweep_rows) - 1
    ax.annotate(
        "Nominal brine point",
        xy=(x[nominal_idx], y_li[nominal_idx]),
        xytext=(7800, 56.0),
        arrowprops=dict(arrowstyle="->", color=TEXT, linewidth=1.2),
        fontsize=11,
        color=TEXT,
        fontweight="bold",
    )

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, frameon=False, fontsize=12, loc="center right")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _write_markdown(
    rows: list[StageRow],
    sweep_rows: list[SweepRow],
    payload: dict,
    out_dir: Path,
    generated_pngs: list[Path],
    generated_csvs: list[Path],
) -> Path:
    path = out_dir / "gando_2025_slide_assets.md"
    params = payload["parameters"]
    final = rows[-1]
    nominal = sweep_rows[-1]

    lines: list[str] = []
    lines.append("# Gando 2025 Slide Assets")
    lines.append("")
    lines.append("## Basis")
    lines.append("")
    lines.append(f"- Config: `{DEFAULT_CONFIG_JSON}`")
    lines.append("- Mechanism: external Li-selective HBTA/TOPO chelation wrapper layered on top of the PC-SAFT phase-split backbone.")
    lines.append(f"- Feed basis: Li = {LI_FEED_MG_L:.3f} mg/L, Na = {NA_FEED_MG_L:.3f} mg/L, O/A = {OA_RATIO:.3f}, TOP = {TOP_MOL_L:.6f} mol/L.")
    lines.append(f"- Fitted parameters: `log10(K_Li) = {params['log10_k_li']:.8f}`, `log10(K_Na) = {params['log10_k_na']:.8f}`, `log10(capacity factor) = {params['log10_capacity_factor']:.8f}`.")
    lines.append("")
    lines.append("## Headline Numbers")
    lines.append("")
    lines.append(f"- Nominal one-stage extraction: Li = {nominal.calc_li_stage_pct:.4f}%, Na = {nominal.calc_na_stage_pct:.4f}%.")
    lines.append(f"- Stage-3 cumulative extraction: Li = {final.li_cumulative_pct:.4f}%, Na = {final.na_cumulative_pct:.4f}%.")
    lines.append(f"- Stage-3 Li/Na selectivity: {final.li_na_selectivity:.4f}.")
    lines.append(f"- Stage-3 Li remaining in raffinate: {final.li_raffinate_mg_L:.4f} mg/L.")
    lines.append("")
    lines.append("## PNG Assets")
    lines.append("")
    for png in generated_pngs:
        lines.append(f"- `{png.name}`")
    lines.append("")
    lines.append("## CSV Tables")
    lines.append("")
    for csv_path in generated_csvs:
        lines.append(f"- `{csv_path.name}`")
    lines.append("")
    lines.append("## Stage Summary")
    lines.append("")
    lines.append("| Stage | Paper $E_{Li,cum}$ (%) | Calc $E_{Li,cum}$ (%) | Calc $E_{Na,cum}$ (%) | $D_{Li}$ | $S_{Li/Na}$ |")
    lines.append("|---:|---:|---:|---:|---:|---:|")
    for row in rows:
        lines.append(
            f"| {row.stage} | {row.paper_li_cumulative_pct:.4f} | {row.li_cumulative_pct:.4f} | {row.na_cumulative_pct:.4f} | {row.li_distribution_ratio:.4f} | {row.li_na_selectivity:.4f} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build_assets(out_dir: Path = OUT_DIR) -> dict[str, list[Path]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    config = load_selective_config(DEFAULT_CONFIG_JSON)
    payload = load_payload(DEFAULT_CONFIG_JSON)

    stage_rows = _compute_stage_rows(config)
    sweep_rows = _compute_sweep_rows(config)

    csv_paths = [
        _write_stage_summary_csv(stage_rows, out_dir),
        _write_sweep_csv(sweep_rows, out_dir),
        _write_kpi_csv(stage_rows, sweep_rows, out_dir),
    ]

    stage_table_rows = [
        [
            str(row.stage),
            f"{row.paper_li_cumulative_pct:.2f}",
            f"{row.li_stage_pct:.2f}",
            f"{row.li_cumulative_pct:.2f}",
            f"{row.na_stage_pct:.2f}",
            f"{row.na_cumulative_pct:.2f}",
            f"{row.li_distribution_ratio:.2f}",
            f"{row.li_na_selectivity:.1f}",
        ]
        for row in stage_rows
    ]
    stage_table_png = _render_table_png(
        "Gando 2025 stage-by-stage selective crossflow summary",
        [
            "Stage",
            "Paper Li cum (%)",
            "Li stage (%)",
            "Li cum (%)",
            "Na stage (%)",
            "Na cum (%)",
            "D_Li",
            "S_Li/Na",
        ],
        stage_table_rows,
        out_dir / "gando_2025_stage_summary_table.png",
        font_size=12,
    )

    final = stage_rows[-1]
    nominal = sweep_rows[-1]
    kpi_table_png = _render_table_png(
        "Gando 2025 headline KPIs for slides",
        ["Metric", "Value"],
        [
            ["Nominal one-stage Li extraction (%)", f"{nominal.calc_li_stage_pct:.2f}"],
            ["Nominal one-stage Na extraction (%)", f"{nominal.calc_na_stage_pct:.2f}"],
            ["Stage 3 cumulative Li extraction (%)", f"{final.li_cumulative_pct:.2f}"],
            ["Stage 3 cumulative Na extraction (%)", f"{final.na_cumulative_pct:.2f}"],
            ["Stage 3 Li/Na selectivity", f"{final.li_na_selectivity:.1f}"],
            ["Stage 3 Li remaining in raffinate (mg/L)", f"{final.li_raffinate_mg_L:.2f}"],
        ],
        out_dir / "gando_2025_kpi_table.png",
        width=11.0,
        font_size=13,
    )

    png_paths = [
        _plot_cumulative(stage_rows, out_dir),
        _plot_stage_bars(stage_rows, out_dir),
        _plot_selectivity(stage_rows, out_dir),
        _plot_nominal_spotlight(stage_rows, sweep_rows, out_dir),
        _plot_na_sweep(sweep_rows, out_dir),
        stage_table_png,
        kpi_table_png,
    ]

    md_path = _write_markdown(stage_rows, sweep_rows, payload, out_dir, png_paths, csv_paths)
    return {"pngs": png_paths, "csvs": csv_paths, "markdown": [md_path]}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate slide-ready PNG and table assets for the Gando 2025 selective crossflow showcase.")
    parser.add_argument("--out-dir", default=str(OUT_DIR))
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    outputs = build_assets(Path(args.out_dir))
    for key in ("pngs", "csvs", "markdown"):
        for path in outputs[key]:
            print(f"{key[:-1].upper()}: {path}")


if __name__ == "__main__":
    main()
