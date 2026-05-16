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


def test_rezaee_reactive_replay_reports_phase_tagged_package_route() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr

    summary = json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    route = summary["package_phase_tagged_cross_phase"]
    figure_validation = summary["figure_validation"]
    paper_figures = figure_validation["paper_figures"]

    assert summary["row_count"] == 26
    assert summary["status"] == "source_mismatch"
    assert route["evaluated_rows"] == 26
    assert route["reaction_phase_scope"] == "phase_tagged_cross_phase"
    assert route["native_reaction_residual_size"] == 2
    assert route["max_element_balance_norm"] < 1.0e-12
    assert route["max_phase_charge_balance_norm"] < 1.0e-5
    assert summary["median_lnQ_minus_lnK"]["Li"] > 5.0
    assert summary["median_lnQ_minus_lnK"]["Na"] > 5.0
    assert summary["median_abs_complex_error_from_paper_K"]["RLi"] < 0.01
    assert summary["median_abs_complex_error_from_paper_K"]["RNa"] < 0.03
    assert figure_validation["status"] == "replay_owned_paper_figure_validation_complete"
    assert figure_validation["digitization"]["figure_count"] == 4
    assert paper_figures["figure_count"] == 4
    assert {entry["figure_id"] for entry in paper_figures["figures"]} == {"fig7", "fig8", "fig10", "fig11"}
    assert figure_validation["after_kij_aard_pct"]["Li_extraction"] < figure_validation["before_kij_aard_pct"]["Li_extraction"]
    assert figure_validation["after_kij_aard_pct"]["selectivity"] < figure_validation["before_kij_aard_pct"]["selectivity"]
