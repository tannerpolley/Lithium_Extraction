# ePC-SAFT LLE Timeout Diagnostics

Date: 2026-05-07

## Later Verification Update

After upstream budget controls were available in the local ePC-SAFT install, the timeout-enabled Hubach single-point diagnostic returned structured package diagnostics instead of hanging:

```powershell
uv run python analyses\electrolyte_lle_literature\scripts\_debug_hubach_single_point.py --timeout-seconds 8 --out-json analyses\electrolyte_lle_literature\results\debug\hubach_single_point_debug_8s_20260507.json
```

Both option rows returned `status=SolutionError`, `acceptance_gate=predictive_budget_exhausted`, and `budget_trigger=timeout_seconds` in about five seconds per option. This closes the immediate "no bounded failure contract" symptom for the timeout-enabled wrapper path. It does not close the scientific hard case: Hubach still does not converge to an accepted fixed-species electrolyte LLE split under the tested options.

Treat the older timeout evidence below as the pre-budget-control baseline and the JSON file above as the current reproduction artifact.

## Scope

This note records why the Lithium_Extraction LLE scripts can time out before they return useful phase-equilibrium diagnostics, and what the upstream ePC-SAFT package should add to make these workflows robust enough for PrOMMiS/IDAES handoff work.

## Downstream evidence

### Hubach 2024 electrolyte LLE

Command inspected:

```powershell
uv run python scripts\lle\_debug_hubach_single_point.py --timeout-seconds 20 --out-json data\multiphase\hubach_2024_single_point_debug_short_2026_05_07.json
```

Result:

- The command exceeded a 70 s outer runner limit before writing the requested JSON.
- The spawned process chain was still alive after the runner timeout and had to be stopped.
- This is not just an outer script loop problem: `scripts\lle\_debug_hubach_single_point.py` already wraps each option in a subprocess and calls `terminate()`/`kill()` after its option timeout.

Relevant downstream call path:

- `scripts\lle\hubach_2024_figure7_rwoa_replication.py::_solve_point`
- `scripts\epcsaft_compat.py::pcsaft_multiphase_lle`
- `ePCSAFTMixture.equilibrium(kind="electrolyte_lle")`

The Hubach script tries every Table S11 row. For each row, the stable profile sends two option sets. In the current compatibility layer, `max_nfev` maps to `EquilibriumOptions.max_iterations`, but `tpdf_global_trials`, `tpdf_local_trials`, and `charge_weight` are ignored legacy keys. The effective iteration budgets are therefore 300 and 1000 per attempted point, but the old trial-count knobs no longer constrain the native search.

### Jang 2017 Li/Na TBP/D2EHPA placeholder

Command inspected:

```powershell
uv run python scripts\lle\jang_2017_stage2_li_na_tbp_d2ehpa.py --mode single
```

Result:

- A 45 s supervised single-contact probe timed out with no stdout or stderr.
- The fallback in `scripts\lle\jang_2017_stage2_li_na_tbp_d2ehpa.py::_contact_fallback` is only reached after the ePC-SAFT call returns a non-two-phase result. If the package call does not return promptly, the script cannot fall back.

Relevant downstream call path:

- `scripts\lle\jang_2017_stage2_li_na_tbp_d2ehpa.py::_solve_lle_with_retries`
- `scripts\epcsaft_compat.py::pcsaft_multiphase_lle`
- `ePCSAFTMixture.equilibrium(kind="electrolyte_lle")`

The Jang script uses a seven-component ionic placeholder system:

- `H2O-2B-Li`
- `Hexane`
- `TBP-SURR`
- `D2EHPA-SURR`
- `Li+`
- `Na+`
- `Cl-`

It sends retry options with effective iteration budgets of 90 and 320. The script contains a defensible engineering fallback for placeholder-stage transfer, but that fallback is downstream-only and cannot protect against a long-running native solve.

## Upstream ePC-SAFT code surfaces

Observed package surfaces:

