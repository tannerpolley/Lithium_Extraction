# Yu 2024 Figure 6 Reactive Replication

## Basis

- Dataset directory: C:\Users\Tanner\Documents\git\Lithium_Extraction\data\pcsaft_parameters\yu_2024
- Digitized experimental points: C:\Users\Tanner\Documents\git\Lithium_Extraction\scripts\Yu_2024_analysis\figure6_digitized_points.csv
- Reactive wrapper config: C:\Users\Tanner\Documents\git\Lithium_Extraction\data\pcsaft_parameters\yu_2024\reactive_eq11.json
- Paper mechanism used in the wrapper: Eq. 11 with 1:1:1 Li exchange stoichiometry and a separate low-affinity Mg exchange branch.
- The current 2025 yu_2024 electrolyte preset is retained as the dataset basis; the reaction is represented outside the core pcsaft flash because the direct six-species flash collapsed to a trivial split under the current build.

## Fitted Parameters

- `log10(K_Li) = 0.223112`
- `log10(K_Mg) = -2.494866`
- `C_IL,org = 0.090000 mol/L`
- `C_TOP,org = 1.900000 mol/L`
- `C_[HOEMIM+]_aq,baseline = 0.005611 mol/L`

## Pointwise Comparison

| O/A | $E_{Li+,exp}$ (%) | $E_{Li+,calc}$ (%) | $E_{Mg2+,exp}$ (%) | $E_{Mg2+,calc}$ (%) |
|---:|---:|---:|---:|---:|
| 1 | 37 | 51.64 | 0.8 | 0.204 |
| 2 | 75 | 71.15 | 0.7 | 0.47 |
| 3 | 83.2 | 79.4 | 0.7 | 0.7325 |
| 4 | 87.3 | 83.76 | 0.9 | 0.9774 |
| 5 | 88.7 | 86.43 | 1.1 | 1.205 |
| 6 | 89 | 88.24 | 1.4 | 1.416 |

## Notes

- This wrapper intentionally follows the paper’s extraction stoichiometry rather than introducing pseudo-species into the pcsaft core dataset.
- The remaining mismatch at `O/A = 1` is directionally consistent with the paper’s own statement that the model overestimates that low-O/A point.