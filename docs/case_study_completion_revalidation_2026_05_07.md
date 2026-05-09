# Case Study Completion Revalidation

Date: 2026-05-07

> Superseded context, 2026-05-08: this document records the pre-pivot HBTA/TOPO review state. The current Phase 0-9 source of truth is the Rezaee DES/TOPO Li/Na bridge after divalent pretreatment. Use `docs/phase0_8_completion_report.md`, `docs/phase9_final_presentation_skeleton.md`, `docs/plans/lithium_project_status_handoff_2026_05_08.md`, and `analyses/rezaee_2026_pcsaft_epcsaft/README.md` before using any HBTA-first claims below.

Scope: HBTA/TOPO source-regressed Li/Na case study, broader Lithium Recovery Zotero evidence, existing article-analysis folders, Quarto/MiKTeX exports, and downstream PrOMMiS/IDAES costing.

## Zotero Access

- Current-thread Zotero MCP status: failed with `Transport closed` after the required single lightweight retry.
- Fresh subagent Zotero MCP status: passed. It resolved `Lithium Recovery` as collection `SAVYNVAK`, with direct item count `30` and recursive item briefs `45`.
- Fallback path used in this thread: Zotero Local API plus the local `zotero-local-research` index. The generated deep-review rows are labeled as fallback evidence.
- API/index coverage used by `scripts/case_study/zotero_lithium_recovery_deep_review.py`: recursive Zotero Local API item count `53`, local index `C:\Users\Tanner\AppData\Local\zotero-local-codex-plugin\index.sqlite`.

## Evidence Artifacts

- `data/reference/produced_water/zotero_lithium_recovery_deep_review_2026_05_07.md`
- `data/reference/produced_water/zotero_lithium_recovery_collection_inventory_2026_05_07.csv`
- `data/reference/produced_water/zotero_lithium_recovery_candidate_expansion_2026_05_07.csv`
- `data/reference/produced_water/zotero_lithium_recovery_api_evidence_2026_05_07.csv`
- `data/reference/produced_water/zotero_lithium_recovery_parameter_fit_opportunities_2026_05_07.csv`
- `data/reference/produced_water/zotero_lithium_recovery_figure_replication_opportunities_2026_05_07.csv`
- `docs/engineering_thermodynamics_score_review_2026_05_07.md`

## Best Candidate Findings

| Candidate | Score | Use |
|---|---:|---|
| HBTA + TOPO + sulfonated kerosene | 88 | Flagship Friday case study and active Li/Na source-regressed model. |
| TBAC + decanoic-acid DES + TOPO | 76 | Best parameter-regression and package-plumbing pilot, not flagship chemistry. |
| D2EHDTPA + BuPhen + octanol modifiers + n-dodecane | 73 | Best non-HBTA multication backup. |
| HBTA/TOPO or HTTA/TOPO synergistic DES | 67 | New pseudo-component physical-property fitting candidate. |
| TBP + FeCl3/HCl + kerosene | 62 | Conventional high-Mg comparator. |
| D2EHPA + TBP + kerosene | 59 | Produced-water limitation baseline. |
| Functional ionic liquids for Canadian produced water | 59 | New alternate real-produced-water evidence, outside the non-ionic flagship pitch. |
| DBM + TOPO synergistic extraction | 58 | High-upside review-only target; primary source must be pinned before deck promotion. |
| Heteropolyacid ionic liquid + hydrophobic ionic-liquid diluent | 56 | New high-Mg selectivity contrast case. |
| Ammonium ionic liquid extraction system | 48 | Ionic-liquid mechanism and cost-bound reference. |

## Model And Costing Status

- HBTA/TOPO predictive audit: Li/Na fit scope passed, no per-case refit passed, aqueous activity passed with fallback, organic ePC-SAFT parameters remain limited, multication competition remains out of first-closure scope, and formal IDAES costing handoff is ready.
- Main fit residuals remain small against source-regressed anchors: Gando/Shan cumulative Li residuals are `-0.0618`, `+0.1224`, and `-0.1315` percentage points for stages 1-3; Zhang 2017 selectivity lower-bound residual is `+0.0080`.
- Formal PrOMMiS/IDAES costing regenerated `hbta_topo_idaes_costing_results.csv` and `.md` in the PrOMMiS checkout.
- Current formal costing result remains intentionally harsh: low/base/high scenarios have negative before-tax margins because solvent, pretreatment, and concentration assumptions are still Class-5 style and not vendor-grade TEA.

