# Zotero MCP Refresh And Case-Study Continuation Handoff

Date: 2026-05-07  
Repo: `C:\Users\Tanner\Documents\git\Lithium_Extraction`  
Primary upstream package repo: `C:\Users\Tanner\Documents\git\ePC-SAFT`  
Downstream integration repos mentioned in the project: `pcsaft-pse`, `prommis`, `idaes-pse`

## Purpose Of This Handoff

This document is for a fresh Codex thread after the Zotero plugin/MCP is refreshed or repaired.

The user explicitly asked the current thread to stop active execution and produce an extremely comprehensive handoff so the new thread can resume the produced-water lithium extraction case-study work without losing:

1. The full scientific goal.
2. The Zotero MCP failure state.
3. The HTTP/local-cache fallback path that is currently working.
4. The solvent-candidate literature inventory.
5. The current branch artifacts and scripts.
6. The explicit instructions to keep retrying Zotero MCP while work continues.
7. The exact remaining steps to reach a defensible Phase 9 case-study package.

## User Intent, Preserved

The user wants a presentation-ready, evidence-backed produced-water lithium extraction case study that sells why ePC-SAFT must be implemented into the PrOMMiS and IDAES ecosystem.

The case study should show:

1. A real produced-water source with real or near-real composition.
2. Lithium concentration, TDS, major ions, and any critical minerals or REE that are actually reported.
3. A realistic solvent extraction process where Li transfers from aqueous brine into an organic phase.
4. Why the thermodynamics are nontrivial.
5. Why ePC-SAFT is uniquely valuable for equilibrium, phase split, chemical speciation, distribution ratios, selectivity, and transfer variables.
6. How a surrogate or bridge can pass ePC-SAFT-derived variables into PrOMMiS/IDAES staged solvent extraction unit models.
7. How PrOMMiS/IDAES then owns staged contacting, flowsheet analysis, optimization, and costing.
8. What remains as true science rather than hidden surrogate assumptions.

The user specifically does not want a shallow answer. Continue until the goal is handled as far as possible unless a true blocker appears.

## Hard Boundaries

1. Exclude ionic liquids from the active benchmark.
   - They may be used only as ePC-SAFT method references.
   - Do not select an ionic-liquid extraction system as the flagship case.
   - Reason: user says ionic liquids are too costly and too unknown.

2. The active case should be conventional non-ionic solvent extraction.
   - Current best flagship: HBTA + TOPO + sulfonated kerosene from Shan/Gando 2025.
   - Other candidates can be ranked as backup or comparison cases.

3. Do not claim true predictive reactive HBTA/TOPO ePC-SAFT is complete.
   - Missing: HBTA parameters, TOPO parameters if not defensibly available, sulfonated kerosene or diluent parameters, Li-ligand complex parameters, competing divalent-complex parameters, binary interactions, and reaction-equilibrium constants.
   - Current HBTA/TOPO model is a calibrated reactive-stage bridge, not a final predictive ePC-SAFT LLE model.

4. Do not claim Shan/Gando field water is Smackover.
   - Current source-composition case is southern Arkansas Smackover.
   - Current extraction-chemistry case is Shan/Gando HBTA/TOPO field-water extraction.
   - The correct presentation wording is: source feed is Smackover-specific; extraction chemistry is Shan/Gando HBTA/TOPO; current model is a calibrated reactive-stage bridge.

5. If REE are not reported for the chosen source, record `not_reported`.
   - Do not infer REE from unrelated reviews or nearby basins.

6. Be realistic where it matters and label shortcuts.
   - It is acceptable to use calibrated bridge/skeleton artifacts if they are clearly labeled.
   - It is not acceptable to present a surrogate as a solved thermodynamic model.

## Zotero Plugin/MCP State

The Zotero plugin/MCP was explicitly requested by the user. The current thread tried it multiple times after the user said another agent was fixing the plugin.

Skill used:

`C:\Users\Tanner\.codex\plugins\cache\zotero\zotero-local-research\0.1.1\skills\zotero-research\SKILL.md`

MCP tools were lazy-loaded through `tool_search` successfully, but direct tool calls failed with:

```text
tool call failed for `zotero-local/<tool>`
Caused by:
    Transport closed
```

Failed MCP calls in this thread:

```text
mcp__zotero_local__.zotero_find_collections({"query":"Organic Solvents","exact":true,"limit":10})
mcp__zotero_local__.zotero_list_collections({"limit":5,"top_only":true})
mcp__zotero_local__.zotero_get_collection_items_by_name({"collection_name":"Organic Solvents","limit":5,"recursive":true,"sort":"title","direction":"asc"})
```

Important instruction for the new thread:

1. Keep retrying Zotero MCP early and periodically.
2. If the MCP starts working, prefer it for collection/item/fulltext reads.
3. If MCP still fails with `Transport closed`, continue with the local Zotero HTTP API and Zotero storage cache.
4. Do not stop the case-study work just because MCP is down.

## Working Zotero Fallback

The local Zotero HTTP API is working:

