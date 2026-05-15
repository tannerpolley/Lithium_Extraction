# Case-Study Claims And Boundaries

## Accepted Claim

This case study demonstrates lithium extraction from produced water using a source-backed produced-water feed, upstream divalent/organics pretreatment, TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO for Li/Na solvent extraction, ePC-SAFT-generated or ePC-SAFT-calibrated transfer variables, and PrOMMiS/IDAES staged extraction with screening-level TEA.

## Scope Decisions

| Topic | Case-study decision | Boundary |
|---|---|---|
| Project purpose | Internal project escalation for ePC-SAFT-to-PrOMMiS/IDAES integration. | Do not present as commercialization readiness or investment-grade TEA. |
| Main feed | `smackover_ms2_main`, a southern Arkansas Smackover MS-2 hard case. | Do not make Permian the main case under current data. |
| Comparison feed | `marcellus_ne_pa_comparison`, a lower-burden comparison case. | Missing Na/Ca/Sr/Ba values must be filled before full process simulation. |
| Sensitivity feed | `smackover_high_observed_sensitivity`, a high-Li Smackover sensitivity. | Use as sensitivity, not as the single base flowsheet. |
| Stress feed | `bakken_high_na_stress`, a high-Na model stress case. | Use for surrogate stress and validity testing only. |
| Pretreatment | Divalent ions, solids, oils, organics, and pretreatment Li loss are explicit upstream variables. | Do not let Ca/Mg/Sr/Ba silently enter the Li/Na extraction model. |
| Solvent formulation | `90 wt% TBAC/DA DES + 10 wt% TOPO` with TBAC:DA fixed at `1:2`. | Do not vary TOPO in the main LHS/LHC design. |
| Thermodynamic basis | ePC-SAFT-generated or ePC-SAFT-calibrated transfer variables. | Direct reactive-LLE closure must pass validation before becoming the model of record. |
| Process basis | PrOMMiS/IDAES staged extraction consumes transfer variables and validity flags. | Process calculations must not erase the thermodynamic validity limits. |
| Economics | Screening-level TEA with sensitivity to stage count, solvent loss, pretreatment Li loss, and throughput. | Cost values are scenario scaffolds until assumptions are approved. |

## Feed Boundary

The selected source row is raw produced water. The extraction model starts after pretreatment removes the major divalent and organic burden. The active extraction feed is therefore a post-pretreatment Li/Na stream that retains salinity and Na/Li burden as process features.

Residual divalent ions may appear only as `residual_divalent_mg_L` guardrail values. A nonzero residual-divalent value means pretreatment leakage risk, not solved divalent extraction.

## Model Boundary

The main deck should use one labeled result layer for the base extraction result. Current roadmap labels separate three numeric layers:

| Layer | Meaning | Deck use |
|---|---|---|
| `bridge_v0_source_regressed` | Earlier source-regressed Li/Na bridge. | Backup validation layer. |
| `surrogate_v1_calibrated_surface` | Current process handoff table. | Main result unless direct ePC-SAFT replaces it. |
| `idaes_costing_v1` | PrOMMiS/IDAES costing implementation. | Screening TEA output. |

The transfer-table recovery and costing recovery should not appear on the same slide unless the recovery definition, stage implementation, or stale-artifact status is explicitly labeled.

## Source And Evidence Boundaries

| Claim type | Allowed language | Required caveat |
|---|---|---|
| Produced-water feed | Source-backed Smackover MS-2 feed basis. | This is not experimental validation of the solvent system on Smackover brine. |
| Solvent chemistry | TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO has source-paper extraction and parameter evidence. | Source-paper author names stay in bibliography/source notes, not solvent labels. |
| Direct ePC-SAFT | Direct ePC-SAFT closure is preferred. | Until validated, use calibrated transfer variables with validity flags. |
| Surrogate design | LHS/LHC covers Li, TDS, Na/Li, O/A, temperature, pH, stage count, residual-divalent guardrail, and feed ID. | TOPO and TBAC:DA are fixed formulation variables. |
| PrOMMiS/IDAES | Staged extraction and costing receive traceable transfer variables. | The process model is not independent proof of thermodynamic validity. |
| Critical minerals | Lithium is the product basis. | Do not claim REE recovery from the selected Smackover feed; REE are not reported in the local source file. |

## Restricted Claims

Do not claim full commercialization readiness, investment-grade TEA, experimental validation on Smackover brine, solved divalent extraction, fully predictive direct reactive-LLE closure, REE recovery from the selected feed, or a general lithium-extraction platform for all brines.

## Required Acceptance Statements

- Smackover MS-2 is the main hard-case flowsheet feed.
- Marcellus NE PA is a comparison case with missing-value flags until Na/Ca/Sr/Ba are sourced.
- Bakken is a high-Na stress case only.
- Permian remains an opportunity-landscape case, not the main case.
- Divalent ions are pretreatment and guardrail variables.
- TOPO is fixed at 10 wt% in the main design.
- The management ask is an internal integration and validation sprint.
