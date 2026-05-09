# Non-Ionic Produced-Water Lithium Solvent Extraction Case Study Plan

Last updated: 2026-05-06

> Superseded context, 2026-05-08: this plan predates the Rezaee pivot. Use it only as historical planning context. The current active case-study basis is Rezaee DES/TOPO Li/Na extraction after divalent pretreatment, not HBTA/TOPO as the flagship.

## Purpose

This document is the durable handoff plan for the next implementation pass after the repository is moved to a `uv`-based workflow. It replaces the earlier ionic-liquid extraction framing with a non-ionic, ligand-based solvent extraction case study that can defend the value of ePC-SAFT inside the PrOMMiS and IDAES ecosystem.

Current deck priority:

- Non-ionic, conventional-organic chemistry only for the flagship produced-water story.
- Explicitly exclude ionic liquids from active benchmarks, while allowing them only as legacy background.
- Emphasize ePC-SAFT as the thermodynamic transfer-variable engine: phase split, equilibrium phase compositions, distribution ratios, selectivity, and validity signals that PrOMMiS/IDAES needs before optimization.

The core claim to present is:

> Source-specific produced-water chemistry controls lithium extraction behavior. ePC-SAFT is the thermodynamic engine that can turn that chemistry, ligand complexation, phase splitting, and competing-ion selectivity into transfer variables that PrOMMiS and IDAES unit models can use for staged solvent extraction, process analysis, optimization, and costing.

## Explicit Scope Correction

Ionic liquids must be ignored as active case-study candidates. They may be mentioned only as excluded background if needed to explain why the case study deliberately focuses on conventional organic extractant systems.

Reason for exclusion:

- Ionic liquids are too costly for this presentation objective.
- Their process uncertainty is too high for the current PrOMMiS/IDAES implementation argument.
- The case study needs a more industrially recognizable solvent extraction chemistry using conventional ligands, synergists, and diluents.

Excluded active case-study bases:

- Functional ionic liquid produced-water extraction systems.
- Bifunctional ionic liquid shale-gas produced-water extraction systems.
- Tetracyanoborate ionic-liquid systems except as prior ePC-SAFT literature background.

Evidence rule:

- Do not claim support from ionic liquids in this pass.
- Keep every unsupported or missing field explicit as `not_reported` and route it through notes.

## Generated Evidence Pack (Deck-Ready)

Use only these local artifacts for direct deck claims unless a source document is newly added and reviewed:

| Artifact | Type | What it provides | Preferred deck use |
|---|---|---|---|
| `data/reference/produced_water/non_ionic_case_study_composition.csv` | CSV | Source-composition basis for Shan 2025 feed cases | source slide, chemical complexity rationale |
| `data/reference/produced_water/non_ionic_case_study_process_summary.csv` | CSV | Process summary rows (selectivity test + three-stage + field-water carbonate-prep) | process section and limitation notes |
| `data/reference/produced_water/non_ionic_case_study_sources.md` | Markdown | Extracted literature anchors and explicit exclusions | evidence provenance slide |
| `data/multiphase/gando_2025_one_stage_assets/gando_2025_one_stage_nominal.csv` | CSV | One-stage transfer metrics \(D\), extraction, selectivity | one-stage quantitative slide |
| `data/multiphase/gando_2025_one_stage_assets/gando_2025_one_stage_species_split.png` | PNG | One-stage species split visual | one-stage visual |
| `data/multiphase/gando_2025_slide_assets/gando_2025_stage_summary.csv` | CSV | Stage-wise cumulative Li/Na extraction and \(S_{Li/Na}\) | multi-stage performance slide |
| `data/multiphase/gando_2025_slide_assets/gando_2025_cumulative_extraction_wide.png` | PNG | three-stage trend curve | staged performance visual |
| `data/multiphase/gando_2025_slide_assets/gando_2025_stage_summary_table.png` | PNG | stage summary values in compact graphic form | executive summary tables |