```text
http://localhost:23119/api/users/0
```

Example command:

```powershell
curl.exe -s "http://localhost:23119/api/users/0/collections/LYN9RATQ/items?format=json&limit=100&sort=title"
```

Use `curl.exe`, not PowerShell `Invoke-WebRequest`, if PowerShell web cmdlets behave oddly.

The Zotero storage full-text caches are also available under:

```text
C:\Users\Tanner\Zotero\storage\<attachment_key>\.zotero-ft-cache
```

## Relevant Zotero Collections

Confirmed collection keys:

| Collection | Key | Role |
|---|---|---|
| Organic Solvents | `LYN9RATQ` | Main non-ionic solvent extraction folder |
| Lithium Recovery | `SAVYNVAK` | Broader produced-water and lithium recovery context |
| Review under Lithium Recovery | `ZT7CGW39` | Review papers |
| ePC-SAFT under Ionic Liquid Solvents | `U7WH3IY4` | Method references only; do not use IL systems as active candidates |

## Key Zotero Items And Attachment Caches

Use these as the first retrieval targets once MCP recovers.

| Zotero key | Attachment cache | Paper | DOI | Role |
|---|---|---|---|---|
| `JUNBXVTI` | `BJ4URKUS` | Gando-Ferreira/Shan 2025, oil-and-gas field-water HBTA/TOPO | `10.3390/w17152258` | Flagship extraction chemistry |
| `9LJWDC7E` | `67B5GGB5` | Zhang 2017, HBTA/TOPO alkaline brine | `10.1016/j.seppur.2017.07.028` | Stoichiometry and Li/Na selectivity anchor |
| `AEL6ZEPG` | `RYM83J2W` | Zhang 2018, beta-diketone lithium extraction | `10.1016/j.hydromet.2017.10.029` | HBTA/TOPO/kerosene process support |
| `GK598336` | `QQN7BD8N` | Hanada 2021, synergistic DES for lithium extraction | `10.1021/acssuschemeng.0c07606` | DES/HTTA/HBTA physical-property and mechanism support |
| `3NMV5MF2` | `TSKR6LVS` | Rezaee 2026, DES/TOPO PC-SAFT approach | `10.1016/j.fluid.2026.114737` | Parameter/regression pilot; not flagship |
| `DQ2M7ZG8` | `V9Y6KZ8L` | Raiguel 2024, D2EHDTPA/BuPhen | `10.1039/d4gc04760e` | Strong non-HBTA backup chemistry |
| `V7EN7V3S` | `E5BMMSJQ` | Kia 2024, TBP/FeCl3 high Mg/Li brines | `10.1007/s11356-024-34617-8` | Mechanistic backup, process-burden comparison |
| `BLUVRJ9Q` | `KI57VRJ6` | Jang 2017, shale-gas produced water D2EHPA/TBP | `10.1016/J.APGEOCHEM.2017.01.016` | Produced-water limitation baseline |
| `W3ELF9TE` | `LZV64YTK` | Lee 2020, shale-gas produced water organic impacts | `10.1016/j.apgeochem.2020.104571` | Produced-water comparison and organic-contaminant context |
| `Z4TRS64E` | `IUPNA7NQ` | Ji 2022, amide/kerosene/FeCl3 | `10.1016/J.JIEC.2022.05.053` | Possible alternate backup |
| `SLMXCPZM` | `2MFZLY5G` | Yu 2024 ePC-SAFT ionic-liquid method | method only | Excluded active, useful package method reference |
| `FGAE94M4` | `CBJZ36VC`, `MJR4ID8X` | Hubach 2024 ePC-SAFT ionic-liquid method | method only | Excluded active, useful package method reference |

## Current Literature Takeaways

These are paraphrased evidence notes from Zotero/local caches. Verify through MCP when it is repaired.

### Shan/Gando 2025, `JUNBXVTI`

Best flagship active extraction chemistry.

Current understanding:

1. Uses actual oil-and-gas field water.
2. Uses HBTA as extractant, TOPO as synergist, and sulfonated kerosene as diluent.
3. Demonstrates high lithium recovery after impurity handling and staged extraction.
4. Ca/Mg and coexisting ions matter and must be modeled or pretreated explicitly.
5. This is the strongest solvent-extraction evidence base for the case-study narrative.

Known current bridge limitation:

The repo can reproduce a calibrated bridge around this chemistry, but not true predictive ePC-SAFT because parameter and reaction-constant payloads are still missing.

### Zhang 2017, `9LJWDC7E`

Mechanistic anchor for HBTA/TOPO.

Current understanding:

1. HBTA/TOPO gives strong Li/Na selectivity.
2. Slope analysis supports a 2 HBTA : 1 TOPO : 1 Li extraction complex in the current bridge.
3. Provides scrubbing/stripping/regeneration context.
4. It is alkaline brine, not produced water, so use it for chemistry, not source composition.

### Zhang 2018, `AEL6ZEPG`

Process support for HBTA/TOPO/kerosene.

Current understanding:

