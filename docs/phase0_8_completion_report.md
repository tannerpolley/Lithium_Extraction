# Phase 0-8 Completion Report

Last updated: 2026-05-07

## Summary

Phases 0-8 are complete to a defensible bridge level in this repository. The old selective wrapper has been replaced for the main Smackover Phase 6-8 path by a calibrated HBTA/TOPO reactive-stage model using the literature-supported `2 HBTA : 1 TOPO : 1 Li` complex stoichiometry and ePC-SAFT aqueous activity coefficients when the local runtime can evaluate them. The remaining hard boundary is the same: this is not yet a full predictive reactive ePC-SAFT LLE model because the HBTA, TOPO, diluent, and complex parameter set is still missing.

## Phase Status

| Phase | Status | Completion artifact | Remaining blocker |
|---:|---|---|---|
| 0 | complete as decision skeleton | `docs/case_study_charter.md` | User can still override flowrate, cost basis, or presentation tone. |
| 1 | complete as source-backed feed skeleton | `smackover_feed_catalog.csv`; `smackover_selected_base_feed_ms2.csv` | A proprietary/operator-specific sample could replace MS-2 if provided. |
| 2 | complete as solvent-ranking skeleton | `non_ionic_solvent_literature_matrix.csv` | Direct DBM/TOPO primary paper not found locally. |
| 3 | complete as literature/source map skeleton | `case_study_claim_source_map.csv`; `case_study_not_found_table.csv` | Full PDF/SI extraction could still improve reaction-constant search. |
| 4 | complete as parameter-gap inventory | `hbta_topo_parameter_inventory.csv`; `hbta_topo_parameter_runtime_notes.md` | HBTA, TOPO, diluent, complexes, Sr/Ba, and some anion/divalent runtime parameters remain unresolved. |
| 5 | complete as calibrated reaction-network bridge | `hbta_topo_reaction_network.csv`; `hbta_topo_reactive_fit_parameters.csv` | Published equilibrium constants and complex parameters were not found; the current constants are fitted bridge parameters. |
| 6 | complete as calibrated reactive-stage solve | `hbta_topo_reactive_stage_results.csv`; `smackover_ms2_transfer_sensitivity.csv` | Extrapolated Smackover rows are not full predictive reactive ePC-SAFT LLE outputs. |
| 7 | complete as PrOMMiS/IDAES stage handoff | `hbta_topo_reactive_prommis_stage_table.csv`; `smackover_prommis_transfer_handoff.csv`; `prommis_stage_mass_balance_skeleton.csv` | Full Pyomo/IDAES MSContactor solve still belongs in the downstream PrOMMiS environment. |
| 8 | complete as formal Class-5 costing scaffold | `hbta_topo_formal_costing_assumptions.csv`; `hbta_topo_formal_costing_results.csv`; `phase9_costing_skeleton.csv` | Prices and cost coefficients are scenario placeholders, not vendor quotes or investment-grade TEA. |

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

At `O/A = 1`, using the calibrated HBTA/TOPO reactive-stage model:

- One-stage Li extraction: `47.2846%`
- One-stage Na extraction: `0.0131%`
- Three-stage model Li extraction: near-total
- Three-stage Na extraction: `0.1160%`
- Trust label: `outside_literature_capacity_envelope_near_total_transfer`

The near-total three-stage result is an extrapolated design signal, not a final physical claim. Formal costing is capped at the Shan/Gando source-backed `97.17%` three-stage lithium-recovery anchor.

## What Was Skipped Or Downgraded

1. Full predictive reactive HBTA/TOPO ePC-SAFT LLE remains a documented gap because organic-phase and complex parameters are still missing.
2. DBM/TOPO was kept as a backup search target because the direct primary paper was not found locally.
3. REE were marked `not_reported` for the selected source feed.
4. Investment-grade TEA remains out of scope, but a formal Class-5 scenario-costing table now exists.
5. Full Pyomo/IDAES solve was downgraded to runnable staged handoff tables in this repo because the active `uv` environment does not include Pyomo/IDAES.

## Validation

Use:

```powershell
uv run python scripts\case_study\smackover_phase6_8_skeleton.py
uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py
uv run python -m compileall -q scripts data
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
```
