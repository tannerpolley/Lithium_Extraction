# Yu 2024 Figure 6 Replication

## Basis

- Dataset directory: C:\Users\Tanner\Documents\git\Lithium_Extraction\data\pcsaft_parameters\yu_2024
- Digitized experimental points: C:\Users\Tanner\Documents\git\Lithium_Extraction\analyses\yu_2024_figure6\data\input\figure6_digitized_points.csv
- Runtime: installed `epcsaft` package through `scripts.epcsaft_compat`.
- Imported pcsaft module: C:\Users\Tanner\Documents\git\Lithium_Extraction\scripts\epcsaft_compat.py
- Effective user options: `{"debug": false, "elec_model": {"DH_model": {"bjeruum_treatment": false, "d_ion_mode": 1, "mu_DH_model": {"comp_dep_rel_perm": true, "differential_mode": "analytical", "include_sum_term": true}}, "born_model": {"bulk_mode": "mix", "d_Born_mode": 3, "dielectric_saturation": true, "mu_born_model": {"comp_dep_delta_d": true, "comp_dep_rel_perm": true, "differential_mode": "numerical", "include_sum_term": true}, "solvation_shell_model": true}, "include_born_model": true, "rel_perm": {"differential_mode": "numerical", "rule": "empirical"}}}`
- Assumed aqueous density for the reported g/L brine basis: `1.000 kg/L`
- Fitted effective TOP concentration used to convert O/A volume ratio into feed moles: `1.900000 mol/L organic`

## Notes

- The paper body is available locally, but Table S6 is not. Experimental points were digitized from the local PDF figure.
- Paper Table 3 interaction parameters were used directly. Only the effective TOP concentration was back-calculated so the `O/A = 2:1` fit anchor can be reconstructed from the reported figure.
- The 2025 electrolyte options were enforced with empirical dielectric mixing and Born `SSM+DS` active, per the current package schema.

## Pointwise Comparison

| O/A | $E_{Li+,exp}$ (%) | $E_{Li+,calc}$ (%) | $E_{Mg2+,exp}$ (%) | $E_{Mg2+,calc}$ (%) | converged |
|---:|---:|---:|---:|---:|:---:|
| 1 | 37 | nan | 0.8 | nan | False |
| 2 | 75 | nan | 0.7 | nan | False |
| 3 | 83.2 | nan | 0.7 | nan | False |
| 4 | 87.3 | nan | 0.9 | nan | False |
| 5 | 88.7 | nan | 1.1 | nan | False |
| 6 | 89 | nan | 1.4 | nan | False |

## Fit Anchor

- `O/A = 2:1`: target `75 %`, model `nan %`
