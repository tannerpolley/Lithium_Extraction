# Gando 2025 Selective-Chelation Reproduction

## Basis

- Config: `C:\Users\Tanner\Documents\git\Lithium_Extraction\data\pcsaft_parameters\gando_2025\reactive_selectivity.json`
- Mechanism: Li-selective HBTA/TOPO chelation wrapper outside the direct PC-SAFT flash.
- Nominal feed: Li = 60.000 mg/L, Na = 10900.000 mg/L, O/A = 1.000, TOP = 0.015000 mol/L.

## Wrapper Parameters

- `log10(K_Li) = 1.96239371`
- `log10(K_Na) = 0.98198807`
- `log10(capacity factor) = -0.18751752`
- `saltout gain = 5.00000000`
- `saltout ref = 10.000000 mol/L`

## Figure 3 Style Na Sweep

| Na (mg/L) | Paper $E_{Li}$ (%) | Calc $E_{Li}$ (%) | Calc $E_{Na}$ (%) | $D_{Li}$ | $S_{Li/Na}$ | Salt-out factor |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 49.8200 | 49.8225 | 0.0000 | 0.9929 | 992927065458465848628443348992.0000 | 1.0000 |
| 2000 |  | 51.3066 | 2.7739 | 1.0537 | 36.9307 | 1.9350 |
| 4000 |  | 51.7663 | 1.8923 | 1.0732 | 55.6427 | 2.8619 |
| 6000 |  | 51.9458 | 1.4373 | 1.0810 | 74.1281 | 3.7809 |
| 8000 |  | 52.0095 | 1.1596 | 1.0837 | 92.3760 | 4.6922 |
| 10900 | 51.8200 | 52.0047 | 0.9067 | 1.0835 | 118.4138 | 6.0000 |

## Table 4 Style Three-Stage Result

| Stage | Paper $E_{Li,cum}$ (%) | Calc $E_{Li,stage}$ (%) | Calc $E_{Li,cum}$ (%) | Calc $E_{Na,stage}$ (%) | Calc $E_{Na,cum}$ (%) |
|---:|---:|---:|---:|---:|---:|
| 1 | 54.9500 | 52.0047 | 52.0047 | 0.9067 | 0.9067 |
| 2 | 85.6000 | 68.4342 | 84.8499 | 1.2021 | 2.0979 |
| 3 | 97.1700 | 85.4948 | 97.8025 | 1.5166 | 3.5827 |

## Interpretation

- The wrapper keeps lithium extraction near the paper range while keeping sodium extraction low enough to demonstrate lithium-specific solvent extraction in the surrogate showcase chain.
- Sodium is modeled as weakly co-extracted and mildly promotive; the large Li-over-Na selectivity comes from the external chelation law rather than bare ion partitioning.
