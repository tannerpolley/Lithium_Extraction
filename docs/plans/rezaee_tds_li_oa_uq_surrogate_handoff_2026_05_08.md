# Rezaee TDS-Li-OA UQ Surrogate Handoff

Date: 2026-05-08

## Purpose

Build the next Lithium_Extraction surrogate-run lane using the Rezaee 2025/2026
Li+Na DES/TOPO bridge. The immediate goal is to generate a practical uncertainty
or design-sweep dataset that maps produced-water-relevant inputs to lithium
extraction, sodium co-extraction, selectivity, and distribution coefficients for
later PrOMMiS/IDAES transfer.

This is **not** a claim that raw ePC-SAFT reactive LLE has independently closed
the Rezaee paper. Use the calibrated Rezaee Section 3.2 basis from the upstream
ePC-SAFT analysis.

## Upstream Modeling Status

Upstream ePC-SAFT analysis:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT\analyses\2026_rezaee
```

Important upstream artifacts:

```text
analyses/2026_rezaee/results/reaction_equilibrium/rezaee_2026_section32_blocker_audit.md
analyses/2026_rezaee/results/reaction_equilibrium/rezaee_2026_section32_table_s2_reconstruction.md
analyses/2026_rezaee/results/reaction_equilibrium/rezaee_2026_section32_calibrated_input_validation.md
analyses/2026_rezaee/results/reaction_equilibrium/rezaee_2026_section32_calibrated_input_validation_summary.json
analyses/2026_rezaee/data/processed/rezaee_2026_master_experiment_digitized_results.csv
```

Current upstream conclusion:

- Public SI Table S2 is internally suspicious.
- SI Table S2 caption says organic phase, but the table header says aqueous
  phase over `DES`, `TOPO`, `RLi`, and `RNa`.
- Public SI `RLi/RNa` implies median Li/Na selectivity about `0.858`, while the
  DOE response median is about `3.43`.
- The useful calibrated lane replaces public SI Table S2 `RLi/RNa` with
  mass-balance reaction-coordinate extents.
- The calibrated lane produces realistic extraction/selectivity values:
  - Li extraction AARD: approximately `0%`.
  - Selectivity AARD: approximately `0.075%`.

Use this model basis label in all new rows:

```text
model_basis = calibrated_rezaee_section32_mass_balance_complex_basis
```

## Consumer Project Context

Current downstream project:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT\.worktrees\downstreams\Lithium_Extraction
```

Existing input files:

```text
docs/plans/rezaee_clean_li_na_compact_agent_handoff_2026_05_08.md
data/reference/produced_water/rezaee_surrogate_input_variable_ranges.csv
data/reference/produced_water/rezaee_surrogate_seed_run_matrix.csv
analyses/rezaee_2026_pcsaft_epcsaft/results/surrogate_input_space/figures/rezaee_surrogate_input_ranges.png
```

The downstream handoff already chooses:

- Produced-water source: Southern Arkansas Smackover.
- Base row: MS-2 / MSPU 4-W1.
- Feed: pretreated clean Li+Na stream.
- Solvent bridge: Rezaee 90 wt% TBAC/decanoic-acid DES + 10 wt% TOPO.
- Divalent ions: removed by pretreatment; carry only as guardrail/cost flags.

Nominal clean feed:

| Quantity | Value |
|---|---:|
| Li | `168 mg/L` |
| Na | `64,100 mg/L` |
| Na/Li mass ratio | `381.55` |
| TDS feature | `305,000 mg/L` |
| residual divalent for extraction model | `0 mg/L` |

## Recommended First UQ Scope

The first useful UQ/surrogate dataset should focus on the three variables the
user cares most about:

| Variable | Range | Nominal | Reason |
|---|---:|---:|---|
| `TDS_feature_mg_L` | `152,500-340,000` | `305,000` | produced-water salinity/process feature |
| `Li_feed_mg_L` | `100-300` | `168` | lithium grade and value driver |
| `organic_to_aqueous_mass_ratio` | `0.5-1.5` | `1.0` | solvent inventory, stage capacity, and distribution coefficient basis |

