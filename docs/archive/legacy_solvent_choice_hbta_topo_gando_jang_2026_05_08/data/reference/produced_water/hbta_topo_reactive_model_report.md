# HBTA/TOPO Reactive Stage Model And Costing

## What Changed

The old Smackover Phase 6-8 path used a selective wrapper. This artifact adds a source-regressed Li/Na-first reactive-stage model with the literature-supported `2 HBTA : 1 TOPO : 1 Li` complex stoichiometry and ePC-SAFT aqueous activity coefficients when the local runtime can evaluate them.

## Scientific Boundary

This is predictive only in the Li/Na staged-transfer sense after divalent pretreatment: one source-regressed parameter payload is reused across feed and O/A cases without per-case refitting. It is still not a full organic-phase ePC-SAFT LLE calculation. HBTA, TOPO, sulfonated kerosene/diluent, and Li-complex ePC-SAFT parameters remain unresolved.

## Sources Used

- Shan/Gando 2025, DOI `10.3390/W17152258`: Table 4 three-stage lithium extraction after impurity removal.
- Zhang et al. 2017, DOI `10.1016/j.seppur.2017.07.028`: HBTA/TOPO slope-analysis stoichiometry and Li/Na selectivity anchor.
- Zhang et al. 2018, DOI `10.1016/j.hydromet.2017.10.029`: HBTA/TOPO/kerosene process support.

## Fitted Parameters

- `log10_beta_li = 1.70058252`
- `log10_beta_na = -0.94738190`
- `log10_capacity_factor = 0.24457360`
- `saltout_gain = 1.02658377`

## MS-2 Base Case, O/A = 1

| Stage | Li stage (%) | Li cumulative (%) | Na stage (%) | Selectivity | Raffinate Li (mg/L) |
|---:|---:|---:|---:|---:|---:|
| 1 | 47.2846 | 47.2846 | 0.013112 | 6840.11 | 88.5619 |
| 2 | 80.2246 | 89.5753 | 0.022261 | 18219.69 | 17.5135 |
| 3 | 99.9999 | 100.0000 | 0.080661 | 1238761355.33 | 0.0000 |

For formal costing, lithium recovery is capped at the source-backed `97.17%` Shan/Gando three-stage anchor when the extrapolated Smackover stage model predicts near-total transfer.

## Generated Files

- `data\reference\extraction_models\gando_2025\hbta_topo_reactive_fit.json`
- `data\reference\produced_water\hbta_topo_reactive_fit_parameters.csv`
- `data\reference\produced_water\hbta_topo_predictive_regression_dataset.csv`
- `data\reference\produced_water\hbta_topo_predictive_regression_residuals.csv`
- `data\reference\produced_water\hbta_topo_predictive_parameter_uncertainty.csv`
- `data\reference\produced_water\hbta_topo_predictive_model_audit.csv`
- `data\reference\produced_water\hbta_topo_reactive_stage_results.csv`
- `data\reference\produced_water\hbta_topo_reactive_prommis_stage_table.csv`
- `data\reference\produced_water\hbta_topo_formal_costing_assumptions.csv`
- `data\reference\produced_water\hbta_topo_formal_costing_results.csv`
- `data\reference\produced_water\hbta_topo_idaes_costing_input.csv`
