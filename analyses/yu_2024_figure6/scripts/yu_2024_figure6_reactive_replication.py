from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np
from scipy.optimize import least_squares

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = REPO_ROOT / "data" / "pcsaft_parameters" / "yu_2024"
ANALYSIS_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIGITIZED_CSV = ANALYSIS_ROOT / "data" / "input" / "figure6_digitized_points.csv"
DEFAULT_OUTPUT_DIR = ANALYSIS_ROOT / "results" / "figure6"
DEFAULT_OUT_CSV = DEFAULT_OUTPUT_DIR / "yu_2024_figure6_reactive_replication.csv"
DEFAULT_OUT_MD = DEFAULT_OUTPUT_DIR / "yu_2024_figure6_reactive_replication.md"
DEFAULT_OUT_PNG = DEFAULT_OUTPUT_DIR / "yu_2024_figure6_reactive_replication.png"
DEFAULT_CONFIG_JSON = DATASET_DIR / "reactive_eq11.json"

LI_G_PER_L = 0.766
MG_G_PER_L = 98.984
MW_LI_G_PER_MOL = 6.94
MW_MG_G_PER_MOL = 24.31
N_LI0_MOL_PER_L_AQ = LI_G_PER_L / MW_LI_G_PER_MOL
N_MG0_MOL_PER_L_AQ = MG_G_PER_L / MW_MG_G_PER_MOL
IL_CONC_MOL_PER_L_ORG = 0.09
TOP_CONC_MOL_PER_L_ORG = 1.90
# Paper reports 0.7135 g/L [HOEMIM]+ in the aqueous phase without metals present.
BASELINE_HOEMIM_CATION_AQ_MOL_PER_L = 0.005611


@dataclass
class ExperimentalPoint:
    oa_ratio: float
    e_li_exp_pct: float
    e_mg_exp_pct: float
    source: str


@dataclass
class ReactivePoint:
    oa_ratio: float
    e_li_exp_pct: float
    e_mg_exp_pct: float
    e_li_calc_pct: float
    e_mg_calc_pct: float
    xi_li_mol_per_l_aq: float
    xi_mg_mol_per_l_aq: float
    free_il_mol_per_l_org: float
    free_top_mol_per_l_org: float
    hoemim_aq_mol_per_l: float


@dataclass
class FitConfig:
    log10_k_li: float
    log10_k_mg: float
    il_conc_mol_per_l_org: float = IL_CONC_MOL_PER_L_ORG
    top_conc_mol_per_l_org: float = TOP_CONC_MOL_PER_L_ORG
    baseline_hoemim_cation_aq_mol_per_l: float = BASELINE_HOEMIM_CATION_AQ_MOL_PER_L


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV is missing a header row: {path}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"CSV has no rows: {path}")
    return rows


def _load_exp_points(path: Path) -> list[ExperimentalPoint]:
    rows = _read_csv_rows(path)
    points = [
        ExperimentalPoint(
            oa_ratio=float(row["oa_ratio"]),
            e_li_exp_pct=float(row["e_li_exp_pct"]),
            e_mg_exp_pct=float(row["e_mg_exp_pct"]),
            source=row.get("source", "").strip(),
        )
        for row in rows
    ]
    return sorted(points, key=lambda item: item.oa_ratio)


def _fit_to_fraction(y: float, upper: float) -> float:
    if upper <= 0.0:
        return 0.0
    return upper / (1.0 + np.exp(-float(y)))