- `src\epcsaft\equilibrium.py::EquilibriumOptions`
- `src\epcsaft\equilibrium.py::_normalize_options`
- `src\epcsaft\equilibrium.py::_call_native_equilibrium`
- `src\epcsaft\equilibrium.py::electrolyte_lle_flash_native`
- `src\epcsaft\native\epcsaft_equilibrium.cpp::electrolyte_lle_failure_result`
- `src\epcsaft\native\epcsaft_equilibrium.cpp::predictive_electrolyte_accepted`
- `src\epcsaft\native\epcsaft_density.cpp::den_cpp`

Current useful diagnostics already exist:

- `phase_equilibrium_model = electrolyte_lle_v5_native_charge_constrained_solve`
- `acceptance_gate = predictive_solve_failed`
- `best_failure_reason = candidate collapsed to one phase`
- `stability_min_tpd`
- `seed_attempts`
- density-root rejection reasons such as `No valid density root found for liquid phase`

Main gap:

The package can explain failures after returning, but the public electrolyte LLE API does not yet provide a reliable wall-clock or total-work budget that guarantees a structured `SolutionError`/diagnostic payload for hard mixtures. Downstream scripts therefore have to wrap calls in subprocesses, and even then the full process chain can outlive the intended diagnostic window.

## Root-cause assessment

1. The downstream scripts pass legacy controls that no longer constrain much of the native work. `max_nfev` still maps to `max_iterations`, but old trial-count options are intentionally ignored.
2. The electrolyte LLE native path can spend substantial time in repeated stability, seed, transformed Newton/Nelder-Mead, and density-root work before returning failure diagnostics.
3. Collapsed-candidate cases are already detectable after failure, but the public route does not have an early-exit policy like "unstable feed plus repeated collapsed candidates means stop and return diagnostics."
4. Density-root failures are structured in the native density code, but they are not yet aggregated into a public, bounded "best diagnostic result" quickly enough for high-component placeholder systems.
5. Downstream fallbacks are script-local. They are useful for presentation-stage surrogate work, but they are not a substitute for package-side bounded failure contracts.

## Recommended upstream improvements

1. Add public work budgets to `EquilibriumOptions`: `timeout_seconds`, `max_seed_attempts`, `max_density_failures`, and `max_total_objective_evaluations`.
2. Thread those budgets through `_options_to_native_dict`, `bindings.cpp`, and `EquilibriumOptionsNative`.
3. Check the wall-clock/work budget inside native stability, seed-generation, Nelder-Mead, Newton, and density-root loops.
4. Return a structured `SolutionError` when the budget is exceeded, with `timeout_trigger`, elapsed wall time, seed attempts, best candidate, density diagnostics, and the same `phase_equilibrium_model`.
5. Add an early-exit gate for `unstable_feed_collapsed_all_candidates`: if stability is strongly negative and N consecutive candidate families collapse to one phase, stop and return the best diagnostic payload instead of exhausting every seed path.
6. Expose a `diagnostic_only=True` or `return_best_effort=True` mode for screening workflows, separate from strict predictive acceptance.
7. Preserve current strict behavior by default for accepted results; the new controls should make failure bounded, not make bad splits look valid.
8. Add regression tests using the Hubach fixed-species row-0 case and the Jang seven-component placeholder input. Acceptance should be either a valid two-phase result or a structured failure within a bounded runtime.

## 2026-05-07 retry with current package features

Retry artifact:

- `scripts/case_study/epcsaft_equilibrium_retry_matrix_2026_05_07.py`
- `data/reference/produced_water/epcsaft_equilibrium_retry_matrix_2026_05_07.json`
- `data/reference/produced_water/epcsaft_equilibrium_retry_matrix_2026_05_07.md`

Current package surface observed from Lithium_Extraction:

