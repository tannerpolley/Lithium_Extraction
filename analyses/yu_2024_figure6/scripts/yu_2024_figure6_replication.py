from __future__ import annotations

import argparse
import copy
import csv
import importlib.util
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np


matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.epcsaft_compat as pcs

DATASET_DIR = REPO_ROOT / "data" / "pcsaft_parameters" / "yu_2024"
ANALYSIS_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIGITIZED_CSV = ANALYSIS_ROOT / "data" / "input" / "figure6_digitized_points.csv"
DEFAULT_OUTPUT_DIR = ANALYSIS_ROOT / "results" / "figure6"
DEFAULT_OUT_CSV = DEFAULT_OUTPUT_DIR / "yu_2024_figure6_replication.csv"
DEFAULT_OUT_MD = DEFAULT_OUTPUT_DIR / "yu_2024_figure6_replication.md"
DEFAULT_OUT_PNG = DEFAULT_OUTPUT_DIR / "yu_2024_figure6_replication.png"

SPECIES = ["H2O", "TOP", "[HOEMIM][Tf2N]", "Li+", "Mg2+", "Cl-"]
IDX = {name: i for i, name in enumerate(SPECIES)}
BASE_KEYS = ["MW", "m", "s", "e", "e_assoc", "vol_a", "assoc_scheme", "dipm", "dip_num", "z", "dielc"]
OPTIONAL_KEYS = ["d_born", "f_solv"]

AQ_VOLUME_L = 1.0
AQ_DENSITY_KG_PER_L = 1.0
LI_G_PER_L = 0.766
MG_G_PER_L = 98.984
IL_CONC_MOL_PER_L_ORG = 0.09
FIT_OA_RATIO = 2.0
TOP_CONC_MOL_PER_L_ORG = 1.90


@dataclass
class ExperimentalPoint:
    oa_ratio: float
    e_li_exp_pct: float
    e_mg_exp_pct: float
    source: str


@dataclass
class SolvePoint:
    oa_ratio: float
    e_li_exp_pct: float
    e_mg_exp_pct: float
    e_li_calc_pct: float
    e_mg_calc_pct: float
    converged: bool
    status: Any
    message: str
    residual_norm: float
    tpdf_min: float
    beta_org: float
    beta_aq: float
    x_li_org: float
    x_mg_org: float


def _must_exist(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    _must_exist(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV is missing a header row: {path}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"CSV has no rows: {path}")
    return rows


def _sigma_water(temp_k: float) -> float:
    return 2.7927 + (10.11 * math.exp(-0.01775 * temp_k) - 1.417 * math.exp(-0.01146 * temp_k))


def _parse_scalar(raw: str, field: str, component: str) -> Any:
    text = (raw or "").strip()
    if field == "assoc_scheme":
        return None if text == "" else text
    if field == "s" and component == "H2O":
        canonical = "sigma=2.7927+(10.11*exp(-0.01775*T)-1.417*exp(-0.01146*T))"
        if text.replace(" ", "") == canonical:
            return _sigma_water
    if text == "":
        raise ValueError(f"Missing value for {component}.{field}")
    value = float(text)
    if not math.isfinite(value):
        raise ValueError(f"Non-finite value for {component}.{field}: {text}")
    return value


def _load_dataset(dataset_dir: Path) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], float], dict[tuple[str, str], float], dict[tuple[str, str], float], dict[str, Any]]:
    pure_rows = _read_csv_rows(dataset_dir / "pure.csv")
    by_component = {row["component"].strip(): row for row in pure_rows}
    missing = [comp for comp in SPECIES if comp not in by_component]
    if missing:
        raise ValueError(f"pure.csv missing components: {missing}")

    user_params: dict[str, dict[str, Any]] = {}
    for comp in SPECIES:
        row = by_component[comp]
        entry: dict[str, Any] = {}
        for key in BASE_KEYS + OPTIONAL_KEYS:
            entry[key] = _parse_scalar(row.get(key, ""), key, comp)
        user_params[comp] = entry

    def _load_matrix(name: str) -> dict[tuple[str, str], float]:
        rows = _read_csv_rows(dataset_dir / "binary_interaction" / name)
        cols = [c for c in rows[0] if c != "component"]
        if cols != SPECIES:
            raise ValueError(f"{name} columns do not match {SPECIES}: {cols}")
        out: dict[tuple[str, str], float] = {}
        for row in rows:
            row_comp = row["component"].strip()
            for col in cols:
                text = (row.get(col, "") or "0").strip()
                out[(row_comp, col)] = float(text)
        return out

    options_payload = json.loads((dataset_dir / "user_options.json").read_text(encoding="utf-8"))
    user_options = options_payload.get("canonical_user_options", options_payload)
    if not isinstance(user_options, dict):
        raise ValueError("user_options.json must contain an object")

    return (
        user_params,
        _load_matrix("k_ij.csv"),
        _load_matrix("k_hb_ij.csv"),
        _load_matrix("l_ij.csv"),
        user_options,
    )


