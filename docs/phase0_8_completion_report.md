# Phase 0-9 Completion Report

Last updated: 2026-05-08

## Summary

Phases 0-9 are now pivoted to a Rezaee 2026 Li/Na bridge after divalent pretreatment. The selected Smackover produced-water site is still the source basis, but the extraction feed is a pretreated clean Li+Na stream. The previous HBTA/TOPO staged model remains a useful conventional-ligand comparison and future parameterization lane, but the current Phase 0-9 case-study basis is Rezaee DES/TOPO because it supplies the strongest package-facing evidence set: reported organic PC-SAFT-style parameters, organic binary interactions, reaction constants, Li/Na extraction responses, and SI aqueous/organic equilibrium-composition rows.

The active model status is `rezaee_source_regressed_li_na_bridge_with_direct_closure_gap`. It produces distribution coefficients and PrOMMiS/IDAES transfer variables from Rezaee source evidence, while carrying ePC-SAFT density regression, electrolyte stability, bounded LLE diagnostics, and a published-constant reactive convention scan as validity evidence. Direct accepted ePC-SAFT LLE phase splits and source-supported published-constant reactive closure remain future closure targets, not hidden assumptions. A separate calibrated surrogate now exercises the TDS, Li, and O/A surrogate contract so PrOMMiS/IDAES transfer and costing phases can be validated before calibrated response rows are available.

## Phase Status

| Phase | Status | Completion artifact | Remaining blocker |
|---:|---|---|---|
| 0 | complete as Rezaee-pivoted decision skeleton | `docs/case_study_charter.md` | User can still override flowrate, cost basis, solvent-cost assumptions, or presentation tone. |
| 1 | complete as source-backed feed plus pretreatment basis | `smackover_feed_catalog.csv`; `smackover_selected_base_feed_ms2.csv`; `rezaee_clean_li_na_pretreated_feed_basis.csv` | A proprietary/operator-specific sample or detailed pretreatment mass balance could replace MS-2 if provided. |
| 2 | complete as archived solvent-screening history | `docs/archive/legacy_solvent_choice_hbta_topo_gando_jang_2026_05_08/` | Active presentation chain now starts from Rezaee DES/TOPO. |
| 3 | complete as literature/source map skeleton | Rezaee input tables under `analyses/rezaee_2026_pcsaft_epcsaft/data/input/`; `zotero_parameter_source_inventory_2026_05_07.csv` | Rezaee direct-LLE closure still needs accepted phase splits across the surrogate domain. |
| 4 | complete as parameter inventory | `rezaee_2026_organic_pcsaft_parameters.csv`; `rezaee_2026_organic_binary_interactions.csv`; `rezaee_2026_reaction_constants.csv`; `des_nonassoc_fit.json` | The package still needs a stronger direct mixed-solvent reactive electrolyte-LLE objective. |
| 5 | complete as Li/Na distribution bridge | `rezaee_li_na_distribution_coefficients.csv`; `rezaee_li_na_distribution_bridge_report.md`; `rezaee_2026_reactive_convention_scan.md` | Distribution coefficients use an explicit equal-phase-volume O/A basis until stronger phase-amount data, direct LLE closure, and source-supported published-constant reactive closure are available. |
| 6 | complete as input space plus calibrated response surrogate | `rezaee_surrogate_input_variable_ranges.csv`; `rezaee_surrogate_seed_run_matrix.csv`; `rezaee_tds_li_oa_uq_predictions.csv`; `rezaee_tds_li_oa_uq_report.md` | Replace scaffold response columns with calibrated Rezaee/ePC-SAFT surrogate outputs before making physical response-surface claims. |
| 7 | complete as current PrOMMiS/IDAES transfer handoff with scaffold rows | `rezaee_tds_li_oa_prommis_idaes_transfer.csv`; `rezaee_calibrated_surrogate_mscontactor_costing_results.csv`; `epcsaft_prommis_bridge_contract.csv` | Upgrade the downstream case from algebraic transfer/costing readiness to a full MSContactor unit-model validation. |
| 8 | complete as IDAES costing input and result scaffold | `rezaee_tds_li_oa_calibrated_idaes_costing_input.csv`; `rezaee_calibrated_surrogate_mscontactor_costing_results.md` | Prices and cost coefficients are scenario assumptions, not vendor quotes or investment-grade TEA. |
| 9 | complete as selected-feed presentation basis with scaffold figures | `smackover_phase9_case_basis.md`; `rezaee_li_na_distribution_bridge_report.md`; `slides/deck.qmd`; `slides/deck.html`; `slides/deck.pptx` | Optional visual polish remains before external presentation, and calibrated surrogate outputs should replace scaffold figures when available. |

## Base Case Now Used

