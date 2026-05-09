# Rezaee Clean Li+Na Produced-Water Handoff

Date: 2026-05-08

This is the compact handoff for the produced-water lithium case study. It replaces the need to read the full set of case-study docs before choosing surrogate variables.

## One-Sentence Direction

Use a selected Smackover produced-water site as the source basis, pretreat first to remove divalent cations, then model lithium extraction from a clean Li+Na stream using the Rezaee 90 wt% TBAC/decanoic-acid DES + 10 wt% TOPO bridge.

## Current Decision Stack

| Decision | Current choice | Why |
|---|---|---|
| Produced-water source | Southern Arkansas Smackover | High lithium, hypersaline brine, existing brine-handling context. |
| Base row | MS-2 / MSPU 4-W1 | Source-backed row with Li `168 mg/L`, TDS `305,000 mg/L`, Na `64,100 mg/L`. |
| Extraction feed | Pretreated clean Li+Na stream | Ca/Mg/Sr/Ba are removed before Rezaee extraction modeling. |
| Extraction chemistry | Rezaee 2025/2026 DES/TOPO | Best current source-backed Li/Na dataset with DOE responses, SI equilibrium rows, organic parameters, interaction values, and reaction constants. |
| Model status | Source-regressed Li/Na bridge with direct thermodynamic closure gap | Useful for distribution coefficients and PrOMMiS/IDAES handoff, but not a fully accepted direct reactive LLE solve across the design space. |
| Divalent ions | Pretreatment/cost/guardrail variables only | Do not model divalent extraction in this phase. |
| Current response lane | Calibrated surrogate-run script | The calibrated Rezaee distribution surrogate now proves the interface and provides process-facing response rows. |

## Clean Li+Na Feed Basis

Nominal extraction feed after pretreatment:

| Quantity | Value |
|---|---:|
| Li | `168 mg/L` |
| Na | `64,100 mg/L` |
| Na/Li mass ratio | `381.55` |
| TDS feature | `305,000 mg/L` |
| Nominal residual divalent for extraction model | `0 mg/L` |

Pretreatment targets carried in the clean-feed basis:

| Divalent removal target | Residual divalent mg/L | Residual divalent/Li mass ratio | Use |
|---:|---:|---:|---|
| `95.0%` | `2107.92` | `12.55` | Loose pretreatment stress case. |
| `99.0%` | `421.58` | `2.51` | Guardrail/leakage case. |
| `99.9%` | `42.16` | `0.25` | Cleaner pretreatment case. |

The extraction surrogate should start with Li and Na as active cations. Residual divalent concentration is a validity flag and pretreatment-cost variable unless a future model explicitly adds divalent chemistry.

## Variable Ranges To Test

| Variable | Rezaee paper-tested range | Recommended produced-water surrogate range | Nominal | Priority | Reason |
|---|---:|---:|---:|---|---|
| Temperature | `20-40 C` | `20-35 C` | `23 C` | High | Strongest reported selectivity factor; lower temperature favored selectivity. |
| pH | `9.0-11.0` | `9.5-10.8` | `10.4` | Very high | Strongest reported lithium-extraction factor; pH above 11 caused third phase/emulsion risk. |
| TOPO in organic | `10-50 wt%` | `10-30 wt%` | `10 wt%` | High | Response is weaker, but solvent cost and capacity matter; 10 wt% was selected in Rezaee for practical operation. |
| Na/Li mass ratio | `5-15` in Rezaee DOE; Rezaee real-brine-style test is much higher | `190-575` | `381.55` | Very high | The selected Smackover clean stream is far above the DOE domain and must be mapped explicitly. |
| Li feed | `50-1000 mg/L` | `100-300 mg/L` | `168 mg/L` | High | Rezaee found extraction percentage relatively stable across Li concentration, but lithium grade drives process value. |
| Organic/aqueous mass ratio | approximately `0.5-2.0` | `0.5-1.5` | `1.0` | Very high | Directly controls stage capacity and distribution-coefficient interpretation. |
| TDS feature | not a fitted Rezaee DOE variable | `152,500-340,000 mg/L` | `305,000 mg/L` | Medium | Carry as salinity/process/costing feature until direct activity/LLE response rows are generated. |
| Residual divalent | not an extraction variable | `0-430 mg/L` | `0 mg/L` | Guardrail | Flags pretreatment leakage; should not silently enter the Li/Na model. |

