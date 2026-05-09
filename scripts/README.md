# Root Scripts

Root `scripts/` is reserved for repository-level helpers shared by multiple
analyses.

Study workflows belong under `analyses/<analysis_id>/scripts/`. Do not add
paper-specific, figure-specific, or case-study execution scripts here.

## Current Root Helpers

- `epcsaft_compat.py` - compatibility bridge for the local ePC-SAFT package
  surface used by several analysis workflows.
