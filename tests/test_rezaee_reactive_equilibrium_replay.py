from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analyses" / "rezaee_2026_pcsaft_epcsaft" / "scripts" / "rezaee_reactive_equilibrium_replay.py"
SUMMARY_JSON = (
    ROOT
    / "analyses"
    / "rezaee_2026_pcsaft_epcsaft"
    / "results"
    / "reaction_equilibrium"
    / "rezaee_2026_reactive_equilibrium_replay_summary.json"
)


def test_rezaee_reactive_replay_reports_calibrated_actual_row_closure() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr

    summary = json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    published = summary["published"]
    calibrated = summary["calibrated_paper_k"]

    assert published["status"] == "source_mismatch"
    assert calibrated["status"] == "source_replay_consistent"
    assert abs(calibrated["median_lnQ_minus_lnK"]["Li"]) < 1.0
    assert abs(calibrated["median_lnQ_minus_lnK"]["Na"]) < 1.0
    assert calibrated["median_abs_complex_error"]["RLi"] < 0.005
    assert calibrated["median_abs_complex_error"]["RNa"] < 0.01
