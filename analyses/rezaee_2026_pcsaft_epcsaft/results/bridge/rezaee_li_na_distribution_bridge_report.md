# Rezaee 2026 Li/Na Distribution Bridge

Last updated: 2026-05-15

## Status

- Model status: `rezaee_source_regressed_li_na_bridge_with_direct_closure_gap`.
- Flagship chemistry for the current Li/Na bridge: Rezaee DES/TOPO with reported DES, TOPO, RLi, RNa, binary-interaction, and reaction-constant inputs.
- Distribution coefficients are source-regressed from Rezaee Li/Na extraction responses using an explicit equal-phase-volume O/A basis.
- The ePC-SAFT package evidence is carried as a diagnostic validity input. The current direct LLE smoke returns bounded diagnostics, not a fully accepted physical split.
- Direct published-constant reactive equilibrium remains blocked by the Section 3.2 initial-mole/reference-state convention gap recorded by the equation-replication scripts.

## Generated Artifacts

- `analyses\rezaee_2026_pcsaft_epcsaft\data\processed\rezaee_li_na_distribution_coefficients.csv`
- `analyses\rezaee_2026_pcsaft_epcsaft\data\processed\rezaee_smackover_tds_na_sensitivity.csv`
- `analyses\rezaee_2026_pcsaft_epcsaft\results\bridge\rezaee_prommis_idaes_transfer_handoff.csv`
- `analyses\rezaee_2026_pcsaft_epcsaft\results\bridge\rezaee_idaes_costing_input.csv`

## Source Evidence

- Extraction target rows used: `32`.
- Surrogate/sensitivity rows generated: `60`.
- Rezaee reaction constants: `analyses\rezaee_2026_pcsaft_epcsaft\data\input\rezaee_2026_reaction_constants.csv`.
- Rezaee organic PC-SAFT parameters: `analyses\rezaee_2026_pcsaft_epcsaft\data\input\rezaee_2026_organic_pcsaft_parameters.csv`.
- Rezaee organic binary interactions: `analyses\rezaee_2026_pcsaft_epcsaft\data\input\rezaee_2026_organic_binary_interactions.csv`.
- Median source-regressed D_Li: `0.6017`.
- Median source-regressed D_Na: `0.1257`.
- Median source-regressed S_Li/Na: `5.004`.
- SI median mole-fraction proxy D_Li: `2.225`.
- SI median mole-fraction proxy D_Na: `2.2`.

## Selected Smackover Transfer Row

- TDS: `305000.000 mg/L`.
- Li: `168.000 mg/L`.
- Na: `64100.000 mg/L`.
- Na/Li mass ratio: `381.548`.
- O/A: `1.000`.
- One-stage Li extraction: `45.366%`.
- One-stage Na extraction: `8.978%`.
- One-stage D_Li: `0.8304`.
- One-stage D_Na: `0.09864`.
- Three-stage Li recovery: `83.692%`.
- Trust label: `anchored_by_rezaee_real_brine_high_na_li`.

## Fit Diagnostics

- Li logit RMSE: `0.154`.
- Na logit RMSE: `0.1615`.
- ePC-SAFT electrolyte stability status: `success`.
- ePC-SAFT minimum TPD: `-0.5346836582364658`.
- ePC-SAFT LLE status: `not_accepted`.
- ePC-SAFT split detected: `False`.
- Reactive convention-scan status: `source_reference_state_gap`.
- Source-supported reactive variant: `paper_eq14_with_activity_vs_paper_k`.
- Source-supported combined median absolute ln residual: `35.04605493133792`.
- Best simple convention-scan variant: `paper_eq14_no_activity_vs_inverse_k`.
- Best simple combined median absolute ln residual: `9.506579080295277`.
- Equilibrium rows used as benchmark: `26`.
- Best aqueous ePC-SAFT option-scan case: `2025_born_no_ssm_empirical`.
- Best aqueous option-scan combined median absolute ln residual: `33.7571925407821`.
- Literal paper-basis reaction-coordinate best mode: `2025_born_no_ssm_empirical`.
- Literal paper-basis median calculated Li extraction: `3.4725128418839075e-10`.
- Section 3.2 direct Held-2014/Table-9 Li extraction AARD: `99.99999999872657`.
- Section 3.2 direct Held-2014/Table-9 selectivity AARD: `56.35718132404997`.
- Section 3.2 best diagnostic case: `held_2014_s2_no_born_table9_kij_inverseK_diagnostic`.
- Section 3.2 basis median organic-total consistency RLi/RNa: `3.6375026056361`.
- Section 3.2 basis median SI xOH / pH-derived xOH estimate: `0.9999690361888166`.

## Boundary

This bridge is now the current flagship Li/Na basis for the presentation and PrOMMiS/IDAES surrogate handoff. It is stronger than the previous HBTA/TOPO bridge for package-facing work because Rezaee supplies organic pseudo-component parameters, binary interactions, reaction constants, extraction responses, and SI equilibrium-composition rows. It is still not investment-grade TEA or a complete direct ePC-SAFT LLE/reactive-equilibrium prediction until accepted phase splits and a source-supported published-constant reactive closure are both available.
