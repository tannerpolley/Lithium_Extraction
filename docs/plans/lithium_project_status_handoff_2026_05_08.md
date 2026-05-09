# Lithium Extraction Project Status And Handoff

Date: 2026-05-08

## Purpose

This handoff is for the next Lithium_Extraction agent. It summarizes the current state after the ePC-SAFT package integration pass, the Rezaee SI data update, the Li/Na-only scope correction, and the latest bounded validation runs.

For a shorter variable-selection handoff, read this first:

```text
docs/plans/rezaee_clean_li_na_compact_agent_handoff_2026_05_08.md
```

The active objective is narrow:

- Show lithium extraction from sodium after divalent pretreatment.
- Treat the selected produced-water site as a pretreated clean Li+Na extraction feed; divalent cations are removed before the Rezaee bridge starts.
- Do not claim divalent extraction or divalent phase/chemical equilibrium.
- Use ePC-SAFT where it is available and useful, but keep the presentation honest about source-regressed versus fully predictive package-owned thermodynamics.

## Current Branch State

Repository:

```text
C:\Users\Tanner\Documents\git\Lithium_Extraction
```

Active integration worktree used for this pass:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT\.worktrees\downstreams\Lithium_Extraction
```

Current integration branch:

```text
codex/epcsaft-local-integration-20260507-1
```

Latest pushed branch commit before this handoff:

```text
e5c0965 Use best-effort electrolyte LLE diagnostics
```

The normal main checkout at `C:\Users\Tanner\Documents\git\Lithium_Extraction` was still on `main` at commit `e8d67bf` during this handoff. The integration branch was `0 11` relative to `origin/main`, meaning it was not behind and was 11 commits ahead.

## Required Upstream Package State

Use current ePC-SAFT main from:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT
```

At handoff time ePC-SAFT main was at:

```text
9aa1419 Ignore Zotero exported references
```

The package-side capability needed by this project is the newer electrolyte LLE best-effort/result diagnostics. It was added in ePC-SAFT PR #42 and is present on current main. The downstream Lithium environment should be reinstalled from the local ePC-SAFT checkout before validation:

```powershell
uv pip install --force-reinstall "epcsaft @ file:///C:/Users/Tanner/Documents/git/ePC-SAFT"
```

Use Python 3.13 for this project. Earlier Python 3.12 environments caused install/build friction before the scientific tests even started.

## What Is Done

### Scope Clarified

The project is no longer trying to prove divalent extraction. The case-study claim is Li/Na separation after divalent pretreatment. Divalent ions can appear in feed context and literature motivation, but they should not be modeled as extracted species for the current objective.

The current clean-feed and surrogate input-space artifacts are:

```text
data/reference/produced_water/rezaee_clean_li_na_pretreated_feed_basis.csv
data/reference/produced_water/rezaee_surrogate_input_variable_ranges.csv
data/reference/produced_water/rezaee_surrogate_seed_run_matrix.csv
data/reference/produced_water/rezaee_clean_li_na_surrogate_input_space.md
analyses/rezaee_2026_pcsaft_epcsaft/results/surrogate_input_space/figures/rezaee_surrogate_input_ranges.png
```

These are input contracts, not surrogate response data. The next concrete script must consume the seed run matrix and emit extraction responses, distribution coefficients, selectivity, diagnostics, and validity flags before any optimizer-ready surrogate is claimed.

### Project Organization

The current branch organizes work under analysis folders:

- `analyses/rezaee_2026_pcsaft_epcsaft/`
- `analyses/hbta_topo_case_study/`
- `analyses/gando_2025_pcsaft_repro/`
- `analyses/electrolyte_lle_literature/`
- `analyses/yu_2024_figure6/`

Reusable parameter and model payloads live under:

- `data/reference/epcsaft_parameters/`
- `data/reference/epcsaft_parameter_fits/`
- `data/reference/extraction_models/`
- `data/reference/produced_water/`

### Rezaee Data, Replay, And Fit Lane

The Rezaee source files are now stored in the project:

```text
papers/pdf/Rezaee et al. - 2025 - Application of Response Surface Methodology for Selective Extraction of Lithium Using a Hydrophobic DES.pdf
papers/pdf/Rezaee et al. - 2025 - Supporting information - Application of Response Surface Methodology for Selective Extraction of Lithium.pdf
papers/pdf/Rezaee et al. - 2026 - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents A PC.pdf
papers/pdf/Rezaee et al. - 2026 - Supplementary material - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents.pdf
```

