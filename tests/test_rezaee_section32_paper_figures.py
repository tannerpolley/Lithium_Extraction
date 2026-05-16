from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIGITIZE_SCRIPT = (
    ROOT
    / "analyses"
    / "rezaee_2026_pcsaft_epcsaft"
    / "scripts"
    / "digitize_rezaee_2026_paper_figures.py"
)
SCRIPT = (
    ROOT
    / "analyses"
    / "rezaee_2026_pcsaft_epcsaft"
    / "scripts"
    / "render_rezaee_2026_section32_paper_figures.py"
)
SUMMARY_JSON = (
    ROOT
    / "analyses"
    / "rezaee_2026_pcsaft_epcsaft"
    / "results"
    / "reaction_equilibrium"
    / "rezaee_2026_section32_paper_figures_summary.json"
)


def test_rezaee_section32_paper_figures_render() -> None:
    digitized = subprocess.run(
        [sys.executable, str(DIGITIZE_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert digitized.returncode == 0, digitized.stdout + digitized.stderr

    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr

    summary = json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    assert summary["figure_count"] == 4
    assert {entry["figure_id"] for entry in summary["figures"]} == {"fig7", "fig8", "fig10", "fig11"}
    for entry in summary["figures"]:
        assert Path(entry["png"]).exists()
        assert Path(entry["svg"]).exists()
        assert entry["row_count"] >= 20
