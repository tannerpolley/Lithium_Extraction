# Phase 9 Final Presentation Skeleton

Last updated: 2026-05-08

## Purpose

This is the Phase 9 presentation-prep document for the produced-water lithium extraction case study. It is designed to be presentation-ready enough to tell the full story, while clearly labeling the scientific/modeling gaps that remain.

## Final Thesis

Southern Arkansas Smackover is a strong flagship produced-water source because the brine is lithium-bearing, hypersaline, and tied to existing brine-handling infrastructure. The selected base site is the source-backed `MS-2 / MSPU 4-W1` Smackover row, but the extraction feed is explicitly pretreated first to remove divalent cations and produce a clean Li+Na stream. The active Li/Na extraction chemistry is now the Rezaee DES/TOPO source-regressed bridge after divalent pretreatment. ePC-SAFT is the thermodynamic layer that ingests source chemistry, evaluates electrolyte/PC-SAFT activity diagnostics, and exports transfer variables for PrOMMiS and IDAES.

## Required Slides

| Slide | Status | Source artifact | Main message |
|---:|---|---|---|
| 1 | scaffolded | `slides/deck.qmd` | ePC-SAFT is the evidence backbone for produced-water lithium extraction. |
| 2 | scaffolded | `slides/deck.qmd` | Produced water is not one feed; basin chemistry changes the answer. |
| 3 | scaffolded | `smackover_usgs_clean_observation_summary.csv` | Smackover is high-value and thermodynamically hard. |
| 4 | scaffolded | `smackover_selected_base_feed_ms2.csv` | The base feed is a real Smackover row: MS-2, 168 mg/L Li, 305,000 mg/L TDS. |
| 4a | scaffolded | `rezaee_clean_li_na_pretreated_feed_basis.csv`; `rezaee_surrogate_input_variable_ranges.csv`; `rezaee_tds_li_oa_uq_predictions.csv` | Pretreatment converts the selected produced water into the clean Li+Na starting basis and the scaffold now exercises the TDS, Li, and O/A response-table shape. |
| 5 | scaffolded | `smackover_critical_minerals_ree_status.csv` | Trace fields exist; REE are not reported and should not be inferred. |
| 6 | archived | `docs/archive/legacy_solvent_choice_hbta_topo_gando_jang_2026_05_08/` | Older solvent-choice material is retained only for traceability. |
| 7 | superseded | `docs/plans/current_rezaee_calibrated_presentation_chain_2026_05_08.md` | The current presentation chain uses Rezaee DES/TOPO and calibrated surrogate outputs. |
| 8 | scaffolded | `rezaee_li_na_distribution_coefficients.csv`; `rezaee_li_na_distribution_bridge_report.md` | The Rezaee source-regressed bridge reproduces Li-over-Na transfer behavior and keeps divalent ions out of the active objective. |
| 9 | scaffolded | `rezaee_tds_li_oa_prommis_idaes_transfer.csv`; `rezaee_tds_li_oa_calibrated_idaes_costing_input.csv` | The staged bridge now emits PrOMMiS/IDAES-ready transfer variables, not only a one-number recovery. |
| 10 | scaffolded | `rezaee_2026_reactive_equilibrium_fit.md`; `rezaee_2026_reactive_equilibrium_replay.md`; `rezaee_2026_reactive_convention_scan.md`; `rezaee_2026_section32_basis_inference.md`; `rezaee_2026_section32_equilibrium_replication.md` | The package evaluates the Rezaee chemical-equilibrium activity terms, and the Section 3.2 diagnostics show the published constants/parameters expose an initial-mole/source-basis gap before direct published-model closure can be claimed. |
| 10a | scaffolded | `rezaee_2026_epcsaft_parameter_smoke_report.md`; `rezaee_calibrated_surrogate_presentation_handoff_2026_05_08.md` | Source verification supports Rezaee DES/TOPO as the active bridge. |
| 11 | scaffolded | `epcsaft_prommis_bridge_contract.csv` and `rezaee_tds_li_oa_prommis_idaes_transfer.csv` | ePC-SAFT-backed outputs become PrOMMiS/IDAES transfer variables. |
| 12 | scaffolded | `rezaee_calibrated_surrogate_mscontactor_costing_results.csv` | Formal IDAES/Pyomo costing scenarios are staged downstream from the Rezaee bridge; values remain scenario scaffolds, not investment-grade TEA. |
| 13 | scaffolded | `docs/plans/prompt.md` | The implementation ask is ePC-SAFT as backend, surrogate generator, or external function. |

## Deck Implementation Status

The Quarto deck now presents the selected base brine slide, Rezaee source-regressed Li/Na transfer slide, calibrated surrogate surface, staged handoff slide, and downstream IDAES costing scaffold. It rendered successfully to `slides/deck.html` and `slides/deck.pptx` on 2026-05-08 before the latest scaffold slide insertion; rerender after any presentation-facing edits. The deck can present the complete current argument with clear caveats: the Li/Na staged-transfer model is source-regressed after divalent pretreatment, while direct published-constant Rezaee thermodynamic closure still has a documented activity/reference-state gap that is not removed by simple convention scans.

## Source Versus Chemistry Boundary

Use this exact distinction:

