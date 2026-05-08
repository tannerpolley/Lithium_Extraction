# Root Scripts

Root `scripts/` is kept for repository-level helpers and backwards-compatible commands.

The study-specific implementation scripts now live under `analyses/<analysis_id>/scripts/`. The files under these legacy paths are thin wrappers:

- `scripts/case_study/*` -> `analyses/hbta_topo_case_study/scripts/*`
- `scripts/lle/*` -> `analyses/electrolyte_lle_literature/scripts/*`
- `scripts/gando_2025_pcsaft_repro/*` -> `analyses/gando_2025_pcsaft_repro/scripts/*`
- `scripts/Yu_2024_analysis/*` -> `analyses/yu_2024_figure6/scripts/*`

New Codex agents should edit the `analyses/` implementation files, not the wrappers, unless they are intentionally changing the compatibility layer.