1. HBTA/TOPO/kerosene process support is strong.
2. Kerosene is the practical diluent direction for the flagship case.
3. Multistage operation and mixer-settler stability are useful for presentation and PrOMMiS/IDAES narrative.

### Hanada 2021, `GK598336`

Useful physical-property and mechanism support.

Current understanding:

1. HTTA/TOPO and HBTA/TOPO DES-type systems show strong lithium selectivity.
2. Physical properties may help a pseudo-component fitting route if the flagship HBTA/TOPO/kerosene system lacks pure-component data.
3. Do not turn this into the active flagship unless the user accepts DES uncertainty/cost as a backup.

### Rezaee 2026, `3NMV5MF2`

Important but easy to misrepresent.

Current understanding:

1. Rezaee uses PC-SAFT for organic DES/TOPO and ePC-SAFT for aqueous electrolyte.
2. It is not a full reactive ePC-SAFT model for the flagship HBTA/TOPO system.
3. It is valuable as a parameter/regression and package-smoke-test source.
4. A local smoke script was created and run before this handoff.

### Raiguel 2024, `DQ2M7ZG8`

Best non-HBTA backup chemistry found so far.

Current understanding:

1. Uses D2EHDTPA + BuPhen + octanol modifiers + n-dodecane.
2. Strong Li selectivity over Na/K/Mg/Ca in synthetic geothermal brine.
3. Conventional/non-IL, but not oil-and-gas produced water.
4. Current package parameter inventory does not contain the needed organic components.

### Kia 2024, `V7EN7V3S`

Mechanistic backup, not ideal flagship.

Current understanding:

1. Uses TBP/FeCl3/HCl chemistry for high Mg/Li brines.
2. Useful reported extraction/selectivity and reaction-expression context.
3. Less attractive for the pitch due to acid, Fe handling, corrosion, possible third phase, and process complexity.
4. Current package parameter inventory does not contain a complete TBP/Fe-complex payload.

### Jang 2017 and Lee 2020, `BLUVRJ9Q`, `W3ELF9TE`

Produced-water baseline and limitation case.

Current understanding:

1. Real shale-gas produced-water context.
2. Existing local script uses a placeholder/surrogate D2EHPA/TBP treatment.
3. Current output shows weak Li/Na separation, making it useful as a baseline that motivates the better HBTA/TOPO and ePC-SAFT story.

## Current Top-Five Candidate Ranking

This ranking was in progress when the user asked to stop and produce this handoff.

| Rank | Candidate | Status | Why |
|---:|---|---|---|
| 1 | HBTA + TOPO + sulfonated kerosene | Flagship | Actual field-water evidence, conventional chemistry, strong PrOMMiS/IDAES story, current bridge artifacts exist |
| 2 | D2EHDTPA + BuPhen + octanol + n-dodecane | Best non-HBTA backup | Very strong multication selectivity, conventional/non-IL, but not produced-water and parameter gaps are large |
| 3 | TBAC/decanoic-acid DES + TOPO from Rezaee | Modeling pilot | Best immediate parameter-regression smoke test, but organic PC-SAFT plus aqueous ePC-SAFT and not flagship chemistry |
| 4 | TBP + FeCl3/HCl | Mechanistic backup | Strong high-Mg extraction context, but process burdens and missing parameters |
| 5 | D2EHPA + TBP | Produced-water limitation baseline | Produced-water relevant and existing local script, but weak selectivity and placeholder-heavy |

Potential alternate:

`Z4TRS64E` Ji 2022 amide/kerosene/FeCl3 may become a better backup after Zotero MCP is repaired and full text/SI are reviewed.

## Current ePC-SAFT Parameter Inventory Check

A direct local parameter check was run:

```powershell
@'
from data.epcsaft_properties import pcsaft_prop
queries = ['dodecane','n-dodecane','Dodecane','TBP','TOPO','tributyl','trioctyl','octanol','1-octanol','2-octanol','kerosene','decanoic','acid','benzoyl','thenoyl','D2EHPA']
for q in queries:
    matches = [k for k in pcsaft_prop.keys() if q.lower() in str(k).lower()]
    print(f'{q}: {matches[:12]}')
print('count', len(pcsaft_prop))
'@ | uv run python -
```

Result:

All queried organic ligand/diluent names returned no matches in `data.epcsaft_properties.pcsaft_prop`; count was 32.

Interpretation:

1. The current repo-level parameter dictionary does not contain direct entries for HBTA, TOPO, D2EHPA, TBP, kerosene, dodecane, octanol, decanoic acid, or related ligand names.
2. This means the top candidates are either:
   - calibrated bridge/status;
   - parameter-regression pilot/status; or
   - blocked parameter-gap/status.
3. The missing parameter set is not a cosmetic issue. It is the core scientific boundary of the current case study.

## Updated ePC-SAFT Capability Map

This section supersedes the earlier vague assumption that the package might not be able to handle reactive chemistry.

