# Rezaee 2026 ePC-SAFT Parameter Smoke Report

Last updated: 2026-05-07

## Boundary

This is a diagnostic package/regression smoke test. Rezaee 2026 uses PC-SAFT for the organic DES/TOPO phase and ePC-SAFT for the aqueous electrolyte phase. It is not the flagship Shan/Gando HBTA/TOPO/sulfonated-kerosene parameterization.

## Density Fit

- DES molecular-weight basis: `0.20748` kg/mol.
- MW note: Average formula-unit molecular weight for TBAC + 2 decanoic acid divided by 3. This is a diagnostic pseudo-component basis for the density fit, not a general DES molecular definition.
- Fit success: `True`.
- Fitted nonassociating `m`: `8.6191367`.
- Fitted nonassociating `sigma`: `3.1085243` A.
- Fitted nonassociating `epsilon/k`: `252.68833` K.
- Density metric: `0.007347057112639847`.

## Equilibrium Smoke

- Electrolyte stability status: `success`.
- Stable flag: `False`.
- Minimum TPD: `-0.5681261687345767`.
- Electrolyte LLE status: `error`.

## Interpretation

The density regression and electrolyte-stability calls exercise the current ePC-SAFT package successfully. The direct LLE call is kept as a diagnostic: if it returns a collapsed/non-predictive candidate for this pseudo-DES system, that is recorded as model-support evidence rather than hidden behind the HBTA/TOPO bridge.