Hold these fixed for the first focused dataset:

| Variable | Fixed value | Reason |
|---|---:|---|
| `temperature_C` | `23` | Rezaee selected operating point; lower temperature favored selectivity. |
| `aqueous_pH` | `10.4` | Rezaee selected operating point; avoid pH > 11 third-phase/emulsion risk. |
| `TOPO_wt_pct_in_organic` | `10` | Rezaee practical/economic selection. |
| `residual_divalent_mg_L` | `0` | pretreatment assumed before Li+Na extraction. |

## Sodium Handling

Do not make sodium an independent fourth UQ variable in the first pass. Derive
it from TDS using the selected MS-2 clean brine ratio:

```text
Na_fraction_of_TDS = 64100 / 305000 = 0.21016
Na_mg_L = TDS_feature_mg_L * Na_fraction_of_TDS
Na_Li_mass_ratio = Na_mg_L / Li_feed_mg_L
```

This keeps TDS, Na, and Li internally consistent while still exploring a wide
Na/Li range as TDS and Li vary.

The generated table should include both:

```text
Na_mg_L
Na_Li_mass_ratio
```

## Recommended UQ Design

Target around `500` rows:

- Keep the existing `19` seed matrix rows as anchor/sanity rows.
- Add `450-500` Latin-hypercube or Sobol samples over:
  - `TDS_feature_mg_L`
  - `Li_feed_mg_L`
  - `organic_to_aqueous_mass_ratio`
- Add explicit stress/corner rows:
  - high TDS + low Li + low O/A
  - high TDS + high Li + low O/A
  - low TDS + high Li + high O/A
  - nominal MS-2 clean Li+Na point
  - Rezaee paper nominal point

Use a fixed random seed and record it in the output summary.

## Model Evaluation Strategy

Use the calibrated Rezaee response lane, not raw public SI Table S2 `RLi/RNa`.

For each UQ row:

1. Resolve inputs:
   - `TDS_feature_mg_L`
   - `Li_feed_mg_L`
   - `organic_to_aqueous_mass_ratio`
   - fixed `T = 23 C`, `pH = 10.4`, `TOPO = 10 wt%`
2. Compute sodium:
   - `Na_mg_L = TDS_feature_mg_L * 0.21016`
   - `Na_Li_mass_ratio = Na_mg_L / Li_feed_mg_L`
3. Evaluate the calibrated Rezaee response.
4. Emit extraction and distribution outputs.
5. Emit validity flags and model-basis notes.

If a direct ePC-SAFT activity feature is used, record it as a diagnostic feature,
not as proof of fully predictive LLE closure.

## Required Outputs

Each output row should include:

```text
case_id
sample_id
sample_type
model_basis
temperature_C
aqueous_pH
TOPO_wt_pct_in_organic
TDS_feature_mg_L
Li_feed_mg_L
Na_mg_L
Na_Li_mass_ratio
organic_to_aqueous_mass_ratio
residual_divalent_mg_L
li_extraction_pct
na_extraction_pct
selectivity_Li_Na
D_Li_equal_phase_basis
D_Na_equal_phase_basis
D_Li_phase_ratio_corrected
D_Na_phase_ratio_corrected
raffinate_Li_mg_L
raffinate_Na_mg_L
extract_Li_loading_mg_per_kg_org
extract_Na_loading_mg_per_kg_org
validity_flag
validity_notes
```

Optional diagnostics:

```text
activity_gamma_Li
activity_gamma_Na
activity_gamma_OH
activity_gamma_H2O
organic_gamma_DES
organic_gamma_RLi
organic_gamma_RNa
log10_Keff_over_Kpaper_Li
log10_Keff_over_Kpaper_Na
```

