# ePC-SAFT Feedback 2026-05-15

## Repo

- `C:\Users\Tanner\Documents\git\Lithium_Extraction`

## Package source

- resolved import path: `C:\Users\Tanner\Documents\git\Lithium_Extraction\.venv\Lib\site-packages\epcsaft\__init__.py`
- package version: `1.5.2`
- pinned source: `git+https://github.com/tannerpolley/ePC-SAFT.git@869e3354ddc0b52075ddc9efe687b34d6aa98316`
- upstream issue: `https://github.com/tannerpolley/ePC-SAFT/issues/127`

## Command

```powershell
uv sync --dev
uv run python scripts/check_epcsaft_integration.py --mode final
uv run python -c "import numpy as np, epcsaft; mix=epcsaft.ePCSAFTMixture.from_dataset('2022_Ascani', ['H2O','Butanol','Na+','Cl-'], np.asarray([0.55,0.40,0.025,0.025]), 298.15)"
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_des_epcsaft_parameter_smoke.py
```

## Minimal Reproduction

```python
import numpy as np
import epcsaft

print(epcsaft.available_datasets())
epcsaft.ePCSAFTMixture.from_dataset(
    "2022_Ascani",
    ["H2O", "Butanol", "Na+", "Cl-"],
    np.asarray([0.55, 0.40, 0.025, 0.025]),
    298.15,
)
```

## Observed Behavior

- The final downstream integration contract passes in `final` mode against the pinned Git install.
- `epcsaft.available_datasets()` is empty from the installed pinned Git package in the downstream environment.
- `ePCSAFTMixture.from_dataset("2022_Ascani", ...)` raises `FileNotFoundError: Unknown dataset '2022_Ascani'. Available datasets: []`.
- The Rezaee DES/LiCl direct electrolyte-LLE smoke now reaches the native Ceres route and returns structured diagnostics, but it is still not accepted for final results: `status=not_accepted`, `split_detected=false`, `acceptance_gate=predictive_budget_exhausted`, `best_effort_phases_returned=true`, and residual norm about `0.558`.

## Expected Behavior

- Public datasets used in docs/tests, especially `2022_Ascani`, should either be installed with the package or the downstream/install-mode docs should state that `from_dataset(...)` is source-tree only.
- Downstream examples should have a minimal installed-package electrolyte-LLE smoke that does not depend on uninstalled repo fixture data.

## Why This Belongs Upstream

This is a package-data and public-example contract gap. Downstream repos can pin and import the package cleanly, but cannot run the documented/public dataset route from the installed package.

The Rezaee result itself is not promoted as a package bug in this note; it remains a downstream/source-basis hard case until an accepted physical split and a source-supported published-constant reactive closure both pass.

## Downstream Validation Command

```powershell
uv run python scripts/check_epcsaft_integration.py --mode final
uv run python analyses\rezaee_2026_pcsaft_epcsaft\scripts\rezaee_des_epcsaft_parameter_smoke.py
```

## Acceptance Criteria

- `epcsaft.available_datasets()` from a pinned Git install includes datasets that public docs/tests expect downstream users to load, or docs identify the source-tree-only boundary.
- A minimal installed-package electrolyte-LLE example can be executed from `Lithium_Extraction` without relying on `C:\Users\Tanner\Documents\git\ePC-SAFT` as a live checkout.
