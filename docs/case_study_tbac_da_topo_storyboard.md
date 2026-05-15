# TBAC/DA/TOPO Produced-Water Case-Study Storyboard

## Story Basis

This internal case-study package supports project escalation for produced-water lithium extraction. The main chain is source-backed feed selection, explicit pretreatment, TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO Li/Na extraction, ePC-SAFT-generated or ePC-SAFT-calibrated transfer variables, PrOMMiS/IDAES staged extraction, and screening-level TEA.

The main deck should be case-study-first. ePC-SAFT is the thermodynamic engine and evidence layer, not the headline topic.

## Main Deck Storyboard

| # | Slide title | One-sentence message | Figure/table needed | Source artifact or source type | Caveat to preserve |
|---:|---|---|---|---|---|
| 1 | Internal Project Ask | Approve an internal integration sprint that turns produced-water feed chemistry into staged extraction and screening TEA variables. | One-line workflow graphic: feed to pretreatment to solvent extraction to PrOMMiS/IDAES to screening TEA. | Master roadmap and current repo case-study charter. | This is internal project escalation, not commercialization funding. |
| 2 | Why Produced Water | Produced water is a large, variable, lithium-bearing waste stream where feed chemistry determines whether extraction is credible. | Basin opportunity map or ranked candidate table. | Produced-water screening table and source literature summary. | Volume alone does not make a feed attractive; lithium grade and interference burden matter. |
| 3 | Candidate Screening | Smackover, Marcellus, Bakken, and Permian belong in the same opportunity landscape but not in the same process role. | Screening matrix with Li, TDS, Na/Li, divalent burden, and role. | `data/reference/produced_water/selected_case_study_feeds.csv`. | Permian remains landscape context unless new high-Li data are added. |
| 4 | Selected Feed Cases | Smackover MS-2 is the flagship hard case, high-observed Smackover is the sensitivity case, Marcellus is the lower-burden comparison, and Bakken is a stress test. | Selected-feed table with missing-value flags. | `data/reference/produced_water/selected_case_study_feeds.csv`. | Marcellus missing Na/Ca/Sr/Ba values must be filled before full process simulation. |
| 5 | Pretreatment Boundary | Raw produced water is not the extraction feed; Ca, Mg, Sr, Ba, suspended solids, oil, organics, and pretreatment Li loss sit upstream. | Block diagram separating raw feed, pretreatment, residual-divalent guardrail, and clean Li/Na extraction feed. | Smackover MS-2 source row and pretreatment basis tables. | Divalent ions are not active extraction species in the Li/Na model unless labeled as leakage guardrails. |
| 6 | Solvent System | TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO is the fixed solvent formulation for the main case-study design. | Solvent-system card with formulation, nominal pH, temperature, and O/A basis. | Source-paper extraction and parameter evidence; `data/reference/produced_water/tbac_da_topo_lhs_input_ranges.csv`. | TOPO is fixed at 10 wt% in the main design and is not an optimization variable. |
| 7 | ePC-SAFT Role | ePC-SAFT supplies activity, density, distribution, selectivity, and validity information that process models can consume. | Thermodynamic-to-process transfer-variable schematic. | ePC-SAFT contract checker, bridge reports, distribution-coefficient tables. | Direct reactive-LLE closure is not the model of record until it passes validation. |
| 8 | Base Extraction Result Placeholder | The main result slot should show one labeled source of truth for Smackover clean Li/Na extraction, stage recovery, sodium co-extraction, and selectivity. | Base result table with one-stage Li, one-stage Na, cumulative Li, cumulative Na, selectivity, O/A, and stage count. | Current transfer-variable artifact or replacement direct ePC-SAFT result from Agent 2. | Do not mix bridge, surrogate, and costing recovery numbers without labels. |
| 9 | Surrogate And Validity Gate | The LHS/LHC space maps produced-water variability into transfer variables while flagging extrapolation and residual-divalent risk. | Input-range table plus validity-flag legend. | `data/reference/produced_water/tbac_da_topo_lhs_input_ranges.csv`. | Produced-water high-Na/Li cases exceed the original low-Na/Li source-paper design space. |
| 10 | PrOMMiS/IDAES Workflow | PrOMMiS/IDAES receives transfer variables, stage count, O/A ratio, and validity flags for staged contactor and flowsheet calculations. | Workflow diagram: ePC-SAFT or calibrated bridge to surrogate block to MSContactor to costing. | PrOMMiS/IDAES handoff tables and integration contract. | The process model consumes traceable variables; it does not hide thermodynamic validity limits. |
| 11 | Screening TEA Structure | Screening TEA compares stress, base, and favorable scenarios using stage count, solvent loss, pretreatment Li loss, and feed throughput assumptions. | TEA assumptions table and tornado/sensitivity placeholder. | Screening-TEA assumptions and costing-output artifacts from Agent 3. | Costing is screening-level until solvent loss, reagent use, flowrate, and equipment assumptions are approved. |
| 12 | Roadmap And Ask | The next funded sprint should close direct thermodynamic validation, generate transfer tables, implement staged process logic, and mature screening TEA. | Roadmap table with workstream, proof artifact, and stop condition. | Master roadmap and Agent 2/Agent 3 handoff outputs. | The ask is integration and validation work, not a claim of plant-ready economics. |

## Old March Deck Treatment

| Old deck material | Treatment | Rationale |
|---|---|---|
| Produced-water motivation and DLE landscape | Retain in main deck after tightening to the selected feed roles. | These slides establish why produced water matters and why solvent extraction is the selected recovery route. |
| Solvent-extraction strengths and weaknesses | Retain in main deck as a concise decision slide. | The case study still needs a technology-selection basis and visible solvent-loss/pretreatment caveats. |
| ePC-SAFT definition, parameter tables, and residual Helmholtz contribution details | Compress into one main-deck slide or move details to backup. | Management needs the thermodynamic role, not a theory lecture. |
| ePC-SAFT package history, C++/Python implementation, and API workflow | Move to backup. | Package maturity supports credibility but should not lead the case-study story. |
| Energy-of-transfer, salt activity, mixed-solvent, and activity-validation slides | Move to backup. | Validation evidence is useful for technical review but too detailed for the main 10-12 slide chain. |
| Multiphase-equilibrium algorithm slide | Move to backup unless Agent 2 validates direct reactive-LLE closure. | The current main story must not imply fully predictive direct reactive-LLE closure before validation. |
| Old water/butanol/salt LLE case study | Remove from main deck. | It is a package demonstration, not part of the produced-water Li/Na case chain. |
| Old second-stage Li/Na extraction slides | Move to backup or replace with the TBAC/DA/TOPO base-result slide. | The main result should use the selected solvent formulation and selected feed basis. |
| PrOMMiS integration slide | Retain in main deck after reframing around transfer variables and staged extraction. | This is the main internal project ask. |
| Tasks and timeline slides | Replace with roadmap-and-ask slide. | The new deck needs a decision-oriented integration sprint, not a development backlog. |

## Slide-Language Guardrails

Use chemical solvent labels in titles and executive text. Source-paper author names belong in bibliography/source notes only.

Use `screening-level TEA`, `internal project escalation`, `post-pretreatment Li/Na extraction feed`, `calibrated transfer variables`, `validity flags`, and `phase-inventory / reaction-coordinate reference-state convention`.

Do not use `commercial-ready`, `validated for Smackover brine`, `fully predictive`, `solved divalent extraction`, `REE recovery`, `investment-grade TEA`, or source-author shorthand for the solvent system.