The matching Markdown source text is stored under `papers/md/`.

The 2025 SI equilibrium mole-fraction data was added from the Zotero SI attachment and converted into:

```text
analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2025_extraction_equilibrium_mole_fractions.csv
```

Generated summaries now show:

- `target_rows = 32`
- `equilibrium_rows = 26`
- Rezaee SI Tables S1/S2 are represented as 26 aqueous/organic equilibrium-composition rows.

The Rezaee smoke now uses `return_best_effort=True` for ePC-SAFT electrolyte LLE diagnostics. The current result should be interpreted as a package-plumbing and parameter-regression smoke, not a final extraction model:

- The diagnostic nonassociating DES pseudo-component density fit runs but currently reports `success=False` because the bounded regression terminates early. The fitted values are still recorded as diagnostics.
- Density metric: about `0.0103035189`.
- Electrolyte stability succeeded with `min_tpd` about `-0.534683658`.
- Electrolyte LLE result mode returns `status=success` because best-effort diagnostics are returned.
- The best-effort LLE did not produce an accepted physical split for this pseudo-DES setup; `split_detected=False`.
- Diagnostics show `acceptance_gate=predictive_budget_exhausted`, with collapsed/nonfavored split behavior.

The new important distinction: Rezaee 2026 does not close the extraction with a conventional same-species LLE flash. It assumes two negligibly miscible phases and closes Li/Na transfer through phase-specific ion-exchange reaction equilibrium. The new replay and fit diagnostics include that chemical-equilibrium layer:

- `scripts/rezaee_reactive_equilibrium_replay.py` evaluates Rezaee Eqs. 5/6 and 14/15 using package ePC-SAFT/PC-SAFT activity calls.
- With the paper Table 2 constants and paper Table 8/9 parameters, the 26 SI phase-composition rows give `status=source_mismatch`.
- Median `lnQ-lnK` is about `32.33` for Li and `37.76` for Na in the direct replay.
- `scripts/rezaee_reactive_equilibrium_fit.py` checks Eqs. 5/6 directly at the experimental SI phase compositions and runs bounded Rezaee-style refits.
- `scripts/rezaee_reactive_convention_scan.py` scans the common activity/reference-state alternatives so the direct-closure gap is reproducible instead of speculative.
- `scripts/rezaee_reactive_epcsaft_option_scan.py` keeps Table 2 constants, Table 8 organic complex parameters, and Table 9 organic binary interactions fixed while scanning aqueous ePC-SAFT options. The Held-2014-style no-Born constant-dielectric cases are included and are the most relevant starting point for this paper.
- `scripts/rezaee_section32_basis_inference.py` back-calculates phase totals from the 26 Table 5 extraction percentages and SI equilibrium mole fractions before any solver tuning. It shows the SI aqueous rows are charge balanced and OH follows pH, but the organic phase total inferred from RLi is a median `3.64x` the total inferred from RNa.
- `scripts/rezaee_section32_equilibrium_replication.py` starts at the text immediately after Table 8 and implements Eqs. 14, 15, 17, 18, 19, and 20 directly. The package is used only for activity coefficients, not for package-owned equilibrium solving.
- Published constants/parameters give a combined median absolute ln residual of about `35.06`.
- The source-supported convention scan variant is `paper_eq14_with_activity_vs_paper_k` with combined median absolute ln residual about `35.0461`.
- The best simple numerical scan variant is `paper_eq14_no_activity_vs_inverse_k`, but it is not source-supported and still has combined median absolute ln residual about `9.5066`.
- The scan rules out a simple one-line fix from gamma on/off, reciprocal constants, inverse quotient, water/OH omission, H+/NH4+ substitution, or TOPO-reactant inclusion.
- The aqueous option scan rules out a Born/dielectric switch as the main issue. The best scanned aqueous option still leaves a combined median absolute ln residual of about `33.76`, and the Held-2014-style no-Born cases do not close the direct published-constant model.
- The Section 3.2 direct equation replication gives about `100%` Li extraction AARD and about `56.36%` selectivity AARD for the direct Held-2014-S2/no-Born/Table-9/pH-stoichiometric case, compared with the paper's post-Table-9 AARD targets of `7.89%` and `8.63%`.
- Rezaee 2026 says the thermodynamic model used `36` equilibrium data points, while the current machine-readable SI extraction has `26` equilibrium-composition rows. The user has decided to treat the 26 rows as the intended benchmark set and the 36-row statement as a clerical mismatch unless a source workbook is later supplied.
- The highest-value next source task is now locating or reconstructing the exact Section 3.2 initial-mole/phase-amount convention behind Eq. 17. The main-text DOE table exposes pH, but the exact initial moles and phase totals used by the paper's reaction-coordinate loop are not listed there, and the SI organic complex mole fractions are not directly conservation-consistent with the Table 5 extraction percentages under a one-RLi/one-Li and one-RNa/one-Na assumption.
- Holding the published constants would require median RLi/RNa activity coefficients of about `3.33e-15` and `1.31e-18`, while the package computes about `0.38` and `0.027` from the published Table 8/9 parameters. This is the direct numerical source of the gap.
- Refitting RLi/RNa parameters and organic `k_ij` while keeping paper constants fixed improves the median absolute ln residual to about `1.28`, but does not close it to the paper's reported extraction-percent AARD.
- Allowing constants to move as diagnostics reduces the median absolute ln residual to about `0.92`, but the fitted constants move far away from Table 2. Treat that as evidence of a source/reference-state or implementation-convention gap, not as the published Rezaee model.

