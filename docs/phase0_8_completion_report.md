# Phase 0-8 Completion Report

Last updated: 2026-05-07

## Summary

Phases 0-8 are complete to the current Li/Na-first predictive scope. The old selective wrapper has been replaced for the main Smackover Phase 6-8 path by a source-regressed HBTA/TOPO reactive-stage model using the literature-supported `2 HBTA : 1 TOPO : 1 Li` complex stoichiometry, Shan/Gando stage targets, Zhang 2017 Li/Na selectivity, and ePC-SAFT aqueous activity coefficients when the local runtime can evaluate them. The remaining hard boundary is narrower and explicit: this is not yet a full multication reactive ePC-SAFT LLE model because the HBTA, TOPO, diluent, complex, and competing-ion parameter set is still missing.

## Phase Status

| Phase | Status | Completion artifact | Remaining blocker |
|---:|---|---|---|
| 0 | complete as decision skeleton | `docs/case_study_charter.md` | User can still override flowrate, cost basis, or presentation tone. |
| 1 | complete as source-backed feed skeleton | `smackover_feed_catalog.csv`; `smackover_selected_base_feed_ms2.csv` | A proprietary/operator-specific sample could replace MS-2 if provided. |
| 2 | complete as solvent-ranking skeleton | `non_ionic_solvent_literature_matrix.csv`; `solvent_candidate_scorecard_2026_05_07.csv`; `solvent_candidate_run_matrix_2026_05_07.csv` | D2EHDTPA/BuPhen, TBP/FeCl3, and D2EHPA/TBP backups still lack runnable local ePC-SAFT parameter payloads. |
| 3 | complete as literature/source map skeleton | `case_study_claim_source_map.csv`; `case_study_not_found_table.csv`; `solvent_candidate_literature_review_2026_05_07.md` | Zotero full-text verification did not find published HBTA/TOPO reaction constants sufficient to replace the source-regressed stage parameters with physical constants. |
| 4 | complete as parameter-gap inventory | `hbta_topo_parameter_inventory.csv`; `hbta_topo_parameter_runtime_notes.md` | HBTA, TOPO, diluent, complexes, Sr/Ba, and some anion/divalent runtime parameters remain unresolved. |
| 5 | complete as source-regressed Li/Na reaction-network model | `hbta_topo_reaction_network.csv`; `hbta_topo_reactive_fit_parameters.csv`; `hbta_topo_predictive_regression_dataset.csv` | Published full ePC-SAFT organic/complex parameters were not found; the current constants are source-regressed stage parameters. |
| 6 | complete as Li/Na predictive stage solve | `hbta_topo_reactive_stage_results.csv`; `hbta_topo_predictive_regression_residuals.csv`; `hbta_topo_predictive_parameter_uncertainty.csv`; `smackover_ms2_transfer_sensitivity.csv` | Extrapolated Smackover rows are not full multication reactive ePC-SAFT LLE outputs. |
| 7 | complete as PrOMMiS/IDAES stage handoff | `hbta_topo_reactive_prommis_stage_table.csv`; `smackover_prommis_transfer_handoff.csv`; `prommis_stage_mass_balance_skeleton.csv` | Full MSContactor unit-model expansion belongs in the downstream PrOMMiS environment. |
| 8 | complete as formal IDAES costing handoff and downstream run | `hbta_topo_idaes_costing_input.csv`; PrOMMiS `hbta_topo_idaes_costing_results.csv` | Prices and cost coefficients are scenario assumptions, not vendor quotes or investment-grade TEA. |

## Base Case Now Used

- Base feed: `MS-2 / MSPU 4-W1`
- Field: `Magnolia Smackover Production Unit`
- Formation: `Smackover`
- Li: `168 mg/L`
- TDS: `305,000 mg/L`
- Na: `64,100 mg/L`
- Ca: `36,900 mg/L`
- Mg: `3,310 mg/L`

## Skeleton Transfer Result

At `O/A = 1`, using the source-regressed Li/Na HBTA/TOPO reactive-stage model:

- One-stage Li extraction: `47.2846%`
- One-stage Na extraction: `0.0131%`
- Three-stage model Li extraction: near-total
- Three-stage Na extraction: `0.1160%`
- Trust label: `outside_literature_capacity_envelope_near_total_transfer`

The Gando regression residuals are `-0.062`, `+0.122`, and `-0.131` percentage points for the three Li cumulative extraction targets, and the Li/Na selectivity prediction remains just above the conservative `2100` lower-bound anchor. The near-total Smackover three-stage result is an extrapolated design signal, not a final physical claim. Formal costing is capped at the Shan/Gando source-backed `97.17%` three-stage lithium-recovery anchor.

## What Was Skipped Or Downgraded

1. Full multication reactive HBTA/TOPO ePC-SAFT LLE remains a documented gap because organic-phase, complex, and competing-ion parameters are still missing.
2. D2EHDTPA/BuPhen is now the best non-HBTA backup chemistry, but it is parameter-blocked in this repo. DBM/TOPO is downgraded to an unresolved historical search target unless a direct primary source is recovered.
3. REE were marked `not_reported` for the selected source feed.
4. Investment-grade TEA remains out of scope, but a downstream PrOMMiS IDAES/Pyomo costing module now consumes the Lithium handoff.
5. Full MSContactor unit-model expansion remains in PrOMMiS; this repository owns the transfer and costing input artifacts.

## Validation

Use:

```powershell
uv run python scripts\case_study\smackover_phase6_8_skeleton.py
uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py
uv run python -m compileall -q scripts data
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
```

Downstream PrOMMiS validation command:

```powershell
& "C:\ProgramData\Miniconda3\envs\prommis\python.exe" -m prommis.solvent_extraction.pcsaft_integration.hbta_topo_idaes_costing
```
