# TBAC/DA DES + 10 wt% TOPO Phase-Inventory Convention Scan

## Decision

No direct reactive-LLE result is promoted for the Agent 2 transfer-variable table. The available diagnostics leave the phase-inventory / reaction-coordinate reference-state convention unresolved, so direct ePC-SAFT remains a validity diagnostic rather than the model of record.

## Solvent And Case Boundary

- Solvent system: `90 wt% TBAC/DA DES + 10 wt% TOPO`.
- Active extraction scope: Li/Na after divalent pretreatment.
- Divalent cations are treated only as residual pretreatment-leakage guardrails.

## Convention Results

| Basis type | Closure status | Residual metric | Failure reason |
|---|---|---:|---|
| O/A as mass ratio | not_closed | 37.75847741297254 | phase-inventory / reaction-coordinate reference-state convention not resolved; do not promote direct reactive-LLE transfer variables |
| O/A as volume ratio | not_closed | 37.75847741297254 | phase-inventory / reaction-coordinate reference-state convention not resolved; do not promote direct reactive-LLE transfer variables |
| equal phase masses | not_closed | 37.75847741297254 | phase-inventory / reaction-coordinate reference-state convention not resolved; do not promote direct reactive-LLE transfer variables |
| equal phase volumes | not_closed | 37.75847741297254 | phase-inventory / reaction-coordinate reference-state convention not resolved; do not promote direct reactive-LLE transfer variables |
| density-corrected O/A | not_closed | 41.41804436254249 | phase-inventory / reaction-coordinate reference-state convention not resolved; do not promote direct reactive-LLE transfer variables |
| pH-stoichiometric H/OH basis | not_closed | 17.551718228347315 | phase-inventory / reaction-coordinate reference-state convention not resolved; do not promote direct reactive-LLE transfer variables |
| NH4/OH buffer basis | not_closed | 24.262806940679756 | phase-inventory / reaction-coordinate reference-state convention not resolved; do not promote direct reactive-LLE transfer variables |
| explicit reaction-coordinate basis | diagnostic_only_not_closed | not_lnQ_metric; max_extraction_pct_error=56.46 | reaction-coordinate replay matches algebraic limits but not a direct phase-equilibrium closure |
| best inverse-constant numerical variant | not_source_supported | 13.568652259064464 | lower residual but not the source-supported constant convention |
| direct ePC-SAFT option scan best case | not_closed | 33.7571925407821 | phase-inventory / reaction-coordinate reference-state convention not resolved; do not promote direct reactive-LLE transfer variables |

## Use In Case Study

The Agent 2 data package therefore uses `surrogate_v1_calibrated_surface` for produced-water transfer variables and keeps `bridge_v0_source_regressed` only for source-paper anchor rows. The `direct_epcsaft_v1` layer is explicitly not promoted because the direct closure checks do not pass the acceptance boundary.
