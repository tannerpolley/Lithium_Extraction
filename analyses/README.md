# Analysis Workflow Index

This folder contains durable analysis workflows organized according to
`C:\Users\Tanner\.codex\PROJECT_ARCHITECTURE.md`.

Root `scripts/` is for shared repository helpers only. New work should edit and
test implementation files under `analyses/<analysis_id>/scripts/`.

| Analysis | Purpose | ePC-SAFT dependency | Primary validation |
|---|---|---:|---|
| `brine_composition_screening` | Cross-brine composition screen and produced-water candidate ranking for the Rezaee DES/TOPO case-study lens. | None for screening; outputs feed Rezaee/ePC-SAFT and PrOMMiS/IDAES workflows. | `uv run python analyses/brine_composition_screening/scripts/build_brine_screening_study.py` |
| `rezaee_2026_pcsaft_epcsaft` | Active Rezaee DES/TOPO Li/Na bridge, parameter smoke, clean-feed surrogate space, and PrOMMiS/IDAES handoff tables. | Required for DES density refit, electrolyte diagnostics, and Rezaee bridge transfer variables. | `uv run python analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_des_epcsaft_parameter_smoke.py`; `uv run python analyses/rezaee_2026_pcsaft_epcsaft/scripts/rezaee_surrogate_input_space.py` |
| `electrolyte_lle_literature` | Hubach, Jang, Gando, and Ascani method-reference scripts for ePC-SAFT/LLE diagnostics and retained benchmark assets. | Required for Hubach/Jang/Yu-style package diagnostics; Gando selective scripts are literature benchmark surrogates. | `uv run python analyses/electrolyte_lle_literature/scripts/gando_2025_three_stage_crossflow.py`; Hubach/Jang are hard-case diagnostics and may time out. |
| `yu_2024_figure6` | Yu 2024 Figure 6 digitized recreation, reactive wrapper, and direct package diagnostic workflow. | Required for direct package diagnostic; digitized recreation can run from curated points. | `uv run python analyses/yu_2024_figure6/scripts/yu_2024_figure6_digitized_recreation.py`; `uv run python analyses/yu_2024_figure6/scripts/yu_2024_figure6_reactive_replication.py` |
| `smackover_sar_li_reference` | Reference workflow and source inputs for the Smackover SAR lithium mapping bundle. | None. | Reference workflow only; generated outputs are not tracked. |

See `docs/analysis_workflow_inventory.md` for the fork/test handoff table.