## Distribution Coefficient Definitions

Use clear definitions because the data will transfer to process models.

Equal phase basis:

```text
D_Li_equal_phase_basis = E_Li / (100 - E_Li)
D_Na_equal_phase_basis = E_Na / (100 - E_Na)
```

Phase-ratio-corrected basis, with `O/A = organic_to_aqueous_mass_ratio`:

```text
D_Li_phase_ratio_corrected = (E_Li / (100 - E_Li)) / O_A
D_Na_phase_ratio_corrected = (E_Na / (100 - E_Na)) / O_A
```

These assume similar phase densities. If density correction is added later,
preserve these columns and add density-corrected columns separately.

Raffinate concentrations:

```text
raffinate_Li_mg_L = Li_feed_mg_L * (1 - li_extraction_pct / 100)
raffinate_Na_mg_L = Na_mg_L * (1 - na_extraction_pct / 100)
```

Organic loading on a mass-ratio basis:

```text
extract_Li_loading_mg_per_kg_org =
    (Li_feed_mg_L * li_extraction_pct / 100) / O_A

extract_Na_loading_mg_per_kg_org =
    (Na_mg_L * na_extraction_pct / 100) / O_A
```

The units are approximate unless aqueous density and phase volumes are made
explicit. Record this in `validity_notes`.

## Current Calibrated Surrogate Files

The calibrated Rezaee distribution surrogate now writes this bundle:

```text
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_uq_design.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_uq_predictions.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_prommis_idaes_transfer.csv
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_calibrated_idaes_costing_input.csv
analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/rezaee_tds_li_oa_uq_summary.json
analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/rezaee_tds_li_oa_uq_report.md
data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.csv
data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.md
```

Figures:

```text
analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/
```

Available figures:

- `calibrated_li_extraction_surface.png`
- `calibrated_selectivity_vs_na_li.png`
- `calibrated_costing_scenarios.png`

## Validation Gates

Before claiming the UQ dataset is ready:

1. Confirm all generated rows have finite outputs.
2. Confirm nominal MS-2 row appears exactly once.
3. Confirm all rows use the correct `model_basis`.
4. Confirm derived sodium is internally consistent:

```text
abs(Na_mg_L - TDS_feature_mg_L * 64100 / 305000) < tolerance
abs(Na_Li_mass_ratio - Na_mg_L / Li_feed_mg_L) < tolerance
```

5. Confirm extraction and distribution values are physically bounded:

```text
0 <= li_extraction_pct <= 100
0 <= na_extraction_pct <= 100
D_Li_phase_ratio_corrected >= 0
D_Na_phase_ratio_corrected >= 0
```

6. Confirm source-domain warnings are flagged:
   - Na/Li outside Rezaee DOE range.
   - TDS used as process/salinity feature, not fitted Rezaee chemistry variable.
   - residual divalent nonzero means guardrail, not active extraction chemistry.

## Hard Boundaries

- Do not claim raw Smackover brine goes directly into Rezaee extraction.
- Do not model Ca/Mg/Sr/Ba extraction in this phase.
- Do not use public SI Table S2 `RLi/RNa` directly as the output calibration
  basis.
- Do not claim direct published-constant Rezaee reactive-equilibrium closure.
- Do not claim the calibrated surrogate rows are direct reactive-LLE closure.
- Keep the `calibrated_*` figure and costing filenames; older `synthetic_*`
  names were superseded because they implied placeholder data.
- Keep HBTA/TOPO as comparison or future parameterization, not this Rezaee
  Li+Na surrogate lane.

## One-Sentence Summary For A New Agent

Use the roughly 500-row calibrated Rezaee distribution surrogate to validate the
TDS, Li feed, O/A, and distribution-coefficient handoff to PrOMMiS/IDAES, while
flagging Smackover rows as high-Na/Li extrapolations beyond the Rezaee DOE
domain.