Important files:

```text
analyses/rezaee_2026_pcsaft_epcsaft/README.md
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_2025_target_summary.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_des_epcsaft_parameter_smoke.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_equilibrium_replay.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_equilibrium_fit.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_convention_scan.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_reactive_epcsaft_option_scan.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_section32_basis_inference.py
analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_section32_equilibrium_replication.py
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2025_extraction_target_summary.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2025_extraction_equilibrium_summary.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_des_parameter_fit_summary.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_reactive_equilibrium_replay.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_reactive_equilibrium_fit.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_reactive_convention_scan_summary.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_reactive_epcsaft_option_scan_summary.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_section32_basis_inference_rows.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_section32_equilibrium_replication_rows.csv
analyses/rezaee_2026_pcsaft_epcsaft/results/smoke/rezaee_2026_epcsaft_phase_equilibrium_smoke.json
analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_reactive_equilibrium_replay.md
analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_reactive_equilibrium_fit.md
analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_reactive_convention_scan.md
analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_reactive_epcsaft_option_scan.md
analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_section32_basis_inference.md
analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_section32_equilibrium_replication.md
```

### HBTA/TOPO Comparison Lane

The HBTA/TOPO lane is no longer the current flagship Li/Na case-study bridge. It remains a useful conventional-ligand comparison and future parameterization lane, but the active Phase 0-9 bridge is Rezaee DES/TOPO after divalent pretreatment.

Current state:

- Source-regressed Li/Na reactive-stage model runs.
- Divalent pretreatment assumption is explicit.
- Stage table and costing bridge are generated.
- A synthetic Rezaee TDS/Li/OA scaffold now generates 523 finite rows for downstream interface validation.
- PrOMMiS consumes the scaffold in a Rezaee-named IDAES/Pyomo costing module and mirrors stress/base/favorable results back into Lithium.
- Current stage-results table has 54 rows.
- Solvent scorecard runs and ranks Rezaee DES/TOPO as the flagship system.

Important files:

```text
analyses/hbta_topo_case_study/README.md
analyses/hbta_topo_case_study/scripts/hbta_topo_reactive_stage_solve.py
analyses/hbta_topo_case_study/scripts/solvent_candidate_scorecard.py
data/reference/extraction_models/gando_2025/hbta_topo_reactive_fit.json
data/reference/produced_water/hbta_topo_reactive_stage_results.csv
data/reference/produced_water/hbta_topo_reactive_model_report.md
data/reference/produced_water/solvent_candidate_scorecard_2026_05_07.csv
data/reference/produced_water/solvent_candidate_run_matrix_2026_05_07.csv
data/reference/produced_water/rezaee_tds_li_oa_uq_predictions.csv
data/reference/produced_water/rezaee_tds_li_oa_prommis_idaes_transfer.csv
data/reference/produced_water/rezaee_tds_li_oa_calibrated_idaes_costing_input.csv
data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.csv
data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.md
```

