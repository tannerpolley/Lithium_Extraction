# Agent 3 Prompt: PrOMMiS/IDAES Staged Extraction, Screening TEA, and Deck Revision

## Required first action

Read `MASTER_CASE_STUDY_CONTEXT_ROADMAP.md`, Agent 1 outputs, and Agent 2 outputs before changing process, costing, or presentation files.

Required Agent 1 outputs:

- `docs/case_study_tbac_da_topo_storyboard.md`
- `docs/case_study_claims_and_boundaries.md`
- `data/reference/produced_water/selected_case_study_feeds.csv`
- `data/reference/produced_water/tbac_da_topo_lhs_input_ranges.csv`

Required Agent 2 outputs:

- `data/processed/tbac_da_topo_li_na_transfer_variables.csv`
- `results/tbac_da_topo_li_na_surrogate_report.md`
- `results/tbac_da_topo_phase_inventory_convention_scan.md`

## Role

Own the process, screening-TEA, and presentation vertical slice. Consume the transfer-variable table and produce the staged extraction, cost-scenario, readiness, and deck artifacts.

## Why this slice exists

The project must look like a case study, not a package lecture. This slice converts ePC-SAFT or calibrated transfer variables into a management-facing demonstration: produced water → pretreatment → Li/Na solvent extraction → staged process model → screening TEA → internal project ask.

## Scope

Focus only on:

- PrOMMiS/IDAES staged extraction,
- transfer-table consumption,
- recovery reconciliation,
- screening TEA,
- clean figures,
- case-study deck.

Do not revise feed selection or model-generation logic unless Agent 1 or Agent 2 outputs are missing or inconsistent. If they are inconsistent, document the inconsistency and use the safest source-backed value.

## Required solvent naming

Use:

- `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`
- `TBAC/DA DES + 10 wt% TOPO`
- `90 wt% TBAC/DA DES + 10 wt% TOPO`

Do not use a source-author name as the solvent-system label in new slides, reports, figure captions, or executive summaries. Existing legacy folder names may remain only as compatibility references.

## Required presentation framing

The deck must support internal project escalation, not commercialization.

Use this case-study claim:

> This case study demonstrates lithium extraction from produced water using a source-backed produced-water feed, upstream divalent/organics pretreatment, TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO for Li/Na solvent extraction, ePC-SAFT-generated or ePC-SAFT-calibrated transfer variables, and PrOMMiS/IDAES staged extraction with screening-level TEA.

Do not make the deck an ePC-SAFT theory lecture. ePC-SAFT theory gets one main slide plus backup.

## Process workflow to implement

Minimum workflow:

1. raw produced water,
2. pretreatment for Ca/Mg/Sr/Ba and organics,
3. clean Li/Na extraction feed,
4. 1–5 solvent-extraction stages,
5. loaded organic,
6. stripping/regeneration placeholder,
7. Li concentrate or Li2CO3-equivalent placeholder,
8. spent brine / Na-bearing raffinate.

Divalent ions must appear in pretreatment cost/loss logic, not as active Li/Na extraction species.

## Transfer-variable consumption

Use Agent 2 transfer variables as the source of truth.

Required consumed variables:

- `D_Li`
- `D_Na`
- `one_stage_Li_extraction_pct`
- `one_stage_Na_extraction_pct`
- `cumulative_Li_recovery_pct`
- `cumulative_Na_recovery_pct`
- `selectivity_Li_Na`
- `organic_to_aqueous_mass_ratio`
- `stage_count`
- `validity_flag`
- `extrapolation_flag`

Do not invent extraction values in the process model.

## Recovery reconciliation requirement

Reconcile transfer-table staged recovery with IDAES/costing recovery.

Create a short reconciliation table with:

- `case_id`,
- transfer-table cumulative Li recovery,
- PrOMMiS/IDAES staged Li recovery,
- absolute difference,
- reason for difference,
- chosen deck value.

Valid reasons may include:

- different stage-count definition,
- different basis after pretreatment Li loss,
- different solvent-ratio implementation,
- stale mirror artifact,
- costing model uses additional process loss.

Do not show conflicting recovery values in the deck without this reconciliation.

## Screening TEA requirements

Create stress/base/favorable scenarios:

1. stress: lower Li, high TDS/high Na, low O/A,
2. base: Smackover MS-2,
3. favorable: Marcellus NE comparison or high-Li/lower-burden case if chemistry is complete,
4. sensitivity: pretreatment Li loss,
5. sensitivity: solvent loss,
6. sensitivity: stage count.

Required TEA fields:

- `case_id`
- `scenario`
- `feed_flow_m3_day`
- `operating_days_per_year`
- `Li_feed_mg_L`
- `Li_recovery_pct`
- `pretreatment_Li_loss_pct`
- `solvent_loss_rate`
- `stage_count`
- `Li2CO3_kg_year`
- `major_cost_assumptions`
- `breakeven_metric`
- `net_before_tax_or_margin_metric`
- `validity_flag`
- `screening_tea_caveat`

All cost values must be labeled screening TEA. Do not imply vendor-grade, design-grade, or investment-grade certainty.

## Deck requirements

Create or revise a 10–12 slide main deck.

Required slide order:

1. Internal project ask.
2. Why produced water.
3. Candidate screening.
4. Selected feed cases.
5. Pretreatment boundary.
6. Solvent system.
7. ePC-SAFT role.
8. Base extraction result.
9. Surrogate/validity gate.
10. PrOMMiS/IDAES workflow.
11. Screening TEA.
12. Roadmap and ask.

Backup slides:

- ePC-SAFT theory details,
- solvent-extraction definitions,
- source-paper benchmark details,
- phase-inventory diagnostics,
- literature scorecard,
- full TEA assumption table.

## Figure requirements

Figures should be clean, sparse, and management-readable.

Preferred figures:

1. produced-water candidate ranking,
2. Smackover vs Marcellus feed card,
3. pretreatment boundary schematic,
4. TBAC/DA DES + 10 wt% TOPO mechanism schematic,
5. Li/Na extraction result card,
6. surrogate validity/extrapolation plot,
7. PrOMMiS/IDAES integration block diagram,
8. screening-TEA scenario bars or tornado chart.

Do not use dense raw plots or theory diagrams in the main deck unless they directly support the case-study decision.

## Deliverables

Create or update:

- `data/processed/tbac_da_topo_prommis_stage_results.csv`
- `results/tbac_da_topo_prommis_stage_results.md`
- `data/processed/tbac_da_topo_screening_tea_results.csv`
- `results/tbac_da_topo_screening_tea.md`
- `slides/case_study_tbac_da_topo_produced_water/deck.qmd` or `deck.tex`
- `slides/case_study_tbac_da_topo_produced_water/figures/`
- `docs/final_case_study_readiness_checklist.md`
- a short changelog listing files touched and tests/renders run

## Acceptance checks

Pass only if:

- the deck is 10–12 main slides,
- the first slide is the internal project ask,
- the deck is case-study-first,
- ePC-SAFT theory is one main slide plus backup,
- the solvent system is named chemically,
- Smackover is the main case and Marcellus is the comparison,
- pretreatment boundary is clear,
- transfer-table and costing recovery are reconciled,
- every major number comes from a source or generated artifact,
- cost numbers are labeled screening TEA,
- the project ask is internal formalization and integration funding.

## Output style restrictions

Do not write conversational filler, apologies, self-reference, “as requested,” “this document aims to,” or progress narration. Use direct technical statements. Every paragraph must support a decision, assumption, benchmark, artifact, model result, risk, or next action.
