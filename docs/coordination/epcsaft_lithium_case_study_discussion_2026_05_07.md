> Superseded context, 2026-05-08: this coordination record predates the Rezaee Phase 0-9 pivot. The active Lithium_Extraction case-study basis is now Rezaee DES/TOPO Li/Na extraction after divalent pretreatment; HBTA/TOPO remains comparison and future parameterization context only.

Context: downstream coordination handoff from `Lithium_Extraction` for the produced-water lithium extraction case study.

Original coordination contract at posting time:
- Upstream package: `tannerpolley/ePC-SAFT` (`C:\Users\Tanner\Documents\git\ePC-SAFT`)
- Upstream fixer thread: `019de54a-261e-74c1-ac1f-1a703e94a020`
- Downstream consumer: `tannerpolley/Lithium_Extraction` (`C:\Users\Tanner\Documents\git\Lithium_Extraction`)
- Downstream tester thread: current local Codex thread in `Lithium_Extraction`
- Shared discussion: this discussion
- Baseline: discussion creation on 2026-05-07
- Current owner: upstream
- Next actor: upstream
- Completion condition: downstream can replace the calibrated HBTA/TOPO reactive-stage bridge with a predictive staged reactive-ePC-SAFT workflow, or upstream clearly documents the package-side limits and the minimum supported staged workflow for this chemistry.

Current status after upstream PR #33 and downstream validation:

- Current owner: none
- Next actor: none
- Downstream validation reply: https://github.com/tannerpolley/ePC-SAFT/discussions/32#discussioncomment-16837532
- Active coordination watchers for this relay were removed after validation.

## Why this handoff exists

The downstream case-study work is no longer blocked on "does ePC-SAFT have any reactive chemistry support at all?" The current package already has real reactive APIs. The actual blocker is narrower and more useful:

1. the flagship HBTA/TOPO/sulfonated-kerosene solvent-extraction chemistry still lacks the needed parameter and reaction payload;
2. the public regression surface is still not enough to close that chemistry directly from extraction/LLE data;
3. the downstream repo needs a documented package-supported path for staged reactive extraction so the PrOMMiS/IDAES bridge can stop pretending the chemistry is a black-box extraction factor.

## Downstream environment and commands

Downstream repo:

```text
C:\Users\Tanner\Documents\git\Lithium_Extraction
```

Key downstream commands:

```text
uv sync --reinstall-package epcsaft
uv run python -m compileall -q scripts data
uv run python legacy HBTA/TOPO stage command removed during cleanup
uv run python analyses\\rezaee_2026_pcsaft_epcsaft\\scripts\\rezaee_des_epcsaft_parameter_smoke.py
uv run python legacy solvent scorecard command removed during cleanup
```

## Current downstream result

### 1. The live installed package already exposes real reactive APIs

After `uv sync --reinstall-package epcsaft`, the downstream environment reports:

- package version: `1.5.0`
- source commit before upstream PR #33: `244ff404008c`
- source commit after upstream PR #33 downstream reinstall: `1ae609c70636`
- path dependency source root: `C:\Users\Tanner\Documents\git\ePC-SAFT`

Confirmed package capabilities in the downstream env:

- `solve_reactive_speciation(...)`
- `solve_reactive_staged_equilibrium(...)`
- `solve_reactive_electrolyte_bubble(...)`
- `solve_reactive_electrolyte_bubble_sweep(...)`
- `mixture.equilibrium(kind="chemical_equilibrium", ...)`
- `mixture.equilibrium(kind="reactive_staged_equilibrium", ...)`
- `mixture.equilibrium(kind="reactive_stability", ...)`
- `mixture.equilibrium(kind="reactive_electrolyte_bubble_pressure", ...)`

Interpretation:

- The package can already solve homogeneous reactive speciation.
- The package can already do staged chemical-equilibrium-then-phase-equilibrium workflows.
- The package can already do staged reactive electrolyte bubble workflows.

### 2. The current package boundary is staged, not fully coupled reactive LLE flash

The current source explicitly rejects:

```text
reactive_flash_tp is not exposed; use an explicit staged phase_kind.
```

Interpretation:

- downstream should not ask for a nonexistent fully coupled reactive flash today;
- but downstream does need a documented package-supported staged route for extraction chemistry, and possibly a roadmap opinion on whether fully coupled reactive LLE belongs in scope later.

### 3. The current public regression surface is still the main blocker for this case

Publicly confirmed now:

- `fit_pure_neutral(...)`: public and native-backed, but current public V1 scope is nonassociating neutral fitting;
- `fit_pure_ion(...)`: public and native-backed;
- `fit_binary_pair(...)`: public and native-backed, but current V1 scope is binary VLE-style fitting and not the LLE/extraction-fitting route needed here.

Interpretation:

This is the concrete downstream gap. The package has reactive chemistry APIs, but the flagship solvent-extraction case still lacks a public supported route for:

