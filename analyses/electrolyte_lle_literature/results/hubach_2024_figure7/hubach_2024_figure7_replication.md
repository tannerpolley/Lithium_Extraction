# Hubach 2024 Figure 7 Replication (Dataset-Driven)

## Basis

- Paper markdown: C:\Users\Tanner\Documents\git\Lithium_Extraction\papers\md\Li+ Extraction from Aqueous Medium Using Tetracyanoborate Ionic.md
- Supporting-info markdown: C:\Users\Tanner\Documents\git\Lithium_Extraction\papers\md\Supporting Information for Li+ extraction from aqueous medium using tetracyanoborate ionic liquids -.md
- Dataset directory: C:\Users\Tanner\Documents\git\Lithium_Extraction\data\reference\epcsaft_parameters\2024_Hubach
- Solver profile: stable
- Effective user_options: {"debug": false, "elec_model": {"base": "2020", "bjeruum_treatment": false, "born_contrib": true, "born_diff_model": "analytic", "born_diff_options": {"include_delta_d_i_conc_dep": true, "include_dielc_conc_dep": true, "include_sum_term": true}, "dielc_diff_mode": "analytic", "dielc_rule": "combined", "eps_r_bulk": "mix", "ssm_ds": false}}

## Definitions

- Primary efficiency: $E_{Li+}^{mb} = 100\cdot n_{Li+,org}/n_{Li+,init}$
- Diagnostic Eq. (13)-style: $E_{Li+}^{(13)} = 100\cdot \phi \cdot x_{Li+,org}/x_{Li+,feed}$ with $\phi=\beta_{org}/\beta_{aq}$

## Pointwise Comparison

| $R^w(O/A)$ | $E_{Li+,exp}$ (%) | $E_{Li+,calc}^{S11}$ (%) | $E_{Li+}^{mb}$ (%) | $E_{Li+}^{(13)}$ (%) | delta vs exp | delta vs S11-calc | converged | status |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.522 | 75.39 | 78.16 | nan | nan | nan | nan | False | SolutionError |
| 0.985 | 89.01 | 88.58 | nan | nan | nan | nan | False | SolutionError |
| 1.976 | 93.5 | 95.02 | nan | nan | nan | nan | False | SolutionError |
| 3.015 | 96.81 | 97.05 | nan | nan | nan | nan | False | SolutionError |
| 3.933 | 98.33 | 97.04 | nan | nan | nan | nan | False | SolutionError |

## Aggregated Deviations

- ARD vs Table S11 experimental (%): nan
- AAD vs Table S11 experimental (pct-pts): nan
- ARD vs Table S11 calc (%): nan
- AAD vs Table S11 calc (pct-pts): nan

## Notes

- Line in Figure uses package-computed values; symbols use Table S11 experimental values.
- If package output differs from S11-calculated values, this report keeps true package output and reports mismatch transparently.