The scorecard currently marks Rezaee DES/TOPO as the flagship source-regressed Li/Na bridge and HBTA/TOPO as the comparison/future parameterization lane.

### Gando 2025 Reproduction Lane

The Gando reproduction runner works and produces a compact nine-row result table. It is useful as a presentation/support lane for the Li/Na source-regressed model.

Important files:

```text
analyses/gando_2025_pcsaft_repro/README.md
analyses/gando_2025_pcsaft_repro/scripts/reproduce_gando_2025_pcsaft.py
data/multiphase/gando_2025_pcsaft_repro.csv
data/multiphase/gando_2025_pcsaft_repro.md
data/multiphase/gando_2025_pcsaft_repro.png
```

### Bounded ePC-SAFT Hard-Case Diagnostics

The ePC-SAFT electrolyte LLE hard cases are no longer allowed to hang indefinitely. The retry matrix and Hubach debug paths now return bounded structured diagnostics.

Latest bounded retry matrix evidence:

- 14 records.
- 2 successful/ok records.
- 12 non-ok records.
- 0 script-level timeouts in the latest bounded run.
- Main failure gates were `predictive_budget_exhausted` and `predictive_solve_failed`.

This closes the workflow problem of unbounded or opaque failures. It does not close the scientific hard case for Hubach/Jang fixed-species electrolyte LLE.

Important files:

```text
docs/epcsaft_lle_timeout_diagnostics_2026_05_07.md
analyses/hbta_topo_case_study/scripts/epcsaft_equilibrium_retry_matrix_2026_05_07.py
analyses/electrolyte_lle_literature/scripts/_debug_hubach_single_point.py
analyses/electrolyte_lle_literature/results/debug/hubach_single_point_debug_8s_20260507.json
data/reference/produced_water/epcsaft_equilibrium_retry_matrix_2026_05_07.md
```

Do not treat the current fixed-species Hubach/Jang ePC-SAFT LLE failures as blockers for the Li/Na presentation goal. Treat them as package diagnostic evidence and future package-hardening targets.

## Parameter Status

See also:

```text
docs/epcsaft_parameter_readiness_audit_2026_05_07.md
data/reference/epcsaft_parameters/README.md
data/reference/epcsaft_parameter_fits/README.md
data/reference/extraction_models/README.md
```

Current parameter picture:

| System or component group | Current state | Use now? | Still needed? |
|---|---|---:|---|
| Water and common simple ions | Available through package/reference payloads | Yes | Validate selected dataset per analysis. |
| `2024_Hubach` TBP/[emim][tcb]/LiCl method case | Local mirror exists under `data/reference/epcsaft_parameters/2024_Hubach/` | Diagnostic only | Not a HBTA/TOPO substitute. |
| `2024_Yu` TOP/[HOEMIM][Tf2N]/Li/Mg/Cl method case | Local payload exists under `data/reference/epcsaft_parameters/2024_Yu/` | Diagnostic/reference only | Do not use as HBTA/TOPO proof. |
| Rezaee DES/TOPO | SI targets, diagnostic DES pseudo-component fit, source-regressed Li/Na distribution bridge, and ePC-SAFT activity diagnostics exist | Yes, current flagship bridge | Direct published-constant thermodynamic replay has a source/reference-state gap. |
| HBTA/TOPO/sulfonated kerosene | Source-regressed stage model exists, but not pure ePC-SAFT component payloads | Comparison/future lane only | Full predictive ePC-SAFT parameter regression still needed for HBTA, TOPO, diluent, and organic complexes. |
| Divalent species | Out of active extraction scope | Feed context only | No for the current Li/Na objective. |

User-options status:

- `2024_Hubach/user_options.json` and `2024_Yu/user_options.json` use a `canonical_user_options` wrapper.
- Runtime flags such as `debug` should not be added to `user_options.json`.
- Script-level options should own solver budgets, debug flags, and result-mode choices.

## Validation Commands

Run these from the Lithium integration worktree or a clean clone of the updated branch:

