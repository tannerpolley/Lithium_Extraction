# Analysis Workflow Index

This folder contains durable analysis workflows organized according to `C:\Users\Tanner\.codex\PROJECT_ARCHITECTURE.md`.

Root `scripts/` now contains compatibility wrappers for older commands. New work should edit and test the implementation files under `analyses/<analysis_id>/scripts/`.

| Analysis | Purpose | ePC-SAFT dependency | Primary validation |
|---|---|---:|---|
| `hbta_topo_case_study` | Shan/Gando HBTA/TOPO case-study bridge, solvent scorecard, Zotero evidence, PrOMMiS/IDAES handoff tables, and hard-case retry matrix. | Required for Rezaee smoke, aqueous activity diagnostics, and retry matrix; HBTA/TOPO stage model is a source-regressed surrogate bridge. | `uv run python analyses/hbta_topo_case_study/scripts/hbta_topo_reactive_stage_solve.py`; `uv run python analyses/hbta_topo_case_study/scripts/solvent_candidate_scorecard.py` |
| `electrolyte_lle_literature` | Hubach, Jang, and Gando LLE literature benchmark scripts plus presentation asset generation. | Required for Hubach/Jang direct electrolyte LLE diagnostics; Gando selective scripts use package-derived/surrogate outputs. | `uv run python analyses/electrolyte_lle_literature/scripts/gando_2025_three_stage_crossflow.py`; Hubach/Jang are hard-case diagnostics and may time out. |
| `gando_2025_pcsaft_repro` | Gando 2025 PC-SAFT reproduction and reusable selective-stage helper. | Required for reproduction and selective-stage helper. | `uv run python analyses/gando_2025_pcsaft_repro/scripts/reproduce_gando_2025_pcsaft.py` |
| `yu_2024_figure6` | Yu 2024 Figure 6 digitized, reactive-wrapper, and direct package diagnostic workflows. | Required for direct package diagnostic; digitized recreation can run from curated points. | `uv run python analyses/yu_2024_figure6/scripts/yu_2024_figure6_digitized_recreation.py`; `uv run python analyses/yu_2024_figure6/scripts/yu_2024_figure6_reactive_replication.py` |

See `docs/analysis_workflow_inventory.md` for the fork/test handoff table.
