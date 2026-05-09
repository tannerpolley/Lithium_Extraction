# Electrolyte LLE Literature Benchmarks

This analysis owns Hubach 2024, Jang 2017, and Gando selective extraction LLE benchmark scripts plus generated slide assets.

## ePC-SAFT Use

- Hubach and Jang call the current ePC-SAFT electrolyte LLE path through `scripts.epcsaft_compat`.
- Hubach/Jang are hard-case diagnostics. Use the timeout-enabled diagnostic commands so package failures return structured `SolutionError` payloads instead of open-ended subprocess runs.
- Hubach single-point diagnostics currently return bounded `predictive_budget_exhausted` results; this is useful package evidence, not a converged fixed-species LLE claim.
- Gando scripts use the project selective-stage helper and generated parameter payloads to produce case-study evidence tables and plots.

## Test Commands

```powershell
uv run python analyses\electrolyte_lle_literature\scripts\gando_2025_three_stage_crossflow.py
uv run python analyses\electrolyte_lle_literature\scripts\gando_2025_one_stage_assets.py
uv run python analyses\electrolyte_lle_literature\scripts\gando_2025_slide_assets.py
uv run python analyses\electrolyte_lle_literature\scripts\_debug_hubach_single_point.py --timeout-seconds 30
```

Avoid using Hubach/Jang full reproduction scripts as routine tests until the hard-case convergence work is resolved. The bounded diagnostic scripts are acceptable when specifically testing package electrolyte-LLE behavior.