## Sodium Issue

The selected Smackover clean stream has a much higher Na/Li ratio than the Rezaee DOE optimum:

- Rezaee DOE/final optimum: Na/Li `5-15`, final selected condition `5`.
- Selected Smackover clean stream: Na/Li `381.55`.
- Rezaee model/natural-brine-style validation: Li about `40.2 mg/L`, Na about `47,705 mg/L`, Na/Li about `1187`.

So the selected Smackover case is outside the DOE sodium range, but not outside the broader high-sodium brine logic of the Rezaee paper. Treat Na/Li as a very-high-priority surrogate variable.

## Seed Runs Already Defined

The current seed matrix has `19` rows:

- Rezaee paper nominal point.
- Smackover clean Li+Na nominal point.
- One-factor low/high points for temperature, pH, TOPO, Na/Li, Li feed, O/A, and TDS.
- Stress point: high Na, high TDS, low solvent inventory.
- Practical selectivity corner: low temperature, controlled pH, nominal TOPO, higher O/A.
- Pretreatment leakage guardrail point.

Do not treat the seed matrix as response data. It is the input contract for calibrated response generation.

## Calibrated Surrogate Now Available

The current calibrated surrogate consumes the clean Li/Na TDS, Li, and O/A input space and emits the downstream response shape needed by PrOMMiS/IDAES. It is calibrated to the upstream Rezaee Section 3.2 DOE-basis surface, but Smackover rows remain high-Na/Li extrapolations.

Key artifacts:

- `data/reference/produced_water/rezaee_tds_li_oa_uq_predictions.csv`
- `data/reference/produced_water/rezaee_tds_li_oa_prommis_idaes_transfer.csv`
- `data/reference/produced_water/rezaee_tds_li_oa_calibrated_idaes_costing_input.csv`
- `data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.csv`
- `data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.md`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/calibrated_li_extraction_surface.png`
- `analyses/rezaee_2026_pcsaft_epcsaft/results/uq_surrogate/figures/calibrated_costing_scenarios.png`

## What The Next Agent Should Build

Build the calibrated surrogate-run script that consumes:

```text
data/reference/produced_water/rezaee_surrogate_seed_run_matrix.csv
```

and emits, for each row:

| Output | Why it is needed |
|---|---|
| Li extraction percent | Primary performance response. |
| Na extraction percent | Sodium co-transfer and selectivity. |
| `D_Li`, `D_Na` | Stage-transfer variables for PrOMMiS/IDAES. |
| `S_Li/Na` | Selectivity surface. |
| Raffinate/extract Li and Na | Material balance and staged-contacting interface. |
| Validity flags | Prevent extrapolated or failed points from entering the surrogate silently. |
| Model status/diagnostics | Needed because direct Rezaee thermodynamic closure is not fully solved yet. |

## Minimal File Bundle

If you want the next agent to use as few files as possible, give them only these:

1. This file:
   `docs/plans/rezaee_clean_li_na_compact_agent_handoff_2026_05_08.md`
2. Machine-readable variable ranges:
   `data/reference/produced_water/rezaee_surrogate_input_variable_ranges.csv`
3. Calibrated surrogate predictions:
   `data/reference/produced_water/rezaee_tds_li_oa_uq_predictions.csv`
4. PrOMMiS/IDAES scaffold results:
   `data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.md`

Everything else is supporting evidence or legacy context.

## Useful Validation Commands

```powershell
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_surrogate_input_space.py
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_tds_li_oa_calibrated_surrogate.py
uv run python analyses\brine_composition_screening\scripts\build_brine_screening_study.py
uv run python -m compileall -q analyses scripts data
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
```

## Hard Boundaries

- Do not claim the raw Smackover brine goes directly into the Rezaee extraction step.
- Do not model Ca/Mg/Sr/Ba extraction in the current Rezaee Li/Na phase.
- Do not claim the calibrated surrogate is direct reactive-LLE closure.
- Do not claim direct published-constant Rezaee reactive-equilibrium closure until the Section 3.2 initial-mole/phase-amount convention gap is resolved.
- Keep HBTA/TOPO as comparison/future parameterization, not the current flagship.

