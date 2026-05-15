"""Small IDAES SurrogateBlock bridge for the frozen AlamoSurrogate artifact."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from idaes.core.surrogate.surrogate_block import SurrogateBlock
from pyomo.environ import ConcreteModel, value

from .alamo_surrogate import INPUT_LABELS, OUTPUT_LABELS, load_surrogate


def build_surrogate_block_model(surrogate_path: Path | None = None) -> tuple[ConcreteModel, object]:
    surrogate = load_surrogate(surrogate_path)
    model = ConcreteModel()
    model.tbac_da_topo_alamo = SurrogateBlock()
    model.tbac_da_topo_alamo.build_model(surrogate)
    return model, surrogate


def surrogate_block_smoke(
    sample: dict[str, float] | None = None,
    surrogate_path: Path | None = None,
    tolerance: float = 1e-8,
) -> dict[str, object]:
    sample = sample or {
        "li_mg_L": 168.0,
        "na_mg_L": 64100.0,
        "o_to_a_ratio": 1.0,
        "topo_wt_pct": 10.0,
    }
    model, surrogate = build_surrogate_block_model(surrogate_path)
    block = model.tbac_da_topo_alamo
    for label in INPUT_LABELS:
        block.inputs[label].fix(float(sample[label]))
    prediction = surrogate.evaluate_surrogate(pd.DataFrame([sample], columns=INPUT_LABELS)).iloc[0]
    residuals: dict[str, float] = {}
    for label in OUTPUT_LABELS:
        block.outputs[label].set_value(float(prediction[label]))
        residuals[label] = abs(float(value(block.alamo_constraint[label].body)))
    return {
        "input_labels": list(block.input_vars_as_dict().keys()),
        "output_labels": list(block.output_vars_as_dict().keys()),
        "constraint_count": len(block.alamo_constraint),
        "residuals": residuals,
        "pass": all(residual <= tolerance for residual in residuals.values()),
    }