Alignment rule:

- Quantitative claims on slides should point to one row in this artifact pack.
- If a claim is not in this pack, mark it as pending or a presenter note rather than hard-typing it on a slide.

## Recommended Case-Study Direction

Use a dual-track evidence basis:

1. Source and siting basis: southern Arkansas Smackover or another stronger U.S. produced-water source if the composition screen proves better.
2. Extraction chemistry basis: the strongest non-ionic solvent extraction literature case with real or realistic produced-water brine composition.

The current best extraction benchmark found in Zotero is:

- Shan, Q.; Zhu, G.; Fan, P.; Liang, M.; Zhang, X.; Liu, J.; Wu, G. 2025. "Influence Mechanism of Coexisting Ions on the Extraction Efficiency of Lithium from Oil and Gas Field Water." Water 17, 2258. DOI: `10.3390/w17152258`. Zotero item key: `JUNBXVTI`.

Why this is the current leading benchmark:

- It uses actual oil and gas field water.
- It uses a non-ionic solvent extraction system: HBTA as extractant, TOPO as synergist, and sulfonated kerosene as diluent.
- It studies coexisting inorganic ions and organic matter that are directly relevant to produced water.
- It reports extraction, back-extraction, impurity removal, multistage cross-flow extraction, and lithium carbonate product purity.
- It gives a direct opening for ePC-SAFT reaction and phase-equilibrium modeling because the chemistry is ligand/complexation driven.

## Literature Evidence Backbone

### Primary Non-Ionic Extraction Candidate

Shan/Zhu/Fan et al. 2025 (`JUNBXVTI`, DOI `10.3390/w17152258`)

Use this paper for:

- Actual oil and gas field water extraction.
- HBTA/TOPO/sulfonated-kerosene solvent system.
- Saponification with NaOH.
- Back-extraction with hydrochloric acid.
- Coexisting-ion effects.
- Multistage cross-flow extraction.
- Lithium carbonate product purity.

Important evidence to extract into a structured data table:

- Initial field-water composition.
- Li concentration.
- Na, K, Mg, Ca, Sr/Ba if reported.
- Anions such as Cl, Br, NO3, SO4 if reported.
- Organic matter or TOC conditions.
- HBTA concentration.
- TOPO concentration.
- Diluent identity.
- Saponification degree.
- O/A ratio.
- Contact time.
- Stage-wise extraction efficiencies.
- Raffinate/extract compositions if available.
- Back-extraction and Li2CO3 precipitation results.

Current Zotero-derived anchors:

- The paper uses HBTA as extractant, TOPO as synergist, and sulfonated kerosene as diluent.
- The paper uses 15 L of actual oil and gas field water as the research object.
- The organic phase example uses 0.15 mol/L HBTA and 0.15 mol/L TOPO.
- The extraction system is saponified by NaOH.
- The three-stage cross-flow process reaches roughly 97 percent cumulative lithium extraction after impurity removal.
- The average transfer efficiency in the 15 L field-water case is reported around 91 percent.
- The final lithium carbonate product purity is reported around 99 percent.
- Ca and Mg are major inhibiting ions; pretreatment/removal is important.

### Secondary Ligand/Extraction Class Evidence

Chen et al. 2025 (`5HLW3Y8W`, DOI `10.1080/00084433.2025.2540724`)

Use this review for:

- DBM/TOPO ligand-class context.
- Beta-diketone and neutral organophosphorus systems.
- The claim that phosphoryl groups and lithium-specific ligands improve selectivity.
- Reported literature performance for DBM/TOPO in actual unconventional oil and gas field brine.

Important point:

- Chen reports that DBM/TOPO was used for actual unconventional oil and gas field brine and could reach high lithium extraction at high Na/Li ratio. The original Zhao paper should still be located and used directly if possible before final presentation claims are made.

