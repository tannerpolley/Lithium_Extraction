"""Generate the T002 foundation artifacts for the produced-water case study."""

from __future__ import annotations

import csv
import itertools
import json
import math
import random
from pathlib import Path
from typing import Iterable

try:  # pragma: no cover - supports script execution before editable install.
    from .backend import STAGE_RESPONSE_BACKEND, require_stage_response_labels
except ImportError:  # pragma: no cover
    from backend import STAGE_RESPONSE_BACKEND, require_stage_response_labels


SOLVENT_BASE = "TBAC(1):DA(2) hydrophobic DES"
TBAC_TO_DA = "1:2"
TEMPERATURE_C = 23.0
AQUEOUS_PH = 10.4
EPS = 1.0e-6

FEED_COLUMNS = [
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
]

SOURCE_REGISTER_COLUMNS = [
    "source_id",
    "source_group",
    "citation_label",
    "artifact_role",
    "source_type",
    "data_scope",
    "fields_used",
    "quality_status",
    "notes",
]

DESIGN_COLUMNS = [
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
]

STAGE_COLUMNS = [
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
]

ALAMO_COLUMNS = [
    "design_id",
    "domain",
    "row_type",
    "li_mg_L",
    "na_mg_L",
    "o_to_a_ratio",
    "topo_wt_pct",
    "logit_k_Li",
    "logit_k_Na",
    "k_Li",
    "k_Na",
    "synthetic_demo_data",
    "model_basis",
    "backend_name",
    "direct_epcsaft_closure",
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _format_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.12g}"
    return str(value)