- `epcsaft` version: `1.5.0`
- source root: `C:\Users\Tanner\Documents\git\ePC-SAFT`
- source commit: `a56d9c81af1b`
- native extension: available
- `cyipopt`: unavailable, so `solver_backend="ipopt"` fails by design
- relevant `EquilibriumOptions` fields: `max_iterations`, `tolerance`, `damping`, `min_composition`, `include_phase_diagnostics`, `stability_precheck`, `legacy_candidate_mode`, `density_diagnostics`, `experimental_coupled_density_lle`, `jacobian_backend`, `solver_backend`, `hessian_strategy`
- exposed helper/API surface includes `capabilities()`, `runtime_build_info()`, `initial_phases_from_result()`, `evaluate_fugacity_coefficients_batch()`, and `solve_reactive_staged_equilibrium()`

Important migration detail:

- Direct ePC-SAFT API calls reject legacy polar keys such as `dipm`.
- The Lithium compatibility bridge already strips these through `scripts.epcsaft_compat._normalized_params()`.
- Direct downstream code needs either the same normalization or a package-supported public migration helper for older parameter dictionaries.

### Retry matrix outcomes

The retry matrix used normalized parameter dictionaries and valid nonzero initial phase seeds. It tested:

- native electrolyte stability
- unseeded electrolyte LLE
- seeded electrolyte LLE
- seeded LLE with `density_diagnostics="full"`
- seeded LLE with `solver_backend="newton"` and `jacobian_backend="autodiff"`
- seeded LLE with `solver_backend="newton"`, `jacobian_backend="finite_difference"`, and `hessian_strategy="lbfgs"`
- seeded LLE with `experimental_coupled_density_lle=True`
- explicit `solver_backend="ipopt"`

Results:

| Case | Result |
|---|---|
| Hubach row-0 stability | returned quickly; `stable=False`, `min_tpd=-2.5058140448113444` |
| Hubach unseeded and seeded native LLE variants | all exceeded the 25 s subprocess budget |
| Hubach explicit IPOPT variant | fast `InputError` because `cyipopt` is not installed |
| Jang single-contact stability | returned quickly; `stable=False`, `min_tpd=-17.358566077818846` |
| Jang unseeded and seeded native LLE variants | all exceeded the 25 s subprocess budget |
| Jang explicit IPOPT variant | fast `InputError` because `cyipopt` is not installed |

Interpretation:

- Stability says both mixtures are unstable, so a split search is thermodynamically justified.
- The new public controls do not recover a bounded electrolyte-LLE result for these downstream hard cases.
- The package now reports IPOPT unavailability cleanly, but IPOPT was not testable in this environment.
- The most important remaining package gap is not a missing stability method; it is that native electrolyte LLE still has no public wall-clock/total-work failure contract.

### Existing workflow retest

Commands that passed:

```powershell
uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py
uv run python scripts\case_study\rezaee_des_epcsaft_parameter_smoke.py
uv run python scripts\lle\gando_2025_three_stage_crossflow.py
uv run python scripts\case_study\solvent_candidate_scorecard.py
```

Observed:

- HBTA/TOPO reactive-stage solve completed and regenerated fit/stage/costing outputs.
- Rezaee smoke completed; density fit succeeded and electrolyte stability returned `min_tpd=-0.5681261249986091`, but direct electrolyte LLE still reported `lle_status='error'`.
- Gando three-stage crossflow completed and regenerated CSV, markdown, and PNG outputs.
- Solvent candidate scorecard completed.

Upstream package tests:

```powershell
uv run python run_pytest.py --equilibrium-confidence
uv run pytest tests\equilibrium\test_electrolyte_lle.py -q
uv run pytest tests\equilibrium\test_hubach_electrolyte_lle.py -q
```

Observed:

- `--equilibrium-confidence`: 2 passed.
- `test_electrolyte_lle.py`: 21 passed, 1 skipped for optional IPOPT.
- `test_hubach_electrolyte_lle.py`: 3 passed, 4 skipped because the native Hubach hard-case regressions are opt-in.

Downstream hard-script retest:

```powershell
uv run python scripts\lle\_debug_hubach_single_point.py --timeout-seconds 30 --out-json data\multiphase\hubach_2024_single_point_debug_retry_2026_05_07.json
uv run python scripts\lle\jang_2017_stage2_li_na_tbp_d2ehpa.py --mode single
```

