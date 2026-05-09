# Rezaee Calibrated Surrogate Presentation And Workflow Handoff

Date: 2026-05-08

## Purpose

This handoff tells the next Lithium_Extraction agent how to use the completed
Rezaee calibrated surrogate matrix in the presentation, PrOMMiS/IDAES handoff
tables, and downstream workflows.

The key point is that the project now has a producible 523-row UQ/design matrix
with distribution coefficients derived from the upstream ePC-SAFT Rezaee
Section 3.2 DOE-basis surface.

## Current State

Upstream package analysis:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT\analyses\2026_rezaee
```

Upstream commit containing the under-20% Rezaee basis-surface validation:

```text
e4ee304 Fit Rezaee DOE basis surface
```

Downstream Lithium_Extraction commit containing the surrogate matrix:

```text
bb138a7 Add Rezaee calibrated surrogate matrix
```

Current downstream worktree:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT\.worktrees\downstreams\Lithium_Extraction
```

## Core Claim To Use

Use this wording:

> A calibrated Rezaee Section 3.2 DOE-basis distribution surrogate was built
> from the upstream ePC-SAFT Rezaee validation. It generates a 523-row
> TDS-Li-O/A design matrix for produced-water process screening and returns
> finite Li extraction, Na extraction, Li/Na selectivity, and distribution
> coefficients for PrOMMiS/IDAES transfer.

Do not call this a raw direct reactive-LLE closure.

## What The Model Is

The runner reads the upstream calibrated Rezaee rows:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT\analyses\2026_rezaee\data\processed\rezaee_2026_section32_revised_31_run_results.csv
```

It fits lightweight response surfaces in log distribution coefficient space:

```text
log(D_Li)
log(D_Na)
```

The features are:

```text
intercept
T_centered_30C_scaled_5C
pH_centered_10_scaled_0p5
TOPO_wt_pct_centered_30_scaled_10
ln_Na_Li_mass_ratio_over_10
pH_x_TOPO
pH_x_ln_Na_Li
TOPO_x_ln_Na_Li
```

The surrogate then evaluates the produced-water UQ matrix over:

```text
TDS_feature_mg_L
Li_feed_mg_L
organic_to_aqueous_mass_ratio
```

with fixed chemistry settings:

```text
temperature_C = 23
aqueous_pH = 10.4
TOPO_wt_pct_in_organic = 10
residual_divalent_mg_L = 0
```

Sodium is derived from TDS using the MS-2 clean brine ratio:

```text
Na_mg_L = TDS_feature_mg_L * 64100 / 305000
Na_Li_mass_ratio = Na_mg_L / Li_feed_mg_L
```

## Main Files To Use

Primary prediction table:

```text
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_uq_predictions.csv
```

Presentation/report summary:

```text
analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/rezaee_tds_li_oa_uq_report.md
```

Summary JSON:

```text
analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/rezaee_tds_li_oa_uq_summary.json
```

PrOMMiS/IDAES transfer table:

```text
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_prommis_idaes_transfer.csv
```

Costing input table:

```text
analyses/rezaee_2026_pcsaft_epcsaft/data/processed/rezaee_tds_li_oa_calibrated_idaes_costing_input.csv
```

Compatibility mirrors are also available under:

```text
data/reference/produced_water/
```

## Presentation Figures

Use these generated figures directly in the deck:

```text
analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/calibrated_li_extraction_surface.png
analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/calibrated_selectivity_vs_na_li.png
analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/calibrated_costing_scenarios.png
```

Suggested slide labels:

- `Calibrated Rezaee surrogate: Li extraction over Li grade and O/A`
- `Calibrated Rezaee surrogate: selectivity under produced-water sodium load`
- `Process-screening economics from surrogate transfer variables`

Flag for future agents: older `synthetic_*` figure and costing filenames were
superseded because they made the calibrated surrogate look like the old
placeholder scaffold. Use the `calibrated_*` names above for new deck and report
work.

## Key Numbers

From the latest run:

```text
row_count = 523
model_basis = calibrated_rezaee_section32_doe_basis_surface_distribution_surrogate
finite_outputs = true
nominal_ms2_count = 1
Li extraction range = 30.18-61.38 %
Na extraction range = 2.67-9.76 %
D_Li_phase_ratio_corrected range = 0.812-1.153
D_Na_phase_ratio_corrected range = 0.0549-0.0721
```

Nominal MS-2 clean Li/Na row:

```text
case_id = nominal_ms2_clean_li_na
Li_feed_mg_L = 168
TDS_feature_mg_L = 305000
Na_mg_L = 64100
Na_Li_mass_ratio = 381.55
organic_to_aqueous_mass_ratio = 1.0
li_extraction_pct = 50.66
na_extraction_pct = 5.67
selectivity_Li_Na = 17.09
D_Li_phase_ratio_corrected = 1.0267
D_Na_phase_ratio_corrected = 0.0601
```

## Columns That Matter Most

For the presentation and process workflows, prioritize:

```text
case_id
sample_type
model_basis
TDS_feature_mg_L
Li_feed_mg_L
Na_mg_L
Na_Li_mass_ratio
organic_to_aqueous_mass_ratio
li_extraction_pct
na_extraction_pct
selectivity_Li_Na
D_Li_phase_ratio_corrected
D_Na_phase_ratio_corrected
three_stage_li_cumulative_pct
three_stage_na_cumulative_pct
raffinate_Li_mg_L
raffinate_Na_mg_L
extract_Li_loading_mg_per_kg_org
extract_Na_loading_mg_per_kg_org
validity_flag
validity_notes
```

`D_Li_phase_ratio_corrected` is the primary distribution-coefficient output for
downstream staged-contacting and process modeling.

## Required Caveat

Every row is currently flagged:

```text
calibrated_surface_with_warnings
```

Reason:

```text
outside_rezaee_doe_na_li
```

This is expected because Smackover clean brine has a very high Na/Li mass ratio
relative to the Rezaee DOE training range:

```text
Rezaee training Na/Li range = 5-25
nominal MS-2 Na/Li = 381.55
```

Use this caveat in the deck. The correct interpretation is:

> The surrogate is useful for produced-water process screening and for
> PrOMMiS/IDAES interface development, but the Smackover rows are extrapolated
> beyond the original Rezaee DOE Na/Li domain.

## What Not To Claim

Do not claim:

- raw Smackover brine goes directly into the Rezaee extraction step,
- divalent ions are modeled in the extraction equilibrium,
- this is a direct reactive-LLE closure,
- every row is inside the Rezaee calibration domain,
- the surrogate replaces future validation against higher-Na/Li experimental
  extraction data.

Do claim:

- divalent pretreatment is assumed before Li/Na extraction,
- Rezaee DES/TOPO is the active Li/Na bridge chemistry,
- the surrogate produces finite process-facing transfer variables,
- distribution coefficients are now explicit and ready for staged-contacting
  and PrOMMiS/IDAES handoff testing,
- extrapolation warnings are tracked per row.

## How To Rerun

From:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT\.worktrees\downstreams\Lithium_Extraction
```

