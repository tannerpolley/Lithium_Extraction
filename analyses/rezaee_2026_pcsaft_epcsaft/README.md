# Rezaee 2026 PC-SAFT/ePC-SAFT Package Smoke

This analysis owns the Rezaee 2026 package-validation lane for produced-water lithium extraction. It is a clean smoke/regression case for the ePC-SAFT package, not a full process-design objective.

## Boundary

- Active objective: lithium extracted from sodium after divalent pretreatment.
- Rezaee role: current source-regressed DES/TOPO Li/Na bridge plus phase/speciation method pilot.
- Not claimed: direct published-constant thermodynamic closure, full HBTA/TOPO closure, divalent extraction, or divalent equilibrium modeling.

## Source Assets

Source papers are stored with the project so agents do not need to re-search Zotero:

- `papers/pdf/Rezaee et al. - 2025 - Application of Response Surface Methodology for Selective Extraction of Lithium Using a Hydrophobic DES.pdf`
- `papers/md/Rezaee et al. - 2025 - Application of Response Surface Methodology for Selective Extraction of Lithium Using a Hydrophobic DES.md`
- `papers/pdf/Rezaee et al. - 2025 - Supporting information - Application of Response Surface Methodology for Selective Extraction of Lithium.pdf`
- `papers/md/Rezaee et al. - 2025 - Supporting information - Application of Response Surface Methodology for Selective Extraction of Lithium.md`
- `papers/pdf/Rezaee et al. - 2026 - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents A PC.pdf`
- `papers/md/Rezaee et al. - 2026 - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents A PC.md`
- `papers/pdf/Rezaee et al. - 2026 - Supplementary material - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents.pdf`
- `papers/md/Rezaee et al. - 2026 - Supplementary material - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents.md`

- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2026_reaction_constants.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2026_organic_pcsaft_parameters.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2026_organic_binary_interactions.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2026_si_density_tables.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2025_headline_extraction_points.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2025_doe_extraction_responses.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2025_extraction_equilibrium_mole_fractions.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2025_optimum_neighborhood.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2025_screening_extraction.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/input/rezaee_2025_real_brine_extraction.csv`
- `data/reference/epcsaft_parameter_fits/rezaee_2026/des_nonassoc_fit.json`

The script refits a diagnostic nonassociating DES pseudo-component against the current package, records the paper-reported DES/TOPO/RLi/RNa parameters and binary interaction values, and runs a small electrolyte stability/LLE smoke with `ePCSAFTMixture.equilibrium`.
The current source-backed smoke uses the 2026 SI density table directly because OCR of the main-paper Tait table can be misread. Rezaee's actual extraction equilibrium is not a conventional same-species LLE flash: the paper assumes two negligibly miscible liquid phases and closes extraction with phase-specific ion-exchange reactions.
For Rezaee's organic activity coefficients, the scripts map the paper's two-site DES to package scheme `2B` and the one-site TOPO entry to package scheme `1`.

Primary generated artifacts are local to this analysis:

- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_des_density_fit_records.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_des_parameter_fit_summary.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/smoke/rezaee_2026_epcsaft_phase_equilibrium_smoke.json`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/smoke/rezaee_2026_epcsaft_parameter_smoke_report.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_reactive_equilibrium_replay.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_reactive_equilibrium_replay.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_reactive_equilibrium_fit.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_reactive_equilibrium_fit.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_reactive_convention_scan_summary.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_reactive_convention_scan.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_reactive_epcsaft_option_scan_summary.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_reactive_epcsaft_option_scan.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_section32_basis_inference_rows.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_section32_basis_inference.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2026_section32_equilibrium_replication_rows.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/reaction_equilibrium/rezaee_2026_section32_equilibrium_replication.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2025_extraction_target_summary.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_2025_extraction_equilibrium_summary.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/targets/rezaee_2025_extraction_target_summary.md`

Compatibility mirrors are also written under `data/reference/produced_water/` for older presentation and report paths.

## Clean Li/Na Input Space

The active produced-water case now starts after divalent pretreatment. Run:

```powershell
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_surrogate_input_space.py
```

This generates the clean Li+Na feed basis, Rezaee/produced-water input-variable ranges, seed run matrix, and presentation figure:

- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_clean_li_na_pretreated_feed_basis.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_surrogate_input_variable_ranges.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_surrogate_seed_run_matrix.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/surrogate_input_space/rezaee_clean_li_na_surrogate_input_space.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/surrogate_input_space/figures/rezaee_surrogate_input_ranges.png`

These files define the input contract for surrogate generation. The calibrated response-producing runner now consumes the upstream ePC-SAFT Rezaee Section 3.2 DOE-basis surface artifacts and generates distribution-coefficient outputs for the UQ/design matrix.

## Calibrated Surrogate Run Matrix

Run:

```powershell
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_tds_li_oa_calibrated_surrogate.py
```

This produces a calibrated Rezaee distribution-coefficient surrogate over the current TDS, Li, and organic/aqueous design space. It reads the upstream 31-row Rezaee Section 3.2 basis-surface output, fits fast log-distribution response surfaces, and emits extraction, selectivity, distribution coefficients, staged recovery, PrOMMiS/IDAES handoff tables, and costing files.

Primary generated artifacts:

- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_uq_design.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_uq_predictions.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_prommis_idaes_transfer.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_calibrated_idaes_costing_input.csv`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/rezaee_tds_li_oa_uq_report.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/calibrated_li_extraction_surface.png`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/calibrated_selectivity_vs_na_li.png`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/calibrated_costing_scenarios.png`

Compatibility mirrors are written under `data/reference/produced_water/`. The current PrOMMiS consumer also mirrors its IDAES/Pyomo costing results there as `rezaee_calibrated_surrogate_mscontactor_costing_results.csv` and `.md`.

## Test Command

```powershell
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_des_epcsaft_parameter_smoke.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_2025_target_summary.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_equilibrium_replay.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_equilibrium_fit.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_convention_scan.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_reactive_epcsaft_option_scan.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_section32_basis_inference.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_section32_equilibrium_replication.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_li_na_distribution_bridge.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_surrogate_input_space.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_tds_li_oa_calibrated_surrogate.py
```

The older `analyses\hbta_topo_case_study\scripts\rezaee_des_epcsaft_parameter_smoke.py` and `scripts\case_study\rezaee_des_epcsaft_parameter_smoke.py` paths remain compatibility wrappers.

## Remaining For Extraction-Percent Comparison

- The main 2025 article now supplies screening rows, 26 designed-experiment Li/Na extraction response rows, five optimum-neighborhood rows, and the real/synthetic brine extraction table.
- The 2025 supporting information now supplies 26 designed-experiment equilibrium mole-fraction rows from Tables S1/S2 for aqueous `H2O`, `Li+`, `Na+`, `Cl-`, `H+`, `OH-`, `NH4+` and organic `DES`, `TOPO`, `RLi`, `RNa`.
- Run `scripts\rezaee_2025_target_summary.py` to generate the 32-row Li/Na comparison target table, a 26-row equilibrium summary, and a short report. These source rows are enough to start the Rezaee-style Li/Na fitting target.
- The reaction/speciation closure has a source-backed replay in `scripts\rezaee_reactive_equilibrium_replay.py`. It computes aqueous ePC-SAFT activity coefficients, organic PC-SAFT activity coefficients from fugacity-ratio Eq. 7, and Rezaee Eqs. 14/15 for RLi/RNa.
- `scripts\rezaee_reactive_equilibrium_fit.py` checks Rezaee Eqs. 5/6 directly at the experimental SI phase compositions and runs bounded Rezaee-style parameter refits.
- `scripts\rezaee_reactive_convention_scan.py` is the guardrail for the current source/reference-state issue. It scans mole-fraction-only, inverse-constant, inverse-quotient, water/OH omission, H+/NH4+ exchange, and TOPO-reactant variants so agents do not keep retrying undocumented one-line convention changes.
- `scripts\rezaee_reactive_epcsaft_option_scan.py` holds the paper organic parameters, Table 9 interactions, and Table 2 constants fixed while scanning aqueous ePC-SAFT options. The most source-aligned starting point is the Held-2014-style no-Born, constant-dielectric family; no scanned Born/dielectric option closes the published-constant equation gap.
- `scripts\rezaee_section32_basis_inference.py` tests whether the 26 DOE extraction percentages and SI equilibrium mole fractions define a self-consistent mole basis for Eq. 17. It finds that SI OH tracks pH and the aqueous rows are charge balanced, but the organic phase total inferred from RLi is a median `3.64x` the total inferred from RNa. This is the current concrete source-basis blocker.
- `scripts\rezaee_section32_equilibrium_replication.py` starts at the text immediately after Table 8 and implements Rezaee Eqs. 14, 15, 17, 18, 19, and 20 directly. The package is used only for activity coefficients. The direct Held-2014-S2/no-Born/Table-9/pH-stoichiometric case currently predicts essentially zero Li extraction and gives about `100%` Li extraction AARD, versus the paper's `7.89%` post-Table-9 target. That makes the missing Section 3.2 initial-mole/base-inventory convention the leading source task.
- Current blocker: with the paper-reported Table 2 constants, Table 8/9 organic parameters, and 2025 SI equilibrium mole fractions, the replay returns a large `lnQ-lnK` offset. The direct required-gamma diagnostic shows that matching the SI RLi/RNa mole fractions under those constants would require median organic complex activity coefficients near `3.33e-15` for RLi and `1.31e-18` for RNa, while the package computes about `0.38` and `0.027` from the published parameters. Refit diagnostics improve the residual but show that a source/reference-state or implementation-convention gap remains before claiming direct reproduction of the published Rezaee thermodynamic model.
- Latest convention scan: the source-supported Eq. 14/15 activity variant has combined median absolute ln residual `35.0461`. The best simple numerical variant is `paper_eq14_no_activity_vs_inverse_k`, but it is not source-supported and still leaves combined median absolute ln residual `9.5066`. This means the direct closure is not fixed by a simple sign, reciprocal-K, gamma on/off, water, hydroxide, hydrogen, ammonium, or TOPO convention change.
- Source-data audit: the local machine-readable SI extraction contains `26` equilibrium-composition rows. Treat the 2026 paper text saying `36` equilibrium data points as a clerical mismatch unless a source-backed original calculation sheet is later found.
- Acceptance criteria for comparing paper extraction percentages to package outputs without treating a diagnostic pseudo-DES density fit or a source-regressed bridge as a complete predictive model.

