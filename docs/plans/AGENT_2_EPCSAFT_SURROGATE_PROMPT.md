# Agent 2 Prompt: ePC-SAFT, Phase-Inventory Diagnostics, and Transfer Variables

## Required first action

Read `MASTER_CASE_STUDY_CONTEXT_ROADMAP.md` and Agent 1 outputs before changing any model files.

Required Agent 1 outputs:

- `docs/case_study_tbac_da_topo_storyboard.md`
- `docs/case_study_claims_and_boundaries.md`
- `data/reference/produced_water/selected_case_study_feeds.csv`
- `data/reference/produced_water/tbac_da_topo_lhs_input_ranges.csv`

## Role

Own the modeling and transfer-variable vertical slice. Revise the TBAC/DA DES + 10 wt% TOPO Li/Na extraction workflow so PrOMMiS/IDAES can consume clean, labeled transfer variables.

## Why this slice exists

The case study needs credible thermodynamic outputs, not just literature numbers. This slice converts chemistry and feed choices into Li/Na extraction variables, validity flags, and surrogate rows.

The preferred source of truth is direct ePC-SAFT output from the package. If direct reactive-LLE closure does not pass validation, retain a calibrated Li/Na bridge only as a labeled fallback.

## Scope

Focus only on:

- solvent-system configuration,
- revised LHS/LHC design generation,
- phase-inventory/reference-state diagnostics,
- direct ePC-SAFT or calibrated Li/Na transfer-variable generation,
- validity and extrapolation flags,
- model report.

Do not build the PrOMMiS flowsheet, TEA, or final presentation. Those are Agent 3 tasks.

## Required solvent naming

Use:

- `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`
- `TBAC/DA DES + 10 wt% TOPO`
- `90 wt% TBAC/DA DES + 10 wt% TOPO`

Do not use a source-author name as the solvent-system label in new reports, result files, figure captions, or user-facing outputs. Existing legacy folder names may remain for compatibility.

New artifact names must use `tbac_da_topo`.

## Model boundary

Active objective:

- Li/Na extraction after divalent pretreatment.

Out of active objective:

- divalent extraction,
- divalent equilibrium,
- REE recovery,
- raw produced-water direct extraction without pretreatment,
- investment-grade cost modeling.

Divalent cations may appear only as pretreatment or residual-leakage guardrails.

## Direct ePC-SAFT preference

Use direct ePC-SAFT calculations where they pass:

- source-row reproduction,
- mass balance,
- charge balance,
- phase-inventory consistency,
- reaction residual tolerance,
- stable/converged phase behavior.

If direct ePC-SAFT does not pass, use the calibrated Li/Na distribution bridge and label it explicitly as calibrated transfer variables, not direct reactive-LLE closure.

## Required phase-inventory diagnostic

Use this term:

> phase-inventory / reaction-coordinate reference-state convention

Do not call it the “weird inlet convention.”

Implement or revise a convention scan with:

- O/A as mass ratio,
- O/A as volume ratio,
- equal phase masses,
- equal phase volumes,
- density-corrected O/A,
- pH-stoichiometric H/OH basis,
- NH4/OH buffer basis if already available,
- explicit reaction-coordinate basis.

For each scanned convention, record:

- `basis_type`,
- `phase_mass_aq`,
- `phase_mass_org`,
- `phase_volume_aq`,
- `phase_volume_org`,
- `density_aq`,
- `density_org`,
- `reaction_extent_Li`,
- `reaction_extent_Na`,
- `mass_balance_residual`,
- `charge_balance_residual`,
- `lnQ_minus_lnK_residual` if applicable,
- `closure_status`,
- `failure_reason` if not closed.

Do not waste time on arbitrary sign flips, reciprocal constants, gamma on/off toggles, or undocumented equation changes after the phase-inventory issue is identified.

## LHS/LHC design requirements

Consume Agent 1 input ranges.

Main design ranges:

| Variable | Range |
|---|---:|
| `Li_feed_mg_L` | `80–300` |
| `TDS_feature_mg_L` | `80,000–360,000` |
| `Na_Li_mass_ratio` | `75–850` |
| `organic_to_aqueous_mass_ratio` | `0.5–2.0` |
| `temperature_C` | `20–35` |
| `aqueous_pH` | `9.5–10.8` |
| `TOPO_wt_pct_in_organic` | fixed `10` |
| `TBAC_to_DA_molar_ratio` | fixed `1:2` |
| `stage_count` | integer `1–5` |
| `residual_divalent_mg_L` | `0–500`, guardrail only |
| `feed_id` | categorical |

Sampling requirements:

- include source-paper anchor rows,
- include Smackover MS-2 nominal,
- include Smackover high sensitivity,
- include Marcellus NE comparison,
- include Bakken stress,
- use log or stratified sampling for `Na_Li_mass_ratio`,
- flag rows outside the source-paper low-Na/Li design space.

## Required transfer-variable table

Generate:

`data/processed/tbac_da_topo_li_na_transfer_variables.csv`

Required columns:

- `case_id`
- `feed_id`
- `model_basis`
- `basis_type`
- `temperature_C`
- `aqueous_pH`
- `TOPO_wt_pct_in_organic`
- `TBAC_to_DA_molar_ratio`
- `TDS_feature_mg_L`
- `Li_feed_mg_L`
- `Na_mg_L`
- `Na_Li_mass_ratio`
- `organic_to_aqueous_mass_ratio`
- `stage_count`
- `D_Li`
- `D_Na`
- `one_stage_Li_extraction_pct`
- `one_stage_Na_extraction_pct`
- `cumulative_Li_recovery_pct`
- `cumulative_Na_recovery_pct`
- `selectivity_Li_Na`
- `mass_balance_residual`
- `charge_balance_residual`
- `reaction_residual_lnQ_minus_lnK`
- `validity_flag`
- `extrapolation_flag`
- `validity_notes`

## Numeric consistency requirement

Preserve distinct labels for existing result layers:

- `bridge_v0_source_regressed`
- `surrogate_v1_calibrated_surface`
- `direct_epcsaft_v1` if direct ePC-SAFT passes validation

Do not blend these layers.

If a new direct ePC-SAFT result replaces the calibrated transfer table, write a short comparison table showing:

- old nominal Smackover values,
- new nominal Smackover values,
- reason for change,
- validation status.

## Deliverables

Create or update:

- `data/processed/tbac_da_topo_lhs_design.csv`
- `data/processed/tbac_da_topo_phase_inventory_convention_scan.csv`
- `results/tbac_da_topo_phase_inventory_convention_scan.md`
- `data/processed/tbac_da_topo_li_na_transfer_variables.csv`
- `results/tbac_da_topo_li_na_surrogate_report.md`
- optional compatibility mirror into the existing produced-water reference folder
- a short changelog listing files touched and tests run

## Acceptance checks

Pass only if:

- nominal Smackover MS-2 output is reproducible and labeled,
- direct ePC-SAFT results are promoted only when validation passes,
- calibrated bridge outputs are labeled if used,
- TOPO is fixed at 10 wt% in the main case,
- divalent cation extraction is not silently included,
- every row has validity and extrapolation flags,
- high Na/Li produced-water extrapolation is visible.

## Output style restrictions

Do not write conversational filler, apologies, self-reference, “as requested,” “this document aims to,” or progress narration. Use direct technical statements. Every paragraph must support a decision, assumption, benchmark, artifact, model result, risk, or next action.
