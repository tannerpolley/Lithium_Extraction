# Gando 2025 Three-Stage Crossflow Showcase

## Basis

- Config: `C:\Users\Tanner\Documents\git\Lithium_Extraction\data\pcsaft_parameters\gando_2025\reactive_selectivity.json`
- Mechanism: external Li-selective HBTA/TOPO chelation wrapper applied outside the bare PC-SAFT phase split.
- Purpose: preserve lithium-specific extraction in the showcase chain while keeping sodium extraction low.
- Feed: Li = 60.000 mg/L, Na = 10900.000 mg/L, O/A = 1.000, TOP = 0.015000 mol/L.

## Fitted Wrapper Parameters

- `log10(K_Li) = 1.96239371`
- `log10(K_Na) = 0.98198807`
- `log10(capacity factor) = -0.18751752`
- `saltout gain = 5.00000000`
- `saltout ref = 10.000000 mol/L`

## Stage Results

| Stage | Paper $E_{Li,cum}$ (%) | Calc $E_{Li,stage}$ (%) | Calc $E_{Li,cum}$ (%) | Calc $E_{Na,stage}$ (%) | Calc $E_{Na,cum}$ (%) | $D_{Li}$ | $S_{Li/Na}$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 54.9500 | 52.0047 | 52.0047 | 0.9067 | 0.9067 | 1.0835 | 118.4138 |
| 2 | 85.6000 | 68.4342 | 84.8499 | 1.2021 | 2.0979 | 2.1680 | 178.1839 |
| 3 | 97.1700 | 85.4948 | 97.8025 | 1.5166 | 3.5827 | 5.8941 | 382.7454 |

## Notes

- This showcase intentionally uses an external reaction/selectivity wrapper because the bare ion-partitioning flash does not preserve the Li-over-Na selectivity seen in the HBTA/TOPO system.
- Sodium extraction is kept near 1% per stage as a showcase calibration target; the paper reports sodium as non-specific and mildly promotive rather than strongly co-extracted.
