# Yu 2024 Figure 6

This analysis owns the Yu 2024 Figure 6 digitized recreation, direct package diagnostic, and reactive-wrapper replication.

## ePC-SAFT Use

- Direct package replication uses `scripts.epcsaft_compat` and current ePC-SAFT parameter payloads.
- The digitized recreation is the stable visual reconstruction path.
- The reactive-wrapper script is the preferred source-backed reproduction when direct LLE collapses.

## Test Commands

```powershell
uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_digitized_recreation.py
uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_reactive_replication.py
```

The direct package script is diagnostic:

```powershell
uv run python analyses\yu_2024_figure6\scripts\yu_2024_figure6_replication.py
```
