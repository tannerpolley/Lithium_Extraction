# Phase 9 Final Presentation Skeleton

Last updated: 2026-05-07

## Purpose

This is the Phase 9 presentation-prep document for the produced-water lithium extraction case study. It is designed to be presentation-ready enough to tell the full story, while clearly labeling the scientific/modeling gaps that remain.

## Final Thesis

Southern Arkansas Smackover is a strong flagship produced-water source because the brine is lithium-bearing, hypersaline, and tied to existing brine-handling infrastructure. The selected base feed is the source-backed `MS-2 / MSPU 4-W1` Smackover row. The non-ionic extraction chemistry is Shan/Gando 2025 HBTA/TOPO/sulfonated kerosene. ePC-SAFT is the thermodynamic layer that should translate source chemistry and solvent chemistry into phase-equilibrium transfer variables for PrOMMiS and IDAES.

## Required Slides

| Slide | Status | Source artifact | Main message |
|---:|---|---|---|
| 1 | scaffolded | `slides/deck.qmd` | ePC-SAFT is the evidence backbone for produced-water lithium extraction. |
| 2 | scaffolded | `slides/deck.qmd` | Produced water is not one feed; basin chemistry changes the answer. |
| 3 | scaffolded | `smackover_usgs_clean_observation_summary.csv` | Smackover is high-value and thermodynamically hard. |
| 4 | scaffolded | `smackover_selected_base_feed_ms2.csv` | The base feed is a real Smackover row: MS-2, 168 mg/L Li, 305,000 mg/L TDS. |
| 5 | scaffolded | `smackover_critical_minerals_ree_status.csv` | Trace fields exist; REE are not reported and should not be inferred. |
| 6 | scaffolded | `non_ionic_solvent_literature_matrix.csv` | HBTA/TOPO is the flagship non-ionic chemistry; DBM/TOPO remains a backup search target. |
| 7 | scaffolded | `jang_2017_stage2_li_na_summary.md` | The old Jang/TBP+D2EHPA placeholder is a limitation baseline. |
| 8 | scaffolded | `hbta_topo_reactive_stage_results.csv` | The calibrated reactive-stage HBTA/TOPO bridge shows Li transfer with very low Na transfer for the selected Smackover feed. |
| 9 | scaffolded | `hbta_topo_reactive_prommis_stage_table.csv` | The staged solve now emits PrOMMiS/IDAES-ready transfer variables, not only a one-number recovery. |
| 10 | scaffolded | `hbta_topo_model_gap_table.csv` and `hbta_topo_reactive_fit.json` | A fitted bridge exists, but full predictive reactive HBTA/TOPO ePC-SAFT still needs validated pure, mixture, complex, and reaction parameters. |
| 10a | scaffolded | `zotero_organic_solvents_review_2026_05_07.md`, `zotero_parameter_source_inventory_2026_05_07.csv`, and `rezaee_2026_epcsaft_parameter_smoke_report.md` | Rezaee 2026 is a DES/TOPO parameter-fitting smoke test and method lead, not proof of full reactive HBTA/TOPO ePC-SAFT. |
| 11 | scaffolded | `epcsaft_prommis_bridge_contract.csv` and `hbta_topo_reactive_prommis_stage_table.csv` | ePC-SAFT-backed outputs become PrOMMiS/IDAES transfer variables. |
| 12 | scaffolded | `hbta_topo_formal_costing_results.csv` | Formal Class-5 costing scenarios exist, with recovery capped to the source-backed 97.17% anchor where the Smackover extrapolation predicts near-total transfer. |
| 13 | scaffolded | `docs/plans/prompt.md` | The implementation ask is ePC-SAFT as backend, surrogate generator, or external function. |

## Deck Implementation Status

The Quarto deck now includes the selected base brine slide, calibrated reactive-stage transfer slide, staged handoff slide, and formal Class-5 costing scaffold. The deck is therefore Phase 9 scaffolded: it can present the complete argument with clear caveats, even though the true predictive reactive HBTA/TOPO ePC-SAFT parameterization is still not complete.

## Source Versus Chemistry Boundary

Use this exact distinction:

- Source feed: selected Smackover `MS-2` brine row.
- Extraction chemistry: Shan/Gando HBTA/TOPO/sulfonated kerosene.
- Current model: calibrated reactive-stage HBTA/TOPO bridge with `2 HBTA : 1 TOPO : 1 Li` stoichiometry, ePC-SAFT aqueous activity coefficients when available, and explicit PrOMMiS/IDAES transfer-variable outputs.
- Future model: true predictive reactive HBTA/TOPO ePC-SAFT LLE after pure-component, diluent, complex, binary-interaction, and reaction-equilibrium gaps close.
- Rezaee model boundary: DES/TOPO organic phase PC-SAFT plus aqueous ePC-SAFT is useful method evidence, but it is not the Shan/Gando HBTA/TOPO/sulfonated-kerosene model.

Do not say the Shan/Gando feed is Smackover. Do not say the Smackover row has measured HBTA/TOPO extraction data.

## ePC-SAFT Novelty Argument

The unique value of ePC-SAFT in this case study is not simply predicting a higher lithium recovery. The value is that it can provide:

1. phase equilibrium under hypersaline conditions;
2. aqueous and organic phase compositions;
3. activity/fugacity-informed distribution behavior;
4. Li/Na and future Li/Mg/Li/Ca selectivity variables;
5. sensitivity surfaces over Li, TDS, O/A, solvent loading, and pretreatment;
6. validity diagnostics for surrogate training;
7. a defensible transfer-variable contract for PrOMMiS and IDAES.

## Costing Scaffold

Use `data/reference/produced_water/hbta_topo_formal_costing_results.csv` as the current formal Class-5 economic scaffold. It is not an investment-grade TEA until the user approves or replaces:

- feed flowrate;
- annual operating hours;
- solvent loss rate;
- HBTA, TOPO, diluent, NaOH, HCl, carbonate reagent prices;
- Li2CO3 product price;
- avoided-disposal-credit policy.

## Acceptance Boundary

This skeleton is presentation-prep complete when:

1. every number points to a local artifact or source;
2. ionic liquids are excluded from the active benchmark;
3. Smackover source chemistry and Shan/Gando extraction chemistry are separated;
4. true reactive HBTA/TOPO ePC-SAFT is marked as a gap, not implied as complete;
5. PrOMMiS/IDAES receives a concrete transfer-variable map;
6. costing is shown as formal Class-5 scenario structure, not investment-grade TEA.

## Remaining Work That Cannot Be Honestly Skipped

1. Approve final flowrate, operating hours, reagent prices, solvent-loss assumptions, Li2CO3 price, and avoided-disposal-credit policy.
2. Find, fit, or formally define HBTA, TOPO, sulfonated-kerosene/diluent, and Li-BTA-TOPO complex ePC-SAFT parameters.
3. Replace the fitted bridge constants with published/validated HBTA deprotonation, saponification, and Li-BTA-TOPO reaction-equilibrium constants, or regress them with a documented uncertainty envelope.
4. Replace the calibrated reactive-stage bridge with a true predictive reactive ePC-SAFT LLE solve once the parameter set is defensible.
5. Convert the Rezaee diagnostic fit into a documented package-regression smoke test and use it to guide, not replace, HBTA/TOPO parameter fitting.
6. Add a true PrOMMiS/IDAES MSContactor solve and IDAES costing block when those dependencies are available in the local environment.
7. If REE matter to the pitch, collect a source that actually reports REE for the selected feed or a separate opportunity dataset.
