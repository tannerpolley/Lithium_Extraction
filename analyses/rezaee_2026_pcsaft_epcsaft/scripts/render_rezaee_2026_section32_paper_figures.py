from __future__ import annotations

import json
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

DIGITIZED_POINTS_CSV = PROCESSED_DIR / "rezaee_2026_paper_figure_digitized_points.csv"
SUMMARY_JSON = RESULTS_DIR / "rezaee_2026_section32_paper_figures_summary.json"
REPORT_MD = RESULTS_DIR / "rezaee_2026_section32_paper_figures.md"

FIGURE_SPECS: list[dict[str, Any]] = [
    {
        "figure_id": "fig7",
        "paper_label": "Fig. 7",
        "caption": "Deviation of calculated extraction percentage from experimental data [17].",
        "x_label": "Experimental data",
        "y_label": "Calculated values",
        "axis_max": 60.0,
    },
    {
        "figure_id": "fig8",
        "paper_label": "Fig. 8",
        "caption": "Deviation of calculated selectivity from experimental data [17].",
        "x_label": "Experimental data",
        "y_label": "Calculated values",
        "axis_max": 6.0,
    },
    {
        "figure_id": "fig10",
        "paper_label": "Fig. 10",
        "caption": "Deviation of calculated lithium extraction percentage from experimental data [17] using $k_{ij}$.",
        "x_label": "Experimental data",
        "y_label": "Calculated values",
        "axis_max": 60.0,
    },
    {
        "figure_id": "fig11",
        "paper_label": "Fig. 11",
        "caption": "Deviation of calculated selectivity from experimental data [17] using $k_{ij}$.",
        "x_label": "Experimental data",
        "y_label": "Calculated values",
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


def _normalize_svg_whitespace(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")


def _render_figure(rows: pd.DataFrame, spec: dict[str, Any]) -> dict[str, Any]:
    x = rows["x"].to_numpy(dtype=float)
    y = rows["y"].to_numpy(dtype=float)
    aard = float((100.0 * np.abs(y - x) / np.clip(x, 1.0e-300, None)).mean())
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

    png_path = FIGURES_DIR / f"{spec['figure_id']}.png"
    svg_path = FIGURES_DIR / f"{spec['figure_id']}.svg"
    fig.savefig(png_path, dpi=220)
    fig.savefig(svg_path)
    _normalize_svg_whitespace(svg_path)
    plt.close(fig)

    return {
        "figure_id": str(spec["figure_id"]),
        "paper_label": str(spec["paper_label"]),
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
        "This renderer reproduces the published scatter-plot form of Rezaee 2026 Figures 7, 8, 10, and 11 from a digitized figure-point table.",
        "",
        "Input table and source note:",
        "",
        f"- `{DIGITIZED_POINTS_CSV.relative_to(ANALYSIS_DIR)}`",
        "",
        "The figure points are digitized from the published paper panels rather than taken from the known-bad direct Section 3.2 replication rows.",
        "",
        "## Figures",
        "",
    ]
    for entry in summary["figures"]:
        lines.extend(
            [
                f"- `{entry['paper_label']}` uses `{entry['row_count']}` digitized points and AARD `{entry['aard_pct']}`%.",
                f"  PNG: `{Path(entry['png']).relative_to(ANALYSIS_DIR)}`",
                f"  SVG: `{Path(entry['svg']).relative_to(ANALYSIS_DIR)}`",
            ]
        )
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows = pd.read_csv(DIGITIZED_POINTS_CSV)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    figure_entries: list[dict[str, Any]] = []
    for spec in FIGURE_SPECS:
        subset = rows.loc[rows["figure_id"] == spec["figure_id"]].copy()
        if subset.empty:
            raise ValueError(f"No rows found for figure_id={spec['figure_id']!r} in {DIGITIZED_POINTS_CSV}")
        figure_entries.append(_render_figure(subset, spec))

    summary = {
        "status": "section32_paper_figures_rendered_from_digitized_points",
        "source_rows": str(DIGITIZED_POINTS_CSV.relative_to(ANALYSIS_DIR)),
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
