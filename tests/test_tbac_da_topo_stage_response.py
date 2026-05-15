from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _required_columns(path: str, columns: set[str]) -> None:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        missing = columns.difference(reader.fieldnames)
    assert not missing, f"{path} missing columns: {sorted(missing)}"


def test_feed_register_schema_and_simulation_flags() -> None:
    required = {
        "feed_id",
        "basin",
        "formation",
        "region",
        "source_type",
        "Li_mg_L",
        "Na_mg_L",
        "K_mg_L",
        "Mg_mg_L",
        "Ca_mg_L",
        "Sr_mg_L",
        "Ba_mg_L",
        "Cl_mg_L",
        "TDS_mg_L",
        "pH",
        "TOC_mg_L",
        "Na_Li_mass_ratio",
        "divalent_Li_mass_ratio",
        "data_quality_flag",
        "simulation_allowed_flag",
        "source_citation",
        "notes",
    }
    _required_columns("data/reference/produced_water/selected_case_study_feeds.csv", required)
    feeds = {row["feed_id"]: row for row in _rows("data/reference/produced_water/selected_case_study_feeds.csv")}
    assert feeds["smackover_ms2_main"]["simulation_allowed_flag"] == "true"
    assert feeds["smackover_high_observed_sensitivity"]["simulation_allowed_flag"] == "true"
    assert feeds["marcellus_ne_pa_comparison"]["simulation_allowed_flag"] == "false"
    assert feeds["bakken_high_na_stress"]["simulation_allowed_flag"] == "false"
    assert feeds["marcellus_ne_pa_comparison"]["Na_mg_L"] == ""
    assert feeds["bakken_high_na_stress"]["Ca_mg_L"] == ""


def test_source_register_names_stage_response_anchor() -> None:
    rows = _rows("data/reference/produced_water/produced_water_feed_source_register.csv")
    source_ids = {row["source_id"] for row in rows}
    assert "rezaee_des_topo_stage_anchor" in source_ids
    assert any(row["quality_status"] == "simulation_allowed" for row in rows)
    assert any("missing" in row["quality_status"] for row in rows)


def test_two_domain_design_counts_and_labels() -> None:
    required = {
        "design_id",
        "domain",
        "row_type",
        "li_mg_L",
        "na_mg_L",
        "na_li_mass_ratio",
        "o_to_a_ratio",
        "topo_wt_pct",
        "temperature_C",
        "aqueous_pH",
        "solvent_base",
        "TBAC_to_DA_molar_ratio",
        "source_anchor_flag",
        "synthetic_demo_data",
        "model_basis",
        "backend_name",
        "direct_epcsaft_closure",
        "validity_flag",
        "extrapolation_flag",
    }
    _required_columns("data/processed/tbac_da_topo_two_domain_lhs_design.csv", required)
    design = _rows("data/processed/tbac_da_topo_two_domain_lhs_design.csv")
    counts = Counter((row["domain"], row["row_type"]) for row in design)
    assert counts[("source-paper-valid", "generated_source_domain")] == 625
    assert counts[("produced-water-centered", "generated_produced_water_domain")] == 625
    assert counts[("source-paper-valid", "source_anchor")] >= 3
    assert counts[("produced-water-centered", "nominal")] == 2
    assert counts[("produced-water-centered", "corner")] == 16
    generated = [row for row in design if row["source_anchor_flag"] == "false"]
    assert all(row["direct_epcsaft_closure"] == "false" for row in generated)
    assert all(row["solvent_base"] == "TBAC(1):DA(2) hydrophobic DES" for row in design)


def test_stage_response_schema_bounds_and_source_anchors() -> None:
    required = {
        "design_id",
        "domain",
        "row_type",
        "li_mg_L",
        "na_mg_L",
        "na_li_mass_ratio",
        "o_to_a_ratio",
        "topo_wt_pct",
        "k_Li",
        "k_Na",
        "logit_k_Li",
        "logit_k_Na",
        "Li_extraction_pct",
        "Na_extraction_pct",
        "D_Li",
        "D_Na",
        "Li_Na_selectivity_process",
        "Li_Na_selectivity_source_definition",
        "validity_flag",
        "extrapolation_flag",
        "synthetic_demo_data",
        "model_basis",
        "backend_name",
        "direct_epcsaft_closure",
    }
    _required_columns("data/processed/tbac_da_topo_stage_response_data.csv", required)
    rows = _rows("data/processed/tbac_da_topo_stage_response_data.csv")
    by_id = {row["design_id"]: row for row in rows}
    assert len(rows) == len(_rows("data/processed/tbac_da_topo_two_domain_lhs_design.csv"))
    for row in rows:
        k_li = float(row["k_Li"])
        k_na = float(row["k_Na"])
        assert 0.0 < k_li < 1.0
        assert 0.0 < k_na < 1.0
        assert float(row["Li_extraction_pct"]) > float(row["Na_extraction_pct"])
        assert math.isfinite(float(row["logit_k_Li"]))
        assert math.isfinite(float(row["logit_k_Na"]))
        if row["row_type"] != "source_anchor":
            assert row["synthetic_demo_data"] == "true"
            assert row["model_basis"] == "source_paper_anchored_synthetic_stage_response"
            assert row["backend_name"] == "synthetic_source_anchored_demo"
            assert row["direct_epcsaft_closure"] == "false"

    optimized = by_id["source_anchor_optimized_10wt_topo"]
    model_brine = by_id["source_anchor_model_brine_li_na"]
    assert abs(float(optimized["Li_extraction_pct"]) - 48.57) < 0.05
    assert abs(float(optimized["Li_Na_selectivity_source_definition"]) - 4.41) < 0.02
    assert abs(float(model_brine["Li_extraction_pct"]) - 51.63) < 0.05
    assert abs(float(model_brine["Na_extraction_pct"]) - 9.97) < 0.05


def test_alamo_training_validation_contract() -> None:
    training = _rows("data/processed/tbac_da_topo_alamo_training_data.csv")
    validation = _rows("data/processed/tbac_da_topo_alamo_validation_data.csv")
    assert training
    assert validation
    required = {"li_mg_L", "na_mg_L", "o_to_a_ratio", "topo_wt_pct", "logit_k_Li", "logit_k_Na"}
    _required_columns("data/processed/tbac_da_topo_alamo_training_data.csv", required)
    _required_columns("data/processed/tbac_da_topo_alamo_validation_data.csv", required)
    assert len(validation) >= 250
    for row in training + validation:
        assert all(math.isfinite(float(row[column])) for column in required)