Nikkhah et al. 2024 (`E5FVQEBP`, DOI `10.1016/j.cej.2024.155349`)

Use this review for:

- Conventional solvent extraction categories.
- TBP/FeCl3 and related co-extractant systems.
- Practical limitations such as corrosion, extractant loss, Fe loss, third-phase risk, and high-acid stripping.
- Motivation for why ePC-SAFT is useful: conventional solvent extraction has nonideal phase behavior and chemistry-dependent selectivity that should not be treated as a black-box recovery factor.

Rezaee et al. 2026 (`3NMV5MF2`, DOI `10.1016/j.fluid.2026.114737`)

Use this paper for:

- A parameter-fitting and package-smoke-test workflow for a DES/TOPO lithium extraction system.
- A concrete example of fitting DES and TOPO PC-SAFT-style parameters from density data.
- A cautionary modeling boundary: the paper uses PC-SAFT for the organic phase and ePC-SAFT for the aqueous electrolyte phase, not a unified full reactive ePC-SAFT LLE closure for HBTA/TOPO.
- Tabulated DES, TOPO, organic product pseudo-species, and binary-interaction values that can test the current ePC-SAFT regression and equilibrium APIs.

Important point:

- Rezaee is a modeling-method lead and a diagnostic parameter source. It does not close the HBTA, TOPO, sulfonated-kerosene, Li-BTA-TOPO complex, or HBTA reaction-equilibrium gaps for the flagship Shan/Gando case.

Knapik et al. 2023 (`DIRN6TP8`, DOI `10.3390/en16186628`)

Use this review for:

- Oilfield brine composition context.
- Resource thresholds for critical minerals.
- Smackover and oilfield-brine lithium context.
- The broader produced-water lithium-recovery opportunity.

### Siting Evidence

The case study should keep Smackover as the leading U.S. site candidate unless the fresh source-composition screen proves a better produced-water brine.

Current siting rationale to preserve:

- Smackover is high-value and hypersaline.
- Smackover has a stronger infrastructure story because of the Arkansas bromine/brine industry.
- Smackover is a practical audience-facing example for why a real produced-water basin needs thermodynamic modeling before flowsheet and costing claims.

Important boundary:

- Do not claim the existing Gando-style showcase is already calibrated to a specific Arkansas well.
- Describe it as a prior selective-extraction benchmark until the new non-ionic case is calibrated.

## Composition Data Requirements

The case study needs a true source-composition table, not a generic brine.

Minimum required fields:

- Source name.
- Formation/basin.
- Sample type.
- Literature source and DOI.
- Zotero item key.
- Units.
- Li.
- Na.
- K.
- Mg.
- Ca.
- Sr.
- Ba if available.
- Cl.
- Br if available.
- SO4 if available.
- B if available.
- Mn, Fe, Zn, Cu, Ni, Al if available.
- REE values if reported.
- Total dissolved solids if reported or computable.
- pH if reported.
- TOC or organic components if reported.
- Notes on pretreatment or impurity removal.

REE rule:

- If the selected source does not report REE, record `not reported`.
- Do not infer REE from nearby basins, reviews, or general produced-water claims.
- If REE are critical for the presentation, perform a separate source search for produced-water REE data and label it as a parallel mineral-opportunity dataset rather than part of the solvent extraction feed.

Suggested file target:

- `data/reference/produced_water/non_ionic_case_study_composition.csv`
- `data/reference/produced_water/non_ionic_case_study_process_summary.csv`
- `data/reference/produced_water/non_ionic_case_study_sources.md`
- `data/reference/produced_water/non_ionic_case_study_transfer_matrix.md`
- `data/reference/produced_water/non_ionic_case_study_transfer_matrix.csv`

## Chemistry And Thermodynamics Model

The model should treat solvent extraction as reactive phase equilibrium.

Relevant chemistry for HBTA/TOPO style extraction:

