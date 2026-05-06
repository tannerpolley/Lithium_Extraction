# Hubach 2024 Electrolyte LLE Phase-Equilibrium Handoff

Date: 2026-05-04

## Purpose

This note summarizes how the current ePC-SAFT phase-equilibrium solver fails on the Hubach 2024 lithium extraction case and recommends implementation work for the ePC-SAFT phase-equilibrium agent.

The immediate goal is not to tune the lithium extraction script around the failure. The goal is to improve the general electrolyte LLE workflow so cases like Hubach 2024 can converge through the public `ePCSAFTMixture.equilibrium(kind="electrolyte_lle")` API.

## Current Case

Lithium repo path:

`C:\Users\Tanner\Documents\git\Lithium_Extraction`

Sibling ePC-SAFT package path:

`C:\Users\Tanner\Documents\git\ePC-SAFT`

Primary runner:

`scripts/lle/hubach_2024_figure7_rwoa_replication.py`

Bounded single-point diagnostic runner:

`scripts/lle/_debug_hubach_single_point.py`

The Hubach case uses the following fixed species basis:

```text
H2O
TBP
[emim][tcb]
Li+
Cl-
```

This is a 1:1 salt case (`LiCl`) in a water / organic extractant / ionic-liquid mixture. It should be an easier target than the Yu 2024 Mg-containing system because it does not require divalent ions.

## Observed Failure

The updated ePC-SAFT package is now being reached correctly. The failure is not an import issue, schema issue, or unsupported-ion issue for Hubach.

The active route is:

```text
electrolyte_lle_v5_native_charge_constrained_solve
```

The bounded diagnostic runs show:

| Row | `R^w(O/A)` | Max iterations | Wall time | Result |
|---:|---:|---:|---:|---|
| 0 | 0.522 | 20 | 19.45 s | `SolutionError`, one phase |
| 0 | 0.522 | 80 | 143.02 s | `SolutionError`, one phase |
| 2 | 1.976 | 20 | 9.10 s | `SolutionError`, one phase |
| 4 | 3.933 | 20 | 18.76 s | `SolutionError`, one phase |

Representative diagnostics from `R^w(O/A)=0.522`, `max_nfev=80`:

```text
phase_equilibrium_model = electrolyte_lle_v5_native_charge_constrained_solve
equilibrium_route = electrolyte_lle
variable_model = ascani_transformed_salt_pairs
stability_min_tpd = -2.5068289650520548
solver_residual_norm = 7.489120434911456e-12
gibbs_delta = -2.4514612562143157e-11
phase_distance = 4.085620730620576e-14
acceptance_gate = predictive_solve_failed
best_failure_reason = candidate collapsed to one phase
n_phases = 1
status = SolutionError
```

## Interpretation

The solver is finding an unstable feed according to TPD, but the subsequent nonlinear solve collapses to the trivial one-phase solution.

This is the important distinction:

- The stability check indicates a split candidate should exist.
- The residual norm is very small, so the equations are numerically satisfied.
- The phase distance is near zero, so the accepted candidate is not a real two-phase split.
- Increasing iteration count slows the solve substantially but does not fix the collapse.

This is therefore not primarily an iteration-budget issue. It is a seed, continuation, formulation, or acceptance-workflow issue.

## Difference From Prior Lithium Repo Outputs

The older or "main-ish" lithium outputs should not be treated as equivalent to the new native ePC-SAFT solver result.

The Hubach report contains:

- Table S11 experimental values.
- Table S11 calculated values from the paper.
- Legacy package-output columns.

In the current retry, the paper/table values still exist, but the true package-computed values from the new `electrolyte_lle` route are `nan` because the native solver rejects the collapsed split.

The earlier "solved" behavior may have come from one of these:

- table-derived values rather than a fresh package phase-equilibrium solve;
- a looser custom `ln(phi*x)` flash routine;
- a fallback/contact model in a different lithium workflow;
- a solver path that reported a mathematically small residual without enforcing a distinct two-phase split.

The new native solver is stricter and is correct to reject an almost identical two-phase composition as a valid LLE result.

## Chemical Equilibrium Question

Chemical/speciation equilibrium should be separated from this Hubach failure.

For Yu 2024, chemical/speciation equilibrium is likely necessary because the paper mechanism involves Li coordination, Mg competition, TOP/IL complexation, and ion exchange. A fixed-species phase flash alone is unlikely to reproduce that system.

For Hubach 2024, do not make chemical equilibrium the first explanation. This is a 1:1 LiCl electrolyte LLE case, and the immediate failure is that the fixed-species phase-equilibrium solver cannot find a distinct aqueous/organic split even though TPD detects instability.

Hubach should first be made to converge as a fixed-species electrolyte LLE problem. Chemical equilibrium can be layered in later if needed.

## Recommended ePC-SAFT Implementation Work

### 1. Add Robust Electrolyte LLE Seed Generation

