# Rezaee 2026 ePC-SAFT Aqueous Option Scan

## Purpose

This scan keeps the Rezaee organic PC-SAFT parameters, organic binary interactions, and reaction constants fixed to the paper values, then varies only the aqueous ePC-SAFT electrolyte option configuration used to calculate aqueous activity coefficients in Eqs. 14/15.

## Input Audit

- Aqueous species: `H2O, Li+, Na+, Cl-, H+, OH-, NH4+`.
- Organic species: `DES, TOPO, RLi, RNa`.
- Organic species match script order: `True`.
- Organic parameter rows: `4`.
- Organic binary-interaction rows: `6`.
- Reaction constant rows: `2`.
- Equilibrium rows available: `26`.
- Equilibrium rows used as benchmark: `26`.
- Row-count note: 2026 text mentions 36 data points; this workflow treats that as a clerical source-text mismatch and uses the 26 source SI rows.

## Result

- Options scanned: `16`.
- Unsupported/failed options recorded: `1`.
- Best option: `2025_born_no_ssm_empirical`.
- Best combined median absolute ln residual: `33.7572`.
- Baseline option: `package_struct_default_no_explicit_elec_model`.
- Baseline combined median absolute ln residual: `35.0461`.
- Accepted direct closure threshold met: `False`.

## Top Options

- `2025_born_no_ssm_empirical`: combined median abs ln residual `33.7572`; Li `31.1031`, Na `36.4113`.
- `legacy_default_born_linear_mole`: combined median abs ln residual `35.0461`; Li `32.3336`, Na `37.7585`.
- `package_struct_default_no_explicit_elec_model`: combined median abs ln residual `35.0461`; Li `32.3336`, Na `37.7585`.
- `held_2020_born_no_ssm_linear_mole`: combined median abs ln residual `35.1768`; Li `32.4348`, Na `37.9189`.
- `held_2014_s1_no_born_constant_eps`: combined median abs ln residual `35.1793`; Li `32.4625`, Na `37.8961`.
- `held_2008_no_born_constant_eps`: combined median abs ln residual `35.1793`; Li `32.4625`, Na `37.8961`.
- `2025_no_born_constant_eps`: combined median abs ln residual `35.2206`; Li `32.5097`, Na `37.9314`.
- `2025_no_born_linear_mole`: combined median abs ln residual `35.301`; Li `32.5901`, Na `38.0119`.

## Unsupported Options

- `2025_bjeruum_on`: `ValueError` - Bjerrum treatment is reserved and not implemented (DH_model=2).

## Interpretation

The aqueous ePC-SAFT option choice materially changes the activity coefficients, but none of the scanned Born, no-Born, dielectric, Bjerrum, or derivative configurations closes the published-constant Rezaee reactive equilibrium while keeping the paper organic parameters and reaction constants fixed.

This does not justify refitting yet. It narrows the next task: reproduce the paper's reaction-coordinate calculation using the 26-row benchmark and the published Table 8/9 parameters before changing those parameters.

## Generated Files

- `data\processed\rezaee_2026_reactive_epcsaft_option_scan_rows.csv`
- `data\processed\rezaee_2026_reactive_epcsaft_option_scan_summary.csv`
- `results\reaction_equilibrium\rezaee_2026_reactive_epcsaft_option_scan_summary.json`