The downstream environment was rechecked against the sibling source checkout:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT
```

After forcing a path-dependency reinstall:

```powershell
uv sync --reinstall-package epcsaft
```

the installed package in `Lithium_Extraction` exposed the current reactive APIs at source commit:

```text
1ae609c70636
```

with package version:

```text
1.5.0
```

### Reactive APIs That Exist Now

The package can already do these things:

1. `solve_reactive_speciation(...)`
   - Solves homogeneous chemical equilibrium in one phase.
   - Inputs: `species`, `balances`, `totals`, `reactions`, `initial_x`, and `mixture_factory`.
   - Reactions are supplied explicitly through `ReactionDefinition(...)`.
   - Supported reaction standard states: `mole_fraction_activity`, `ideal_mole_fraction`, and `concentration`.

2. `solve_reactive_staged_equilibrium(...)`
   - Solves chemical equilibrium first, then passes the chemically equilibrated composition into a phase-equilibrium route.
   - Available phase routes include `auto`, `tp_flash`, `lle_flash`, `stability`, `electrolyte_lle`, `electrolyte_stability`, and `electrolyte_bubble_pressure`.

3. Mixture-level public routes:
   - `mixture.equilibrium(kind="chemical_equilibrium", ...)`
   - `mixture.equilibrium(kind="reactive_staged_equilibrium", ...)`
   - `mixture.equilibrium(kind="reactive_stability", ...)`
   - `mixture.equilibrium(kind="reactive_electrolyte_bubble_pressure", ...)`

4. Reactive electrolyte bubble workflows:
   - `solve_reactive_electrolyte_bubble(...)`
   - `solve_reactive_electrolyte_bubble_sweep(...)`
   - These run native reactive speciation first and then native fixed-liquid electrolyte bubble pressure.

### Important Boundary On What It Still Does Not Do

The package does not currently expose a fully coupled reactive flash solve for the kind of organic extraction problem we want.

The clearest source-code boundary is:

```text
reactive_flash_tp is not exposed; use an explicit staged phase_kind.
```

That means:

1. The package can do staged:
   - chemical equilibrium first;
   - then phase equilibrium or stability.

2. The package does not yet expose a single fully coupled reactive LLE flash route where reaction and phase split are solved in one monolithic flash solve for the flagship HBTA/TOPO extraction chemistry.

### Current Public Regression Boundaries

Public regression capabilities confirmed now:

1. `fit_pure_neutral(...)`
   - Public and native-backed.
   - Current public V1 scope is nonassociating neutral-component fitting for `m`, `s`, and `e`.

2. `fit_pure_ion(...)`
   - Public and native-backed.
   - Fits ionic parameters including ion `s`, `e`, and optional `d_born`.

3. `fit_binary_pair(...)`
   - Public and native-backed.
   - Current V1 scope is binary VLE fitting for constant `k_ij`-style targets.
   - It does not currently support binary LLE regression as a public finished route.

4. There is code for associating-neutral fitting internally, but it is not the public finished route that this downstream case study can rely on yet.

### What This Means For The Case Study

Accurate statement:

```text
The package can already represent homogeneous reactive speciation and staged chemical-equilibrium-then-phase-equilibrium workflows. The missing closure for the flagship HBTA/TOPO case is not the absence of any reactive API; it is the absence of the full solvent/complex parameter payload, reaction constants, and a finished public regression path for this extraction chemistry.
```

So the package is already strong enough to support:

1. explicit Li complexation reactions;
2. a staged reactive extraction approximation driven by ePC-SAFT activities;
3. a better bridge than the old generic wrapper;

while these still remain open:

1. full predictive HBTA/TOPO reactive LLE closure;
2. public associating-neutral regression workflow adequate for HBTA/TOPO;
3. public LLE/extraction-data regression workflow for the required binary and complex interactions.

### Validation Notes From This Recheck

Validated in the downstream `Lithium_Extraction` environment:

```powershell
uv sync --reinstall-package epcsaft
uv run python scripts\case_study\rezaee_des_epcsaft_parameter_smoke.py
```

Upstream package fix and downstream validation:

```powershell
uv sync --reinstall-package epcsaft
uv run python -c "import epcsaft, json; print(epcsaft.__git_commit__); print(json.dumps(epcsaft.capabilities(), indent=2))"
uv run python scripts\case_study\rezaee_des_epcsaft_parameter_smoke.py
uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py
```

Current outcome after upstream PR #33:

1. `uv sync --reinstall-package epcsaft` succeeded.
2. Installed `epcsaft.__git_commit__` reports `1ae609c70636`.
3. Capabilities report `reactive_speciation`, `reactive_electrolyte_bubble`, `electrolyte_lle`, `pure_neutral`, `pure_ion`, and `binary_pair`.
4. `rezaee_des_epcsaft_parameter_smoke.py` succeeded:
   - `fit_success = True`
   - `density_metric = 0.007347057112639847`
   - `stability_min_tpd = -0.5681261687345767`
   - `lle_status = error diagnostic / collapsed-candidate path`
5. `hbta_topo_reactive_stage_solve.py` succeeded and regenerated:
   - `hbta_topo_reactive_fit.json`
   - `hbta_topo_reactive_stage_results.csv`
   - `hbta_topo_reactive_prommis_stage_table.csv`
   - `hbta_topo_formal_costing_results.csv`
   - `hbta_topo_reactive_model_report.md`

Interpretation:

The earlier concentration-standard-state diagnostics mismatch was fixed upstream by PR #33 and validated downstream at the package-install and capability level. The remaining case-study limits are scientific/modeling limits, not a basic package install/API blocker.

## Existing And New Artifacts In This Branch

Important current files and artifacts:

### Planning And Deck

```text
docs/plans/prompt.md
docs/non_ionic_solvent_extraction_case_study_plan.md
docs/non_ionic_case_study_dependency_roadmap.md
docs/case_study_charter.md
docs/phase0_8_completion_report.md
docs/phase9_final_presentation_skeleton.md
docs/Slides/case_study_section_spec.md
slides/deck.qmd
slides/deck.html
```

### uv Setup

```text
pyproject.toml
uv.lock
.python-version
docs/uv_workflow.md
```

Known commands:

```powershell
uv sync --dev
uv sync --reinstall-package epcsaft
uv run python -m compileall -q scripts data
uv run python -c "import epcsaft; from epcsaft import ePCSAFTMixture; print(epcsaft.__file__)"
```

### Source Composition And Smackover Basis

```text
data/reference/produced_water/smackover_usgs_clean_observation_summary.csv
data/reference/produced_water/smackover_li_tds_sensitivity_basis.csv
data/reference/produced_water/smackover_critical_minerals_ree_status.csv
data/reference/produced_water/smackover_selected_base_feed_ms2.csv
data/reference/produced_water/smackover_phase9_case_basis.md
```

Current Smackover base case:

`MS-2 / MSPU 4-W1`

Recorded values:

```text
Li = 168 mg/L
TDS = 305,000 mg/L
Na = 64,100 mg/L
Ca = 36,900 mg/L
Mg = 3,310 mg/L
```

REE status:

`not_reported` in the local USGS source file used for this case.

### HBTA/TOPO Reactive Bridge

```text
scripts/case_study/hbta_topo_reactive_stage_solve.py
data/pcsaft_parameters/gando_2025/hbta_topo_reactive_fit.json
data/reference/produced_water/hbta_topo_reactive_fit_parameters.csv
data/reference/produced_water/hbta_topo_reactive_stage_results.csv
data/reference/produced_water/hbta_topo_reactive_prommis_stage_table.csv
data/reference/produced_water/hbta_topo_formal_costing_assumptions.csv
data/reference/produced_water/hbta_topo_formal_costing_results.csv
data/reference/produced_water/hbta_topo_reactive_model_report.md
```

Validated earlier:

```powershell
uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py
```

Current model status:

```text
calibrated_reactive_hbta_topo_not_full_predictive_epcsaft
```

Important current metrics:

```text
One-stage MS-2 bridge:
Li extraction = 47.2846 percent
Na extraction = 0.0131 percent
D_Li = 0.8970
S_Li/Na = 6840.1071

