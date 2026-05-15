from __future__ import annotations

from pathlib import Path

import pandas as pd
from idaes.core.surrogate.alamopy import AlamoSurrogate, AlamoTrainer

from lithium_extraction.prommis_case_study.alamo_bridge import surrogate_block_smoke
from lithium_extraction.prommis_case_study.alamo_surrogate import (
    INPUT_LABELS,
    OUTPUT_LABELS,
    build_alamo_trainer,
    load_surrogate,
    load_training_validation,
    validate_surrogate,
)


ROOT = Path(__file__).resolve().parents[1]


def test_frozen_alamo_json_loads_with_idaes_api() -> None:
    path = ROOT / "models/tbac_da_topo_alamo_surrogate.json"
    assert path.exists()
    surrogate = AlamoSurrogate.load_from_file(path)
    assert isinstance(surrogate, AlamoSurrogate)
    assert surrogate.input_labels() == INPUT_LABELS
    assert surrogate.output_labels() == OUTPUT_LABELS
    assert set(surrogate.input_bounds()) == set(INPUT_LABELS)


def test_alamo_trainer_contract_is_constructible() -> None:
    training, validation = load_training_validation(ROOT)
    trainer = build_alamo_trainer(training, validation)
    assert isinstance(trainer, AlamoTrainer)
    assert trainer.input_labels() == INPUT_LABELS
    assert trainer.output_labels() == OUTPUT_LABELS


def test_surrogate_validation_metrics_and_figures() -> None:
    _, validation = load_training_validation(ROOT)
    surrogate = load_surrogate(ROOT / "models/tbac_da_topo_alamo_surrogate.json")
    predicted, metrics = validate_surrogate(surrogate, validation)
    assert isinstance(predicted, pd.DataFrame)
    assert set(predicted.columns) == set(OUTPUT_LABELS)
    assert metrics["logit_k_Li"]["r2"] > 0.99
    assert metrics["logit_k_Na"]["r2"] > 0.99
    for figure in (
        "figures/alamo_parity_logit_k_Li.png",
        "figures/alamo_parity_logit_k_Na.png",
        "figures/alamo_residual_logit_k_Li.png",
        "figures/alamo_residual_logit_k_Na.png",
    ):
        assert (ROOT / figure).stat().st_size > 10_000


def test_surrogate_block_smoke_check() -> None:
    result = surrogate_block_smoke(surrogate_path=ROOT / "models/tbac_da_topo_alamo_surrogate.json")
    assert result["pass"] is True
    assert result["input_labels"] == INPUT_LABELS
    assert result["output_labels"] == OUTPUT_LABELS
    assert result["constraint_count"] == 2