def _solve_extents(oa_ratio: float, config: FitConfig) -> ReactivePoint:
    v_aq = 1.0
    v_org = float(oa_ratio)
    n_li0 = N_LI0_MOL_PER_L_AQ * v_aq
    n_mg0 = N_MG0_MOL_PER_L_AQ * v_aq
    n_il0 = config.il_conc_mol_per_l_org * v_org
    n_top0 = config.top_conc_mol_per_l_org * v_org
    k_li = 10.0 ** config.log10_k_li
    k_mg = 10.0 ** config.log10_k_mg

    upper_mg = min(n_mg0, 0.999 * n_il0)

    def residual(y: np.ndarray) -> np.ndarray:
        xi_li = _fit_to_fraction(y[0], n_li0)
        xi_mg = _fit_to_fraction(y[1], upper_mg)
        if xi_li + xi_mg >= 0.999 * min(n_il0, n_top0):
            return np.full(2, 1e3, dtype=float)

        n_li_aq = n_li0 - xi_li
        n_mg_aq = n_mg0 - xi_mg
        n_il_org = n_il0 - xi_li - xi_mg
        n_top_org = n_top0 - xi_li - xi_mg
        n_hoemim_aq = config.baseline_hoemim_cation_aq_mol_per_l * v_aq + xi_li + xi_mg

        if min(n_li_aq, n_mg_aq, n_il_org, n_top_org, n_hoemim_aq) <= 0.0:
            return np.full(2, 1e3, dtype=float)

        c_li_aq = n_li_aq / v_aq
        c_mg_aq = n_mg_aq / v_aq
        c_il_org = n_il_org / v_org
        c_top_org = n_top_org / v_org
        c_hoemim_aq = n_hoemim_aq / v_aq
        c_li_complex_org = xi_li / v_org
        c_mg_complex_org = xi_mg / v_org

        r_li = np.log10(c_hoemim_aq * c_li_complex_org / (c_il_org * c_li_aq * c_top_org)) - np.log10(k_li)
        r_mg = np.log10(c_hoemim_aq * c_mg_complex_org / (c_il_org * c_mg_aq * c_top_org)) - np.log10(k_mg)
        return np.asarray([r_li, r_mg], dtype=float)

    sol = least_squares(
        residual,
        x0=np.asarray([0.0, -8.0], dtype=float),
        bounds=(-20.0, 20.0),
        ftol=1e-12,
        xtol=1e-12,
        gtol=1e-12,
        max_nfev=300,
    )

    xi_li = _fit_to_fraction(sol.x[0], n_li0)
    xi_mg = _fit_to_fraction(sol.x[1], upper_mg)
    n_il_org = n_il0 - xi_li - xi_mg
    n_top_org = n_top0 - xi_li - xi_mg
    n_hoemim_aq = config.baseline_hoemim_cation_aq_mol_per_l * v_aq + xi_li + xi_mg

    return ReactivePoint(
        oa_ratio=float(oa_ratio),
        e_li_exp_pct=float("nan"),
        e_mg_exp_pct=float("nan"),
        e_li_calc_pct=100.0 * xi_li / n_li0,
        e_mg_calc_pct=100.0 * xi_mg / n_mg0,
        xi_li_mol_per_l_aq=xi_li / v_aq,
        xi_mg_mol_per_l_aq=xi_mg / v_aq,
        free_il_mol_per_l_org=n_il_org / v_org,
        free_top_mol_per_l_org=n_top_org / v_org,
        hoemim_aq_mol_per_l=n_hoemim_aq / v_aq,
    )


def _fit_config(points: list[ExperimentalPoint]) -> FitConfig:
    def objective(params: np.ndarray) -> np.ndarray:
        cfg = FitConfig(log10_k_li=float(params[0]), log10_k_mg=float(params[1]))
        residuals: list[float] = []
        for point in points:
            row = _solve_extents(point.oa_ratio, cfg)
            residuals.append((row.e_li_calc_pct - point.e_li_exp_pct) / 3.0)
            residuals.append((row.e_mg_calc_pct - point.e_mg_exp_pct) / 0.3)
        return np.asarray(residuals, dtype=float)

    sol = least_squares(
        objective,
        x0=np.asarray([0.2, -2.5], dtype=float),
        bounds=(np.asarray([-4.0, -10.0]), np.asarray([6.0, 2.0])),
        ftol=1e-12,
        xtol=1e-12,
        gtol=1e-12,
        max_nfev=200,
    )
    return FitConfig(log10_k_li=float(sol.x[0]), log10_k_mg=float(sol.x[1]))