Three-stage bridge:
Li extraction nearly total in the mathematical bridge
Costing/narrative should cap to the source-backed Shan/Gando 97.17 percent anchor
```

### Smackover Phase 6-9 Skeleton/Handoff

```text
scripts/case_study/smackover_phase6_8_skeleton.py
data/reference/produced_water/smackover_ms2_transfer_sensitivity.csv
data/reference/produced_water/smackover_prommis_transfer_handoff.csv
data/reference/produced_water/phase8_costing_scenarios_skeleton.csv
data/reference/produced_water/phase9_costing_skeleton.csv
data/reference/produced_water/prommis_stage_mass_balance_skeleton.csv
data/reference/produced_water/epcsaft_prommis_bridge_contract.csv
data/reference/produced_water/smackover_ms2_surrogate_schema.csv
```

These are defensible skeleton/handoff artifacts, not final predictive thermodynamics.

### Rezaee 2026 DES/TOPO Smoke Test

```text
scripts/case_study/rezaee_des_epcsaft_parameter_smoke.py
data/reference/produced_water/rezaee_2026_des_density_fit_records.csv
data/reference/produced_water/rezaee_2026_des_parameter_fit_summary.csv
data/reference/produced_water/rezaee_2026_epcsaft_parameter_smoke_report.md
data/reference/produced_water/rezaee_2026_epcsaft_phase_equilibrium_smoke.json
data/pcsaft_parameters/rezaee_2026/des_nonassoc_fit.json
```

Validated earlier:

```powershell
uv run python scripts\case_study\rezaee_des_epcsaft_parameter_smoke.py
```

Current result:

```text
density fit success = True
m = 8.619136661242647
sigma = 3.108524323527317
epsilon/k = 252.6883264625197
density metric = 0.007347057112639847
electrolyte stability success = True
stable = False
min_tpd = -0.5681261687345767
electrolyte LLE status = error / SolutionError / candidate collapsed to one phase
```

Interpretation:

This successfully exercises package parameter fitting and electrolyte-stability plumbing. It does not complete a flagship reactive HBTA/TOPO model.

### Jang D2EHPA/TBP Baseline

```text
scripts/lle/jang_2017_stage2_li_na_tbp_d2ehpa.py
data/multiphase/jang_2017_stage2_li_na_summary.md
data/multiphase/jang_2017_stage2_li_na_summary.csv
```

Known issue:

The script can be slow and previously timed out at 180 seconds in one pass.

Current existing output:

```text
10-cycle crossflow:
Li extraction about 40.13 percent
Na extraction about 38.21 percent
```

Use as a limitation/baseline case, not as proof of selective extraction.

### New Scorecard Script Added But Not Yet Validated

This thread added:

```text
scripts/case_study/solvent_candidate_scorecard.py
```

It is intended to write:

```text
data/reference/produced_water/solvent_candidate_scorecard_2026_05_07.csv
data/reference/produced_water/solvent_candidate_run_matrix_2026_05_07.csv
data/reference/produced_water/solvent_candidate_literature_review_2026_05_07.md
```

Important:

The user asked this thread to stop and produce this handoff before the scorecard script was run or validated. A new thread should inspect it, run it, and correct it if needed.

Suggested command:

```powershell
uv run python scripts\case_study\solvent_candidate_scorecard.py
```

Then validate:

```powershell
uv run python -m compileall -q scripts data
```

## Subagent Status From This Thread

The user explicitly wanted subagents with smaller models for efficiency.

Known subagents from this run:

```text
019e012a-88dc-7ba2-aa03-828c35e48fc0 Descartes, explorer, gpt-5.4-mini
019e012a-a7a0-7341-a68c-f6b4ae637eb7 Plato, explorer, gpt-5.3-codex-spark
```

Descartes completed a repo-artifact search and reported four runnable paths:

1. HBTA/TOPO/sulfonated kerosene bridge.
2. Jang D2EHPA/TBP placeholder baseline.
3. Gando HBTA/TOPO chelation wrapper.
4. Rezaee 2026 DES/TOPO smoke test.

Descartes did not find runnable DBM/TOPO or TBP/FeCl3 execution paths in the repo.

Plato status was not finalized before this handoff. A new thread may wait on or ignore it depending on whether the agent is still reachable.

## Current Git Worktree State

The worktree is dirty. Do not revert unrelated changes.

Known unrelated or pre-existing dirty changes:

```text
.idea/Lithium_Extraction.iml
data/multiphase/gando_2025_* generated PNGs
data/multiphase/gando_2025_stage3_efficiency_plot.png
```

Many new files are untracked from the ongoing case-study work. Do not clean them. They are part of the in-progress branch handoff.

Before making a commit, review the diff carefully and avoid staging unrelated IDE files unless the user asks.

## Validation Commands Already Known Good In This Branch

Use `uv` as the package manager.

Core commands:

```powershell
uv sync --dev
uv sync --reinstall-package epcsaft
uv run python -m compileall -q scripts data
uv run python -c "import epcsaft; from epcsaft import ePCSAFTMixture; print(epcsaft.__file__)"
uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py
uv run python scripts\case_study\rezaee_des_epcsaft_parameter_smoke.py
```

Quarto deck render:

```powershell
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
```

Known Quarto path:

```text
C:\Users\Tanner\AppData\Local\Apps\Quarto\bin\quarto.exe
```

## Package/Discussion Coordination Need

The upstream ePC-SAFT package is at:

```text
C:\Users\Tanner\Documents\git\ePC-SAFT
```

GitHub repo:

```text
tannerpolley/ePC-SAFT
```

User said another thread is waiting to improve the package if downstream finds ePC-SAFT package problems.

Current downstream finding:

This is not primarily an API-absence problem anymore. The package already has reactive-speciation and staged reactive-equilibrium APIs. The bigger issue is missing parameter/regression support for the solvent-extraction systems needed by the case study:

1. HBTA/TOPO/sulfonated kerosene flagship parameters are missing.
2. Li-BTA-TOPO and competing divalent complex parameters are missing.
3. Binary interactions and reaction-equilibrium constants are missing.
4. D2EHDTPA/BuPhen, TBP/FeCl3, D2EHPA/TBP backup systems also lack complete local parameter payloads.
5. Public regression is still incomplete for this use case:
   - public neutral regression is still V1/nonassociating;
   - public binary-pair regression is still V1/VLE-oriented and does not yet close the needed LLE/extraction fitting path.
6. Rezaee smoke test shows density fitting and stability calls can run, but direct pseudo-DES LLE is diagnostic and can collapse to one phase.
7. The earlier upstream reactive-speciation concentration-standard-state diagnostics mismatch was fixed by upstream PR #33 and downstream validation now installs commit `1ae609c70636`.

Recommended next action:

Create or update a GitHub Discussion in `tannerpolley/ePC-SAFT` after the new thread confirms current package capabilities. The discussion should be a package-support request, not a bug accusation unless a reproducible package error is found.

Suggested discussion title:

```text
Downstream lithium extraction case study needs neutral associating solvent and reactive LLE parameter-fitting support
```

Suggested discussion body should include:

1. Downstream repo path.
2. Exact commands:
   - `uv run python scripts\case_study\rezaee_des_epcsaft_parameter_smoke.py`
   - `uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py`
   - `uv run python scripts\case_study\solvent_candidate_scorecard.py`
3. Current model boundary.
4. Needed package support:
   - public associating-neutral parameter regression suitable for HBTA/TOPO-class solvents;
   - binary-interaction fitting from LLE/extraction data;
   - a stronger public workflow for extraction-relevant LLE/reactive fitting, even if the solver remains staged;
   - eventual fully coupled reactive LLE support if the package roadmap wants to go beyond staged chemistry-plus-phase workflows;
   - documented pattern for passing ePC-SAFT equilibrium results to downstream PrOMMiS/IDAES transfer tables.
5. Completion condition:
   - downstream can replace calibrated HBTA/TOPO bridge with a true reactive ePC-SAFT parameter payload and run a staged handoff table.

Coordination skill file:

```text
C:\Users\Tanner\.codex\skills\coordination\SKILL.md
```

GitHub CLI path:

```text
C:\Program Files\GitHub CLI\gh.exe
```

Known auth rule:

If needed, verify GH CLI with:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" --version
& "C:\Program Files\GitHub CLI\gh.exe" auth status --active -h github.com
& "C:\Program Files\GitHub CLI\gh.exe" api user --jq .login
```