- Base feed: `MS-2 / MSPU 4-W1`
- Field: `Magnolia Smackover Production Unit`
- Formation: `Smackover`
- Li: `168 mg/L`
- TDS: `305,000 mg/L`
- Na: `64,100 mg/L`
- Ca: `36,900 mg/L`
- Mg: `3,310 mg/L`

## Pretreated Starting Basis

The extraction model does not start from the raw multication row. It starts after a pretreatment step removes the divalent cation burden and produces a clean Li+Na stream. The nominal clean stream uses Li `168 mg/L`, Na `64,100 mg/L`, and Na/Li mass ratio `381.55`. TDS remains a salinity/process feature until a concrete pretreatment mass-balance script updates chloride, alkalinity, and reagent additions.

The current input-space artifacts are:

- `data/reference/produced_water/rezaee_clean_li_na_pretreated_feed_basis.csv`
- `data/reference/produced_water/rezaee_surrogate_input_variable_ranges.csv`
- `data/reference/produced_water/rezaee_surrogate_seed_run_matrix.csv`
- `data/reference/produced_water/rezaee_clean_li_na_surrogate_input_space.md`

The current calibrated surrogate artifacts are:

- `data/reference/produced_water/rezaee_tds_li_oa_uq_predictions.csv`
- `data/reference/produced_water/rezaee_tds_li_oa_prommis_idaes_transfer.csv`
- `data/reference/produced_water/rezaee_tds_li_oa_calibrated_idaes_costing_input.csv`
- `data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.csv`
- `data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.md`

## Rezaee Bridge Result

For the selected Smackover base row at `O/A = 1`, using the Rezaee source-regressed Li/Na distribution bridge:

- One-stage Li extraction: `45.3660%`
- One-stage Na extraction: `8.9780%`
- One-stage `D_Li`: `0.8304`
- One-stage `D_Na`: `0.0986`
- One-stage `S_Li/Na`: `8.4185`
- Three-stage Li recovery: `83.6925%`
- Three-stage Na recovery: `24.5883%`
- Trust label: `anchored_by_rezaee_real_brine_high_na_li`

The bridge uses 32 Rezaee Li/Na extraction target rows and 26 machine-readable SI equilibrium-composition rows. The 26 rows are the active benchmark set; treat the Rezaee 2026 main-text reference to 36 equilibrium points as a clerical mismatch unless an original source workbook is later supplied. The bridge generates 60 Smackover sensitivity rows across TDS, Na, and O/A ratio for surrogate and PrOMMiS/IDAES handoff work.

The reactive convention scan now records the exact activity/reference-state blocker:

- Source-supported Eq. 14/15 activity variant combined median absolute ln residual: `35.0461`.
- Best simple numerical variant: `paper_eq14_no_activity_vs_inverse_k`.
- Best simple numerical combined median absolute ln residual: `9.5066`.
- Interpretation: no simple sign, reciprocal-K, gamma on/off, water, hydroxide, hydrogen, ammonium, or TOPO convention change closes the direct published-constant thermodynamic model.
- Section 3.2 direct equation replication now starts immediately after Table 8, uses Eqs. 14/15/17/18/19/20 directly, uses package calls only for activity coefficients, and starts from the Held-2014-S2-like no-Born constant-dielectric aqueous option with Table 9 organic interactions.
- Direct Held-2014/Table-9/pH-stoichiometric result: Li extraction AARD is about `100%` and selectivity AARD is about `56.36%`, versus the paper's `7.89%` and `8.63%` post-Table-9 AARD targets. The leading unresolved source input is the exact initial-mole/base-inventory convention behind Eq. 17, not a missing package equilibrium call.
- Section 3.2 basis inference: the SI aqueous rows are charge balanced and SI `xOH` tracks reported pH, but the organic total inferred from RLi is a median `3.64x` the organic total inferred from RNa when combined with Table 5 extraction percentages. This is the current concrete source-basis blocker for exact paper replication.

## What Was Skipped Or Downgraded

1. Direct accepted ePC-SAFT LLE phase splits for the Rezaee pseudo-DES system are not yet available across the surrogate region; the current package output is bounded diagnostic evidence.
2. HBTA/TOPO is no longer the flagship Li/Na bridge for Phase 0-9, but remains important as the conventional field-water comparison and future parameterization lane.
3. Divalent extraction remains out of scope; divalent ions are pretreatment/feed-context species.
4. REE remain `not_reported` for the selected source feed.
5. Investment-grade TEA remains out of scope, but the repository now emits Rezaee-specific PrOMMiS/IDAES transfer and costing inputs.
6. Calibrated surrogate response rows are process-integration test data; they are not calibrated thermodynamic evidence.

## Validation

Use:

```powershell
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
uv run python -m compileall -q analyses scripts data
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to pptx
```

Downstream PrOMMiS validation now uses the calibrated result mirror:

```powershell
data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.csv
data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.md
```