Observed:

- Hubach option 1 (`max_nfev=300`) timed out at 30 s.
- Hubach option 2 (`max_nfev=1000`) timed out at 30 s.
- Jang single-contact exceeded a 180 s outer runner timeout and left a child process that had to be stopped.

### Updated issue list

1. **No public runtime budget for electrolyte LLE.** Downstream can kill a subprocess, but the package does not return a structured budget-exhausted `SolutionError`.
2. **Seeded hard cases still hang.** Valid, nonzero `initial_phases` did not make Hubach/Jang return under 25 s.
3. **Autodiff/finite-difference/Hessian controls do not solve these cases.** The tested `jacobian_backend` and `hessian_strategy` options did not change the timeout outcome.
4. **Coupled-density mode does not solve these cases.** `experimental_coupled_density_lle=True` still exceeded the budget.
5. **IPOPT path is unavailable in this environment.** This is correctly reported by the package, but means the new IPOPT route could not be used as a practical fallback here.
6. **Legacy parameter migration is still a downstream concern.** Current Lithium scripts must strip removed polar keys before direct package calls; a public package helper would make this safer.
7. **Opt-in hard-case tests allow package CI to pass while downstream hard cases remain unsolved.** The package’s own electrolyte confidence tests pass, but the real Hubach/Jang downstream cases are skipped or not represented as bounded-failure contracts.

## Proposed GitHub issue body

Title:

```text
Bound electrolyte LLE runtime and return structured diagnostics for collapsed-candidate/density-root failures
```

Body:

```markdown
Downstream Lithium_Extraction workflows are timing out before ePC-SAFT returns diagnostics for hard electrolyte LLE cases.

Observed downstream probes:

- `uv run python scripts\lle\_debug_hubach_single_point.py --timeout-seconds 20 --out-json data\multiphase\hubach_2024_single_point_debug_short_2026_05_07.json`
  - Outer 70 s runner timed out before JSON was written.
  - This script already supervises each option in a subprocess.
- `uv run python scripts\lle\jang_2017_stage2_li_na_tbp_d2ehpa.py --mode single`
  - A 45 s supervised single-contact probe timed out with no stdout/stderr.

Relevant package route:

- `ePCSAFTMixture.equilibrium(kind="electrolyte_lle")`
- `electrolyte_lle_v5_native_charge_constrained_solve`
- native density root calls from `epcsaft_density.cpp`

Useful diagnostics already exist after return:

- `acceptance_gate = predictive_solve_failed`
- `best_failure_reason = candidate collapsed to one phase`
- `stability_min_tpd`
- `seed_attempts`
- density-root rejection messages such as `No valid density root found for liquid phase`

Requested package-side improvement:

Add a bounded failure contract for public electrolyte LLE:

1. Add `timeout_seconds`, `max_seed_attempts`, `max_density_failures`, and `max_total_objective_evaluations` to `EquilibriumOptions`.
2. Pass those controls through Python, pybind, and native C++ options.
3. Check the budget inside stability, seed generation, Nelder-Mead, Newton, and density-root loops.
4. Raise/return a structured `SolutionError` on budget exhaustion, preserving seed attempts, best candidate, density diagnostics, elapsed wall time, and model route.
5. Add an early-exit policy for repeated `candidate collapsed to one phase` cases when stability indicates the feed is thermodynamically unstable but every candidate family collapses.
6. Keep strict predictive acceptance unchanged; this request is for bounded diagnostics and fail-fast behavior, not weaker acceptance.

Downstream validation need:

After the package change, Lithium_Extraction should be able to rerun:

- `uv run python scripts\lle\_debug_hubach_single_point.py --timeout-seconds 20`
- `uv run python scripts\lle\jang_2017_stage2_li_na_tbp_d2ehpa.py --mode single`
- the HBTA/TOPO case-study solve and PrOMMiS/IDAES handoff checks

Expected behavior:

Each hard case should return a valid two-phase result or a structured diagnostic failure within the configured budget.
```