def _load_pcsaft_runtime_module():
    module_path = REPO_ROOT / "data" / "epcsaft_properties.py"
    _must_exist(module_path)
    spec = importlib.util.spec_from_file_location("pcsaft_dataset_runtime", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module spec from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_params(
    species: list[str],
    temp_k: float,
    user_params: dict[str, dict[str, Any]],
    matrices: dict[str, dict[tuple[str, str], float]],
    user_options: dict[str, Any],
    runtime_mod: Any,
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for key in BASE_KEYS:
        values = []
        for comp in species:
            value = user_params[comp][key]
            values.append(float(value(temp_k)) if callable(value) else value)
        params[key] = list(values) if key == "assoc_scheme" else np.asarray(values, dtype=float)

    for key in OPTIONAL_KEYS:
        values = []
        for comp in species:
            value = user_params[comp][key]
            values.append(float(value(temp_k)) if callable(value) else value)
        params[key] = np.asarray(values, dtype=float)

    for matrix_name, matrix_data in matrices.items():
        arr = np.zeros((len(species), len(species)), dtype=float)
        for i, a in enumerate(species):
            for j, b in enumerate(species):
                arr[i, j] = float(matrix_data.get((a, b), 0.0))
        params[matrix_name] = arr

    runtime_payload = runtime_mod._resolve_runtime_options(copy.deepcopy(user_options))
    params["elec_model"] = copy.deepcopy(runtime_payload["model"])
    params["elec_model_preset"] = runtime_payload.get("preset_key", "dataset_canonical")
    params["z"] = np.asarray(params["z"], dtype=float)
    return params


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


def _build_feed_moles(oa_ratio: float, top_conc_mol_per_l_org: float, mw: dict[str, float]) -> np.ndarray:
    n_li = (LI_G_PER_L * AQ_VOLUME_L * 1e-3) / mw["Li+"]
    n_mg = (MG_G_PER_L * AQ_VOLUME_L * 1e-3) / mw["Mg2+"]
    n_cl = n_li + 2.0 * n_mg

    m_li = n_li * mw["Li+"]
    m_mg = n_mg * mw["Mg2+"]
    m_cl = n_cl * mw["Cl-"]
    m_water = AQ_DENSITY_KG_PER_L * AQ_VOLUME_L - m_li - m_mg - m_cl
    if m_water <= 0.0:
        raise ValueError("Computed non-positive water mass. Adjust the aqueous basis assumption.")

    v_org = oa_ratio * AQ_VOLUME_L
    n_top = top_conc_mol_per_l_org * v_org
    n_il = IL_CONC_MOL_PER_L_ORG * v_org

    feed = np.zeros(len(SPECIES), dtype=float)
    feed[IDX["H2O"]] = m_water / mw["H2O"]
    feed[IDX["TOP"]] = n_top
    feed[IDX["[HOEMIM][Tf2N]"]] = n_il
    feed[IDX["Li+"]] = n_li
    feed[IDX["Mg2+"]] = n_mg
    feed[IDX["Cl-"]] = n_cl
    return feed


def _organic_marker(x: np.ndarray, mw: dict[str, float]) -> float:
    masses = np.asarray([x[IDX[name]] * mw[name] for name in SPECIES], dtype=float)
    total = float(np.sum(masses))
    if total <= 0.0:
        return float("nan")
    return float((masses[IDX["TOP"]] + masses[IDX["[HOEMIM][Tf2N]"]]) / total)


def _solver_profiles() -> list[dict[str, Any]]:
    return [
        {
            "tpdf_global_trials": 80,
            "tpdf_local_trials": 40,
            "solver_tol": 1e-8,
            "max_nfev": 100,
            "split_tol": 1e-4,
            "debug": False,
        },
        {
            "tpdf_global_trials": 200,
            "tpdf_local_trials": 100,
            "solver_tol": 1e-9,
            "max_nfev": 200,
            "charge_weight": 5000.0,
            "solver_accept_norm": 0.5,
            "split_tol": 1e-4,
            "debug": False,
        },
    ]


def _solve_point(
    oa_ratio: float,
    e_li_exp_pct: float,
    e_mg_exp_pct: float,
    top_conc_mol_per_l_org: float,
    temp_k: float,
    pressure_pa: float,
    user_params: dict[str, dict[str, Any]],
    matrices: dict[str, dict[tuple[str, str], float]],
    user_options: dict[str, Any],
    runtime_mod: Any,
) -> SolvePoint:
    mw = {comp: float(user_params[comp]["MW"]) for comp in SPECIES}
    n_feed = _build_feed_moles(oa_ratio, top_conc_mol_per_l_org, mw)
    z_feed = n_feed / float(np.sum(n_feed))
    params = _build_params(SPECIES, temp_k, user_params, matrices, user_options, runtime_mod)

    last: dict[str, Any] | None = None
    for options in _solver_profiles():
        result = pcs.pcsaft_multiphase_lle(temp_k, pressure_pa, z_feed, params, SPECIES, options=options)
        last = result
        if bool(result.get("converged", False)) and int(result.get("n_phases", 0)) == 2:
            break

    if last is None:
        return SolvePoint(oa_ratio, e_li_exp_pct, e_mg_exp_pct, float("nan"), float("nan"), False, None, "No solver result", float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"))

    if int(last.get("n_phases", 0)) != 2:
        return SolvePoint(
            oa_ratio,
            e_li_exp_pct,
            e_mg_exp_pct,
            float("nan"),
            float("nan"),
            bool(last.get("converged", False)),
            last.get("status"),
            str(last.get("message", "No two-phase split")),
            float(last.get("residual_norm", float("nan"))),
            float(last.get("tpdf_min", float("nan"))),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
        )

    p0, p1 = last["phases"][0], last["phases"][1]
    x0 = np.asarray(p0["x"], dtype=float)
    x1 = np.asarray(p1["x"], dtype=float)
    org, aq = (p0, p1) if _organic_marker(x0, mw) >= _organic_marker(x1, mw) else (p1, p0)

    n_tot = float(np.sum(n_feed))
    beta_org = float(org["beta"])
    beta_aq = float(aq["beta"])
    n_li_org = beta_org * float(org["x"][IDX["Li+"]]) * n_tot
    n_mg_org = beta_org * float(org["x"][IDX["Mg2+"]]) * n_tot
    e_li_calc_pct = 100.0 * n_li_org / max(float(n_feed[IDX["Li+"]]), 1e-300)
    e_mg_calc_pct = 100.0 * n_mg_org / max(float(n_feed[IDX["Mg2+"]]), 1e-300)

    return SolvePoint(
        oa_ratio=oa_ratio,
        e_li_exp_pct=e_li_exp_pct,
        e_mg_exp_pct=e_mg_exp_pct,
        e_li_calc_pct=e_li_calc_pct,
        e_mg_calc_pct=e_mg_calc_pct,
        converged=bool(last.get("converged", False)),
        status=last.get("status"),
        message=str(last.get("message", "")),
        residual_norm=float(last.get("residual_norm", float("nan"))),
        tpdf_min=float(last.get("tpdf_min", float("nan"))),
        beta_org=beta_org,
        beta_aq=beta_aq,
        x_li_org=float(org["x"][IDX["Li+"]]),
        x_mg_org=float(org["x"][IDX["Mg2+"]]),
    )


def _fit_top_concentration(
    fit_target_pct: float,
    temp_k: float,
    pressure_pa: float,
    user_params: dict[str, dict[str, Any]],
    matrices: dict[str, dict[tuple[str, str], float]],
    user_options: dict[str, Any],
    runtime_mod: Any,
) -> tuple[float, SolvePoint]:
    candidates = [0.75, 1.0, 1.25, 1.5, 1.9, 2.4, 3.0, 3.8]
    best_point: SolvePoint | None = None
    best_top = float("nan")
    best_obj = float("inf")
    for top_conc in candidates:
        point = _solve_point(
            oa_ratio=FIT_OA_RATIO,
            e_li_exp_pct=fit_target_pct,
            e_mg_exp_pct=float("nan"),
            top_conc_mol_per_l_org=top_conc,
            temp_k=temp_k,
            pressure_pa=pressure_pa,
            user_params=user_params,
            matrices=matrices,
            user_options=user_options,
            runtime_mod=runtime_mod,
        )
        if not point.converged or not math.isfinite(point.e_li_calc_pct):
            continue
        obj = (point.e_li_calc_pct - fit_target_pct) ** 2
        if obj < best_obj:
            best_obj = obj
            best_top = top_conc
            best_point = point
    if best_point is None or not math.isfinite(best_top):
        raise RuntimeError("Failed to evaluate any O/A = 2 fit candidates.")
    return best_top, best_point


def _fmt(value: Any, digits: int = 6) -> str:
    if isinstance(value, (float, np.floating)):
        if not math.isfinite(float(value)):
            return "nan"
        return f"{float(value):.{digits}g}"
    return str(value)


def _write_csv(path: Path, point_rows: list[SolvePoint], dense_rows: list[SolvePoint], top_conc_mol_per_l_org: float, fit_point: SolvePoint) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "section",
        "oa_ratio",
        "e_li_exp_pct",
        "e_mg_exp_pct",
        "e_li_calc_pct",
        "e_mg_calc_pct",
        "converged",
        "status",
        "message",
        "residual_norm",
        "tpdf_min",
        "beta_org",
        "beta_aq",
        "x_li_org",
        "x_mg_org",
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
                    "converged": row.converged,
                    "status": row.status,
                    "message": row.message,
                    "residual_norm": row.residual_norm,
                    "tpdf_min": row.tpdf_min,
                    "beta_org": row.beta_org,
                    "beta_aq": row.beta_aq,
                    "x_li_org": row.x_li_org,
                    "x_mg_org": row.x_mg_org,
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
                    "converged": row.converged,
                    "status": row.status,
                    "message": row.message,
                    "residual_norm": row.residual_norm,
                    "tpdf_min": row.tpdf_min,
                    "beta_org": row.beta_org,
                    "beta_aq": row.beta_aq,
                    "x_li_org": row.x_li_org,
                    "x_mg_org": row.x_mg_org,
                }
            )
        writer.writerow(
            {
                "section": "fit_summary",
                "oa_ratio": FIT_OA_RATIO,
                "e_li_exp_pct": fit_point.e_li_exp_pct,
                "e_li_calc_pct": fit_point.e_li_calc_pct,
                "message": f"effective_TOP_concentration_mol_per_L_org={top_conc_mol_per_l_org:.8f}",
            }
        )


def _write_markdown(path: Path, point_rows: list[SolvePoint], top_conc_mol_per_l_org: float, fit_point: SolvePoint, args: argparse.Namespace, user_options: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Yu 2024 Figure 6 Replication")
    lines.append("")
    lines.append("## Basis")
    lines.append("")
    lines.append(f"- Dataset directory: {args.dataset_dir}")
    lines.append(f"- Digitized experimental points: {args.exp_csv}")
    lines.append("- Runtime: installed `epcsaft` package through `scripts.epcsaft_compat`.")
    lines.append(f"- Imported pcsaft module: {Path(pcs.__file__).resolve()}")
    lines.append(f"- Effective user options: `{json.dumps(user_options, sort_keys=True)}`")
    lines.append(f"- Assumed aqueous density for the reported g/L brine basis: `{AQ_DENSITY_KG_PER_L:.3f} kg/L`")
    lines.append(f"- Fitted effective TOP concentration used to convert O/A volume ratio into feed moles: `{top_conc_mol_per_l_org:.6f} mol/L organic`")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- The paper body is available locally, but Table S6 is not. Experimental points were digitized from the local PDF figure.")
    lines.append("- Paper Table 3 interaction parameters were used directly. Only the effective TOP concentration was back-calculated so the `O/A = 2:1` fit anchor can be reconstructed from the reported figure.")
    lines.append("- The 2025 electrolyte options were enforced with empirical dielectric mixing and Born `SSM+DS` active, per the current package schema.")
    lines.append("")
    lines.append("## Pointwise Comparison")
    lines.append("")
    lines.append("| O/A | $E_{Li+,exp}$ (%) | $E_{Li+,calc}$ (%) | $E_{Mg2+,exp}$ (%) | $E_{Mg2+,calc}$ (%) | converged |")
    lines.append("|---:|---:|---:|---:|---:|:---:|")
    for row in point_rows:
        lines.append(
            f"| {_fmt(row.oa_ratio, 4)} | {_fmt(row.e_li_exp_pct, 5)} | {_fmt(row.e_li_calc_pct, 5)} | {_fmt(row.e_mg_exp_pct, 5)} | {_fmt(row.e_mg_calc_pct, 5)} | {row.converged} |"
        )
    lines.append("")
    lines.append("## Fit Anchor")
    lines.append("")
    lines.append(f"- `O/A = 2:1`: target `{_fmt(fit_point.e_li_exp_pct, 5)} %`, model `{_fmt(fit_point.e_li_calc_pct, 5)} %`")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_plot(path: Path, point_rows: list[SolvePoint], dense_rows: list[SolvePoint]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 5.2), dpi=180)

    x_points = np.asarray([row.oa_ratio for row in point_rows], dtype=float)
    li_exp = np.asarray([row.e_li_exp_pct for row in point_rows], dtype=float)
    mg_exp = np.asarray([row.e_mg_exp_pct for row in point_rows], dtype=float)
    x_dense = np.asarray([row.oa_ratio for row in dense_rows], dtype=float)
    li_calc = np.asarray([row.e_li_calc_pct for row in dense_rows], dtype=float)
    mg_calc = np.asarray([row.e_mg_calc_pct for row in dense_rows], dtype=float)

    ax.scatter(x_points, li_exp, facecolors="white", edgecolors="red", s=52, linewidths=1.3, label=r"$E_{Li^+,exp.}$")
    ax.plot(x_dense[np.isfinite(li_calc)], li_calc[np.isfinite(li_calc)], color="red", linewidth=1.3, label=r"$E_{Li^+,calc.}$")
    ax.scatter(x_points, mg_exp, facecolors="white", edgecolors="cornflowerblue", marker="s", s=40, linewidths=1.2, label=r"$E_{Mg^{2+},exp.}$")
    ax.plot(x_dense[np.isfinite(mg_calc)], mg_calc[np.isfinite(mg_calc)], color="cornflowerblue", linewidth=1.3, label=r"$E_{Mg^{2+},calc.}$")

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


def run(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    dataset_dir = Path(args.dataset_dir)
    exp_csv = Path(args.exp_csv)
    runtime_mod = _load_pcsaft_runtime_module()
    user_params, k_ij, k_hb, l_ij, user_options = _load_dataset(dataset_dir)
    matrices = {"k_ij": k_ij, "k_hb": k_hb, "l_ij": l_ij}
    exp_points = _load_exp_points(exp_csv)

    temp_k = 298.15
    pressure_pa = 1.013e5
    fit_target = next((point.e_li_exp_pct for point in exp_points if abs(point.oa_ratio - FIT_OA_RATIO) < 1e-12), None)
    if fit_target is None:
        raise ValueError("Digitized points must include the O/A = 2 anchor.")

    top_conc_mol_per_l_org = TOP_CONC_MOL_PER_L_ORG

    point_rows = [
        _solve_point(
            oa_ratio=point.oa_ratio,
            e_li_exp_pct=point.e_li_exp_pct,
            e_mg_exp_pct=point.e_mg_exp_pct,
            top_conc_mol_per_l_org=top_conc_mol_per_l_org,
            temp_k=temp_k,
            pressure_pa=pressure_pa,
            user_params=user_params,
            matrices=matrices,
            user_options=user_options,
            runtime_mod=runtime_mod,
        )
        for point in exp_points
    ]

    fit_point = next(row for row in point_rows if abs(row.oa_ratio - FIT_OA_RATIO) < 1e-12)

    dense_grid = np.asarray([point.oa_ratio for point in exp_points], dtype=float)
    dense_rows = [
        _solve_point(
            oa_ratio=float(oa),
            e_li_exp_pct=float("nan"),
            e_mg_exp_pct=float("nan"),
            top_conc_mol_per_l_org=top_conc_mol_per_l_org,
            temp_k=temp_k,
            pressure_pa=pressure_pa,
            user_params=user_params,
            matrices=matrices,
            user_options=user_options,
            runtime_mod=runtime_mod,
        )
        for oa in dense_grid
    ]

    _write_csv(Path(args.out_csv), point_rows, dense_rows, top_conc_mol_per_l_org, fit_point)
    _write_markdown(Path(args.out_md), point_rows, top_conc_mol_per_l_org, fit_point, args, user_options)
    _write_plot(Path(args.out_png), point_rows, dense_rows)

    print(f"Imported pcsaft: {Path(pcs.__file__).resolve()}")
    print(f"Effective TOP concentration (fit reconstruction): {top_conc_mol_per_l_org:.8f} mol/L organic")
    print(f"Saved CSV: {args.out_csv}")
    print(f"Saved Markdown: {args.out_md}")
    print(f"Saved Plot: {args.out_png}")
    return Path(args.out_csv), Path(args.out_md), Path(args.out_png)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recreate Yu 2024 Figure 6 with the current PC-SAFT build.")
    parser.add_argument("--dataset-dir", default=str(DATASET_DIR))
    parser.add_argument("--exp-csv", default=str(DEFAULT_DIGITIZED_CSV))
    parser.add_argument("--out-csv", default=str(DEFAULT_OUT_CSV))
    parser.add_argument("--out-md", default=str(DEFAULT_OUT_MD))
    parser.add_argument("--out-png", default=str(DEFAULT_OUT_PNG))
    return parser.parse_args()


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()