Run:

```powershell
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_surrogate_input_space.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_tds_li_oa_calibrated_surrogate.py
```

If the upstream ePC-SAFT analysis lives somewhere else, set:

```powershell
$env:EPCSAFT_REZAEE_SECTION32_ROWS = "C:\path\to\rezaee_2026_section32_revised_31_run_results.csv"
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_tds_li_oa_calibrated_surrogate.py
```

## Validation Checklist

Before using in a deck or workflow, verify:

- `status` in `rezaee_tds_li_oa_uq_summary.json` is `passed`.
- `finite_outputs` is `true`.
- `nominal_ms2_count` is `1`.
- all rows have the model basis:

```text
calibrated_rezaee_section32_doe_basis_surface_distribution_surrogate
```

- sodium is internally consistent:

```text
Na_mg_L = TDS_feature_mg_L * 64100 / 305000
Na_Li_mass_ratio = Na_mg_L / Li_feed_mg_L
```

- distribution coefficients are nonnegative and finite.
- extrapolated rows keep their warning flags.

## Suggested Deck Flow

1. Problem framing: produced water after divalent pretreatment is reduced to a
   clean Li/Na separation problem.
2. Chemistry bridge: Rezaee 90 wt% TBAC/decanoic-acid DES + 10 wt% TOPO is used
   as the Li/Na solvent basis.
3. Upstream validation: ePC-SAFT/Rezaee Section 3.2 basis-surface model gets
   figure-level mean AARD values below 20%.
4. Surrogate construction: fit log-distribution surfaces from the 31 upstream
   calibrated rows.
5. Surrogate matrix: show the 523-row TDS-Li-O/A design and the three generated
   figures.
6. Process transfer: show PrOMMiS/IDAES table columns and nominal MS-2 row.
7. Caveat slide: Smackover Na/Li is outside Rezaee DOE range, so this is a
   process-screening extrapolation that motivates future high-Na/Li validation.

## Handoff Summary

The Lithium_Extraction agent can now build presentation and workflow materials
from the calibrated Rezaee surrogate outputs. The main CSV is
`rezaee_tds_li_oa_uq_predictions.csv`, the main process output is
`D_Li_phase_ratio_corrected`, and the main caveat is the high-Na/Li
extrapolation warning on all produced-water rows.
