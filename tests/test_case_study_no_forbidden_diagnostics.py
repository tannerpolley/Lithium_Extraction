from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_FINAL_PHRASES = [
    "diagnostic",
    "diagnostic failure",
    "failed direct",
    "failed phase",
    "failed regression",
    "failed",
    "failure",
    "partial diagnostic",
    "not converged",
    "phase-inventory",
    "convention scan",
    "Trust Region Framework",
    "fabricated data",
    "fake results",
    "investment-grade",
    "vendor-grade",
    "plant-ready",
]


def _existing_final_facing_paths() -> list[Path]:
    candidates = [
        ROOT / "docs/tutorials/tbac_da_topo_produced_water_case_study.ipynb",
        ROOT / "results/tbac_da_topo_alamo_validation.md",
        ROOT / "results/tbac_da_topo_prommis_stage_results.md",
        ROOT / "results/tbac_da_topo_screening_tea.md",
        ROOT / "results/tbac_da_topo_success_gate_report.md",
        ROOT / "slides/case_study_tbac_da_topo_produced_water/deck.qmd",
        ROOT / "slides/case_study_tbac_da_topo_produced_water/deck.html",
    ]
    return [path for path in candidates if path.exists()]


def _notebook_markdown_and_outputs(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    pieces: list[str] = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            pieces.append("".join(cell["source"]))
        for output in cell.get("outputs", []):
            pieces.append(json.dumps(output, sort_keys=True))
    return "\n".join(pieces)


def _html_visible_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b[^>]*>.*?</style>", "", text, flags=re.IGNORECASE | re.DOTALL)
    return re.sub(r"<[^>]+>", " ", text)


def test_final_facing_artifacts_avoid_forbidden_phrases() -> None:
    scanned = _existing_final_facing_paths()
    assert scanned
    for path in scanned:
        if path.suffix == ".ipynb":
            text = _notebook_markdown_and_outputs(path)
        elif path.suffix == ".html":
            text = _html_visible_text(path)
        else:
            text = path.read_text(encoding="utf-8", errors="replace")
        lowered = text.lower()
        offenders = [phrase for phrase in FORBIDDEN_FINAL_PHRASES if phrase.lower() in lowered]
        assert not offenders, f"{path.relative_to(ROOT)} contains forbidden phrases: {offenders}"


def test_notebook_has_no_recorded_error_outputs() -> None:
    notebook_path = ROOT / "docs/tutorials/tbac_da_topo_produced_water_case_study.ipynb"
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    for index, cell in enumerate(notebook["cells"], start=1):
        for output in cell.get("outputs", []):
            assert output.get("output_type") != "error", f"notebook cell {index} contains an error output"
