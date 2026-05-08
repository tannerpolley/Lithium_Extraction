from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analyses.gando_2025_pcsaft_repro.scripts.gando_2025_selective_model import (
    DEFAULT_CONFIG_JSON,
    MW,
    load_payload,
    load_selective_config,
    mg_L_to_mol_L,
    solve_selective_stage,
)

OUT_DIR = REPO_ROOT / "data" / "multiphase" / "gando_2025_one_stage_assets"
LI_FEED_MG_L = 60.0
NA_FEED_MG_L = 10900.0
TOP_MOL_L = 0.015
OA_RATIO = 1.0
SALT_SWEEP_NA_MG_L = np.array([0.0, 1000.0, 2000.0, 4000.0, 6000.0, 8000.0, 10900.0, 15000.0, 20000.0], dtype=float)
OA_SWEEP = np.array([0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.70, 1.80], dtype=float)

BG = "#f6f1e8"
TEXT = "#182028"
GRID = "#aab3bb"
LI_COLOR = "#0b7a75"
NA_COLOR = "#d95f02"
AQUEOUS_COLOR = "#d7dfe4"
PAPER_COLOR = "#2f3e46"
SELECTIVITY_COLOR = "#8c564b"
RATIO_COLOR = "#3b5b92"
ACCENT = "#f0c34e"


@dataclass
class OneStageRow:
    sweep_type: str
    condition_label: str
    na_mg_L: float
    oa_ratio: float
    li_extraction_pct: float
    na_extraction_pct: float
    li_org_mg_L_basis: float
    na_org_mg_L_basis: float
    li_raffinate_mg_L: float
    na_raffinate_mg_L: float
    d_li: float
    d_na: float
    selectivity: float
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


def _annotate_series(ax: plt.Axes, x_values, y_values, color: str, fmt: str = "{:.2f}") -> None:
    for x_val, y_val in zip(x_values, y_values, strict=True):
        if not np.isfinite(y_val):
            continue
        ax.text(x_val, y_val, fmt.format(float(y_val)), color=color, fontsize=10, fontweight="bold", ha="left", va="bottom")


def _solve_case(*, na_mg_L: float, oa_ratio: float, label: str, sweep_type: str, config) -> OneStageRow:
    li_feed_mol = mg_L_to_mol_L(LI_FEED_MG_L, "Li+")
    na_feed_mol = mg_L_to_mol_L(na_mg_L, "Na+")
    stage = solve_selective_stage(
        li_mol_L=li_feed_mol,
        na_mol_L=na_feed_mol,
        top_mol_L=TOP_MOL_L,
        o_to_a_ratio=oa_ratio,
        config=config,
    )

    li_raff_mol = max(li_feed_mol - stage.li_extracted_mol, 0.0)
    na_raff_mol = max(na_feed_mol - stage.na_extracted_mol, 0.0)
    d_na = float("nan")
    if na_feed_mol > 0.0:
        d_na = stage.na_extracted_mol / max(na_raff_mol, 1e-30)

    return OneStageRow(
        sweep_type=sweep_type,
        condition_label=label,
        na_mg_L=float(na_mg_L),
        oa_ratio=float(oa_ratio),
        li_extraction_pct=stage.li_extraction_pct,
        na_extraction_pct=stage.na_extraction_pct,
        li_org_mg_L_basis=_mol_L_to_mg_L(stage.li_extracted_mol, "Li+"),
        na_org_mg_L_basis=_mol_L_to_mg_L(stage.na_extracted_mol, "Na+"),
        li_raffinate_mg_L=_mol_L_to_mg_L(li_raff_mol, "Li+"),
        na_raffinate_mg_L=_mol_L_to_mg_L(na_raff_mol, "Na+"),
        d_li=stage.li_distribution_ratio,
        d_na=d_na,
        selectivity=stage.li_na_selectivity,
        saltout_factor=stage.saltout_factor,
    )


def _compute_nominal(config) -> OneStageRow:
    return _solve_case(
        na_mg_L=NA_FEED_MG_L,
        oa_ratio=OA_RATIO,
        label=f"Na = {NA_FEED_MG_L:.0f} mg/L, O/A = {OA_RATIO:.2f}",
        sweep_type="nominal",
        config=config,
    )


