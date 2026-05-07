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
| 6 | scaffolded | `non_ionic_solvent_literature_matrix.csv`; `solvent_candidate_scorecard_2026_05_07.csv`; `solvent_candidate_run_matrix_2026_05_07.csv` | HBTA/TOPO is the flagship non-ionic chemistry; D2EHDTPA/BuPhen is the best non-HBTA backup, and Rezaee is the parameter-regression pilot. |
| 7 | scaffolded | `jang_2017_stage2_li_na_summary.md` | The old Jang/TBP+D2EHPA placeholder is a limitation baseline. |
| 8 | scaffolded | `hbta_topo_reactive_stage_results.csv`; `hbta_topo_predictive_regression_residuals.csv` | The source-regressed Li/Na HBTA/TOPO stage model reproduces the Gando/Zhang anchors and shows Li transfer with very low Na transfer for the selected Smackover feed. |
| 9 | scaffolded | `hbta_topo_reactive_prommis_stage_table.csv` | The staged solve now emits PrOMMiS/IDAES-ready transfer variables, not only a one-number recovery. |
| 10 | scaffolded | `hbta_topo_model_gap_table.csv`, `hbta_topo_reactive_fit.json`, and `hbta_topo_predictive_model_audit.csv` | The Li/Na model is now source-regressed and reusable, but full multication reactive HBTA/TOPO ePC-SAFT still needs validated pure, mixture, complex, and reaction parameters. |
| 10a | scaffolded | `solvent_candidate_literature_review_2026_05_07.md`, `solvent_candidate_run_matrix_2026_05_07.csv`, `zotero_organic_solvents_review_2026_05_07.md`, `zotero_parameter_source_inventory_2026_05_07.csv`, and `rezaee_2026_epcsaft_parameter_smoke_report.md` | Zotero MCP verification supports the Gando/Zhang HBTA/TOPO claims and the backup ranking; Rezaee 2026 remains a DES/TOPO parameter-fitting smoke test, not proof of full reactive HBTA/TOPO ePC-SAFT. |
| 11 | scaffolded | `epcsaft_prommis_bridge_contract.csv` and `hbta_topo_reactive_prommis_stage_table.csv` | ePC-SAFT-backed outputs become PrOMMiS/IDAES transfer variables. |
| 12 | scaffolded | `hbta_topo_idaes_costing_input.csv`; PrOMMiS `hbta_topo_idaes_costing_results.csv` | Formal IDAES/Pyomo costing scenarios exist downstream, with recovery capped to the source-backed 97.17% anchor where the Smackover extrapolation predicts near-total transfer. |
| 13 | scaffolded | `docs/plans/prompt.md` | The implementation ask is ePC-SAFT as backend, surrogate generator, or external function. |

## Deck Implementation Status

The Quarto deck now includes the selected base brine slide, source-regressed Li/Na stage-transfer slide, staged handoff slide, and formal downstream IDAES costing scaffold. The deck can present the complete current argument with clear caveats: the Li/Na staged-transfer model is now source-regressed, while full multication reactive HBTA/TOPO ePC-SAFT parameterization is still not complete.

## Source Versus Chemistry Boundary

Use this exact distinction:

- Source feed: selected Smackover `MS-2` brine row.
- Extraction chemistry: Shan/Gando HBTA/TOPO/sulfonated kerosene.
- Current model: source-regressed Li/Na HBTA/TOPO stage model with `2 HBTA : 1 TOPO : 1 Li` stoichiometry, ePC-SAFT aqueous activity coefficients when available, and explicit PrOMMiS/IDAES transfer-variable outputs.
- Future model: full multication reactive HBTA/TOPO ePC-SAFT LLE after pure-component, diluent, complex, binary-interaction, and reaction-equilibrium gaps close.
- Rezaee model boundary: DES/TOPO organic phase PC-SAFT plus aqueous ePC-SAFT is useful method evidence, but it is not the Shan/Gando HBTA/TOPO/sulfonated-kerosene model.

Do not say the Shan/Gando feed is Smackover. Do not say the Smackover row has measured HBTA/TOPO extraction data.

## Solvent-Selection Status

Use `data/reference/produced_water/solvent_candidate_literature_review_2026_05_07.md` as the current deck-facing scorecard. Zotero MCP full-text verification in this continuation supports:

- Shan/Gando 2025 as the active field-water HBTA/TOPO/sulfonated-kerosene process anchor.
- Zhang 2017 as the HBTA/TOPO stoichiometry and Li/Na selectivity anchor, including the `2 HBTA : 1 TOPO : 1 Li` slope-analysis basis.
- Zhang 2018 as the HBTA/TOPO/kerosene process and mixer-settler support source.
- Rezaee 2026 as a DES/TOPO PC-SAFT/ePC-SAFT parameter-regression smoke test, not the flagship chemistry.

The literature search found reaction expressions and thermodynamic-parameter relationships for the HBTA/TOPO extraction chemistry, but not a complete published parameter payload that can replace the source-regressed stage constants with fully physical ePC-SAFT/reaction parameters for the Smackover case.

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

Use `data/reference/produced_water/hbta_topo_idaes_costing_input.csv` as the Lithium-to-PrOMMiS costing handoff and `C:\Users\Tanner\Documents\git\prommis\src\prommis\solvent_extraction\pcsaft_integration\hbta_topo_idaes_costing_results.csv` as the downstream formal IDAES/Pyomo economic scaffold. It is not an investment-grade TEA until the user approves or replaces:

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
4. full multication reactive HBTA/TOPO ePC-SAFT is marked as a gap, not implied as complete;
5. PrOMMiS/IDAES receives a concrete transfer-variable map;
6. costing is shown as a formal downstream IDAES/Pyomo scenario structure, not investment-grade TEA.

## Remaining Work That Cannot Be Honestly Skipped

1. Approve final flowrate, operating hours, reagent prices, solvent-loss assumptions, Li2CO3 price, and avoided-disposal-credit policy.
2. Find, fit, or formally define HBTA, TOPO, sulfonated-kerosene/diluent, and Li-BTA-TOPO complex ePC-SAFT parameters.
3. Replace the source-regressed stage constants with published/validated HBTA deprotonation, saponification, and Li-BTA-TOPO reaction-equilibrium constants if those become available, or expand the current uncertainty envelope with raw replicated data.
4. Replace the Li/Na stage model with a full multication reactive ePC-SAFT LLE solve once the parameter set is defensible.
5. Convert the Rezaee diagnostic fit into a documented package-regression smoke test and use it to guide, not replace, HBTA/TOPO parameter fitting.
6. Expand the current PrOMMiS IDAES/Pyomo costing block into detailed unit-model costing once solvent loss, reagent usage, and equipment sizing are approved.
7. If REE matter to the pitch, collect a source that actually reports REE for the selected feed or a separate opportunity dataset.
