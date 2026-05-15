from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_tea_assumption_register_schema() -> None:
    rows = _rows("data/reference/tea/tbac_da_topo_tea_assumption_register.csv")
    assert len(rows) >= 8
    required = {
        "assumption_id",
        "parameter",
        "base_value",
        "low_value",
        "high_value",
        "units",
        "distribution",
        "role",
        "source_basis",
        "notes",
    }
    assert required.issubset(rows[0])
    parameters = {row["parameter"] for row in rows}
    assert {"pretreatment_li_loss_pct", "solvent_loss_kg_m3", "annualized_capex_usd_y"}.issubset(parameters)


def test_screening_tea_results_schema_and_bounds() -> None:
    rows = _rows("data/processed/tbac_da_topo_screening_tea_results.csv")
    assert len(rows) == 7
    required = {
        "scenario_id",
        "feed_id",
        "stage_count",
        "li_feed_mg_L",
        "prommis_li_recovery_pct",
        "net_li_recovery_pct",
        "annual_lce_kg",
        "annual_cost_usd",
        "breakeven_usd_kg_LCE",
        "uq_p10_usd_kg_LCE",
        "uq_p50_usd_kg_LCE",
        "uq_p90_usd_kg_LCE",
        "estimate_class",
        "screening_only",
        "source_case_id",
        "model_basis",
    }
    assert required.issubset(rows[0])
    scenario_ids = {row["scenario_id"] for row in rows}
    assert {"base_smackover_ms2", "high_li_smackover", "five_stage_smackover", "lower_throughput"}.issubset(scenario_ids)
    for row in rows:
        assert row["estimate_class"] == "screening"
        assert row["screening_only"] == "True"
        assert float(row["annual_lce_kg"]) > 0.0
        assert float(row["annual_cost_usd"]) > 0.0
        assert 0.0 < float(row["net_li_recovery_pct"]) <= float(row["prommis_li_recovery_pct"])
        assert float(row["uq_p10_usd_kg_LCE"]) <= float(row["uq_p50_usd_kg_LCE"]) <= float(row["uq_p90_usd_kg_LCE"])
        assert 0.0 < float(row["breakeven_usd_kg_LCE"]) < 100.0


def test_deck_required_content_and_figures() -> None:
    deck = (ROOT / "slides/case_study_tbac_da_topo_produced_water/deck.qmd").read_text(encoding="utf-8")
    required_phrases = [
        "Produced-Water Lithium Extraction Case Study",
        "produced_water_basin_map.png",
        "feed_variance_matrix.png",
        "IDAES AlamoSurrogate",
        "SurrogateBlock",
        "SolventExtraction",
        "MSContactor",
        "screening_tea_uq.png",
        "epcsaft_gap_roadmap.png",
        "CMM/REE",
        "hydrocarbon_vle_lle_extension.png",
    ]
    for phrase in required_phrases:
        assert phrase in deck
    for figure in [
        "produced_water_basin_map.png",
        "feed_variance_matrix.png",
        "alamo_validation_summary.png",
        "prommis_stage_recovery.png",
        "screening_tea_uq.png",
        "epcsaft_gap_roadmap.png",
        "cmm_ree_extension_table.png",
        "hydrocarbon_vle_lle_extension.png",
    ]:
        assert (ROOT / "slides/case_study_tbac_da_topo_produced_water/figures" / figure).stat().st_size > 10_000


def test_notebook_metadata_records_original_prommis_tutorial() -> None:
    notebook = json.loads((ROOT / "docs/tutorials/tbac_da_topo_produced_water_case_study.ipynb").read_text(encoding="utf-8"))
    metadata = notebook["metadata"]["case_study"]
    assert metadata["active_solvent_system"] == "TBAC(1):DA(2) hydrophobic DES + TOPO"
    assert metadata["original_prommis_notebook_cell_count"] == 22
    assert len(metadata["original_prommis_notebook_sha256"]) == 64