## Revalidation Commands

| Command | Result |
|---|---|
| `uv run python legacy Zotero review command removed during cleanup` | Passed; regenerated Zotero evidence and candidate artifacts. |
| `uv run python legacy HBTA/TOPO stage command removed during cleanup` | Passed; regenerated source-regressed HBTA/TOPO model artifacts. |
| `uv run python analyses\\rezaee_2026_pcsaft_epcsaft\\scripts\\rezaee_des_epcsaft_parameter_smoke.py` | Passed; density fit succeeded, ePC-SAFT LLE remains diagnostic error. |
| `uv run python analyses\\rezaee_2026_pcsaft_epcsaft\\scripts\\rezaee_surrogate_input_space.py` | Passed; regenerated Smackover transfer and PrOMMiS handoff skeletons. |
| `uv run python legacy solvent scorecard command removed during cleanup` | Passed; regenerated active scorecard and run matrix. |
| `uv run python analyses\\yu_2024_figure6\\scripts\\yu_2024_figure6_digitized_recreation.py` | Passed. |
| `uv run python analyses\\yu_2024_figure6\\scripts\\yu_2024_figure6_reactive_replication.py` | Passed. |
| `uv run python analyses\\electrolyte_lle_literature\\scripts\\gando_2025_three_stage_crossflow.py` | Passed. |
| `uv run python analyses\\electrolyte_lle_literature\\scripts\\gando_2025_three_stage_crossflow.py` | Passed. |
| `uv run python analyses\\electrolyte_lle_literature\\scripts\\gando_2025_one_stage_assets.py` | Passed. |
| `uv run python analyses\\electrolyte_lle_literature\\scripts\\gando_2025_slide_assets.py` | Passed. |
| `uv run python analyses\\electrolyte_lle_literature\\scripts\\_debug_hubach_single_point.py` | Timed out at 180 seconds; stopped the two remaining child PIDs. |
| `uv run python analyses\\electrolyte_lle_literature\\scripts\\jang_2017_stage2_li_na_tbp_d2ehpa.py` | Timed out at 180 seconds; stopped the two remaining child PIDs. |
| `uv run python -m compileall -q scripts data` | Passed. |
| `C:\ProgramData\Miniconda3\envs\prommis\python.exe -m prommis.solvent_extraction.pcsaft_integration.hbta_topo_idaes_costing` | Passed. |
| `C:\ProgramData\Miniconda3\envs\prommis\python.exe -m pytest src\prommis\solvent_extraction\pcsaft_integration\tests -q` | Passed: `144 passed, 3 skipped`. |

## MiKTeX And Deck Exports

- MiKTeX is installed at `C:\Users\Tanner\AppData\Local\Programs\MiKTeX\miktex\bin\x64`.
- `pdflatex --version` reports `MiKTeX-pdfTeX 4.23 (MiKTeX 25.12)`.
- The package-database lock seen during diagnostics was caused by parallel MiKTeX package-manager commands. No stale lock remained after those commands exited.
- Quarto revealjs render passed: `slides/deck.html`.
- Quarto PPTX render passed: `slides/deck.pptx`.
- Quarto PDF render passed with `lualatex`: `slides/deck.pdf`.

## Highest-Value Improvements Remaining

1. Pin or digitize Zhang 2017 direct HBTA/TOPO distribution, O/A, pH, temperature, and capacity figures; this is the strongest route to improving parameter identifiability and distribution-coefficient confidence.
2. Extract Gando/Shan cation-effect tables separately from staged Li recovery to keep divalent assumptions quantitative but not fabricated.
3. Use Zhang 2018 mixer-settler data as process-scale validation for stage count, residence, and concentration behavior.
4. Build a true PrOMMiS MSContactor solve against the source-regressed transfer table, then propagate uncertainty bands instead of point values only.
5. Replace Class-5 costing assumptions with solvent price/loss, acid/base regeneration, pretreatment reagent, concentration-energy, and contactor-sizing ranges.