def _compute_salt_rows(config) -> list[OneStageRow]:
    rows: list[OneStageRow] = []
    for na_mg_L in SALT_SWEEP_NA_MG_L:
        rows.append(
            _solve_case(
                na_mg_L=float(na_mg_L),
                oa_ratio=OA_RATIO,
                label=f"Na = {na_mg_L:.0f} mg/L",
                sweep_type="salt",
                config=config,
            )
        )
    return rows


def _compute_oa_rows(config) -> list[OneStageRow]:
    rows: list[OneStageRow] = []
    for oa_ratio in OA_SWEEP:
        rows.append(
            _solve_case(
                na_mg_L=NA_FEED_MG_L,
                oa_ratio=float(oa_ratio),
                label=f"O/A = {oa_ratio:.2f}",
                sweep_type="oa",
                config=config,
            )
        )
    return rows


def _write_case_csv(rows: list[OneStageRow], path: Path) -> Path:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "sweep_type",
                "condition_label",
                "na_mg_L",
                "oa_ratio",
                "li_extraction_pct",
                "na_extraction_pct",
                "li_org_mg_L_basis",
                "na_org_mg_L_basis",
                "li_raffinate_mg_L",
                "na_raffinate_mg_L",
                "d_li",
                "d_na",
                "selectivity",
                "saltout_factor",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.sweep_type,
                    row.condition_label,
                    row.na_mg_L,
                    row.oa_ratio,
                    row.li_extraction_pct,
                    row.na_extraction_pct,
                    row.li_org_mg_L_basis,
                    row.na_org_mg_L_basis,
                    row.li_raffinate_mg_L,
                    row.na_raffinate_mg_L,
                    row.d_li,
                    row.d_na,
                    row.selectivity,
                    row.saltout_factor,
                ]
            )
    return path


def _render_table_png(
    title: str,
    columns: list[str],
    rows: list[list[str]],
    out_path: Path,
    *,
    width: float = 13.33,
    row_height: float = 0.56,
    title_height: float = 1.1,
    font_size: int = 12,
) -> Path:
    fig_height = max(2.6, title_height + row_height * (len(rows) + 1))
    fig, ax = plt.subplots(figsize=(width, fig_height), dpi=180)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.text(0.0, 1.03, title, transform=ax.transAxes, ha="left", va="bottom", fontsize=20, fontweight="bold", color=TEXT)

    table = ax.table(cellText=rows, colLabels=columns, loc="upper left", cellLoc="center", bbox=[0.0, 0.02, 1.0, 0.90])
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


