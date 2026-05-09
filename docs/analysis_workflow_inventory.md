# Analysis Workflow Inventory

Date: 2026-05-07

2026-05-08 update: the active Phase 0-9 case-study basis is now the Rezaee DES/TOPO Li/Na bridge after divalent pretreatment. HBTA/TOPO workflows remain comparison and future-parameterization lanes, not the current flagship presentation path.

This is the fork/test handoff for Codex agents working in `Lithium_Extraction`.

The implementation scripts now live under `analyses/<analysis_id>/scripts/`. Legacy root commands under `scripts/` are compatibility wrappers only.

## Repository Layout

| Path | Role | Edit policy |
|---|---|---|
| `analyses/<analysis_id>/README.md` | Human workflow summary | Update when commands, scope, or dependency status changes. |
| `analyses/<analysis_id>/analysis.yaml` | Machine-readable analysis metadata | Update when inputs, outputs, or validation commands change. |
| `analyses/<analysis_id>/scripts/` | Analysis-owned implementation scripts | Edit these for scientific workflow changes. |
| `scripts/<legacy_path>/` | Thin wrappers for old commands | Do not put new analysis logic here. |
| `scripts/epcsaft_compat.py` | Shared compatibility bridge for current ePC-SAFT package calls | Keep until package-side legacy migration helpers replace it. |
| `data/reference/produced_water/` | Shared case-study reference and generated handoff tables | Treat as the current cross-analysis artifact surface. |
| `data/reference/epcsaft_parameters/` | Shared ePC-SAFT parameter payloads | Test carefully when changing; multiple analyses read these. |
| `data/multiphase/` | Legacy generated LLE/multiphase outputs | Still used by docs/slides; migrate only with a focused output-path pass. |

## Analysis Map

| Analysis | Implementation path | ePC-SAFT reliance | Fork/test priority | Commands to run |
|---|---|---|---|---|
| Brine composition screening | `analyses/brine_composition_screening/scripts/` | None for the composition screen itself. It produces the feed/candidate basis that the Rezaee/ePC-SAFT and PrOMMiS/IDAES workflows can consume. | Highest for feed-basis and basin-selection work. | `uv run python analyses\brine_composition_screening\scripts\build_brine_screening_study.py` |
| Rezaee 2025/2026 Li/Na bridge | `analyses/rezaee_2026_pcsaft_epcsaft/scripts/` | Required for current Phase 0-9 presentation. Provides Rezaee source targets, clean Li+Na post-pretreatment input space, DES/TOPO parameter smoke, reactive-equilibrium diagnostics, aqueous option scans, direct Section 3.2 basis inference and equation replication, convention-scan guardrails, and PrOMMiS/IDAES transfer handoff. | Highest for presentation/case-study work. | `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_2025_target_summary.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_des_epcsaft_parameter_smoke.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_surrogate_input_space.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_equilibrium_replay.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_equilibrium_fit.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_convention_scan.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_epcsaft_option_scan.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_section32_basis_inference.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_section32_equilibrium_replication.py`; `uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_li_na_distribution_bridge.py` |
| HBTA/TOPO case study | `analyses/hbta_topo_case_study/scripts/` | Comparison/future-parameterization lane. HBTA/TOPO stage model is source-regressed surrogate, not full predictive reactive LLE. | Medium; useful for conventional-ligand comparison, not the active Phase 0-9 proof. | `uv run python analyses\hbta_topo_case_study\scripts\hbta_topo_reactive_stage_solve.py`; `uv run python analyses\hbta_topo_case_study\scripts\solvent_candidate_scorecard.py`; legacy Rezaee smoke wrapper: `uv run python analyses\hbta_topo_case_study\scripts\rezaee_des_epcsaft_parameter_smoke.py` |
| Electrolyte LLE literature | `analyses/electrolyte_lle_literature/scripts/` | Required. Hubach/Jang are direct hard cases for `ePCSAFTMixture.equilibrium(kind="electrolyte_lle")`. | High if testing upstream ePC-SAFT fixes; not a routine fast suite. | `uv run python analyses\electrolyte_lle_literature\scripts\gando_2025_three_stage_crossflow.py`; hard case: `uv run python analyses\electrolyte_lle_literature\scripts\_debug_hubach_single_point.py --timeout-seconds 30` |
| Gando 2025 PC-SAFT repro | `analyses/gando_2025_pcsaft_repro/scripts/` | Required for package-backed reproduction and selective-stage helper. | High for validating Gando chemistry set assumptions. | `uv run python analyses\gando_2025_pcsaft_repro\scripts\reproduce_gando_2025_pcsaft.py` |
| Yu 2024 Figure 6 | `analyses/yu_2024_figure6/scripts/` | Mixed. Digitized recreation is stable; reactive wrapper is preferred; direct package script is diagnostic. | Medium for extra literature evidence; useful for ePC-SAFT LLE diagnostics. | `uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_digitized_recreation.py`; `uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_reactive_replication.py` |

