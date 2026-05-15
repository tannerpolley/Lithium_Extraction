# TBAC/DA DES + TOPO PrOMMiS/IDAES Stage Results

These rows come from real PrOMMiS `SolventExtraction` objects containing IDAES `MSContactor` units. Li and Na transfer are active material-transfer constraints. Chloride transfer is held inactive for the Li/Na extraction boundary.

| Case | Final Li recovery (%) | Final Na co-transfer (%) | Max mass-balance residual (mol/h) |
|---|---:|---:|---:|
| smackover_ms2_main_1stage | 45.681 | 10.714 | 4.547e-13 |
| smackover_ms2_main_3stage | 83.770 | 29.008 | 4.547e-13 |
| smackover_ms2_main_5stage | 95.100 | 43.740 | 4.547e-13 |
| smackover_high_observed_sensitivity_3stage | 83.911 | 28.900 | 4.547e-13 |

Model basis: source-anchored generated demonstration stage-response data propagated through IDAES AlamoSurrogate and PrOMMiS/IDAES unit models.