def _write_config(path: Path, config: FitConfig, points: list[ExperimentalPoint]) -> None:
    payload: dict[str, Any] = {
        "model": "eq11_reactive_wrapper",
        "fit_timestamp_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "basis": {
            "paper_equation": "Eq. 11",
            "paper_mechanism": "1 IL + 1 TOP + 1 Li <-> 1 aqueous [HOEMIM]+ + 1 organic Li complex",
            "current_user_options": "2025 preset retained in yu_2024 dataset; reaction handled in a wrapper outside the core pcsaft flash",
            "digitized_points_csv": str(DEFAULT_DIGITIZED_CSV),
        },
        "constants": {
            "li_feed_mol_per_l_aq": N_LI0_MOL_PER_L_AQ,
            "mg_feed_mol_per_l_aq": N_MG0_MOL_PER_L_AQ,
            "il_conc_mol_per_l_org": config.il_conc_mol_per_l_org,
            "top_conc_mol_per_l_org": config.top_conc_mol_per_l_org,
            "baseline_hoemim_cation_aq_mol_per_l": config.baseline_hoemim_cation_aq_mol_per_l,
        },
        "fit_parameters": {
            "log10_k_li": config.log10_k_li,
            "log10_k_mg": config.log10_k_mg,
        },
        "fit_points": [
            {
                "oa_ratio": point.oa_ratio,
                "e_li_exp_pct": point.e_li_exp_pct,
                "e_mg_exp_pct": point.e_mg_exp_pct,
            }
            for point in points
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_csv(path: Path, point_rows: list[ReactivePoint], dense_rows: list[ReactivePoint], config: FitConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "section",
        "oa_ratio",
        "e_li_exp_pct",
        "e_mg_exp_pct",
        "e_li_calc_pct",
        "e_mg_calc_pct",
        "xi_li_mol_per_l_aq",
        "xi_mg_mol_per_l_aq",
        "free_il_mol_per_l_org",
        "free_top_mol_per_l_org",
        "hoemim_aq_mol_per_l",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in point_rows:
            writer.writerow(
                {
                    "section": "digitized_point",
                    "oa_ratio": row.oa_ratio,
                    "e_li_exp_pct": row.e_li_exp_pct,
                    "e_mg_exp_pct": row.e_mg_exp_pct,
                    "e_li_calc_pct": row.e_li_calc_pct,
                    "e_mg_calc_pct": row.e_mg_calc_pct,
                    "xi_li_mol_per_l_aq": row.xi_li_mol_per_l_aq,
                    "xi_mg_mol_per_l_aq": row.xi_mg_mol_per_l_aq,
                    "free_il_mol_per_l_org": row.free_il_mol_per_l_org,
                    "free_top_mol_per_l_org": row.free_top_mol_per_l_org,
                    "hoemim_aq_mol_per_l": row.hoemim_aq_mol_per_l,
                }
            )
        for row in dense_rows:
            writer.writerow(
                {
                    "section": "dense_curve",
                    "oa_ratio": row.oa_ratio,
                    "e_li_exp_pct": "",
                    "e_mg_exp_pct": "",
                    "e_li_calc_pct": row.e_li_calc_pct,
                    "e_mg_calc_pct": row.e_mg_calc_pct,
                    "xi_li_mol_per_l_aq": row.xi_li_mol_per_l_aq,
                    "xi_mg_mol_per_l_aq": row.xi_mg_mol_per_l_aq,
                    "free_il_mol_per_l_org": row.free_il_mol_per_l_org,
                    "free_top_mol_per_l_org": row.free_top_mol_per_l_org,
                    "hoemim_aq_mol_per_l": row.hoemim_aq_mol_per_l,
                }
            )
        writer.writerow(
            {
                "section": "fit_parameters",
                "oa_ratio": "",
                "e_li_calc_pct": config.log10_k_li,
                "e_mg_calc_pct": config.log10_k_mg,
                "xi_li_mol_per_l_aq": config.il_conc_mol_per_l_org,
                "xi_mg_mol_per_l_aq": config.top_conc_mol_per_l_org,
                "free_il_mol_per_l_org": config.baseline_hoemim_cation_aq_mol_per_l,
            }
        )


def _write_markdown(path: Path, point_rows: list[ReactivePoint], config: FitConfig, args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Yu 2024 Figure 6 Reactive Replication")
    lines.append("")
    lines.append("## Basis")
    lines.append("")
    lines.append(f"- Dataset directory: {DATASET_DIR}")
    lines.append(f"- Digitized experimental points: {args.exp_csv}")
    lines.append(f"- Reactive wrapper config: {args.config_json}")
    lines.append("- Paper mechanism used in the wrapper: Eq. 11 with 1:1:1 Li exchange stoichiometry and a separate low-affinity Mg exchange branch.")
    lines.append("- The current 2025 yu_2024 electrolyte preset is retained as the dataset basis; the reaction is represented outside the core pcsaft flash because the direct six-species flash collapsed to a trivial split under the current build.")
    lines.append("")
    lines.append("## Fitted Parameters")
    lines.append("")
    lines.append(f"- `log10(K_Li) = {config.log10_k_li:.6f}`")
    lines.append(f"- `log10(K_Mg) = {config.log10_k_mg:.6f}`")
    lines.append(f"- `C_IL,org = {config.il_conc_mol_per_l_org:.6f} mol/L`")
    lines.append(f"- `C_TOP,org = {config.top_conc_mol_per_l_org:.6f} mol/L`")
    lines.append(f"- `C_[HOEMIM+]_aq,baseline = {config.baseline_hoemim_cation_aq_mol_per_l:.6f} mol/L`")
    lines.append("")
    lines.append("## Pointwise Comparison")
    lines.append("")
    lines.append("| O/A | $E_{Li+,exp}$ (%) | $E_{Li+,calc}$ (%) | $E_{Mg2+,exp}$ (%) | $E_{Mg2+,calc}$ (%) |")
    lines.append("|---:|---:|---:|---:|---:|")
    for row in point_rows:
        lines.append(
            f"| {row.oa_ratio:.3g} | {row.e_li_exp_pct:.4g} | {row.e_li_calc_pct:.4g} | {row.e_mg_exp_pct:.4g} | {row.e_mg_calc_pct:.4g} |"
        )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- This wrapper intentionally follows the paper’s extraction stoichiometry rather than introducing pseudo-species into the pcsaft core dataset.")
    lines.append("- The remaining mismatch at `O/A = 1` is directionally consistent with the paper’s own statement that the model overestimates that low-O/A point.")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_plot(path: Path, point_rows: list[ReactivePoint], dense_rows: list[ReactivePoint]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 5.2), dpi=180)

    x_points = np.asarray([row.oa_ratio for row in point_rows], dtype=float)
    li_exp = np.asarray([row.e_li_exp_pct for row in point_rows], dtype=float)
    mg_exp = np.asarray([row.e_mg_exp_pct for row in point_rows], dtype=float)
    x_dense = np.asarray([row.oa_ratio for row in dense_rows], dtype=float)
    li_calc = np.asarray([row.e_li_calc_pct for row in dense_rows], dtype=float)
    mg_calc = np.asarray([row.e_mg_calc_pct for row in dense_rows], dtype=float)

    ax.scatter(x_points, li_exp, facecolors="white", edgecolors="red", s=52, linewidths=1.3, label=r"$E_{Li^+,exp.}$")
    ax.plot(x_dense, li_calc, color="red", linewidth=1.3, label=r"$E_{Li^+,calc.}$")
    ax.scatter(x_points, mg_exp, facecolors="white", edgecolors="cornflowerblue", marker="s", s=40, linewidths=1.2, label=r"$E_{Mg^{2+},exp.}$")
    ax.plot(x_dense, mg_calc, color="cornflowerblue", linewidth=1.3, label=r"$E_{Mg^{2+},calc.}$")

    ax.set_xlim(0.8, 6.2)
    ax.set_ylim(-2.0, 100.0)
    ax.set_xticks(np.arange(1.0, 7.0, 1.0))
    ax.set_xlabel("O/A")
    ax.set_ylabel(r"$E_i$ (%)")
    ax.grid(alpha=0.15, linewidth=0.6)
    ax.legend(frameon=False, loc="center right")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def run(args: argparse.Namespace) -> tuple[Path, Path, Path, Path]:
    points = _load_exp_points(Path(args.exp_csv))
    config = _fit_config(points)
    _write_config(Path(args.config_json), config, points)

    point_rows: list[ReactivePoint] = []
    for point in points:
        row = _solve_extents(point.oa_ratio, config)
        row.e_li_exp_pct = point.e_li_exp_pct
        row.e_mg_exp_pct = point.e_mg_exp_pct
        point_rows.append(row)

    dense_grid = np.linspace(min(point.oa_ratio for point in points), max(point.oa_ratio for point in points), 251)
    dense_rows = [_solve_extents(float(oa), config) for oa in dense_grid]

    _write_csv(Path(args.out_csv), point_rows, dense_rows, config)
    _write_markdown(Path(args.out_md), point_rows, config, args)
    _write_plot(Path(args.out_png), point_rows, dense_rows)

    print(f"Saved config: {args.config_json}")
    print(f"Saved CSV: {args.out_csv}")
    print(f"Saved Markdown: {args.out_md}")
    print(f"Saved Plot: {args.out_png}")
    return Path(args.config_json), Path(args.out_csv), Path(args.out_md), Path(args.out_png)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reactive Eq. 11 replication of Yu 2024 Figure 6.")
    parser.add_argument("--exp-csv", default=str(DEFAULT_DIGITIZED_CSV))
    parser.add_argument("--config-json", default=str(DEFAULT_CONFIG_JSON))
    parser.add_argument("--out-csv", default=str(DEFAULT_OUT_CSV))
    parser.add_argument("--out-md", default=str(DEFAULT_OUT_MD))
    parser.add_argument("--out-png", default=str(DEFAULT_OUT_PNG))
    return parser.parse_args()


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()



