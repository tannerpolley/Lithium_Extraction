# Rezaee 2026 Reactive Equilibrium Fit Diagnostics

## Source Basis

- 2025 main paper and supporting information supply the experimental phase-composition rows.
- 2026 main paper and supporting information supply the reaction equations, Gibbs-energy constants, organic parameters, and binary interactions.
- This script checks Rezaee Eqs. 5/6 directly at the experimental SI phase compositions.

## Diagnostic Results

- Published-parameter median abs ln residual: `35.05766754566956`.
- Published-parameter mean abs ln residual: `35.22329451228562`.
- Refit with paper constants fixed median abs ln residual: `1.2822520386159937`.
- Refit with paper constants fixed mean abs ln residual: `1.5569707657701175`.
- Diagnostic refit with constants free median abs ln residual: `0.9225531387295298`.
- Diagnostic refit with constants free fitted K Li/Na: `2.3366171740031277e+17`, `4051388828.268564`.
- Median required/package gamma gap for RLi: `32.333632449703295` ln units.
- Median required/package gamma gap for RNa: `37.75847741297254` ln units.

## Interpretation

The package can evaluate the aqueous ePC-SAFT and organic PC-SAFT activity terms needed by the Rezaee formulation. The published constants and published parameter table do not satisfy the SI phase-composition rows under the package's activity-reference convention. Allowing the organic RLi/RNa parameters and organic binary interactions to refit while keeping the paper constants fixed improves the residual but does not close it to the paper's reported extraction-percent AARD.

The direct cause is now quantified: matching the SI RLi/RNa mole fractions while holding the published Table 2 constants would require organic complex activity coefficients many orders of magnitude smaller than the package computes from the published Table 8/9 parameters.

The constants-free fit is diagnostic only: it shows that the remaining gap is a source/reference-state or implementation-convention issue, because the fitted constants move far away from Table 2. Do not present that constants-free fit as the published Rezaee thermodynamic model.
