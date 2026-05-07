# uv Workflow

Last updated: 2026-05-06

This repository uses `uv` as the default Python environment and package manager.

## Setup

From the repository root:

```powershell
uv sync --dev
```

The project pins Python through `.python-version` and records resolved packages in `uv.lock`.

## ePC-SAFT Dependency

The local ePC-SAFT package is installed from:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT
```

The dependency is declared as a direct file dependency in `pyproject.toml`:

```toml
"epcsaft @ file:///C:/Users/Tanner/Documents/git/ePC-SAFT"
```

Use this direct file dependency rather than `tool.uv.sources` with `editable = true`. The current ePC-SAFT build backend does not implement editable builds, and the sibling repo's `tool.uv.package = false` setting causes `tool.uv.sources` to be treated as a virtual package source instead of an installed module.

## Validation

Use these checks after setup:

```powershell
uv run python -c "import epcsaft; from epcsaft import ePCSAFTMixture; print(epcsaft.__file__)"
uv run python -m compileall -q scripts data
```

The Quarto deck is still rendered with the installed Quarto binary:

```powershell
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
```

## Common Commands

Run Python scripts through `uv run`:

```powershell
uv run python scripts\lle\gando_2025_three_stage_crossflow.py
uv run python scripts\lle\gando_2025_one_stage_assets.py
uv run python scripts\lle\gando_2025_slide_assets.py
```

If the local ePC-SAFT checkout changes native code, rerun:

```powershell
uv sync --dev --reinstall-package epcsaft
```

