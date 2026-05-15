# TBAC/DA DES + 10 wt% TOPO Li/Na Transfer-Variable Report

## Model Basis

The transfer table is a calibrated transfer-variable bridge for `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`. Produced-water rows use `surrogate_v1_calibrated_surface`; source-paper anchor rows remain separate as `bridge_v0_source_regressed`; no `direct_epcsaft_v1` rows are promoted.

## Generated Artifacts

- Design rows: `19` in `data/processed/tbac_da_topo_lhs_design.csv`.
- Transfer rows: `19` in `data/processed/tbac_da_topo_li_na_transfer_variables.csv`.
- Rows with extrapolation flags: `19`.
- `bridge_v0_source_regressed`: `3` rows
- `surrogate_v1_calibrated_surface`: `16` rows

## Nominal Smackover MS-2 Result

- Case id: `smackover_ms2_main_anchor`.
- One-stage Li extraction: `50.659%`.
- One-stage Na extraction: `5.667%`.
- Stage count: `3`.
- Cumulative Li recovery: `87.988%`.
- Cumulative Na recovery: `16.056%`.
- Li/Na selectivity: `17.090`.
- Validity: `calibrated_transfer_variable`; extrapolation: `outside_low_na_li_source_paper_design_space`.

## Acceptance Boundary

`TOPO_wt_pct_in_organic` is fixed at `10` in every generated row, and `TBAC_to_DA_molar_ratio` is fixed at `1:2`. Divalent cation extraction is not modeled; nonzero residual divalent values are only guardrails. Rows above the low-Na/Li source-paper design space are visibly flagged because produced-water sodium loads exceed the source-paper calibration domain.

## Transfer To Agent 3

Agent 3 should consume `D_Li`, `D_Na`, one-stage extraction percentages, cumulative recovery percentages, and the validity/extrapolation flags directly from `data/processed/tbac_da_topo_li_na_transfer_variables.csv`. Costing or staged-contacting outputs must keep the calibrated transfer-variable label unless a later direct ePC-SAFT validation closes the convention gap.

High-Na/Li flagged rows: `17`.
