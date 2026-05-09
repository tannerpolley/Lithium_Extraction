# Gando 2025 PC-SAFT Reproduction

This analysis owns the Gando 2025 PC-SAFT reproduction runner and reusable selective-stage model helper.

## ePC-SAFT Use

- Required for package-backed reproduction diagnostics.
- Provides the selective-stage helper imported by the electrolyte-LLE benchmark scripts.

## Test Commands

```powershell
uv run python analyses\gando_2025_pcsaft_repro\scripts\reproduce_gando_2025_pcsaft.py
```

The equivalent legacy `scripts\gando_2025_pcsaft_repro\reproduce_gando_2025_pcsaft.py` command is a wrapper.