- HBTA is the acidic beta-diketone extractant.
- NaOH saponifies or deprotonates the extractant.
- Lithium extraction likely proceeds through ligand coordination/complexation in the organic phase.
- TOPO acts as a neutral synergist through phosphoryl oxygen coordination.
- Divalent cations, especially Ca2+ and Mg2+, compete strongly and can suppress lithium extraction.
- Pretreatment or impurity removal must be modeled or parameterized when the literature shows it is required.

ePC-SAFT role:

- Phase split between aqueous and organic phases.
- Nonideal activity/fugacity contributions in high-salinity brines and organic solvent mixtures.
- Chemical reaction/speciation support for ligand deprotonation and lithium complex formation.
- Distribution ratios for lithium and competing ions.
- Selectivity factors such as Li/Na, Li/Mg, Li/Ca, and Li/Sr.
- Raffinate and extract phase compositions.
- Diagnostics that show whether a point is thermodynamically valid or outside the model's confidence region.

Minimum reaction set to evaluate:

- Ligand deprotonation or saponification: `HBTA + NaOH -> NaBTA + H2O`, or the equivalent ionic/speciation representation supported by ePC-SAFT.
- Lithium complexation: `Li+ + BTA- + n TOPO -> Li(BTA)(TOPO)n`.
- Competing divalent complexation where data support it: `M2+ + 2 BTA- + n TOPO -> M(BTA)2(TOPO)n`, with M as Ca or Mg.
- Back-extraction can be represented later as acid-driven reversal if needed for the full process story.

Implementation default:

- Start with the smallest chemically defensible reaction network needed to compute Li transfer and competing-ion inhibition.
- Add divalent reactions only after the Li-only and Li/Na cases are stable.
- Keep unsupported species as explicit diagnostics rather than silently dropping them.

## ePC-SAFT Parameter Strategy

Use existing ePC-SAFT parameter values where possible.

Parameter targets:

- Water.
- Kerosene or representative alkane/diluent surrogate.
- TOPO or a chemically defensible neutral organophosphorus surrogate.
- HBTA or a beta-diketone surrogate if direct parameters are unavailable.
- Li+, Na+, K+, Mg2+, Ca2+, Sr2+, Cl-, Br-, SO4 where available.
- Neutral or ionic ligand-complex pseudo-species only if needed and clearly documented.

Parameter hierarchy:

1. Existing ePC-SAFT package parameter tables.
2. Local literature-derived parameter files already in this repo.
3. Peer-reviewed ePC-SAFT or PC-SAFT parameter literature.
4. Closest defensible surrogate species with a clear limitation note.
5. Fitted pseudo-parameter only as a documented case-study calibration, not as a general package parameter.

Important implementation boundary:

- If a parameter is missing, do not fake it inside the package.
- Record the missing parameter, choose a documented surrogate or reduced model, and continue.

### Rezaee 2026 Parameter-Fitting Smoke Test

Use Rezaee 2026 as a diagnostic bridge between the literature search and the current ePC-SAFT package:

- Fit a nonassociating DES pseudo-component from the reported density correlation only as a runtime smoke test.
- Preserve the paper's reported associating PC-SAFT parameters separately, because the current package regression helper does not fit association parameters from density-only data.
- Run a minimal aqueous-electrolyte plus DES phase-stability or LLE test to verify that package plumbing works.
- Label the result as `regression_smoke_test`, not as a predictive HBTA/TOPO parameter set.

## `epcsaft-pse` Bridge Implementation Plan

The bridge repo should be renamed as a hard break:

- Old project name: `pcsaft-pse`.
- New project name: `epcsaft-pse`.
- Old import: `pcsaft_pse`.
- New import: `epcsaft_pse`.
- No compatibility shim.

Bridge responsibilities:

