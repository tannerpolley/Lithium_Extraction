# Gando 2025 Slide Assets

## Basis

- Config: `C:\Users\Tanner\Documents\git\Lithium_Extraction\data\pcsaft_parameters\gando_2025\reactive_selectivity.json`
- Mechanism: external Li-selective HBTA/TOPO chelation wrapper layered on top of the PC-SAFT phase-split backbone.
- Feed basis: Li = 60.000 mg/L, Na = 10900.000 mg/L, O/A = 1.000, TOP = 0.015000 mol/L.
- Fitted parameters: `log10(K_Li) = 1.96239371`, `log10(K_Na) = 0.98198807`, `log10(capacity factor) = -0.18751752`.

## Headline Numbers

- Nominal one-stage extraction: Li = 52.0047%, Na = 0.9067%.
- Stage-3 cumulative extraction: Li = 97.8025%, Na = 3.5827%.
- Stage-3 Li/Na selectivity: 382.7454.
- Stage-3 Li remaining in raffinate: 1.3185 mg/L.

## PNG Assets

- `gando_2025_cumulative_extraction_wide.png`
- `gando_2025_stagewise_extraction_bars.png`
- `gando_2025_selectivity_profile.png`
- `gando_2025_nominal_spotlight.png`
- `gando_2025_na_sweep_wide.png`
- `gando_2025_stage_summary_table.png`
- `gando_2025_kpi_table.png`

## CSV Tables

- `gando_2025_stage_summary.csv`
- `gando_2025_na_sweep.csv`
- `gando_2025_kpis.csv`

## Stage Summary

| Stage | Paper $E_{Li,cum}$ (%) | Calc $E_{Li,cum}$ (%) | Calc $E_{Na,cum}$ (%) | $D_{Li}$ | $S_{Li/Na}$ |
|---:|---:|---:|---:|---:|---:|
| 1 | 54.9500 | 52.0047 | 0.9067 | 1.0835 | 118.4138 |
| 2 | 85.6000 | 84.8499 | 2.0979 | 2.1680 | 178.1839 |
| 3 | 97.1700 | 97.8025 | 3.5827 | 5.8941 | 382.7454 |
