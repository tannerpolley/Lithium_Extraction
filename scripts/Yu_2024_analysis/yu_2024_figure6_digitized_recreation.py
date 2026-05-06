from __future__ import annotations

import csv
from pathlib import Path

import matplotlib
import numpy as np
from scipy.interpolate import PchipInterpolator

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
EXP_CSV = ROOT / "figure6_digitized_points.csv"
CALC_CSV = ROOT / "figure6_digitized_calc_curve.csv"
OUT_DIR = ROOT / "output"
OUT_PNG = OUT_DIR / "yu_2024_figure6_digitized_recreation.png"
OUT_MD = OUT_DIR / "yu_2024_figure6_digitized_recreation.md"


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    exp_rows = _read_rows(EXP_CSV)
    calc_rows = _read_rows(CALC_CSV)
    x_exp = np.asarray([float(r["oa_ratio"]) for r in exp_rows], dtype=float)
    y_li_exp = np.asarray([float(r["e_li_exp_pct"]) for r in exp_rows], dtype=float)
    y_mg_exp = np.asarray([float(r["e_mg_exp_pct"]) for r in exp_rows], dtype=float)
    x_calc = np.asarray([float(r["oa_ratio"]) for r in calc_rows], dtype=float)
    y_li_calc = np.asarray([float(r["e_li_calc_pct"]) for r in calc_rows], dtype=float)
    y_mg_calc = np.asarray([float(r["e_mg_calc_pct"]) for r in calc_rows], dtype=float)
    x_dense = np.linspace(x_calc.min(), x_calc.max(), 200)
    li_spline = PchipInterpolator(x_calc, y_li_calc)
    mg_spline = PchipInterpolator(x_calc, y_mg_calc)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 5.2), dpi=180)
    ax.scatter(x_exp, y_li_exp, facecolors="white", edgecolors="red", s=52, linewidths=1.3, label=r"$E_{Li^+,exp.}$")
    ax.plot(x_dense, li_spline(x_dense), color="red", linewidth=1.3, label=r"$E_{Li^+,calc.}$")
    ax.scatter(x_exp, y_mg_exp, facecolors="white", edgecolors="cornflowerblue", marker="s", s=40, linewidths=1.2, label=r"$E_{Mg^{2+},exp.}$")
    ax.plot(x_dense, mg_spline(x_dense), color="cornflowerblue", linewidth=1.3, label=r"$E_{Mg^{2+},calc.}$")
    ax.set_xlim(0.8, 6.2)
    ax.set_ylim(-2.0, 100.0)
    ax.set_xticks(np.arange(1.0, 7.0, 1.0))
    ax.set_xlabel("O/A")
    ax.set_ylabel(r"$E_i$ (%)")
    ax.grid(alpha=0.15, linewidth=0.6)
    ax.legend(frameon=False, loc="center right")
    fig.tight_layout()
    fig.savefig(OUT_PNG, bbox_inches="tight")
    plt.close(fig)

    OUT_MD.write_text(
        "\n".join(
            [
                "# Yu 2024 Figure 6 Digitized Recreation",
                "",
                "- Experimental points were digitized from the local paper PDF.",
                "- Calculated lines were digitized from the local paper PDF and smoothed with monotone cubic interpolation.",
                "- This artifact is a visual recreation of the published figure.",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Saved: {OUT_PNG}")
    print(f"Saved: {OUT_MD}")


if __name__ == "__main__":
    main()