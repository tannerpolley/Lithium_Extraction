# Jang 2017 Stage-2 Li/Na Extraction (TBP + D2EHPA Placeholder)

## Scope

- Focus: stage-2 hypothetical Li+/Na+ separation only.
- Modes: single equilibrium contact and crossflow repeated contacts.
- No fitting loop: all surrogate and $k_{ij}$ values are fixed assumptions.

## Working Equations

- Extraction efficiency: $E_i = \frac{n_{i,\mathrm{org}}}{n_{i,\mathrm{in}}}\times 100$
- Distribution ratio: $D_i = \frac{n_{i,\mathrm{org}}}{n_{i,\mathrm{aq}}}$
- Selectivity factor: $S_{\mathrm{Na}}^{\mathrm{Li}} = \frac{D_{\mathrm{Li}}}{D_{\mathrm{Na}}}$

## Inputs

- Temperature: 298.15 K
- Pressure: 100000 Pa
- O/A ratio: 1
- Organic: TBP 0.3 mol/L + D2EHPA 1.5 mol/L
- Feed proxy (Jang Table 3, 50x): Li 0.97 mg/L, Na 437 mg/L

| Species | mg/L | mol/L |
|---|---:|---:|
| Li+ | 0.97 | 0.000139769 |
| Na+ | 437 | 0.0190085 |
| Cl- (electroneutrality) | 678.805 | 0.0191482 |

## Fixed Surrogates

- TBP-SURR uses Hubach 2024-style placeholder values: $m=10.796$, $\sigma=3.2510 \AA$, $\epsilon/k_B=217.09$ K.
- D2EHPA-SURR uses temporary fixed placeholders pending data-based fitting.
- Fixed contact approach factors: $\\alpha_{Li} = 0.05$, $\\alpha_{Na} = 0.047$ per contact.

## Mode: single

| Cycle | Li stage % | Li cumulative % | Na stage % | Na cumulative % | $D_{Li}$ | $D_{Na}$ | $S_{Na}^{Li}$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 5 | 4.7 | 4.7 | 0.0526316 | 0.0493179 | 1.06719 |

## Mode: crossflow

| Cycle | Li stage % | Li cumulative % | Na stage % | Na cumulative % | $D_{Li}$ | $D_{Na}$ | $S_{Na}^{Li}$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 5 | 4.7 | 4.7 | 0.0526316 | 0.0493179 | 1.06719 |
| 2 | 5 | 9.75 | 4.7 | 9.1791 | 0.0526316 | 0.0493179 | 1.06719 |
| 3 | 5 | 14.2625 | 4.7 | 13.4477 | 0.0526316 | 0.0493179 | 1.06719 |
| 4 | 5 | 18.5494 | 4.7 | 17.5156 | 0.0526316 | 0.0493179 | 1.06719 |
| 5 | 5 | 22.6219 | 4.7 | 21.3924 | 0.0526316 | 0.0493179 | 1.06719 |
| 6 | 5 | 26.4908 | 4.7 | 25.087 | 0.0526316 | 0.0493179 | 1.06719 |
| 7 | 5 | 30.1663 | 4.7 | 28.6079 | 0.0526316 | 0.0493179 | 1.06719 |
| 8 | 5 | 33.658 | 4.7 | 31.9633 | 0.0526316 | 0.0493179 | 1.06719 |
| 9 | 5 | 36.9751 | 4.7 | 35.161 | 0.0526316 | 0.0493179 | 1.06719 |
| 10 | 5 | 40.1263 | 4.7 | 38.2085 | 0.0526316 | 0.0493179 | 1.06719 |

## Target Check

- Crossflow final lithium extraction after 10 cycles: 40.1263% (target around 40-41.2%).

## Sensitivity: TBP Concentration

| TBP (mol/L) | Li cumulative % after 10-cycle crossflow |
|---:|---:|
| 0.1 | 40.1263 |
| 0.3 | 40.1263 |
| 0.5 | 40.1263 |
| 0.8 | 40.1263 |

- Behavior note: this fixed-assumption set gives a mostly monotone trend; no clear internal optimum is resolved.

## Diagnostics

| Mode | Max mass-balance abs error | Max |charge(org)| | Max |charge(aq)| | Max residual norm |
|---|---:|---:|---:|---:|
| single | 0 | 5.42101e-20 | 5.42101e-20 | nan |
| crossflow | 0 | 1.89735e-19 | 5.42101e-20 | nan |