Do not run `gh auth token`.

## Recommended New Thread Workflow

Use this sequence.

### Step 1 - Load Skills And Local Startup Context

Use these skills:

```text
zotero-local-research:zotero-research
academic-researcher
chemical-engineer
coordination
```

Read local startup files:

```text
docs/.codex-journal/user_preferences.md
docs/.codex-journal/project_memory.md
```

Read:

```text
docs/plans/prompt.md
docs/plans/zotero_mcp_refresh_case_study_handoff_2026_05_07.md
```

Before making any package-capability claim, refresh the local path install and print the live capability map:

```powershell
uv sync --reinstall-package epcsaft
uv run python -c "import epcsaft, json; print(epcsaft.__git_commit__); print(json.dumps(epcsaft.capabilities(), indent=2))"
```

### Step 2 - Retry Zotero MCP

Immediately retry:

```text
mcp__zotero_local__.zotero_find_collections({"query":"Organic Solvents","exact":true,"limit":10})
mcp__zotero_local__.zotero_get_collection_items_by_name({"collection_name":"Organic Solvents","limit":20,"recursive":true,"sort":"title","direction":"asc"})
mcp__zotero_local__.zotero_hybrid_search({"collection_key":"LYN9RATQ","query":"lithium solvent extraction HBTA TOPO produced water parameter PC-SAFT ePC-SAFT","limit":10,"group_by_item":true,"include_snippets":true})
```