def _plot_species_split(nominal: OneStageRow, out_dir: Path) -> Path:
    path = out_dir / "gando_2025_one_stage_species_split.png"
    species = ["Li", "Na"]
    to_org = np.array([nominal.li_extraction_pct, nominal.na_extraction_pct], dtype=float)
    to_aq = 100.0 - to_org

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    ax.bar(species, to_aq, color=AQUEOUS_COLOR, width=0.60, label="Remaining in aqueous raffinate")
    ax.bar(species, to_org, bottom=to_aq, color=[LI_COLOR, NA_COLOR], width=0.60, label="Transferred to organic extract")
    ax.set_ylim(0.0, 100.0)
    ax.set_ylabel("One-stage split (%)", fontsize=13, fontweight="bold")
    ax.set_title("One-stage showcase: lithium moves, sodium stays behind", fontsize=22, fontweight="bold", pad=18)
    ax.legend(frameon=False, fontsize=12, loc="lower center")
    ax.text(0, 50.0, f"{to_org[0]:.2f}% to organic", ha="center", va="center", fontsize=12, fontweight="bold", color="white")
    ax.text(1, 8.0, f"{to_org[1]:.2f}% to organic", ha="center", va="center", fontsize=11, fontweight="bold", color=TEXT)
    ax.text(
        0.67,
        0.93,
        f"$D_{{Li}}$ = {nominal.d_li:.2f}\n$D_{{Na}}$ = {nominal.d_na:.4f}\n$S_{{Li/Na}}$ = {nominal.selectivity:.1f}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        color=TEXT,
        bbox=dict(facecolor="#fffdf8", edgecolor="#d7d1c3", boxstyle="round,pad=0.35"),
    )
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _plot_extraction_vs_salt(rows: list[OneStageRow], nominal: OneStageRow, out_dir: Path) -> Path:
    path = out_dir / "gando_2025_one_stage_extraction_vs_salt.png"
    x = np.array([row.na_mg_L for row in rows], dtype=float)
    li = np.array([row.li_extraction_pct for row in rows], dtype=float)
    na = np.array([row.na_extraction_pct for row in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    ax.plot(x, li, color=LI_COLOR, linewidth=3.0, marker="o", markersize=8, label="Li extraction")
    ax.plot(x, na, color=NA_COLOR, linewidth=2.6, marker="s", markersize=7, label="Na extraction")
    ax.axvline(nominal.na_mg_L, color=PAPER_COLOR, linestyle="--", linewidth=1.4, alpha=0.8)
    ax.set_xlabel("Na concentration in feed (mg/L)", fontsize=13, fontweight="bold")
    ax.set_ylabel("One-stage extraction (%)", fontsize=13, fontweight="bold")
    ax.set_ylim(0.0, 60.0)
    ax.set_title("Salt-rich feeds keep lithium extraction high while sodium remains low", fontsize=22, fontweight="bold", pad=18)
    ax.legend(frameon=False, fontsize=12, loc="lower right")
    ax.annotate("Nominal brine", xy=(nominal.na_mg_L, nominal.li_extraction_pct), xytext=(14000, 56.0), arrowprops=dict(arrowstyle="->", color=TEXT, linewidth=1.2), fontsize=11, color=TEXT, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _plot_distribution_vs_salt(rows: list[OneStageRow], nominal: OneStageRow, out_dir: Path) -> Path:
    path = out_dir / "gando_2025_one_stage_distribution_vs_salt.png"
    x = np.array([row.na_mg_L for row in rows], dtype=float)
    d_li = np.array([row.d_li for row in rows], dtype=float)
    d_na = np.array([row.d_na if np.isfinite(row.d_na) and row.d_na > 0.0 else np.nan for row in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    ax.set_yscale("log")
    ax.plot(x, d_li, color=RATIO_COLOR, linewidth=3.0, marker="o", markersize=8, label="$D_{Li}$")
    ax.plot(x, d_na, color=NA_COLOR, linewidth=2.4, marker="s", markersize=7, label="$D_{Na}$")
    ax.axvline(nominal.na_mg_L, color=PAPER_COLOR, linestyle="--", linewidth=1.4, alpha=0.8)
    ax.set_xlabel("Na concentration in feed (mg/L)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Distribution coefficient", fontsize=13, fontweight="bold")
    ax.set_title("Distribution coefficients separate sharply with salt concentration", fontsize=22, fontweight="bold", pad=18)
    ax.legend(frameon=False, fontsize=12, loc="upper left")
    ax.text(
        0.60,
        0.92,
        f"Nominal $D_{{Li}}$ = {nominal.d_li:.2f}\nNominal $D_{{Na}}$ = {nominal.d_na:.4f}\n$S_{{Li/Na}}$ = {nominal.selectivity:.1f}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        color=TEXT,
        bbox=dict(facecolor="#fffdf8", edgecolor="#d7d1c3", boxstyle="round,pad=0.35"),
    )
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _plot_extraction_vs_oa(rows: list[OneStageRow], nominal: OneStageRow, out_dir: Path) -> Path:
    path = out_dir / "gando_2025_one_stage_extraction_vs_oa.png"
    x = np.array([row.oa_ratio for row in rows], dtype=float)
    li = np.array([row.li_extraction_pct for row in rows], dtype=float)
    na = np.array([row.na_extraction_pct for row in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    ax.plot(x, li, color=LI_COLOR, linewidth=3.0, marker="o", markersize=8, label="Li extraction")
    ax.plot(x, na, color=NA_COLOR, linewidth=2.6, marker="s", markersize=7, label="Na extraction")
    ax.axvline(nominal.oa_ratio, color=PAPER_COLOR, linestyle="--", linewidth=1.4, alpha=0.8)
    ax.set_xlabel("Organic-to-aqueous ratio (O/A)", fontsize=13, fontweight="bold")
    ax.set_ylabel("One-stage extraction (%)", fontsize=13, fontweight="bold")
    ax.set_ylim(0.0, 100.0)
    ax.set_title("Higher O/A boosts lithium transfer much faster than sodium", fontsize=22, fontweight="bold", pad=18)
    ax.legend(frameon=False, fontsize=12, loc="lower right")
    ax.annotate("Nominal O/A", xy=(nominal.oa_ratio, nominal.li_extraction_pct), xytext=(1.55, 61.0), arrowprops=dict(arrowstyle="->", color=TEXT, linewidth=1.2), fontsize=11, color=TEXT, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _plot_distribution_vs_oa(rows: list[OneStageRow], nominal: OneStageRow, out_dir: Path) -> Path:
    path = out_dir / "gando_2025_one_stage_distribution_vs_oa.png"
    x = np.array([row.oa_ratio for row in rows], dtype=float)
    d_li = np.array([row.d_li for row in rows], dtype=float)
    d_na = np.array([row.d_na for row in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    fig.patch.set_facecolor(BG)
    _style_axes(ax)
    ax.set_yscale("log")
    ax.plot(x, d_li, color=RATIO_COLOR, linewidth=3.0, marker="o", markersize=8, label="$D_{Li}$")
    ax.plot(x, d_na, color=NA_COLOR, linewidth=2.4, marker="s", markersize=7, label="$D_{Na}$")
    ax.axvline(nominal.oa_ratio, color=PAPER_COLOR, linestyle="--", linewidth=1.4, alpha=0.8)
    ax.set_xlabel("Organic-to-aqueous ratio (O/A)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Distribution coefficient", fontsize=13, fontweight="bold")
    ax.set_title("Distribution coefficients widen further as O/A increases", fontsize=22, fontweight="bold", pad=18)
    ax.legend(frameon=False, fontsize=12, loc="upper left")
    ax.text(
        0.60,
        0.92,
        f"Nominal $D_{{Li}}$ = {nominal.d_li:.2f}\nNominal $D_{{Na}}$ = {nominal.d_na:.4f}\n$S_{{Li/Na}}$ = {nominal.selectivity:.1f}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        color=TEXT,
        bbox=dict(facecolor="#fffdf8", edgecolor="#d7d1c3", boxstyle="round,pad=0.35"),
    )
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _write_markdown(nominal: OneStageRow, png_paths: list[Path], csv_paths: list[Path], payload: dict, out_dir: Path) -> Path:
    path = out_dir / "gando_2025_one_stage_assets.md"
    params = payload["parameters"]
    lines: list[str] = []
    lines.append("# Gando 2025 One-Stage Showcase Assets")
    lines.append("")
    lines.append("## Basis")
    lines.append("")
    lines.append(f"- Config: `{DEFAULT_CONFIG_JSON}`")
    lines.append(f"- Feed basis: Li = {LI_FEED_MG_L:.3f} mg/L, Na = {NA_FEED_MG_L:.3f} mg/L, O/A = {OA_RATIO:.3f}, TOP = {TOP_MOL_L:.6f} mol/L.")
    lines.append(f"- Wrapper parameters: `log10(K_Li) = {params['log10_k_li']:.8f}`, `log10(K_Na) = {params['log10_k_na']:.8f}`, `log10(capacity factor) = {params['log10_capacity_factor']:.8f}`.")
    lines.append("")
    lines.append("## Headline Numbers")
    lines.append("")
    lines.append(f"- One-stage Li extraction = {nominal.li_extraction_pct:.4f}%.")
    lines.append(f"- One-stage Na extraction = {nominal.na_extraction_pct:.4f}%.")
    lines.append(f"- $D_{{Li}}$ = {nominal.d_li:.4f}, $D_{{Na}}$ = {nominal.d_na:.6f}, $S_{{Li/Na}}$ = {nominal.selectivity:.4f}.")
    lines.append(f"- Raffinate after one stage: Li = {nominal.li_raffinate_mg_L:.4f} mg/L, Na = {nominal.na_raffinate_mg_L:.4f} mg/L.")
    lines.append("")
    lines.append("## PNG Assets")
    lines.append("")
    for png in png_paths:
        lines.append(f"- `{png.name}`")
    lines.append("")
    lines.append("## CSV Tables")
    lines.append("")
    for csv_path in csv_paths:
        lines.append(f"- `{csv_path.name}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build_assets(out_dir: Path = OUT_DIR) -> dict[str, list[Path]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    config = load_selective_config(DEFAULT_CONFIG_JSON)
    payload = load_payload(DEFAULT_CONFIG_JSON)

    nominal = _compute_nominal(config)
    salt_rows = _compute_salt_rows(config)
    oa_rows = _compute_oa_rows(config)

    nominal_csv = _write_case_csv([nominal], out_dir / "gando_2025_one_stage_nominal.csv")
    salt_csv = _write_case_csv(salt_rows, out_dir / "gando_2025_one_stage_salt_sweep.csv")
    oa_csv = _write_case_csv(oa_rows, out_dir / "gando_2025_one_stage_oa_sweep.csv")

    anchor_rows = [
        salt_rows[0],
        salt_rows[2],
        salt_rows[6],
        salt_rows[-1],
        oa_rows[1],
        oa_rows[3],
        oa_rows[-1],
    ]
    anchor_csv = _write_case_csv(anchor_rows, out_dir / "gando_2025_one_stage_anchor_rows.csv")

    nominal_table_png = _render_table_png(
        "Gando 2025 one-stage nominal split",
        ["Metric", "Value"],
        [
            ["Li extraction (%)", f"{nominal.li_extraction_pct:.2f}"],
            ["Na extraction (%)", f"{nominal.na_extraction_pct:.2f}"],
            ["$D_{Li}$", f"{nominal.d_li:.2f}"],
            ["$D_{Na}$", f"{nominal.d_na:.4f}"],
            ["$S_{Li/Na}$", f"{nominal.selectivity:.1f}"],
            ["Li raffinate (mg/L)", f"{nominal.li_raffinate_mg_L:.2f}"],
            ["Na raffinate (mg/L)", f"{nominal.na_raffinate_mg_L:.2f}"],
            ["Salt-out factor", f"{nominal.saltout_factor:.2f}"],
        ],
        out_dir / "gando_2025_one_stage_nominal_table.png",
        width=11.0,
        font_size=13,
    )

    anchor_table_png = _render_table_png(
        "Gando 2025 one-stage sweep anchors",
        ["Case", "Na (mg/L)", "O/A", "Li ext (%)", "Na ext (%)", "$D_{Li}$", "$D_{Na}$", "$S_{Li/Na}$"],
        [
            [row.condition_label, f"{row.na_mg_L:.0f}", f"{row.oa_ratio:.2f}", f"{row.li_extraction_pct:.2f}", f"{row.na_extraction_pct:.2f}", f"{row.d_li:.2f}", ("nan" if not np.isfinite(row.d_na) else f"{row.d_na:.4f}"), f"{row.selectivity:.1f}"]
            for row in anchor_rows
        ],
        out_dir / "gando_2025_one_stage_anchor_table.png",
        width=14.5,
        font_size=11,
    )

    png_paths = [
        _plot_species_split(nominal, out_dir),
        _plot_extraction_vs_salt(salt_rows, nominal, out_dir),
        _plot_distribution_vs_salt(salt_rows, nominal, out_dir),
        _plot_extraction_vs_oa(oa_rows, nominal, out_dir),
        _plot_distribution_vs_oa(oa_rows, nominal, out_dir),
        nominal_table_png,
        anchor_table_png,
    ]
    csv_paths = [nominal_csv, salt_csv, oa_csv, anchor_csv]
    md_path = _write_markdown(nominal, png_paths, csv_paths, payload, out_dir)
    return {"pngs": png_paths, "csvs": csv_paths, "markdown": [md_path]}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one-stage slide-ready PNG and table assets for the Gando 2025 Li/Na split showcase.")
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