- Source feed: selected Smackover `MS-2` brine row.
- Pretreatment basis: remove Ca/Mg/Sr/Ba before extraction and start the Rezaee model from the clean Li+Na stream.
- Extraction chemistry: Rezaee DES/TOPO Li/Na extraction after divalent pretreatment.
- Current model: source-regressed Rezaee Li/Na distribution bridge with ePC-SAFT/PC-SAFT activity diagnostics and explicit PrOMMiS/IDAES transfer-variable outputs.
- Future model: direct published-constant Rezaee reactive equilibrium only after the activity-reference gap is resolved, or full organic-phase HBTA/TOPO ePC-SAFT after pure-component, diluent, Li-complex, binary-interaction, and Li/Na reaction-equilibrium gaps close.
- HBTA/TOPO boundary: Shan/Gando HBTA/TOPO/sulfonated kerosene remains a comparison and future parameterization lane, not the active Phase 0-9 flagship bridge.

Do not say the Shan/Gando feed is Smackover. Do not say the Smackover row has measured HBTA/TOPO extraction data.

## Solvent-Selection Status

Use `data/reference/produced_water/solvent_candidate_literature_review_2026_05_07.md` as the current deck-facing scorecard. Zotero MCP full-text verification in this continuation supports:

- Rezaee 2025/2026 as the active DES/TOPO Li/Na source-regressed bridge and package-facing thermodynamic diagnostic lane.
- Shan/Gando 2025 as the field-water HBTA/TOPO/sulfonated-kerosene comparison and future parameterization anchor.
- Zhang 2017 as the HBTA/TOPO stoichiometry and Li/Na selectivity anchor, including the `2 HBTA : 1 TOPO : 1 Li` slope-analysis basis.
- Zhang 2018 as the HBTA/TOPO/kerosene process and mixer-settler support source.
- Rezaee 2026 as a DES/TOPO PC-SAFT/ePC-SAFT parameter-regression and reactive-equilibrium diagnostic lane, with source-regressed bridge outputs used for the current Li/Na presentation.

The literature search found complete Rezaee source inputs for a source-regressed bridge and thermodynamic diagnostics. It did not yet close the direct published-constant reactive-equilibrium model because the package-computed activity coefficients and paper constants require incompatible activity scales. The active benchmark set is the 26 machine-readable SI equilibrium-composition rows; treat the 2026 main-text statement of 36 equilibrium data points as a clerical mismatch unless a source-backed calculation workbook is later supplied.

The newest Section 3.2 replication script starts immediately after Table 8 and uses Eqs. 14/15/17/18/19/20 directly, with ePC-SAFT used only for activity coefficients. The direct Held-2014-S2/no-Born/Table-9/pH-stoichiometric case gives about `100%` Li extraction AARD and about `56.36%` selectivity AARD, not the paper's `7.89%` and `8.63%` post-Table-9 targets. The matching basis-inference script shows the SI aqueous rows are charge balanced and `xOH` follows pH, but the organic total inferred from RLi is a median `3.64x` the organic total inferred from RNa when combined with Table 5 extraction percentages. That means the missing piece is the exact Section 3.2 initial-mole/phase-amount convention, not a missing package `electrolyte_lle` call.

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

Use `data/reference/produced_water/rezaee_tds_li_oa_calibrated_idaes_costing_input.csv` as the Lithium-to-PrOMMiS costing handoff and `data/reference/produced_water/rezaee_calibrated_surrogate_mscontactor_costing_results.csv` as the current PrOMMiS-side IDAES/Pyomo result mirror. It is not an investment-grade TEA until the user approves or replaces:

- feed flowrate;
- annual operating hours;
- solvent loss rate;
- DES, TOPO, NaOH, HCl, carbonate reagent, and replacement-solvent prices;
- Li2CO3 product price;
- avoided-disposal-credit policy.

## Acceptance Boundary

This skeleton is presentation-prep complete when:

1. every number points to a local artifact or source;
2. ionic liquids are excluded from the active benchmark;
3. Smackover source chemistry and Rezaee extraction chemistry are separated;
4. divalent extraction/equilibrium is marked out of scope for the active Li/Na showcase;
5. PrOMMiS/IDAES receives a concrete transfer-variable map;
6. costing is shown as a formal downstream IDAES/Pyomo scenario structure, not investment-grade TEA.

Current status: complete for the Rezaee source-regressed presentation basis and calibrated downstream readiness workflow. Remaining work below is scientific/process depth beyond the current deck, not a blocker to the Rezaee-pivoted Phase 9 artifact.

## Remaining Work That Cannot Be Honestly Skipped

1. Approve final flowrate, operating hours, reagent prices, solvent-loss assumptions, Li2CO3 price, and avoided-disposal-credit policy.
2. Resolve the Rezaee published-constant activity/reference-state gap by locating the original Section 3.2 initial-mole/base-inventory worksheet, or explicitly retain the source-regressed bridge as the accepted presentation model.
3. Replace the calibrated surrogate response columns with calibrated Rezaee/ePC-SAFT extraction, distribution, selectivity, diagnostics, and validity flags.
4. Upgrade the Rezaee-named downstream PrOMMiS/IDAES case from algebraic transfer/costing readiness to a detailed MSContactor unit-model validation.
5. Replace the Li/Na stage bridge with a direct reactive ePC-SAFT phase-equilibrium solve only after the Rezaee activity-reference gap is defensibly closed.
6. Keep HBTA/TOPO parameter fitting as a future comparison lane, not as the current Phase 0-9 blocker.
7. Expand the current PrOMMiS IDAES/Pyomo costing block into detailed unit-model costing once solvent loss, reagent usage, and equipment sizing are approved.
8. If REE matter to the pitch, collect a source that actually reports REE for the selected feed or a separate opportunity dataset.