1. associating-neutral solvent fitting suitable for HBTA/TOPO-class molecules;
2. binary-interaction fitting from extraction/LLE data rather than only VLE-style data;
3. a defensible workflow for fitting reaction constants plus complex/pseudo-species behavior for staged extraction.

## Flagship downstream chemistry and why it matters

The active downstream benchmark is:

```text
HBTA + TOPO + sulfonated kerosene
```

with the case-study assumption that divalent ions are handled upstream by pretreatment, so the thermodynamic focus is the harder:

```text
Li / Na / Cl / water + organic ligand/synergist
```

separation slice.

This is the exact story downstream needs to support:

1. ePC-SAFT computes the high-TDS aqueous activity landscape;
2. Li transfer is enhanced because Li is consumed by complexation in the organic-side chemistry;
3. the process model needs transfer variables generated from that thermodynamic + reaction picture, not fixed extraction factors.

This is conceptually similar to staged reactive absorption logic:

- transfer driven by activity/chemical-potential differences;
- reaction consumes the transferred species and sustains further transfer;
- staged process model consumes the resulting effective transfer behavior.

## Current downstream artifacts

Relevant downstream files:

```text
scripts/case_study/hbta_topo_reactive_stage_solve.py
scripts/case_study/rezaee_des_epcsaft_parameter_smoke.py
scripts/case_study/solvent_candidate_scorecard.py
docs/plans/zotero_mcp_refresh_case_study_handoff_2026_05_07.md
data/reference/produced_water/hbta_topo_reactive_model_report.md
data/reference/produced_water/rezaee_2026_epcsaft_parameter_smoke_report.md
data/reference/produced_water/solvent_candidate_literature_review_2026_05_07.md
```

Current downstream model boundary:

- the HBTA/TOPO case is a calibrated reactive-stage bridge, not final predictive reactive ePC-SAFT LLE;
- Rezaee 2026 is a parameter-regression and package-plumbing pilot, not the flagship chemistry;
- Smackover is the source-composition anchor; Shan/Gando HBTA/TOPO is the extraction-chemistry anchor.

## Concrete package-side needs

Requested upstream help is not "please add generic reactivity somehow." It is more specific:

1. Confirm the recommended package-supported staged workflow for solvent-extraction chemistry like:
   - aqueous electrolyte feed;
   - explicit Li complexation reaction(s);
   - chemically equilibrated staged feed;
   - then phase-equilibrium or stability route.

2. Clarify whether the intended downstream route should use:
   - `solve_reactive_speciation(...)` directly;
   - `solve_reactive_staged_equilibrium(...)`;
   - `mixture.equilibrium(kind="reactive_staged_equilibrium", ...)`;
   - or a newer pattern the downstream repo should adopt.

3. Close or roadmap the regression gap for this class of chemistry:
   - public associating-neutral regression for HBTA/TOPO-class solvents;
   - extraction/LLE-relevant binary interaction fitting;
   - support or guidance for complex/pseudo-species fitting and reaction-constant fitting.

4. Clarify whether a staged reactive extraction path is the intended final package story for now, or whether a coupled reactive LLE flash is on the roadmap.

## Upstream fix and downstream validation

Running the upstream test slice:

```text
uv run python run_pytest.py tests\api\test_reactive_speciation.py tests\api\test_reactive_staged_equilibrium.py -q
```

gave:

- most tests passing;
- one failure in `test_solve_reactive_speciation_concentration_standard_state_uses_molar_density`.

Observed mismatch:

```text
expected diagnostics["activity_basis"] == "concentration"
observed diagnostics["activity_basis"] == "mole_fraction"
```

Original interpretation:

- this does not invalidate the existence of the reactive solver;
- it looks like either a diagnostics-label inconsistency or a real concentration-standard-state bookkeeping issue;
- downstream would like upstream judgment on whether this is a simple reporting bug or a chemistry-basis bug.

Upstream result:

- PR #33 merged into `tannerpolley/ePC-SAFT`.
- Main commit `1ae609c` fixed the concentration-standard-state diagnostics label path.
- The upstream note was posted at https://github.com/tannerpolley/ePC-SAFT/discussions/32#discussioncomment-16837422.

Downstream validation result:

```text
uv sync --reinstall-package epcsaft: succeeded
installed epcsaft commit: 1ae609c70636
rezaee_des_epcsaft_parameter_smoke.py: succeeded
hbta_topo_reactive_stage_solve.py: succeeded
```

The downstream validation reply was posted at https://github.com/tannerpolley/ePC-SAFT/discussions/32#discussioncomment-16837532.

## Requested next step

No immediate upstream action is needed for discussion #32 unless a new package-side failure or missing package API appears during the next modeling pass.

## Completion condition

This coordination relay is complete. The remaining HBTA/TOPO lithium case-study work is downstream scientific/modeling work: true solvent/complex parameters, extraction-oriented regression data, reaction constants, and full PrOMMiS/IDAES staged solve/costing depth.

Next actor: none

