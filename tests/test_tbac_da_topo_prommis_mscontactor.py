from __future__ import annotations

import csv
from pathlib import Path

from idaes.core.util.model_statistics import degrees_of_freedom

from lithium_extraction.prommis_case_study.tbac_da_topo_mscontactor import (
    build_single_stage_model,
    predict_stage_k,
)


ROOT = Path(__file__).resolve().parents[1]


def _stage_rows() -> list[dict[str, str]]:
    path = ROOT / "data/processed/tbac_da_topo_prommis_stage_results.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_real_prommis_mscontactor_model_contract() -> None:
    k_values = predict_stage_k(li_mg_L=168.0, na_mg_L=64100.0, o_to_a_ratio=1.0, topo_wt_pct=10.0)
    model = build_single_stage_model(
        li_feed_mg_L=168.0,
        na_feed_mg_L=64100.0,
        k_Li=k_values["k_Li"],
        k_Na=k_values["k_Na"],
        o_to_a_ratio=1.0,
        topo_wt_pct=10.0,
    )
    assert type(model.fs.solex).__name__.endswith("SolventExtraction")
    assert type(model.fs.solex.mscontactor).__name__.endswith("MSContactor")
    assert degrees_of_freedom(model) == 0
    assert model.fs.li_mass_transfer_constraint[0].active
    assert model.fs.na_mass_transfer_constraint[0].active
    assert model.fs.cl_mass_transfer_constraint[0].active
    stage = model.fs.solex.mscontactor.elements.first()
    terms = model.fs.solex.mscontactor.material_transfer_term
    assert terms[0, stage, ("aqueous", "organic", "Li")].is_variable_type()
    assert terms[0, stage, ("aqueous", "organic", "Na")].is_variable_type()
    assert terms[0, stage, ("aqueous", "organic", "Cl")].is_variable_type()


def test_prommis_stage_results_are_accepted_and_bounded() -> None:
    rows = _stage_rows()
    assert len(rows) == 12
    assert {row["case_id"] for row in rows} >= {
        "smackover_ms2_main_1stage",
        "smackover_ms2_main_3stage",
        "smackover_ms2_main_5stage",
        "smackover_high_observed_sensitivity_3stage",
    }
    for row in rows:
        assert row["prommis_object_type"].endswith("SolventExtraction")
        assert row["mscontactor_object_type"].endswith("MSContactor")
        assert int(row["degrees_of_freedom"]) == 0
        assert row["termination_condition"] == "optimal"
        assert row["material_transfer_constraints_active"] == "True"
        assert row["chloride_transfer_allowed"] == "False"
        assert row["model_basis"] == "source_paper_anchored_synthetic_stage_response"
        assert row["backend_name"] == "synthetic_source_anchored_demo"
        assert row["direct_epcsaft_closure"] == "False"
        assert float(row["mass_balance_residual_mol_per_h"]) < 1e-8
        assert 0.0 < float(row["li_stage_extraction_pct"]) < 100.0
        assert 0.0 < float(row["na_stage_extraction_pct"]) < float(row["li_stage_extraction_pct"])


def test_nominal_three_stage_summary_row() -> None:
    rows = _stage_rows()
    nominal_final = [
        row
        for row in rows
        if row["case_id"] == "smackover_ms2_main_3stage" and row["stage"] == row["stage_count"]
    ][0]
    assert 80.0 < float(nominal_final["li_cumulative_recovery_pct"]) < 90.0
    assert 20.0 < float(nominal_final["na_cumulative_recovery_pct"]) < 35.0