def _write_csv(path: Path, columns: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row_list = list(rows)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in row_list:
            writer.writerow({column: _format_value(row.get(column)) for column in columns})


def feed_rows() -> list[dict[str, object]]:
    return [
        {
            "feed_id": "smackover_ms2_main",
            "basin": "Gulf Coast",
            "formation": "Smackover",
            "region": "Southern Arkansas",
            "source_type": "source_backed_local_clean_row",
            "Li_mg_L": 168.0,
            "Na_mg_L": 64100.0,
            "K_mg_L": 2300.0,
            "Mg_mg_L": 3310.0,
            "Ca_mg_L": 36900.0,
            "Sr_mg_L": 1940.0,
            "Ba_mg_L": 8.39,
            "Cl_mg_L": None,
            "TDS_mg_L": 305000.0,
            "pH": None,
            "TOC_mg_L": None,
            "Na_Li_mass_ratio": 381.548,
            "divalent_Li_mass_ratio": 250.943,
            "data_quality_flag": "complete_major_ions_chloride_toc_unknown",
            "simulation_allowed_flag": True,
            "source_citation": "local clean Smackover row MS-2 / MSPU 4-W1",
            "notes": "Main produced-water case; divalent ions are upstream pretreatment burden, not active Li/Na extraction species.",
        },
        {
            "feed_id": "smackover_high_observed_sensitivity",
            "basin": "Gulf Coast",
            "formation": "Smackover",
            "region": "Southern Arkansas",
            "source_type": "source_backed_local_clean_row",
            "Li_mg_L": 252.0,
            "Na_mg_L": 70800.0,
            "K_mg_L": 3160.0,
            "Mg_mg_L": 3130.0,
            "Ca_mg_L": 39900.0,
            "Sr_mg_L": 2490.0,
            "Ba_mg_L": 26.1,
            "Cl_mg_L": None,
            "TDS_mg_L": 340000.0,
            "pH": None,
            "TOC_mg_L": None,
            "Na_Li_mass_ratio": 280.952,
            "divalent_Li_mass_ratio": 180.738,
            "data_quality_flag": "complete_major_ions_chloride_toc_unknown",
            "simulation_allowed_flag": True,
            "source_citation": "local clean Smackover row BR-2 / BSW 12 M",
            "notes": "High-observed-Li sensitivity case for feed variance and screening TEA propagation.",
        },
        {
            "feed_id": "marcellus_ne_pa_comparison",
            "basin": "Appalachian",
            "formation": "Marcellus",
            "region": "Northeast Pennsylvania",
            "source_type": "peer_reviewed_regional_screening_row",
            "Li_mg_L": 205.0,
            "Na_mg_L": None,
            "K_mg_L": None,
            "Mg_mg_L": 1000.0,
            "Ca_mg_L": None,
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "Cl_mg_L": None,
            "TDS_mg_L": 100000.0,
            "pH": None,
            "TOC_mg_L": None,
            "Na_Li_mass_ratio": None,
            "divalent_Li_mass_ratio": 4.878,
            "data_quality_flag": "missing_na_ca_sr_ba",
            "simulation_allowed_flag": False,
            "source_citation": "peer-reviewed regional Marcellus screening row",
            "notes": "Comparison-card row only until the missing major-ion fields are source-filled.",
        },
        {
            "feed_id": "bakken_high_na_stress",
            "basin": "Williston",
            "formation": "Bakken",
            "region": "North Dakota",
            "source_type": "peer_reviewed_high_li_county_signal",
            "Li_mg_L": 103.0,
            "Na_mg_L": 79415.0,
            "K_mg_L": 11730.0,
            "Mg_mg_L": None,
            "Ca_mg_L": None,
            "Sr_mg_L": 1631.66,
            "Ba_mg_L": None,
            "Cl_mg_L": None,
            "TDS_mg_L": 258193.0,
            "pH": None,
            "TOC_mg_L": None,
            "Na_Li_mass_ratio": 771.019,
            "divalent_Li_mass_ratio": 15.841,
            "data_quality_flag": "missing_mg_ca_ba",
            "simulation_allowed_flag": False,
            "source_citation": "peer-reviewed Bakken high-Li county screening row",
            "notes": "High-Na stress context only until missing divalent fields are source-filled.",
        },
        {
            "feed_id": "permian_wolfcamp_context",
            "basin": "Permian",
            "formation": "Wolfcamp",
            "region": "Delaware and Midland basins",
            "source_type": "context_only",
            "Li_mg_L": None,
            "Na_mg_L": None,
            "K_mg_L": None,
            "Mg_mg_L": None,
            "Ca_mg_L": None,
            "Sr_mg_L": None,
            "Ba_mg_L": None,
            "Cl_mg_L": None,
            "TDS_mg_L": None,
            "pH": None,
            "TOC_mg_L": None,
            "Na_Li_mass_ratio": None,
            "divalent_Li_mass_ratio": None,
            "data_quality_flag": "context_location_only",
            "simulation_allowed_flag": False,
            "source_citation": "master case-study context requirement",
            "notes": "Large produced-water volume context; not the flagship simulation feed.",
        },
    ]


def source_register_rows() -> list[dict[str, object]]:
    return [
        {
            "source_id": "smackover_ms2_main",
            "source_group": "produced_water_feed",
            "citation_label": "local clean Smackover row MS-2 / MSPU 4-W1",
            "artifact_role": "main_case_feed",
            "source_type": "source_backed_local_table",
            "data_scope": "Li, Na, K, Mg, Ca, Sr, Ba, TDS",
            "fields_used": "selected_case_study_feeds.csv",
            "quality_status": "simulation_allowed",
            "notes": "Used for nominal produced-water simulation after upstream pretreatment boundary.",
        },
        {
            "source_id": "smackover_high_observed_sensitivity",
            "source_group": "produced_water_feed",
            "citation_label": "local clean Smackover row BR-2 / BSW 12 M",
            "artifact_role": "high_li_sensitivity_feed",
            "source_type": "source_backed_local_table",
            "data_scope": "Li, Na, K, Mg, Ca, Sr, Ba, TDS",
            "fields_used": "selected_case_study_feeds.csv",
            "quality_status": "simulation_allowed",
            "notes": "Used for feed-variance sensitivity after upstream pretreatment boundary.",
        },
        {
            "source_id": "marcellus_ne_pa_comparison",
            "source_group": "produced_water_feed",
            "citation_label": "peer-reviewed regional Marcellus screening row",
            "artifact_role": "comparison_card",
            "source_type": "peer_reviewed_screening_row",
            "data_scope": "Li, Mg, TDS",
            "fields_used": "selected_case_study_feeds.csv",
            "quality_status": "comparison_only_missing_major_ions",
            "notes": "Not used for PrOMMiS stage simulation or TEA while Na/Ca/Sr/Ba are missing.",
        },
        {
            "source_id": "bakken_high_na_stress",
            "source_group": "produced_water_feed",
            "citation_label": "peer-reviewed Bakken high-Li county screening row",
            "artifact_role": "stress_context_card",
            "source_type": "peer_reviewed_screening_row",
            "data_scope": "Li, Na, K, Sr, TDS",
            "fields_used": "selected_case_study_feeds.csv",
            "quality_status": "context_only_missing_divalents",
            "notes": "Not used for final PrOMMiS stage simulation or TEA while Mg/Ca/Ba are missing.",
        },
        {
            "source_id": "rezaee_des_topo_stage_anchor",
            "source_group": "stage_response_anchor",
            "citation_label": "TBAC(1):DA(2) DES + 10 wt% TOPO source paper",
            "artifact_role": "source_anchor_for_stage_response",
            "source_type": "literature_extraction_anchor",
            "data_scope": "optimized Li extraction, source selectivity, model-brine Li and Na extraction",
            "fields_used": "stage_response_generator.py anchor overrides",
            "quality_status": "source_anchor",
            "notes": "Anchors the generated stage-response surface while direct ePC-SAFT closure is not accepted.",
        },
    ]


def _lhs_samples(count: int, bounds: list[tuple[float, float]], seed: int) -> list[list[float]]:
    rng = random.Random(seed)
    dimensions: list[list[float]] = []
    for low, high in bounds:
        bins = list(range(count))
        rng.shuffle(bins)
        width = high - low
        values = [low + width * ((bin_index + rng.random()) / count) for bin_index in bins]
        dimensions.append(values)
    return [[dimensions[j][i] for j in range(len(bounds))] for i in range(count)]


def _base_design_row(
    *,
    design_id: str,
    domain: str,
    row_type: str,
    li_mg_l: float,
    na_mg_l: float,
    o_to_a_ratio: float,
    topo_wt_pct: float,
    source_anchor_flag: bool = False,
    validity_flag: str = "generated_design_point",
    extrapolation_flag: str = "within_declared_domain",
    synthetic_demo_data: bool | None = None,
    model_basis: str | None = None,
    backend_name: str | None = None,
    direct_epcsaft_closure: bool | None = None,
) -> dict[str, object]:
    synthetic = STAGE_RESPONSE_BACKEND.synthetic_demo_data if synthetic_demo_data is None else synthetic_demo_data
    model = STAGE_RESPONSE_BACKEND.model_basis if model_basis is None else model_basis
    backend = STAGE_RESPONSE_BACKEND.backend_name if backend_name is None else backend_name
    direct = STAGE_RESPONSE_BACKEND.direct_epcsaft_closure if direct_epcsaft_closure is None else direct_epcsaft_closure
    return {
        "design_id": design_id,
        "domain": domain,
        "row_type": row_type,
        "li_mg_L": li_mg_l,
        "na_mg_L": na_mg_l,
        "na_li_mass_ratio": na_mg_l / li_mg_l,
        "o_to_a_ratio": o_to_a_ratio,
        "topo_wt_pct": topo_wt_pct,
        "temperature_C": TEMPERATURE_C,
        "aqueous_pH": AQUEOUS_PH,
        "solvent_base": SOLVENT_BASE,
        "TBAC_to_DA_molar_ratio": TBAC_TO_DA,
        "source_anchor_flag": source_anchor_flag,
        "synthetic_demo_data": synthetic,
        "model_basis": model,
        "backend_name": backend,
        "direct_epcsaft_closure": direct,
        "validity_flag": validity_flag,
        "extrapolation_flag": extrapolation_flag,
    }


def design_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, (li, na_li, o_to_a, topo) in enumerate(
        _lhs_samples(625, [(1000.0, 2000.0), (5.0, 25.0), (0.5, 1.5), (5.0, 15.0)], 20260515),
        start=1,
    ):
        rows.append(
            _base_design_row(
                design_id=f"src_lhs_{index:03d}",
                domain="source-paper-valid",
                row_type="generated_source_domain",
                li_mg_l=li,
                na_mg_l=li * na_li,
                o_to_a_ratio=o_to_a,
                topo_wt_pct=topo,
                validity_flag="source_paper_valid_domain",
            )
        )

    for index, (li, na, o_to_a, topo) in enumerate(
        _lhs_samples(625, [(80.0, 300.0), (10000.0, 90000.0), (0.5, 2.0), (5.0, 15.0)], 20260516),
        start=1,
    ):
        rows.append(
            _base_design_row(
                design_id=f"pw_lhs_{index:03d}",
                domain="produced-water-centered",
                row_type="generated_produced_water_domain",
                li_mg_l=li,
                na_mg_l=na,
                o_to_a_ratio=o_to_a,
                topo_wt_pct=topo,
                validity_flag="produced_water_centered_domain",
                extrapolation_flag="outside_source_paper_li_na_range",
            )
        )

    rows.extend(
        [
            _base_design_row(
                design_id="source_anchor_optimized_10wt_topo",
                domain="source-paper-valid",
                row_type="source_anchor",
                li_mg_l=1000.0,
                na_mg_l=5000.0,
                o_to_a_ratio=1.0,
                topo_wt_pct=10.0,
                source_anchor_flag=True,
                validity_flag="source_paper_anchor_optimized",
                synthetic_demo_data=False,
                model_basis="source_paper_reported_anchor",
                backend_name="source_paper_anchor",
            ),
            _base_design_row(
                design_id="source_anchor_rsm_midpoint",
                domain="source-paper-valid",
                row_type="source_anchor",
                li_mg_l=1000.0,
                na_mg_l=15000.0,
                o_to_a_ratio=1.0,
                topo_wt_pct=10.0,
                source_anchor_flag=True,
                validity_flag="source_paper_anchor_rsm_midpoint",
                synthetic_demo_data=False,
                model_basis="source_paper_reported_anchor",
                backend_name="source_paper_anchor",
            ),
            _base_design_row(
                design_id="source_anchor_model_brine_li_na",
                domain="source-paper-valid",
                row_type="source_anchor",
                li_mg_l=1000.0,
                na_mg_l=1186696.5174129352,
                o_to_a_ratio=1.0,
                topo_wt_pct=10.0,
                source_anchor_flag=True,
                validity_flag="source_paper_anchor_model_brine",
                extrapolation_flag="source_anchor_na_burden_outside_lhs_domain",
                synthetic_demo_data=False,
                model_basis="source_paper_reported_anchor",
                backend_name="source_paper_anchor",
            ),
        ]
    )

    for feed in feed_rows():
        if feed["simulation_allowed_flag"] is not True:
            continue
        li = float(feed["Li_mg_L"])
        na = float(feed["Na_mg_L"])
        rows.append(
            _base_design_row(
                design_id=f"nominal_{feed['feed_id']}",
                domain="produced-water-centered",
                row_type="nominal",
                li_mg_l=li,
                na_mg_l=na,
                o_to_a_ratio=1.0,
                topo_wt_pct=10.0,
                validity_flag="produced_water_nominal_simulation_feed",
                extrapolation_flag="outside_source_paper_li_na_range",
            )
        )

    for index, (li, na, o_to_a, topo) in enumerate(
        itertools.product((80.0, 300.0), (10000.0, 90000.0), (0.5, 2.0), (5.0, 15.0)),
        start=1,
    ):
        rows.append(
            _base_design_row(
                design_id=f"pw_corner_{index:02d}",
                domain="produced-water-centered",
                row_type="corner",
                li_mg_l=li,
                na_mg_l=na,
                o_to_a_ratio=o_to_a,
                topo_wt_pct=topo,
                validity_flag="produced_water_corner_or_stress",
                extrapolation_flag="outside_source_paper_li_na_range",
            )
        )
    return rows


def _clip_fraction(value: float) -> float:
    return min(max(value, EPS), 1.0 - EPS)


def _fraction_to_d(fraction: float, o_to_a_ratio: float) -> float:
    return fraction / ((1.0 - fraction) * o_to_a_ratio)


def _logit(fraction: float) -> float:
    return math.log(fraction / (1.0 - fraction))


def _stage_anchor_override(row: dict[str, object]) -> tuple[float, float] | None:
    design_id = str(row["design_id"])
    if design_id == "source_anchor_optimized_10wt_topo":
        return 0.4857, 0.4857 / 4.41
    if design_id == "source_anchor_rsm_midpoint":
        return 0.455, 0.084
    if design_id == "source_anchor_model_brine_li_na":
        return 0.5163, 0.0997
    return None


def _stage_response(row: dict[str, object]) -> dict[str, object]:
    override = _stage_anchor_override(row)
    li = float(row["li_mg_L"])
    na = float(row["na_mg_L"])
    o_to_a = float(row["o_to_a_ratio"])
    topo = float(row["topo_wt_pct"])
    na_li = na / li
    if override is None:
        topo_effect = max(0.68, 1.0 - 0.0105 * (topo - 10.0) ** 2)
        li_conc_effect = 1.0 + 0.045 * math.tanh((li - 1000.0) / 700.0)
        na_pressure = max(0.0, math.log10(max(na_li, 1.0) / 5.0))
        domain_effect = 0.985 if row["domain"] == "produced-water-centered" else 1.0
        d_li = 0.9443904336 * topo_effect * li_conc_effect * (1.0 - 0.028 * min(na_pressure, 4.0))
        d_li *= domain_effect
        d_na = 0.1107408642 * (1.0 + 0.060 * min(na_pressure, 5.0))
        d_na *= 1.0 + 0.018 * max(0.0, topo - 10.0)
        d_na *= 0.95 if topo < 10.0 else 1.0
        k_li = _clip_fraction((d_li * o_to_a) / (1.0 + d_li * o_to_a))
        k_na = _clip_fraction((d_na * o_to_a) / (1.0 + d_na * o_to_a))
    else:
        k_li, k_na = override
    d_li = _fraction_to_d(k_li, o_to_a)
    d_na = _fraction_to_d(k_na, o_to_a)
    return {
        **{column: row[column] for column in DESIGN_COLUMNS if column in row},
        "k_Li": k_li,
        "k_Na": k_na,
        "logit_k_Li": _logit(k_li),
        "logit_k_Na": _logit(k_na),
        "Li_extraction_pct": 100.0 * k_li,
        "Na_extraction_pct": 100.0 * k_na,
        "D_Li": d_li,
        "D_Na": d_na,
        "Li_Na_selectivity_process": d_li / d_na,
        "Li_Na_selectivity_source_definition": k_li / k_na,
        "temperature_C": row["temperature_C"],
        "aqueous_pH": row["aqueous_pH"],
    }


def stage_rows(design: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = [_stage_response(row) for row in design]
    require_stage_response_labels(rows)
    return rows


def split_alamo_rows(stage: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    candidates = [row for row in stage if row["row_type"] != "source_anchor"]
    anchors = [row for row in stage if row["row_type"] == "source_anchor"]
    training: list[dict[str, object]] = []
    validation: list[dict[str, object]] = []
    for index, row in enumerate(candidates):
        if index % 5 == 0:
            validation.append(row)
        else:
            training.append(row)
    training.extend(anchors)
    return training, validation


def _notebook_cell(cell_type: str, source: str) -> dict[str, object]:
    cell: dict[str, object] = {"cell_type": cell_type, "metadata": {}, "source": source.splitlines(True)}
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def notebook_document() -> dict[str, object]:
    cells = [
        _notebook_cell("markdown", "# TBAC/DA DES + TOPO Produced-Water Lithium Case Study\n"),
        _notebook_cell(
            "markdown",
            "This revised Lithium_Extraction notebook preserves the compact interface philosophy of the upstream PrOMMiS tutorial while using the TBAC/DA DES + TOPO chemistry and produced-water feed basis required by the local case-study specification.\n",
        ),
        _notebook_cell(
            "code",
            "from lithium_extraction.prommis_case_study.stage_response_generator import generate_foundation_artifacts\n"
            "summary = generate_foundation_artifacts()\n"
            "summary\n",
        ),
        _notebook_cell("markdown", "## 1. Source and feed registers\n"),
        _notebook_cell("markdown", "## 2. Two-domain design\n"),
        _notebook_cell("markdown", "## 3. Source-anchored generated demonstration data\n"),
        _notebook_cell("markdown", "## 4. ALAMO training or frozen surrogate loading\n"),
        _notebook_cell("markdown", "## 5. ALAMO validation plots\n"),
        _notebook_cell("markdown", "## 6. SurrogateBlock evaluation\n"),
        _notebook_cell("markdown", "## 7. PrOMMiS single-stage model\n"),
        _notebook_cell("markdown", "## 8. PrOMMiS 1-5 stage sensitivity\n"),
        _notebook_cell("markdown", "## 9. Screening TEA and UQ\n"),
        _notebook_cell("markdown", "## 10. Figures and deck exports\n"),
        _notebook_cell("markdown", "## 11. Final pass summary\n"),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
            "case_study": {
                "active_solvent_system": "TBAC(1):DA(2) hydrophobic DES + TOPO",
                "original_prommis_notebook": "C:/Users/Tanner/Documents/git/prommis/docs/tutorials/pcsaft_lithium_sodium_case_study.ipynb",
                "stage_response_backend": STAGE_RESPONSE_BACKEND.backend_name,
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def copy_success_spec(root: Path) -> Path:
    source = root / "docs" / "plans" / "MASTER_LITHIUM_CASE_STUDY_SUCCESS_ONLY_AGENT_SPEC.md"
    target = root / "docs" / "plans" / "tbac_da_topo_success_only_case_study_spec.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return target


def generate_foundation_artifacts(root: Path | None = None) -> dict[str, object]:
    root = project_root() if root is None else Path(root)
    design = design_rows()
    stage = stage_rows(design)
    training, validation = split_alamo_rows(stage)

    _write_csv(root / "data/reference/produced_water/selected_case_study_feeds.csv", FEED_COLUMNS, feed_rows())
    _write_csv(
        root / "data/reference/produced_water/produced_water_feed_source_register.csv",
        SOURCE_REGISTER_COLUMNS,
        source_register_rows(),
    )
    _write_csv(root / "data/processed/tbac_da_topo_two_domain_lhs_design.csv", DESIGN_COLUMNS, design)
    _write_csv(root / "data/processed/tbac_da_topo_stage_response_data.csv", STAGE_COLUMNS, stage)
    _write_csv(root / "data/processed/tbac_da_topo_alamo_training_data.csv", ALAMO_COLUMNS, training)
    _write_csv(root / "data/processed/tbac_da_topo_alamo_validation_data.csv", ALAMO_COLUMNS, validation)

    notebook_path = root / "docs/tutorials/tbac_da_topo_produced_water_case_study.ipynb"
    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    notebook_path.write_text(json.dumps(notebook_document(), indent=2), encoding="utf-8")
    spec_path = copy_success_spec(root)

    return {
        "selected_feeds": len(feed_rows()),
        "source_register_rows": len(source_register_rows()),
        "design_rows": len(design),
        "stage_rows": len(stage),
        "training_rows": len(training),
        "validation_rows": len(validation),
        "notebook": str(notebook_path),
        "success_spec": str(spec_path),
    }


def main() -> None:
    print(json.dumps(generate_foundation_artifacts(), indent=2))


if __name__ == "__main__":
    main()