```powershell
uv sync
uv pip install --force-reinstall "epcsaft @ file:///C:/Users/Tanner/Documents/git/ePC-SAFT"
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_2025_target_summary.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_des_epcsaft_parameter_smoke.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_equilibrium_replay.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_equilibrium_fit.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_convention_scan.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_epcsaft_option_scan.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_section32_basis_inference.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_section32_equilibrium_replication.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_li_na_distribution_bridge.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_tds_li_oa_calibrated_surrogate.py
uv run python analyses\hbta_topo_case_study\scripts\hbta_topo_reactive_stage_solve.py
uv run python analyses\hbta_topo_case_study\scripts\solvent_candidate_scorecard.py
uv run python analyses\gando_2025_pcsaft_repro\scripts\reproduce_gando_2025_pcsaft.py
```

PrOMMiS-side calibrated result mirror:

```powershell
data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.csv
data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.md
```

Run the bounded hard-case matrix only when you need package diagnostics:

```powershell
uv run python analyses\electrolyte_lle_literature\scripts\_debug_hubach_single_point.py --timeout-seconds 30
uv run python analyses\electrolyte_lle_literature\scripts\_debug_hubach_single_point.py --timeout-seconds 30
```

The retry matrix can generate a very large JSON diagnostics artifact. Do not commit the expanded JSON unless you intentionally want a full diagnostic snapshot. The Markdown summary and this handoff are usually enough.

## What Still Needs To Be Done

### Required For Current Li/Na Objective

1. Merge the integration branch into Lithium_Extraction main after review.
2. Rebuild or refresh the presentation/deck after presentation-facing scaffold edits.
3. Keep the claim scoped as source-regressed Li/Na extraction after divalent pretreatment.
4. In the deck and paper text, label Rezaee DES/TOPO as a source-regressed Li/Na bridge with ePC-SAFT diagnostic support, not as direct published-constant thermodynamic closure yet.
5. Treat scaffold response rows as process-integration test data until calibrated Rezaee/ePC-SAFT surrogate values replace them.

### Recommended Before Final Presentation

1. Add one small summary table to the deck showing:
   - current branch/commit,
   - Rezaee DES/TOPO bridge status,
   - Rezaee smoke status,
   - ePC-SAFT LLE hard-case diagnostic status,
   - explicit "divalents pretreated" assumption.
2. Update any slide text that implies full predictive ePC-SAFT closure for HBTA/TOPO or Rezaee.
3. Prefer the Rezaee source-regressed Li/Na bridge for audience-facing extraction results.
4. Use Rezaee diagnostics to show the package can ingest SI targets, evaluate ePC-SAFT/PC-SAFT activity terms, expose the published-constant convention gap, and still support a bounded source-regressed Li/Na bridge.

### Future Work Beyond Current Objective

These are not blockers for the current Li/Na presentation goal:

1. Regress full ePC-SAFT pure and interaction parameters for HBTA, TOPO, diluent or surrogate solvent, and organic lithium complex species.
2. Build a coupled reactive-LLE objective using source extraction targets, phase compositions, and current package primitives.
3. Add or install IPOPT/cyipopt only if the future objective specifically needs explicit IPOPT residual minimization.
4. Convert the Rezaee SI mole-fraction tables into a stronger regression objective that includes phase amounts or a defensible way to infer extraction percentages.
5. Continue hardening ePC-SAFT fixed-species electrolyte LLE for Hubach/Jang-style cases, but keep those as package-hardening tests rather than presentation blockers.

## Known Worktree Hygiene Notes

The latest validation reruns can modify generated outputs with local absolute paths. Do not assume every generated diff is a scientific change.

Known examples:

- `analyses/yu_2024_figure6/results/figure6/*` can change only because the worktree path changed.
- `data/reference/produced_water/epcsaft_equilibrium_retry_matrix_2026_05_07.json` can become very large after a full diagnostic run.
- `data/reference/produced_water/solvent_candidate_run_matrix_2026_05_07.csv` should retain the updated Rezaee row showing electrolyte LLE result-mode status as `success`, while still noting it remains diagnostic.

Before committing final presentation work, inspect:

```powershell
git status --short
git diff --stat
```

Commit only high-signal docs, source inputs, scripts, and curated final outputs. Avoid committing huge raw solver diagnostics unless the handoff explicitly requires that snapshot.

