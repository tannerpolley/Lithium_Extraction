# Rezaee Calibrated Surrogate MSContactor/IDAES Costing Results

This PrOMMiS-side artifact consumes the Lithium_Extraction Rezaee clean Li/Na calibrated distribution surrogate. It verifies the staged transfer and costing interface shape using the current calibrated surrogate transfer table.

| Scenario | Case | Flow m3/day | Li recovery % | Li2CO3 kg/year | Breakeven $/kg | Net before tax $/year |
|---|---|---:|---:|---:|---:|---:|
| stress | corner_high_tds_low_li_low_oa | 1000 | 60.13 | 106702.59 | 8.60 | 363320.09 |
| base | nominal_ms2_clean_li_na | 1000 | 82.85 | 246997.33 | 6.19 | 3410614.11 |
| favorable | corner_low_tds_high_li_high_oa | 1000 | 93.22 | 496268.22 | 4.94 | 14918606.69 |

## Boundary

- The input rows are calibrated Rezaee distribution-surrogate rows for process-integration readiness.
- The module uses a formal IDAES/Pyomo flowsheet block and algebraic costing expressions.
- The rows remain high-Na/Li extrapolations beyond the original Rezaee DOE domain; do not call this direct reactive-LLE closure.