The current predictive route appears to collapse from a feed-like or formula-feed seed. Add multiple seed families before returning `SolutionError`:

- water-rich / organic-rich neutral solvent endpoint seeds;
- TPD trial composition plus lever-rule complement;
- several beta guesses, especially small organic fractions and large organic fractions;
- salt mostly aqueous / trace organic variants;
- salt partially organic variants;
- solvent-only LLE seed followed by electrolyte insertion;
- previous converged point as a continuation seed for O/A sweeps.

If `stability_min_tpd < 0`, do not stop after one collapsed nonlinear candidate.

### 2. Continue After Collapsed Candidates

A collapsed candidate should be treated as a failed attempt, not as the terminal result, when the stability analysis says the feed is unstable.

Suggested behavior:

```text
if stability_min_tpd < -threshold and candidate_collapsed:
    try next seed family
else:
    return stable/no_split or accepted split
```

The solver should only return `SolutionError` after exhausting distinct seed attempts.

### 3. Improve `initial_phases` Support And Examples

The public API already accepts:

```python
mixture.equilibrium(
    kind="electrolyte_lle",
    T=...,
    P=...,
    z=feed,
    initial_phases={
        "aq": aq_composition,
        "org": org_composition,
        "phase_fraction": beta_org,
    },
)
```

This should become a first-class workflow for hard electrolyte LLE cases.

Recommended additions:

- helper to construct charge-neutral aq/org guesses from formula-phase compositions;
- helper to construct charge-neutral aq/org guesses from solvent-rich endpoints;
- validation messages that explain charge-balance and material-balance failures;
- examples that show how to seed a paper-derived electrolyte LLE case.

For Hubach, the next concrete experiment should be to reconstruct approximate aq/org phase compositions from Table S11 or supporting data and pass them as `initial_phases`.

### 4. Preserve Best Noncollapsed Diagnostics

Current diagnostics mostly expose the final collapsed candidate. For debugging hard cases, diagnostics should preserve:

- best noncollapsed candidate composition;
- beta / phase fraction;
- phase distance;
- residual norm;
- material-balance error;
- charge-balance error;
- Gibbs delta;
- seed name;
- rejection reason.

This would make it much easier to tell whether the solver is nearly correct, physically impossible under the parameter set, or just poorly seeded.

### 5. Add Continuation Mode For Curves

Figure replication workflows should not cold-start every O/A point.

Recommended workflow:

1. solve one point with strong initial guesses;
2. use that accepted split as the initial seed for the nearest neighboring point;
3. march across the O/A curve in both directions;
4. fall back to global seed generation only when continuation fails.

This is likely essential for robust LLE curve generation.

### 6. Add Hubach-Style Regression Tests

The current ePC-SAFT tests cover Ascani-style water/butanol electrolyte LLE examples. Those are useful but not enough for ionic-liquid extraction systems.

Add a regression fixture for:

```text
H2O / TBP / [emim][tcb] / Li+ / Cl-
```

Minimum acceptance target:

- solver returns `split_detected=True`;
- two phases are distinct;
- aqueous phase is water-rich;
- organic phase is TBP / ionic-liquid rich;
- charge balance is preserved in both phases;
- material balance is preserved;
- diagnostics include the accepted seed path.

### 7. Keep Chemical Equilibrium As A Separate Layer

Do not mix the first Hubach convergence fix with a general reaction/speciation framework.

Recommended order:

1. Fixed-species electrolyte LLE convergence for Hubach.
2. Seed and continuation improvements.
3. General mixed-salt / mixed-ion extension.
4. Optional chemical/speciation equilibrium layer for Yu-like extraction chemistry.

## Recommended Next Task For The ePC-SAFT Agent

Implement a focused Hubach seed test in the ePC-SAFT repo:

1. Build the five-species Hubach mixture.
2. Use the current feed for `R^w(O/A)=0.522`.
3. Supply explicit charge-neutral aq/org initial phases.
4. Verify `electrolyte_lle` accepts a distinct two-phase split.
5. Generalize the seed construction into the default native electrolyte LLE workflow.
6. Add a regression test so this case does not regress.

## Local Evidence Files

Generated debug artifacts in the lithium repo:

```text
data/multiphase/hubach_single_point_option1_nfev20.json
data/multiphase/hubach_single_point_option1_nfev80.json
data/multiphase/hubach_single_point_row2_nfev20.json
data/multiphase/hubach_single_point_row4_nfev20.json
```

Useful code paths:

```text
scripts/epcsaft_compat.py
scripts/lle/hubach_2024_figure7_rwoa_replication.py
scripts/lle/_debug_hubach_single_point.py
```

Relevant ePC-SAFT API/test paths:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT\src\epcsaft\equilibrium.py
C:\Users\Tanner\Documents\git\ePC-SAFT\tests\equilibrium\test_electrolyte_lle.py
```
