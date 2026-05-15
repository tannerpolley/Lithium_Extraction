# Agent 1 Prompt: Case-Study Framing, Feed Choices, Naming, and Storyboard

## Required first action

Read `MASTER_CASE_STUDY_CONTEXT_ROADMAP.md` before changing any files.

## Role

Own the case-study framing vertical slice. Revise the project story, feed choices, naming, LHS/LHC scope, and presentation storyboard. Do not rebuild the project. Most artifacts already exist and should be revised, cleaned, or aliased.

## Why this slice exists

The old March presentation was correct for its original context: ePC-SAFT package capability and integration status. The current task is to convert that foundation into an internal produced-water lithium extraction case-study package with screening TEA.

This slice prevents the other agents from using inconsistent claims, old solvent naming, stale feed choices, or a package-first story.

## Scope

Focus only on:

- case-study claim discipline,
- chemical naming cleanup,
- produced-water feed selection,
- LHS/LHC input ranges,
- deck storyboard,
- slide-retention plan for the old package deck.

Do not implement the ePC-SAFT model, PrOMMiS flowsheet, or TEA. Those are Agent 2 and Agent 3 tasks.

## Required solvent naming

Use:

- `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`
- `TBAC/DA DES + 10 wt% TOPO`
- `90 wt% TBAC/DA DES + 10 wt% TOPO`

Do not use a source-author name as the solvent-system label. A source-author name may appear only in bibliography/source notes or existing legacy paths. Do not use it in slide titles, executive summaries, figure captions, artifact names, or new prose as shorthand for the solvent system.

New user-facing artifact names must use `tbac_da_topo`.

## Required project framing

Use this accepted claim:

> This case study demonstrates lithium extraction from produced water using a source-backed produced-water feed, upstream divalent/organics pretreatment, TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO for Li/Na solvent extraction, ePC-SAFT-generated or ePC-SAFT-calibrated transfer variables, and PrOMMiS/IDAES staged extraction with screening-level TEA.

Do not claim:

- full commercialization readiness,
- investment-grade TEA,
- experimental validation on Smackover brine,
- solved divalent extraction,
- fully predictive direct reactive-LLE closure unless Agent 2 validates it,
- REE recovery from the selected feed.

## Feed decisions to implement

Define these selected case-study feeds:

1. `smackover_ms2_main`
   - main flowsheet case,
   - Li `168 mg/L`, TDS `305,000 mg/L`, Na `64,100 mg/L`, Ca `36,900 mg/L`, Mg `3,310 mg/L`,
   - source-backed hard case.

2. `smackover_high_observed_sensitivity`
   - high-Li Smackover sensitivity,
   - Li approximately `252 mg/L`, TDS approximately `340,000 mg/L`.

3. `marcellus_ne_pa_comparison`
   - lower-burden comparison,
   - Li approximately `205 mg/L`, TDS approximately `100,000 mg/L`,
   - missing Na/Ca/Sr/Ba values must be filled from a source or explicitly flagged.

4. `bakken_high_na_stress`
   - model stress case only,
   - Li approximately `103 mg/L`, TDS approximately `258,193 mg/L`, Na/Li approximately `771`.

Do not make Permian the main case. Keep Permian in the landscape/comparison table only unless new high-Li data are added.

## LHS/LHC ranges to implement

Create or revise the LHS/LHC input-range artifact using:

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

Do not vary TOPO from 10–30 wt% in the main case-study design. That makes the case look like the solvent formulation is still being optimized. The official formulation is fixed at 10 wt% TOPO.

## Deck storyboard to produce

Produce a 10–12 slide storyboard with this structure:

1. Internal project ask.
2. Why produced water.
3. Candidate screening.
4. Selected feed cases.
5. Pretreatment boundary.
6. Solvent system.
7. ePC-SAFT role.
8. Base extraction result placeholder.
9. Surrogate/validity gate.
10. PrOMMiS/IDAES workflow.
11. Screening TEA structure.
12. Roadmap and ask.

Each slide entry must include:

- slide title,
- one-sentence message,
- figure/table needed,
- source artifact or source type,
- caveat to preserve.

## Old deck treatment

Identify which parts of the March deck should be:

- retained in main deck,
- compressed into one slide,
- moved to backup,
- removed from the case-study deck.

The old deck is context, not a mistake. Do not write language implying the old deck was wrong.

## Deliverables

Create or update:

- `docs/case_study_tbac_da_topo_storyboard.md`
- `docs/case_study_claims_and_boundaries.md`
- `data/reference/produced_water/selected_case_study_feeds.csv`
- `data/reference/produced_water/tbac_da_topo_lhs_input_ranges.csv`
- a short changelog listing files touched

## Acceptance checks

Pass only if:

- no executive-facing title uses a source-author name as the solvent label,
- Smackover and Marcellus are separated,
- divalent ions are pretreatment/feed-context variables,
- the case is framed as screening TEA/internal project escalation,
- TOPO is fixed at 10 wt% in the main design,
- the storyboard is case-study-first rather than ePC-SAFT-theory-first.

## Output style restrictions

Do not write conversational filler, apologies, self-reference, “as requested,” “this document aims to,” or progress narration. Use direct technical statements. Every paragraph must support a decision, assumption, benchmark, artifact, model boundary, risk, or next action.