If MCP works, use it to verify:

1. All top-five candidate items.
2. Attachment availability.
3. Full-text evidence for the scorecard.
4. Any annotations the user may have added.

If MCP still fails, continue with local HTTP/cache:

```powershell
curl.exe -s "http://localhost:23119/api/users/0/collections/LYN9RATQ/items?format=json&limit=100&sort=title"
rg -n "HBTA|TOPO|D2EHDTPA|BuPhen|TBP|FeCl3|D2EHPA|kerosene|produced water|PC-SAFT|ePC-SAFT" "C:\Users\Tanner\Zotero\storage" -g ".zotero-ft-cache"
```

### Step 3 - Validate Or Fix The Candidate Scorecard

Run:

```powershell
uv run python scripts\case_study\solvent_candidate_scorecard.py
```

Inspect outputs:

```text
data/reference/produced_water/solvent_candidate_scorecard_2026_05_07.csv
data/reference/produced_water/solvent_candidate_run_matrix_2026_05_07.csv
data/reference/produced_water/solvent_candidate_literature_review_2026_05_07.md
```

Fix the script if it fails or if Zotero MCP evidence changes the ranking.

### Step 4 - Run/Confirm Candidate Execution Status

Run the two robust current scripts:

```powershell
uv run python scripts\case_study\hbta_topo_reactive_stage_solve.py
uv run python scripts\case_study\rezaee_des_epcsaft_parameter_smoke.py
```

Optional slow baseline:

```powershell
uv run python scripts\lle\jang_2017_stage2_li_na_tbp_d2ehpa.py
```

Use a timeout if needed. Existing artifacts are acceptable if the script times out.

Parameter-gap candidates:

1. Raiguel D2EHDTPA/BuPhen.
2. Kia TBP/FeCl3.
3. Ji amide/kerosene/FeCl3.

For these, do not invent solves. Record parameter gaps and data needs unless sufficient paper/SI data can be extracted to fit parameters.