## ePC-SAFT-Dependent Scripts

These scripts should be included when a fork is meant to test the current ePC-SAFT package:

```text
analyses/hbta_topo_case_study/scripts/epcsaft_equilibrium_retry_matrix_2026_05_07.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_des_epcsaft_parameter_smoke.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_equilibrium_replay.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_equilibrium_fit.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_convention_scan.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_epcsaft_option_scan.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_section32_basis_inference.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_section32_equilibrium_replication.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_li_na_distribution_bridge.py
analyses/hbta_topo_case_study/scripts/rezaee_des_epcsaft_parameter_smoke.py
analyses/electrolyte_lle_literature/scripts/_debug_hubach_single_point.py
analyses/electrolyte_lle_literature/scripts/hubach_2024_figure7_rwoa_replication.py
analyses/electrolyte_lle_literature/scripts/jang_2017_stage2_li_na_tbp_d2ehpa.py
analyses/gando_2025_pcsaft_repro/scripts/reproduce_gando_2025_pcsaft.py
analyses/yu_2024_figure6/scripts/yu_2024_figure6_replication.py
```

Expected current status:

- ePC-SAFT package confidence tests pass upstream.
- Hubach and Jang stability calculations return quickly.
- Hubach single-point electrolyte-LLE diagnostics now return structured budget-exhausted `SolutionError` payloads when the timeout-enabled wrapper is used. The current evidence file is `analyses/electrolyte_lle_literature/results/debug/hubach_single_point_debug_8s_20260507.json`.
- Hubach/Jang hard cases still do not converge as predictive fixed-species LLE in the current package; treat them as diagnostic hard cases, not routine validation.
- ePC-SAFT issue #37 tracks the remaining hard-case convergence and diagnostic polish work.

## Recommended Fork Validation Ladder

For a downstream Lithium_Extraction fork that wants to test ePC-SAFT changes:

```powershell
uv run python -m compileall -q scripts analyses data
uv run python analyses\brine_composition_screening\scripts\build_brine_screening_study.py
uv run python analyses\hbta_topo_case_study\scripts\hbta_topo_reactive_stage_solve.py
uv run python analyses\hbta_topo_case_study\scripts\rezaee_des_epcsaft_parameter_smoke.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_convention_scan.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_epcsaft_option_scan.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_surrogate_input_space.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_section32_basis_inference.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_section32_equilibrium_replication.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_li_na_distribution_bridge.py
uv run python analyses\hbta_topo_case_study\scripts\solvent_candidate_scorecard.py
uv run python analyses\gando_2025_pcsaft_repro\scripts\reproduce_gando_2025_pcsaft.py
uv run python analyses\electrolyte_lle_literature\scripts\gando_2025_three_stage_crossflow.py
uv run python analyses\hbta_topo_case_study\scripts\epcsaft_equilibrium_retry_matrix_2026_05_07.py --timeout-seconds 25
```

Run these only when explicitly testing hard electrolyte-LLE behavior:

```powershell
uv run python analyses\electrolyte_lle_literature\scripts\_debug_hubach_single_point.py --timeout-seconds 30
uv run python analyses\electrolyte_lle_literature\scripts\jang_2017_stage2_li_na_tbp_d2ehpa.py --mode single
```

## Legacy Commands

These still work through wrappers for old handoff docs:

```powershell
uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py
uv run python scripts\case_study\solvent_candidate_scorecard.py
uv run python scripts\lle\gando_2025_three_stage_crossflow.py
uv run python scripts\gando_2025_pcsaft_repro\reproduce_gando_2025_pcsaft.py
uv run python scripts\Yu_2024_analysis\yu_2024_figure6_reactive_replication.py
```

Prefer the `analyses/` commands in new docs and new Codex plans.
