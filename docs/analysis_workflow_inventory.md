# Analysis Workflow Inventory

Date: 2026-05-08

This is the fork/test handoff for Codex agents working in `Lithium_Extraction`.
The active Phase 0-9 case-study basis is the Rezaee DES/TOPO Li/Na bridge after
divalent pretreatment. HBTA/TOPO artifacts are historical only and are not part
of the active working tree.

## Repository Layout

| Path | Role | Edit policy |
|---|---|---|
| `analyses/<analysis_id>/README.md` | Human workflow summary | Update when commands, scope, or dependency status changes. |
| `analyses/<analysis_id>/analysis.yaml` | Machine-readable analysis metadata | Update when inputs, outputs, or validation commands change. |
| `analyses/<analysis_id>/scripts/` | Analysis-owned implementation scripts | Edit these for scientific workflow changes. |
| `scripts/epcsaft_compat.py` | Shared compatibility bridge for current ePC-SAFT package calls | Keep until package-side migration helpers replace it. |
| `data/reference/produced_water/` | Shared current Rezaee/Smackover handoff tables | Keep curated cross-analysis artifacts only. |
| `data/reference/epcsaft_parameters/` | Shared ePC-SAFT parameter payloads | Test carefully when changing; multiple analyses read these. |
| `data/reference/smackover_sar_li/` | Smackover SAR source bundle inputs and metadata | Source/reference data only; generated rasters stay out of git. |

## Analysis Map

| Analysis | Implementation path | ePC-SAFT reliance | Fork/test priority | Commands to run |
|---|---|---|---|---|
| Brine composition screening | `analyses/brine_composition_screening/scripts/` | None for the composition screen itself. | Highest for feed-basis and basin-selection work. | `uv run python analyses\brine_composition_screening\scripts\build_brine_screening_study.py` |
| Rezaee 2025/2026 Li/Na bridge | `analyses/rezaee_2026_pcsaft_epcsaft/scripts/` | Required for current case-study transfer variables, ePC-SAFT smoke, and surrogate handoff. | Highest for presentation/case-study work. | `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_2025_target_summary.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_des_epcsaft_parameter_smoke.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_surrogate_input_space.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_tds_li_oa_calibrated_surrogate.py` |
| Electrolyte LLE literature | `analyses/electrolyte_lle_literature/scripts/` | Required for Hubach/Jang hard cases and Gando literature benchmark surrogates. | High if testing upstream ePC-SAFT fixes; not a routine fast suite. | `uv run python analyses\electrolyte_lle_literature\scripts\gando_2025_three_stage_crossflow.py`; hard case: `uv run python analyses\electrolyte_lle_literature\scripts\_debug_hubach_single_point.py --timeout-seconds 30` |
| Yu 2024 Figure 6 | `analyses/yu_2024_figure6/scripts/` | Mixed. Digitized recreation is stable; direct package script is diagnostic. | Medium for extra literature evidence and ePC-SAFT diagnostics. | `uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_digitized_recreation.py`; `uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_reactive_replication.py` |
| Smackover SAR Li reference | `analyses/smackover_sar_li_reference/scripts/` | None. | Reference only. | Run manually only when regenerating SAR-derived maps from `data/reference/smackover_sar_li/`. |

## ePC-SAFT-Dependent Scripts

These scripts should be included when a fork is meant to test the current
ePC-SAFT package:

```text
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_des_epcsaft_parameter_smoke.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_equilibrium_replay.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_equilibrium_fit.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_convention_scan.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_epcsaft_option_scan.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_section32_basis_inference.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_section32_equilibrium_replication.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_li_na_distribution_bridge.py
analyses/electrolyte_lle_literature/scripts/_debug_hubach_single_point.py
analyses/electrolyte_lle_literature/scripts/hubach_2024_figure7_rwoa_replication.py
analyses/electrolyte_lle_literature/scripts/jang_2017_stage2_li_na_tbp_d2ehpa.py
analyses/yu_2024_figure6/scripts/yu_2024_figure6_replication.py
```

Expected current status:

- ePC-SAFT package confidence tests pass upstream.
- Hubach/Jang hard cases still do not converge as predictive fixed-species LLE
  in the current package; treat them as diagnostic hard cases, not routine
  validation.
- ePC-SAFT issue #37 tracks the remaining hard-case convergence and diagnostic
  polish work.

## Recommended Validation Ladder

```powershell
uv run python -m compileall -q scripts analyses data
uv run python analyses\brine_composition_screening\scripts\build_brine_screening_study.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_2025_target_summary.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_des_epcsaft_parameter_smoke.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_surrogate_input_space.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_tds_li_oa_calibrated_surrogate.py
uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_digitized_recreation.py
uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_reactive_replication.py
uv run python analyses\electrolyte_lle_literature\scripts\gando_2025_three_stage_crossflow.py
```

Run these only when explicitly testing hard electrolyte-LLE behavior:

```powershell
uv run python analyses\electrolyte_lle_literature\scripts\_debug_hubach_single_point.py --timeout-seconds 30
uv run python analyses\electrolyte_lle_literature\scripts\jang_2017_stage2_li_na_tbp_d2ehpa.py --mode single
```