- Import the current `epcsaft` package directly.
- Accept produced-water brine composition in mass concentration units.
- Convert brine composition to mole-based ePC-SAFT inputs.
- Charge-balance or report charge imbalance.
- Apply pretreatment assumptions explicitly.
- Build ePC-SAFT mixture/reaction definitions.
- Run equilibrium or reduced equilibrium calculations.
- Return transfer variables for PrOMMiS/IDAES.
- Generate surrogate training rows over relevant operating and composition ranges.

Suggested public bridge inputs:

- `source_id`.
- `temperature_K`.
- `pressure_Pa`.
- `aqueous_feed_mg_L`.
- `organic_phase_components`.
- `extractant_concentration_mol_L`.
- `synergist_concentration_mol_L`.
- `diluent`.
- `organic_to_aqueous_ratio`.
- `saponification_degree`.
- `pretreatment_case`.
- `stage_index`.

Suggested public bridge outputs:

- `eta_li_pct`.
- `eta_i_pct` for competing ions.
- `D_li`.
- `D_i` for competing ions.
- `selectivity_li_na`.
- `selectivity_li_mg`.
- `selectivity_li_ca`.
- `aqueous_out_mg_L`.
- `organic_out_mg_L`.
- `phase_fractions`.
- `reaction_extents` if available.
- `validity_status`.
- `diagnostics`.

## Surrogate Plan

The surrogate is the bridge from ePC-SAFT to PrOMMiS/IDAES.

Purpose:

- Avoid forcing PrOMMiS to call expensive or fragile ePC-SAFT solves at every flowsheet iteration.
- Preserve thermodynamic structure by training the surrogate on ePC-SAFT outputs.
- Provide smooth transfer variables to MSContactor and costing workflows.

Minimum features:

- Li concentration.
- Na concentration.
- Mg concentration.
- Ca concentration.
- Sr concentration if available.
- TDS.
- Temperature.
- O/A ratio.
- HBTA concentration.
- TOPO concentration.
- Saponification degree.
- Pretreatment flag or categorical encoding.

Minimum targets:

- Li extraction efficiency.
- Na extraction efficiency.
- Mg extraction efficiency.
- Ca extraction efficiency.
- Li distribution ratio.
- Competing-ion distribution ratios.
- Li/Na selectivity.
- Li/Mg selectivity.
- Li/Ca selectivity.
- Validity flag.

Surrogate quality checks:

- Training bounds must be stored with the surrogate.
- Predictions outside the training range must be flagged.
- Monotonicity and directionality should be checked against literature trends.
- A small holdout set should be used before sending the surrogate to PrOMMiS.

## PrOMMiS And IDAES Demonstration Plan

PrOMMiS should be the final result destination.

Core framing:

- ePC-SAFT is not presented as a full flow-sheet solution; it generates equilibrium-derived transfer variables that PrOMMiS/IDAES can consume as staged-material-balance inputs.
- The value in this pass is to show a reusable handoff: `feed chemistry -> ePC-SAFT equilibrium/sensitivity -> process-stage variables`.

Expected PrOMMiS work:

- Update existing solvent extraction proof-of-concept code to import `epcsaft_pse`.
- Use PrOMMiS solvent extraction/MSContactor as the staged unit model.
- Feed the model with the selected produced-water composition.
- Use surrogate-derived transfer variables for Li and competing ions.
- Run one-stage and multistage extraction demonstrations.
- Report raffinate/extract stream composition.
- Report lithium recovery and selectivity.
- If feasible, expose the stream/design variables needed for IDAES costing.

IDAES role:

- Do not modify IDAES itself.
- Use IDAES through PrOMMiS unit models, costing, and process-system tooling.
- Treat costing as a second-level output once stream and stage variables are stable.

Minimum final PrOMMiS artifacts:

- Composition input table.
- ePC-SAFT/surrogate transfer-variable table.
- One-stage extraction result.
- Multistage extraction result.
- Diagnostics and limitations.
- Costing-readiness report.

## Presentation Storyline

Recommended slide logic:

1. The opportunity is not generic lithium-in-water; it is source-specific produced-water valorization.
2. Ionic liquids are intentionally excluded because the implementation case needs lower-cost, more conventional extraction chemistry.
3. The selected non-ionic solvent system gives a literature-grounded extraction mechanism.
4. Produced-water brines are chemically crowded, so selectivity cannot be assumed from a single lithium concentration.
5. ePC-SAFT adds unique value by computing phase equilibrium, reaction/speciation effects, and competing-ion transfer.
6. The surrogate converts ePC-SAFT rigor into a fast PrOMMiS/IDAES interface.
7. PrOMMiS/IDAES then supplies staged contactors, flowsheet analysis, optimization, and costing.
8. The result is a defensible implementation path for adding ePC-SAFT to the PrOMMiS/IDAES ecosystem.

Core novelty sentence:

> ePC-SAFT is the missing thermodynamic layer between real produced-water chemistry and process-level lithium extraction economics.

## Validation Commands After `uv` Migration

Use these commands from the `Lithium_Extraction` repo root:

```powershell
uv sync --dev
uv run python -m compileall -q scripts data
uv run python scripts\lle\gando_2025_three_stage_crossflow.py
uv run python scripts\lle\gando_2025_one_stage_assets.py
uv run python scripts\lle\gando_2025_slide_assets.py
```

For ePC-SAFT package smoke testing:

```powershell
uv run python -c "import epcsaft; from epcsaft import ePCSAFTMixture; print(epcsaft.__file__)"
```

For the Quarto deck:

```powershell
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
```

## Failure And Issue Policy

If ePC-SAFT fails on the selected reactive extraction case:

1. Try a reduced species set.
2. Try Li/Na before adding Mg/Ca/Sr.
3. Try non-reactive phase equilibrium before reactive phase equilibrium.
4. Try bounded single-point solves before sweeps.
5. If the failure appears to be package-level after repeated attempts, open a GitHub issue in the ePC-SAFT repo.

The GitHub issue should include:

- Minimal script.
- Species list.
- Feed composition.
- Reaction definitions.
- Temperature and pressure.
- Solver options.
- Full traceback.
- Expected behavior.
- Whether fallback or reduced chemistry worked.

Continue the case study with a clearly labeled fallback rather than stopping the whole presentation build.

## Near-Term Implementation Order

1. Finish `uv` migration for `Lithium_Extraction`.
2. Extract the full composition, operating table, and stage-result tables from the 2025 HBTA/TOPO paper.
3. Run the Rezaee 2026 DES/TOPO regression and phase-equilibrium smoke test to prove package-level parameter and LLE plumbing.
4. Search for and retrieve the original DBM/TOPO unconventional oil and gas field brine paper cited by Chen 2025.
5. Build the source-composition CSV, processed process-summary table, and evidence markdown.
6. Rewrite `pcsaft-pse` to `epcsaft-pse`.
7. Implement the first reduced ePC-SAFT reactive extraction smoke test.
8. Generate a first surrogate dataset.
9. Update the PrOMMiS MSContactor demonstration to consume `epcsaft_pse`.
10. Update the deck/spec to the non-ionic story.
11. Run validation and produce the final case-study artifacts.

## Decision Defaults

- Default extraction case: HBTA/TOPO actual oil and gas field water.
- Default siting case: Smackover unless a better U.S. produced-water source emerges from source-specific composition screening.
- Default package manager: `uv`.
- Default Python version: 3.12.
- Default bridge rename: hard break to `epcsaft_pse`.
- Default PrOMMiS strategy: update the existing proof-of-concept destination without changing core PrOMMiS unless blocked.
- Default IDAES strategy: consume through PrOMMiS; do not modify IDAES.
- Default citation rule: use only Zotero-verified or directly inspected sources for scholarly claims.
- Default REE rule: report missing REE as missing, not inferred.
