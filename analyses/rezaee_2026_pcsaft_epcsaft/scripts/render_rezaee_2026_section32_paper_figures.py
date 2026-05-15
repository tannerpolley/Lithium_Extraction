from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use("Agg")

ANALYSIS_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ANALYSIS_DIR / "data" / "processed"
RESULTS_DIR = ANALYSIS_DIR / "results" / "reaction_equilibrium"
FIGURES_DIR = RESULTS_DIR / "figures" / "rezaee_2026_section32_paper_figures"

ROWS_CSV = PROCESSED_DIR / "rezaee_2026_section32_equilibrium_replication_rows.csv"
SUMMARY_JSON = RESULTS_DIR / "rezaee_2026_section32_paper_figures_summary.json"
REPORT_MD = RESULTS_DIR / "rezaee_2026_section32_paper_figures.md"

FIGURE_SPECS: list[dict[str, Any]] = [
    {
        "figure_id": "fig7",
        "paper_label": "Fig. 7",
        "case_id": "held_2014_s2_no_born_no_kij_pH_stoich",
        "x_col": "Li_extraction_pct_exp",
        "y_col": "Li_extraction_pct_calc",
        "aard_col": "Li_extraction_AARD_contribution_pct",
        "x_label": "Experimental data",
        "y_label": "Calculated values",
        "caption": "Deviation of calculated extraction percentage from experimental data [17].",
        "axis_max": 60.0,
    },
    {
        "figure_id": "fig8",
        "paper_label": "Fig. 8",
        "case_id": "held_2014_s2_no_born_no_kij_pH_stoich",
        "x_col": "selectivity_exp",
        "y_col": "selectivity_calc",
        "aard_col": "selectivity_AARD_contribution_pct",
        "x_label": "Experimental data",
        "y_label": "Calculated values",
        "caption": "Deviation of calculated selectivity from experimental data [17].",
        "axis_max": 6.0,
    },
    {
        "figure_id": "fig10",
        "paper_label": "Fig. 10",
        "case_id": "held_2014_s2_no_born_table9_kij_pH_stoich",
        "x_col": "Li_extraction_pct_exp",
        "y_col": "Li_extraction_pct_calc",
        "aard_col": "Li_extraction_AARD_contribution_pct",
        "x_label": "Experimental data",
        "y_label": "Calculated values",
        "caption": "Deviation of calculated lithium extraction percentage from experimental data [17] using $k_{ij}$.",
        "axis_max": 60.0,
    },
    {
        "figure_id": "fig11",
        "paper_label": "Fig. 11",
        "case_id": "held_2014_s2_no_born_table9_kij_pH_stoich",
        "x_col": "selectivity_exp",
        "y_col": "selectivity_calc",
        "aard_col": "selectivity_AARD_contribution_pct",
        "x_label": "Experimental data",
        "y_label": "Calculated values",
        "caption": "Deviation of calculated selectivity from experimental data [17] using $k_{ij}$.",
        "axis_max": 6.0,
    },
]


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


def _configure_axes(ax: plt.Axes, axis_max: float, x_label: str, y_label: str) -> None:
    ax.set_xlim(-0.05 * axis_max, 1.05 * axis_max)
    ax.set_ylim(-0.05 * axis_max, 1.05 * axis_max)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.spines["top"].set_linewidth(1.1)
    ax.spines["right"].set_linewidth(1.1)
    ax.spines["left"].set_linewidth(1.1)
    ax.spines["bottom"].set_linewidth(1.1)
    ax.tick_params(direction="out", length=5, width=1.0)


def _render_figure(rows: pd.DataFrame, spec: dict[str, Any]) -> dict[str, Any]:
    x = rows[spec["x_col"]].to_numpy(dtype=float)
    y = rows[spec["y_col"]].to_numpy(dtype=float)
    aard = float(rows[spec["aard_col"]].mean())
    axis_max = float(spec["axis_max"])

    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 14,
            "axes.labelsize": 16,
            "xtick.labelsize": 13,
            "ytick.labelsize": 13,
        }
    )
    fig, ax = plt.subplots(figsize=(8.6, 6.4), constrained_layout=True)
    ax.scatter(x, y, s=110, color="black", edgecolors="none", zorder=3)
    ax.plot([0.0, axis_max], [0.0, axis_max], color="red", linewidth=2.2, zorder=2)
    _configure_axes(ax, axis_max, str(spec["x_label"]), str(spec["y_label"]))
    ax.set_title(f"{spec['paper_label']} Replication", fontsize=15)

    png_path = FIGURES_DIR / f"{spec['figure_id']}.png"
    svg_path = FIGURES_DIR / f"{spec['figure_id']}.svg"
    fig.savefig(png_path, dpi=220)
    fig.savefig(svg_path)
    plt.close(fig)

    return {
        "figure_id": str(spec["figure_id"]),
        "paper_label": str(spec["paper_label"]),
        "case_id": str(spec["case_id"]),
        "row_count": int(len(rows)),
        "aard_pct": aard,
        "png": str(png_path),
        "svg": str(svg_path),
        "caption": str(spec["caption"]),
    }


def _write_report(summary: dict[str, Any]) -> None:
    lines = [
        "# Rezaee 2026 Section 3.2 Paper Figure Replications",
        "",
        "## Scope",
        "",
        "This renderer reproduces the published scatter-plot form of Rezaee 2026 Figures 7, 8, 10, and 11 from the existing processed Section 3.2 comparison table.",
        "",
        "Input table:",
        "",
        f"- `{ROWS_CSV.relative_to(ANALYSIS_DIR)}`",
        "",
        "The figure points are taken directly from the stored comparison rows in `rezaee_2026_section32_equilibrium_replication_rows.csv`.",
        "",
        "## Figures",
        "",
    ]
    for entry in summary["figures"]:
        lines.extend(
            [
                f"- `{entry['paper_label']}` uses case `{entry['case_id']}` with `{entry['row_count']}` rows and AARD `{entry['aard_pct']}`%.",
                f"  PNG: `{Path(entry['png']).relative_to(ANALYSIS_DIR)}`",
                f"  SVG: `{Path(entry['svg']).relative_to(ANALYSIS_DIR)}`",
            ]
        )
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows = pd.read_csv(ROWS_CSV)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    figure_entries: list[dict[str, Any]] = []
    for spec in FIGURE_SPECS:
        subset = rows.loc[rows["case_id"] == spec["case_id"]].copy()
        if subset.empty:
            raise ValueError(f"No rows found for case_id={spec['case_id']!r} in {ROWS_CSV}")
        figure_entries.append(_render_figure(subset, spec))

    summary = {
        "status": "section32_paper_figures_rendered",
        "source_rows": str(ROWS_CSV.relative_to(ANALYSIS_DIR)),
        "figure_count": len(figure_entries),
        "figures": figure_entries,
    }
    SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_JSON.write_text(json.dumps(_jsonable(summary), indent=2) + "\n", encoding="utf-8")
    _write_report(summary)
    print(json.dumps(_jsonable(summary), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
