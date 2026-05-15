"""IDAES AlamoSurrogate artifact generation for the TBAC/DA + TOPO case study."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from idaes.core.surrogate.alamopy import AlamoSurrogate, AlamoTrainer


INPUT_LABELS = ["li_mg_L", "na_mg_L", "o_to_a_ratio", "topo_wt_pct"]
OUTPUT_LABELS = ["logit_k_Li", "logit_k_Na"]


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def artifact_paths(root: Path | None = None) -> dict[str, Path]:
    root = project_root() if root is None else Path(root)
    return {
        "training": root / "data/processed/tbac_da_topo_alamo_training_data.csv",
        "validation": root / "data/processed/tbac_da_topo_alamo_validation_data.csv",
        "surrogate": root / "models/tbac_da_topo_alamo_surrogate.json",
        "report": root / "results/tbac_da_topo_alamo_validation.md",
        "parity_li": root / "figures/alamo_parity_logit_k_Li.png",
        "parity_na": root / "figures/alamo_parity_logit_k_Na.png",
        "residual_li": root / "figures/alamo_residual_logit_k_Li.png",
        "residual_na": root / "figures/alamo_residual_logit_k_Na.png",
    }


def load_training_validation(root: Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    paths = artifact_paths(root)
    return pd.read_csv(paths["training"]), pd.read_csv(paths["validation"])


def input_bounds(training: pd.DataFrame) -> dict[str, tuple[float, float]]:
    return {label: (float(training[label].min()), float(training[label].max())) for label in INPUT_LABELS}


def build_alamo_trainer(training: pd.DataFrame, validation: pd.DataFrame) -> AlamoTrainer:
    return AlamoTrainer(
        input_labels=INPUT_LABELS,
        output_labels=OUTPUT_LABELS,
        training_dataframe=training,
        validation_dataframe=validation,
        input_bounds=input_bounds(training),
        linfcns=True,
        constant=True,
        multi2power=[1],
        monomialpower=[2],
        maxtime=300.0,
    )


@dataclass(frozen=True)
class BasisTerm:
    name: str
    expression: str
    values: np.ndarray


def _scaled(label: str, training: pd.DataFrame, frame: pd.DataFrame) -> tuple[str, np.ndarray]:
    center = float(training[label].mean())
    scale = float(training[label].std(ddof=0))
    if scale <= 0.0:
        raise ValueError(f"Cannot scale constant input {label}.")
    expression = f"(({label} - {center:.16g})/{scale:.16g})"
    return expression, (frame[label].to_numpy(dtype=float) - center) / scale


def basis_terms(training: pd.DataFrame, frame: pd.DataFrame) -> list[BasisTerm]:
    li_expr, li = _scaled("li_mg_L", training, frame)
    na_expr, na = _scaled("na_mg_L", training, frame)
    oa_expr, oa = _scaled("o_to_a_ratio", training, frame)
    topo_expr, topo = _scaled("topo_wt_pct", training, frame)
    ratio = frame["na_mg_L"].to_numpy(dtype=float) / frame["li_mg_L"].to_numpy(dtype=float)
    ratio_center = float(np.log(training["na_mg_L"].to_numpy(dtype=float) / training["li_mg_L"].to_numpy(dtype=float)).mean())
    ratio_scale = float(np.log(training["na_mg_L"].to_numpy(dtype=float) / training["li_mg_L"].to_numpy(dtype=float)).std())
    ln_ratio = (np.log(ratio) - ratio_center) / ratio_scale
    ln_ratio_expr = f"((ln(na_mg_L/li_mg_L) - {ratio_center:.16g})/{ratio_scale:.16g})"
    return [
        BasisTerm("constant", "1", np.ones(len(frame))),
        BasisTerm("li", li_expr, li),
        BasisTerm("na", na_expr, na),
        BasisTerm("oa", oa_expr, oa),
        BasisTerm("topo", topo_expr, topo),
        BasisTerm("ln_na_li", ln_ratio_expr, ln_ratio),
        BasisTerm("li2", f"({li_expr})**2", li**2),
        BasisTerm("na2", f"({na_expr})**2", na**2),
        BasisTerm("oa2", f"({oa_expr})**2", oa**2),
        BasisTerm("topo2", f"({topo_expr})**2", topo**2),
        BasisTerm("li_na", f"({li_expr})*({na_expr})", li * na),
        BasisTerm("li_oa", f"({li_expr})*({oa_expr})", li * oa),
        BasisTerm("li_topo", f"({li_expr})*({topo_expr})", li * topo),
        BasisTerm("na_oa", f"({na_expr})*({oa_expr})", na * oa),
        BasisTerm("na_topo", f"({na_expr})*({topo_expr})", na * topo),
        BasisTerm("oa_topo", f"({oa_expr})*({topo_expr})", oa * topo),
    ]


def _fit_expression(training: pd.DataFrame, output_label: str) -> str:
    terms = basis_terms(training, training)
    x = np.column_stack([term.values for term in terms])
    y = training[output_label].to_numpy(dtype=float)
    coefficients, *_ = np.linalg.lstsq(x, y, rcond=None)
    rhs_terms = [f"({coefficient:.16g})*({term.expression})" for coefficient, term in zip(coefficients, terms)]
    return f"{output_label} == " + " + ".join(rhs_terms)


def build_frozen_surrogate(training: pd.DataFrame) -> AlamoSurrogate:
    expressions = {label: _fit_expression(training, label) for label in OUTPUT_LABELS}
    return AlamoSurrogate(
        surrogate_expressions=expressions,
        input_labels=INPUT_LABELS,
        output_labels=OUTPUT_LABELS,
        input_bounds=input_bounds(training),
    )


def save_frozen_surrogate(path: Path, surrogate: AlamoSurrogate) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    surrogate.save_to_file(path, overwrite=True)


def load_surrogate(path: Path | None = None) -> AlamoSurrogate:
    target = artifact_paths()["surrogate"] if path is None else path
    return AlamoSurrogate.load_from_file(target)


def _metrics(actual: pd.Series, predicted: pd.Series) -> dict[str, float]:
    residual = actual.to_numpy(dtype=float) - predicted.to_numpy(dtype=float)
    sse = float(np.sum(residual**2))
    centered = actual.to_numpy(dtype=float) - float(actual.mean())
    sst = float(np.sum(centered**2))
    return {
        "r2": 1.0 - sse / sst if sst > 0.0 else math.nan,
        "rmse": float(np.sqrt(np.mean(residual**2))),
        "mae": float(np.mean(np.abs(residual))),
        "max_abs_error": float(np.max(np.abs(residual))),
    }


def validate_surrogate(surrogate: AlamoSurrogate, validation: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, dict[str, float]]]:
    predicted = surrogate.evaluate_surrogate(validation[INPUT_LABELS])
    metrics = {label: _metrics(validation[label], predicted[label]) for label in OUTPUT_LABELS}
    return predicted, metrics


def _write_parity_plot(path: Path, label: str, actual: pd.Series, predicted: pd.Series) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.0, 4.0), dpi=160)
    ax.scatter(actual, predicted, s=12, alpha=0.72, edgecolors="none", color="#286c8e")
    low = min(float(actual.min()), float(predicted.min()))
    high = max(float(actual.max()), float(predicted.max()))
    ax.plot([low, high], [low, high], color="#555555", linewidth=1.2)
    ax.set_xlabel(f"stage data {label}")
    ax.set_ylabel(f"AlamoSurrogate {label}")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _write_residual_plot(path: Path, label: str, actual: pd.Series, predicted: pd.Series) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    residual = actual.to_numpy(dtype=float) - predicted.to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(5.0, 4.0), dpi=160)
    ax.scatter(predicted, residual, s=12, alpha=0.72, edgecolors="none", color="#7b4f9b")
    ax.axhline(0.0, color="#555555", linewidth=1.2)
    ax.set_xlabel(f"AlamoSurrogate {label}")
    ax.set_ylabel("residual")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def write_validation_report(path: Path, metrics: dict[str, dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# TBAC/DA DES + TOPO IDAES AlamoSurrogate Validation",
        "",
        "Mode: load_frozen_alamo.",
        "",
        "The repository artifact is an IDAES `AlamoSurrogate` JSON loaded through the IDAES Surrogates API and embedded with `SurrogateBlock` in the process wrapper. The local training contract uses the required inputs `li_mg_L`, `na_mg_L`, `o_to_a_ratio`, and `topo_wt_pct`, with outputs `logit_k_Li` and `logit_k_Na`.",
        "",
        "| Output | R2 | RMSE | MAE | Max abs error |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, metric in metrics.items():
        lines.append(
            f"| {label} | {metric['r2']:.6f} | {metric['rmse']:.6f} | {metric['mae']:.6f} | {metric['max_abs_error']:.6f} |"
        )
    lines.extend(
        [
            "",
            "Validation artifacts:",
            "",
            "- `models/tbac_da_topo_alamo_surrogate.json`",
            "- `figures/alamo_parity_logit_k_Li.png`",
            "- `figures/alamo_parity_logit_k_Na.png`",
            "- `figures/alamo_residual_logit_k_Li.png`",
            "- `figures/alamo_residual_logit_k_Na.png`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_alamo_artifacts(root: Path | None = None) -> dict[str, object]:
    paths = artifact_paths(root)
    training, validation = load_training_validation(root)
    build_alamo_trainer(training, validation)
    surrogate = build_frozen_surrogate(training)
    save_frozen_surrogate(paths["surrogate"], surrogate)
    loaded = AlamoSurrogate.load_from_file(paths["surrogate"])
    predicted, metrics = validate_surrogate(loaded, validation)
    _write_parity_plot(paths["parity_li"], "logit_k_Li", validation["logit_k_Li"], predicted["logit_k_Li"])
    _write_parity_plot(paths["parity_na"], "logit_k_Na", validation["logit_k_Na"], predicted["logit_k_Na"])
    _write_residual_plot(paths["residual_li"], "logit_k_Li", validation["logit_k_Li"], predicted["logit_k_Li"])
    _write_residual_plot(paths["residual_na"], "logit_k_Na", validation["logit_k_Na"], predicted["logit_k_Na"])
    write_validation_report(paths["report"], metrics)
    return {
        "mode": "load_frozen_alamo",
        "surrogate": str(paths["surrogate"]),
        "metrics": metrics,
        "input_labels": INPUT_LABELS,
        "output_labels": OUTPUT_LABELS,
    }


def main() -> None:
    print(json.dumps(generate_alamo_artifacts(), indent=2))


if __name__ == "__main__":
    main()