### Step 5 - Create The Package Discussion If Confirmed Needed

After confirming package/regression gaps, create a GitHub Discussion in `tannerpolley/ePC-SAFT`.

Use the coordination contract from:

```text
C:\Users\Tanner\.codex\skills\coordination\SKILL.md
```

Do not create a vague issue. Make it actionable:

1. Downstream command.
2. Exact failure or missing feature.
3. Exact data required.
4. Expected package-side support.
5. Downstream validation condition.

### Step 6 - Update The Deck And Phase 9 Docs

After the scorecard and run matrix are finalized, update:

```text
docs/phase9_final_presentation_skeleton.md
docs/Slides/case_study_section_spec.md
slides/deck.qmd
```

Recommended deck narrative:

1. Smackover is the source-composition anchor.
2. HBTA/TOPO is the best non-ionic extraction-chemistry anchor.
3. ePC-SAFT matters because high-TDS brine and ligand extraction are equilibrium/speciation problems, not simple fixed recovery factors.
4. Current bridge generates PrOMMiS/IDAES transfer variables, but true predictive ePC-SAFT requires parameter fitting.
5. Rezaee proves the package/regression path is plausible but does not solve HBTA/TOPO.
6. Backup chemistries are ranked and their gaps are explicit.

Render:

```powershell
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
```

## Suggested Opening Prompt For The New Thread

Copy this into the new Codex thread:

```text
Continue the Lithium_Extraction produced-water lithium case study from:

C:\Users\Tanner\Documents\git\Lithium_Extraction\docs\plans\zotero_mcp_refresh_case_study_handoff_2026_05_07.md

Use the Zotero plugin/MCP first and keep retrying it because another agent is fixing the plugin. If MCP still returns Transport closed, use the local Zotero HTTP API at http://localhost:23119/api/users/0 and the Zotero storage full-text caches, but keep periodically retrying MCP.

Use these skills/plugins where applicable:
- zotero-local-research:zotero-research
- academic-researcher
- chemical-engineer
- coordination

Keep ionic liquids excluded from the active benchmark. They are method references only.

Your immediate tasks:
1. Verify the Zotero collection and full-text evidence for the top candidate solvent systems.
2. Run and validate scripts/case_study/solvent_candidate_scorecard.py.
3. Confirm the top five solvent ranking and update the generated scorecard/review artifacts if needed.
4. Run or confirm the available candidate scripts: HBTA/TOPO bridge, Rezaee DES/TOPO smoke, and the Jang baseline if practical.
5. If package-side ePC-SAFT parameter/regression/reactive-LLE support is missing, create a GitHub Discussion in tannerpolley/ePC-SAFT using the coordination skill contract.
   - The discussion should say that reactive APIs do exist now.
   - The request is for parameterization and extraction-oriented regression/workflow support, not for basic reactive-speciation existence.
6. Update the Phase 9 docs and slides/deck.qmd so the presentation clearly shows why ePC-SAFT is needed for PrOMMiS/IDAES.

Do not stop at a high-level plan unless a real blocker occurs. Label all shortcuts and do not claim true predictive reactive HBTA/TOPO ePC-SAFT is complete.
```

## What Is Still Truly Unfinished

This is the most important remaining science and engineering work:

1. Fit or find HBTA parameters.
2. Fit or find TOPO parameters.
3. Fit or find sulfonated kerosene or defensible diluent surrogate parameters.
4. Fit or find Li-BTA-TOPO complex parameters.
5. Fit or find competing Mg/Ca/Sr/Ba complex parameters if those ions remain in the feed.
6. Fit or find binary interaction parameters for aqueous/organic and organic/organic pairs.
7. Fit reaction-equilibrium constants from Zhang/Shan/Gando/Hanada/Rezaee data or digitized curves.
8. Replace the calibrated HBTA/TOPO reactive-stage bridge with a predictive staged reactive-ePC-SAFT workflow or a fully coupled reactive LLE route if the upstream package exposes one later.
9. Expand the PrOMMiS artifact from handoff tables into an actual staged MSContactor solve for the flagship case.
10. Add formal IDAES costing hooks for pretreatment, extraction/contacting, stripping, solvent makeup/loss, concentration, Li2CO3 precipitation, and waste handling.
11. Tighten source-specific Smackover critical-mineral/REE evidence if the user can provide or locate a source that reports REE.
12. Finalize deck figures and tables from the generated artifacts.

## Current Best Answer To The Scientific Framing

The case study should not say:

```text
We already solved produced-water lithium extraction with true predictive reactive ePC-SAFT.
```

It should say:

```text
This case study shows why ePC-SAFT belongs in the PrOMMiS/IDAES ecosystem. A real high-TDS produced-water source and a source-backed non-ionic extraction chemistry require equilibrium, speciation, selectivity, and phase-split calculations that fixed recovery factors cannot defend. The current repository already generates bridge transfer variables and costing skeletons, while the unresolved parameter/regression work defines the exact package capability needed to turn the bridge into a predictive thermodynamic model.
```
