# Rezaee TDS-Li-OA Calibrated Distribution Surrogate

Date: 2026-05-08

## Purpose

This dataset is a deterministic calibrated surrogate-run matrix for exercising the Lithium_Extraction to PrOMMiS/IDAES workflow with Rezaee Section 3.2 distribution-coefficient outputs. It consumes the upstream ePC-SAFT Rezaee DOE-basis surface results and fits a lightweight log-distribution response surface for fast UQ/design sweeps.

## Scope

- Rows: `523`
- Random seed: `20260508`
- Model basis label: `calibrated_rezaee_section32_doe_basis_surface_distribution_surrogate`
- Upstream rows: `31` from `C:\Users\Tanner\Documents\git\ePC-SAFT\analyses\2026_rezaee\data\processed\rezaee_2026_section32_revised_31_run_results.csv`
- UQ variables: TDS feature, Li feed concentration, organic/aqueous mass ratio.
- Fixed chemistry variables: T = 23 C, pH = 10.4, TOPO = 10 wt%, residual divalent = 0 mg/L except guardrail rows.

## Costing Readiness Scenarios

| Scenario | Li recovery used (%) | Li2CO3 t/year | Net before tax (million USD/year) |
|---|---:|---:|---:|
| stress | 74.47 | 132.14 | 0.59 |
| base | 87.99 | 262.31 | 3.67 |
| favorable | 90.83 | 483.56 | 14.52 |

## Validation Summary

- Status: `passed`
- Finite outputs: `True`
- Nominal MS-2 row count: `1`
- Li extraction range: `30.18-61.38%`
- Na extraction range: `2.67-9.76%`
- Phase-ratio-corrected D_Li range: `0.812-1.153`
- Phase-ratio-corrected D_Na range: `0.05491-0.07209`

## Figures

![Li extraction surrogate](figures/calibrated_li_extraction_surface.png)

![Selectivity surrogate](figures/calibrated_selectivity_vs_na_li.png)

![Costing scenarios](figures/calibrated_costing_scenarios.png)

## Boundary

This is a surrogate over the calibrated Rezaee Section 3.2 DOE-basis surface, not a new direct reactive-LLE closure. Rows outside the Rezaee Na/Li training range are flagged and should be interpreted as produced-water extrapolations.
