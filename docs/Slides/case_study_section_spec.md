# Produced-Water Case Study Section Spec

## 2026-05-08 Rezaee Pivot Note

This file started as the HBTA/TOPO case-study section spec. The current Phase 0-9 presentation basis has pivoted to the Rezaee DES/TOPO Li/Na bridge after divalent pretreatment. Treat older HBTA/TOPO language below as comparison and future-parameterization context unless it is explicitly marked as current. The current slide source is `slides/deck.qmd`; the current status handoff is `docs/plans/lithium_project_status_handoff_2026_05_08.md`; the current bridge report is `data/reference/produced_water/rezaee_li_na_distribution_bridge_report.md`.

## Scope And Intent

- Target replacement scope: current deck case-study region around slides 15 to 19 in `docs/Slides/Lithium Extraction with ePC-SAFT.pptx`.
- Deliverable type: slide-by-slide markdown handoff for later deck authoring, not a finished `.pptx`.
- Section objective: replace the current generic LLE example and repeated stage-2 lithium/sodium slides with a produced-water-first story that shows:
  1. basin chemistry varies enough that screening matters;
  2. ionic-liquid extraction is explicitly out of scope for the active benchmark;
  3. the earlier placeholder workflow did not preserve lithium-selective behavior well enough to be the hero case;
  4. the current ePC-SAFT-supported Rezaee DES/TOPO Li/Na bridge can support a source-backed process-design handoff while direct published-constant closure remains diagnostic.
- Non-negotiable narrative boundary for this deck:
  - Active benchmark chemistry is Rezaee DES/TOPO Li/Na extraction after divalent pretreatment.
  - HBTA/TOPO + conventional diluent/synergist context remains comparison and future parameterization only.
  - Ionic-liquid systems stay in background only.
- Source priority used for this draft:
  1. Zotero local API at `http://localhost:23119/api/` if available in the execution environment.
  2. Fallback to browsed primary literature and USGS sources.
- Zotero status for this revision: the Zotero MCP is reachable in the 2026-05-07 continuation and was used to verify the Organic Solvents collection plus full-text evidence for Shan/Gando 2025, Zhang 2017, and Zhang 2018. The local Zotero HTTP API at `http://localhost:23119/api/` remains a working fallback.

## Source Legend

- `repo-derived`: quantitative value taken from local repo outputs, scripts, or project memory.
- `external-source`: quantitative value taken from a cited paper, report, or public data release.
- `zotero-local`: article discovered and summarized from the local Zotero library via `http://localhost:23119/api/`, then cited by DOI or publisher URL.
- `to-be-generated`: visual or table still needs to be built before slide authoring.
- `to-confirm`: drafting placeholder that should be replaced with a database-backed percentile or basin summary before final slide build.

## Generated Evidence Pack

Anchor every numeric deck claim to local generated artifacts so the case study is reproducible and auditable:

| Artifact | Type | Deck purpose |
|---|---|---|
| `data/reference/produced_water/non_ionic_case_study_sources.md` | Markdown | Literature anchor provenance and exclusion notes |
| `data/reference/produced_water/non_ionic_case_study_composition.csv` | CSV | Source-composition basis for Shan 2025 selectivity and process cases |
| `data/reference/produced_water/non_ionic_case_study_process_summary.csv` | CSV | Extraction-stage percentages and purity outcomes |
| `data/reference/produced_water/non_ionic_case_study_transfer_matrix.md` | Markdown | Slide-ready transfer-variable narrative (with staged \(D\)/selectivity summary) |
| `data/reference/produced_water/non_ionic_case_study_transfer_matrix.csv` | CSV | Copy-safe CSV values for stage and one-stage KPI slides |
| `data/reference/produced_water/smackover_usgs_clean_observation_summary.csv` | CSV | Clean local USGS Smackover observation summary after duplicate/blank filtering |
| `data/reference/produced_water/smackover_li_tds_sensitivity_basis.csv` | CSV | Actual low/base/high rows and slide-friendly Li/TDS sensitivity rows |
| `data/reference/produced_water/smackover_critical_minerals_ree_status.csv` | CSV | Trace-metal and REE reporting status for the local Smackover source set |
| `data/reference/produced_water/smackover_selected_base_feed_ms2.csv` | CSV | Selected Phase 9 base Smackover produced-water feed row |
| `data/reference/produced_water/smackover_phase9_case_basis.md` | Markdown | Source-vs-chemistry boundary for the final skeleton |
| `data/reference/produced_water/rezaee_li_na_distribution_bridge_report.md` | Markdown | Current Rezaee source-regressed Li/Na bridge status |
| `data/reference/produced_water/rezaee_li_na_distribution_coefficients.csv` | CSV | Rezaee source-regressed Li/Na distribution coefficients |
| `data/reference/produced_water/rezaee_prommis_idaes_transfer_handoff.csv` | CSV | Current PrOMMiS/IDAES transfer-variable handoff |
| `data/reference/produced_water/rezaee_idaes_costing_input.csv` | CSV | Current Rezaee costing-input scaffold |
| `data/reference/produced_water/phase9_costing_skeleton.csv` | CSV | Early costing-hook skeleton retained for provenance |
| `data/reference/produced_water/smackover_ms2_transfer_sensitivity.csv` | CSV | MS-2 transfer-variable sensitivity rows from the source-regressed Li/Na stage model |
| `data/reference/produced_water/hbta_topo_reactive_stage_results.csv` | CSV | Source-regressed HBTA/TOPO Li/Na crossflow results with ePC-SAFT aqueous activity support |
| `data/reference/produced_water/hbta_topo_reactive_prommis_stage_table.csv` | CSV | Stage-by-stage PrOMMiS/IDAES transfer-variable handoff table |
| `data/reference/produced_water/hbta_topo_reactive_fit_parameters.csv` | CSV | Fitted bridge constants and status labels |
| `data/reference/produced_water/hbta_topo_idaes_costing_input.csv` | CSV | Lithium-to-PrOMMiS formal IDAES costing input |
| PrOMMiS `hbta_topo_idaes_costing_results.csv` | CSV | Downstream IDAES/Pyomo costing scenarios with recovery cap basis |
| `data/reference/produced_water/smackover_prommis_transfer_handoff.csv` | CSV | PrOMMiS/IDAES handoff variables for the base case |
| `data/reference/produced_water/phase8_costing_scenarios_skeleton.csv` | CSV | Throughput and Li2CO3 skeleton scenarios |
| `data/reference/produced_water/prommis_stage_mass_balance_skeleton.csv` | CSV | Stage-by-stage Li/Na material-balance skeleton |
| `data/reference/produced_water/non_ionic_solvent_literature_matrix.csv` | CSV | Non-ionic solvent ranking, Zotero keys, and claim status |
| `data/reference/produced_water/solvent_candidate_scorecard_2026_05_07.csv` | CSV | Current presentation-priority solvent scorecard |
| `data/reference/produced_water/solvent_candidate_run_matrix_2026_05_07.csv` | CSV | Candidate execution status and package gaps |
| `data/reference/produced_water/solvent_candidate_literature_review_2026_05_07.md` | Markdown | Deck-facing solvent-selection synthesis |
| `data/reference/produced_water/hbta_topo_model_gap_table.csv` | CSV | Explicit ePC-SAFT parameter and reaction-constant gaps |
| `data/multiphase/gando_2025_one_stage_assets/gando_2025_one_stage_nominal.csv` | CSV | One-stage quantitative metrics |
| `data/multiphase/gando_2025_slide_assets/gando_2025_stage_summary.csv` | CSV | Stage-wise cumulative Li/Na extraction and \(S_{Li/Na}\) |
| `data/multiphase/gando_2025_one_stage_assets/gando_2025_one_stage_species_split.png` | PNG | One-stage species split figure |
| `data/multiphase/gando_2025_slide_assets/gando_2025_cumulative_extraction_wide.png` | PNG | Multi-stage cumulative performance figure |

Claims not represented in this pack should stay tagged `to-confirm`.

## Zotero-Derived Produced-Water Extraction Literature Anchors

These are the local-library papers that most directly improved this spec.

| Paper | Why it matters to the case study | Key extractable takeaway | Claim tag |
|---|---|---|---|
| Jang et al., 2017, *Lithium recovery from shale gas produced water using solvent extraction* | Baseline two-stage produced-water solvent-extraction paper already referenced by the current placeholder model | Produced water in the Marcellus area contains about `95 mg/L` lithium on average; first-stage divalent removal exceeded `94.4%`; second-stage lithium extraction reached `41.2%`; total recovered lithium was `30.8%` after lithium loss in pretreatment | `zotero-local` |
| Shan et al., 2025, *Influence Mechanism of Coexisting Ions on the Extraction Efficiency of Lithium from Oil and Gas Field Water* | Primary non-ionic benchmark for the rebuilt case study | Table 1 is a simulated coexisting-ion feed; the 15 L actual-field-water process case uses HBTA extractant, TOPO synergist, sulfonated kerosene diluent, 100% saponification, and a three-stage cross-flow result above `97%` lithium extraction after impurity removal | `zotero-local` |
| Zhang et al., 2017, *Selective extraction of lithium from alkaline brine using HBTA-TOPO synergistic extraction system* | Mechanistic anchor for the source-regressed Li/Na model | Slope analysis supports a `2 HBTA : 1 TOPO : 1 Li` extraction complex; the paper reports Li/Na separation over `2100` under its alkaline-brine process conditions | `zotero-local` |
| Zhang et al., 2018, *Recovery of lithium from alkaline brine by solvent extraction with beta-diketone* | Process support for HBTA/TOPO/kerosene | The paper selects HBTA/TOPO/kerosene, uses three extraction stages for about `95%` lithium extraction, and reports stable mixer-settler operation without third phase or emulsification | `zotero-local` |
| Gerardo and Song, 2025, *Lithium recovery from U.S. oil and gas produced waters: resource quality and siting considerations* | Best local paper for connecting chemistry to basin screening, plant location, and realistic basin-grade comparisons | Marcellus was highlighted as attractive because of lower secondary-cation burden, estimated annual output around `930 metric tons` lithium metal, and proximity to battery-manufacturing demand centers; Wolfcamp averages about `14 ppm` Li and the top water-producing Permian formations fall in the `1-30 ppm` range | `zotero-local` |
| Knapik et al., 2023, *Recovery of lithium from oilfield brines - current achievements and future perspectives* | Background review for oilfield brine context and process boundaries | Supports the produced-water opportunity framing without turning the deck into an ionic-liquid survey | `zotero-local` |
| Chen et al., 2025, *Qualitative Assessment of PC88A and HBTA Extractants in Lithium Recovery Processes Using Solvent Extraction* | Secondary ligand-class comparison for HBTA/TOPO and DBM/TOPO context | Gives a literature bridge for conventional beta-diketone / organophosphorus extraction classes without making ionic liquids the active benchmark | `zotero-local` |
| Kumar et al., 2019, *Lithium Recovery from Oil and Gas Produced Water: A Need for a Growing Energy Industry* | High-level framing paper for why produced water matters as a lithium resource | Use this as a concise motivation source, not as the main quantitative anchor | `zotero-local` |
| Liu et al., 2023, *Lithium recovery from oil and gas produced water: Opportunities, challenges, and future outlook* | Useful review for technology buckets and the hybrid-process framing | Supports the idea that pretreatment plus enrichment/separation plus recovery is the right conceptual process chain | `zotero-local` |

Ionic-liquid papers such as Zante 2020 and Wang 2024 remain background citations only. They are excluded from the active benchmark set for this case study.

## Recommended Flagship Basin

- Proposed flagship basin for the rebuilt case-study story: `southern Arkansas Smackover`.
- Why this is the strongest first detailed case:
  - Lithium grade is premium by U.S. produced-water standards: observed Smackover lithium spans roughly `1-477 mg/L`, many wells exceed `100 mg/L`, and USGS notes southern-Arkansas observations above `400 mg/L`. `external-source`
  - The brine is chemically hard enough to justify a real thermodynamic model: in the USGS 2022 southern-Arkansas Smackover observations file, clean Smackover samples span `156,000-340,000 mg/L` TDS with a median of `305,000 mg/L`. `external-source`
  - Smackover and Marcellus have the most favorable major-metals-to-Li and divalent-to-Li ratios among the key U.S. O&G plays evaluated by Gerardo and Song, whereas Bakken and Wolfcamp are markedly less amenable for downstream separations. `zotero-local`
  - Southern Arkansas already has commercial brine-handling and bromine-processing infrastructure, so the case study can plausibly connect chemistry to existing field operations rather than to a greenfield hypothetical. `external-source`
- Recommended presenter line:
  - `Smackover is the right flagship basin because it is attractive enough to matter, saline enough to be genuinely hard, and already industrial enough that process integration is credible.`
- Required caution:
  - The current repo showcase result is still a selective Li/Na extraction demonstration, not a fully site-calibrated Arkansas flowsheet.
  - The Shan 2025 benchmark is a process-evidence anchor for actual field water, but not a Smackover composition source.
  - The new local source table gives Smackover feed chemistry and Li/TDS sensitivity rows, but it still does not supply HBTA/TOPO extraction data for those exact rows.
  - The non-ionic benchmark chemistry should be presented as HBTA/TOPO actual oil and gas field water.
  - D2EHDTPA/BuPhen can stay in the background as the strongest non-HBTA backup chemistry, but it should not displace the HBTA/TOPO benchmark. DBM/TOPO is currently only an unresolved historical search target.

## Full Case Study Thesis

The finished presentation should make one argument in four connected steps:

1. `Where`: produced-water lithium extraction is not one generic feed problem; the best first flagship location is southern Arkansas Smackover because the brine is high-value, high-salinity, and already tied to brine-handling infrastructure.
2. `Why`: that combination is exactly where a simple fixed recovery factor or low-order surrogate is weakest, because lithium value, salt load, divalent burden, solvent chemistry, and O/A ratio all change the separation result.
3. `How`: ePC-SAFT provides the thermodynamic backbone for calculating the phase split, phase compositions, activity/fugacity-driven equilibrium behavior, and distribution variables that a solvent-extraction process model needs.
4. `What for`: PrOMMiS/IDAES needs this backbone so solvent-extraction unit models can be driven by physically meaningful equilibrium variables, trust-region surrogates, or external-function blocks instead of unsupported case-specific placeholders.

Recommended core message for broad audiences:

`The novelty is not just that Smackover has lithium. The novelty is that ePC-SAFT can turn a messy produced-water basin into a computable process-design case: which feed is worth targeting, how the aqueous/organic split responds to chemistry, and what equilibrium-derived transfer variables should enter the PrOMMiS and IDAES solvent-extraction models.`

## Evidence Backbone Required For A Full Presentation

The current spec is strong enough to support the story, but the full case study should be presented as an evidence ladder rather than a single result slide.

| Evidence layer | What it must show | Why it matters for the sales case | Current status |
|---|---|---|---|
| Basin screen | Smackover has a premium Li signal, very high TDS, and industrial brine context | Establishes that the selected location is not arbitrary | Mostly ready from USGS and literature citations |
| Chemistry difficulty | The feed is hypersaline and contains competing ions / produced-water complexity | Shows why a physics-based electrolyte model is needed | Ready conceptually; final slide needs a clean sensitivity matrix |
| Prior limitation | The old Jang-style placeholder did not preserve a convincing Li-over-Na split | Shows the failure mode of weak placeholders | Ready from repo outputs and project memory |
| ePC-SAFT role | The model computes equilibrium/phase split behavior and supports structured sensitivity over TDS, O/A, solvent, and ion burden | Makes ePC-SAFT the backbone, not a decorative model mention | Needs a dedicated explanatory slide |
| Selective extraction result | The current source-regressed Li/Na HBTA/TOPO stage model moves Li while keeping Na low | Gives a quantitative proof point that the workflow can support a better case | Ready from reactive-stage and PrOMMiS handoff artifacts |
| Process-model bridge | Map equilibrium outputs into PrOMMiS/IDAES variables: phase compositions, phase fractions, distribution ratios, selectivity, raffinate/extract compositions, and validity bounds | Makes the implementation ask concrete | Needs a new slide and handoff table |
| Integration ask | ePC-SAFT should enter PrOMMiS/IDAES as a property/equilibrium service, surrogate source, or external-function block | Turns the technical result into a clear software roadmap | Needs a closing slide |

## ePC-SAFT Role In The Solvent-Extraction Model

The deck should be precise about what ePC-SAFT contributes and what remains in the unit model.

ePC-SAFT should be framed as computing or supporting:

- phase stability and number of liquid phases for aqueous/organic/electrolyte systems;
- equilibrium phase compositions for water, organic solvent/extractant, lithium, sodium, chloride, and future competing ions;
- phase fractions or organic/aqueous split quantities that become stage material-balance inputs;
- activity/fugacity-coefficient behavior behind the equilibrium split;
- distribution ratios such as \(D_{Li}\) and \(D_{Na}\);
- selectivity metrics such as \(S_{Li/Na}\);
- raffinate and extract compositions after a stage or staged chain;
- sensitivity surfaces over TDS, O/A ratio, extractant concentration, and feed composition;
- trust-region boundaries showing where a surrogate should or should not be trusted.

ePC-SAFT should not be oversold as directly supplying:

- mass-transfer coefficients;
- interfacial area;
- residence time;
- mixer-settler hydraulics;
- solvent degradation;
- plant cost.

Those remain PrOMMiS/IDAES unit-model, costing, or calibration responsibilities. The pitch is stronger if the boundary is explicit: ePC-SAFT supplies the thermodynamic equilibrium and distribution layer, while PrOMMiS/IDAES supplies the process flowsheet, unit-model equations, optimization, costing hooks, and deployment environment.

## PrOMMiS / IDAES Transfer-Variable Handoff

The full case study should include one slide that directly maps ePC-SAFT outputs to process-model variables.

| Process-model need | ePC-SAFT-derived quantity | How it would be used in PrOMMiS / IDAES |
|---|---|---|
| Feed characterization | \(z_i\), TDS, Li/Na/Mg/Ca/Sr/Ba/Cl basis, temperature | Defines the inlet state for a basin-specific solvent extraction train |
| Phase split | aqueous and organic phase compositions, phase fraction | Provides equilibrium targets or closure equations for a stage model |
| Transfer strength | \(D_i = C_{i,org}/C_{i,aq}\) for Li, Na, and future competing ions | Supplies distribution behavior for solvent-extraction balances |
| Selectivity | \(S_{Li/Na}\), and later \(S_{Li/Mg}\), \(S_{Li/Ca}\) | Supports separation-performance constraints and solvent screening |
| Stage outlet estimates | raffinate composition, loaded organic composition, cumulative extraction | Initializes or validates multi-stage unit models |
| Sensitivity surface | response to O/A, TDS, extractant concentration, and feed chemistry | Feeds ALAMO or another surrogate generator inside a trust region |
| Validity diagnostics | convergence status, phase-distance checks, residuals, bounds | Prevents an optimizer from treating failed or collapsed equilibrium points as real process data |

Recommended presenter line:

`PrOMMiS and IDAES do not just need a lithium recovery number. They need a defensible map from produced-water chemistry to stage transfer variables. ePC-SAFT is the candidate engine for that map.`

The intended bridge story is:

- non-ionic field-water chemistry in;
- equilibrium and selectivity variables out;
- PrOMMiS stage models and IDAES costing in.

## Novel Insight To Emphasize

The case study should not claim novelty from a single high recovery number. The stronger novelty claim is:

- `Location selection becomes thermodynamic`: Smackover is attractive not only because of lithium grade, but because its combination of high Li, high salinity, favorable basin context, and process infrastructure creates a high-value test of electrolyte thermodynamics.
- `The model explains why one feed is harder than another`: TDS, competing ions, organics, O/A ratio, and solvent chemistry are variables in the thermodynamic/process story, not nuisance caveats.
- `The workflow separates physics from staged-regression limits`: ePC-SAFT handles the electrolyte activity/equilibrium backbone; the source-regressed Li/Na stage model captures chemistry-specific selectivity after divalent pretreatment until full organic-phase HBTA/TOPO LLE parameters are available.
- `The process model gets reusable variables`: the output is not just a plot; it is a pathway to distribution coefficients, phase compositions, selectivity, and validity bounds for PrOMMiS/IDAES.

Use this wording for the strongest claim:

`ePC-SAFT makes the case study reusable. Without it, the deck can only say a solvent worked for one brine. With it, the project can ask where that solvent system should work, why it should change across basins, and how those equilibrium results become process-model transfer variables.`

## Main Arc

### Slide 1

- Title: `Produced Water Is Not One Feed`
- Purpose: open the case study with the basin-variability argument so the audience immediately sees why a single fixed feed is not a credible produced-water story.
- Visual concept:
  - U.S. map with four highlighted basins: Appalachian, Permian, Williston, and Smackover.
  - Right-side comparison table with lithium and TDS bands.
  - Bottom callout: `same separation train will not behave the same across these feeds`.
- Exact quantitative claims:

| Basin | Representative lithium signal | Representative TDS signal | Separation implication | Claim tag | Source |
|---|---:|---:|---|---|---|
| Appalachian (Marcellus/Utica) | Marcellus NE PA median Li = 205 mg/L; SW PA median Li = 127 mg/L | Marcellus produced water TDS exceeds 100,000 mg/L | High Li is attractive, but Mg/Li and brine strength vary enough within-basin to change pretreatment and extraction difficulty | `external-source` | Mackey et al., 2024, Sci. Rep. [https://www.nature.com/articles/s41598-024-58887-x](https://www.nature.com/articles/s41598-024-58887-x); USGS Appalachian isotopes paper [https://pubs.usgs.gov/publication/70255920](https://pubs.usgs.gov/publication/70255920) |
| Permian (Delaware/Wolfcamp emphasis) | Wolfcamp average Li `~14 ppm`; top water-producing Permian formations range `1-30 ppm` Li | Wolfcamp TDS spans `<25 g/L` in basin-center waters to `100-140 g/L` toward margins | Large water volume does not imply high-grade lithium; this is a low-grade, screening-heavy basin where chemistry quality matters as much as throughput | `zotero-local` for Li, `external-source` for TDS | Gerardo and Song, 2025, Environ. Sci.: Water Res. Technol. [https://doi.org/10.1039/D4EW00422A](https://doi.org/10.1039/D4EW00422A); Nicot et al., 2020, Appl. Geochem. [https://doi.org/10.1016/j.apgeochem.2020.104771](https://doi.org/10.1016/j.apgeochem.2020.104771) |
| Williston (Bakken / deeper basin brines) | Historically `>100 mg/L`; Duperow/Birdbear brines reported up to `~200 mg/L` | Bakken/Three Forks brines average `308 g/L` TDS | Very high salinity increases pretreatment burden even when lithium is economically interesting | `external-source` | Peterman et al., 2017 [https://pubs.usgs.gov/publication/70190270](https://pubs.usgs.gov/publication/70190270); USGS Mendenhall listing [https://www.usgs.gov/index.php/centers/mendenhall-research-fellowship-program/23-04-evaluation-oilfield-brine-lithium-commodity](https://www.usgs.gov/index.php/centers/mendenhall-research-fellowship-program/23-04-evaluation-oilfield-brine-lithium-commodity) |
| Smackover (southern Arkansas) | Observed Li spans approximately `1-477 mg/L`; many wells exceed `100 mg/L`; predicted hotspots reach `399 mg/L`; USGS summary notes `>400 mg/L` observed in southern Arkansas | USGS 2022 southern-Arkansas Smackover samples span `156,000-340,000 mg/L` TDS with a clean-sample median of `305,000 mg/L`; the basin is also the core of Arkansas's bromine-brine industry | Strongest domestic premium-feed contrast in this set: high Li, very high salinity, existing brine infrastructure, and more favorable metals-to-Li ratios than Bakken/Wolfcamp | `external-source` | Knierim et al., 2024 USGS fact sheet [https://doi.org/10.3133/fs20243052](https://doi.org/10.3133/fs20243052); Knierim et al., 2024 Science Advances summary [https://www.usgs.gov/publications/evaluation-lithium-resource-smackover-formation-brines-southern-arkansas-using-machine](https://www.usgs.gov/publications/evaluation-lithium-resource-smackover-formation-brines-southern-arkansas-using-machine); USGS data release [https://doi.org/10.5066/P9QPRYZN](https://doi.org/10.5066/P9QPRYZN) using `southAR_brines_2022.txt` Smackover rows with duplicate/blank rows removed; Gerardo and Song, 2025 [https://doi.org/10.1039/D4EW00422A](https://doi.org/10.1039/D4EW00422A); Arkansas bromine-brine geology page [https://www.geology.ar.gov/energy/brine-in-arkansas.html](https://www.geology.ar.gov/energy/brine-in-arkansas.html) |

- Speaker points:
  - Produced water is not a single “representative brine”; both lithium value and impurity burden move by basin and even within basin.
  - Appalachian brines make the high-lithium case obvious, but they are still hypersaline and chemically heterogeneous.
  - Permian water is compelling because of scale and infrastructure, not because it is always the richest lithium feed.
  - Williston and Smackover show opposite extremes: very high salinity versus very high lithium.
  - This is why the case study should start with screening logic, not with a single fixed feed and one equilibrium result.
- Asset sources:
  - Basin map: `to-be-generated` from public basin outlines plus source-cited labels.
  - Comparison table: `to-be-generated`.
- Build note:
  - The last major basin placeholder is now closed. If time permits, refine the Smackover row from the current 2022 observed-sample summary to a broader formation-wide percentile from the USGS Produced Waters Database plus the USGS southern-Arkansas observations release.

### Slide 2

- Title: `What A Real Produced-Water Case Study Must Vary`
- Purpose: make the sensitivity frame explicit and separate chemistry variables from site-integration variables.
- Visual concept:
  - Two-lane funnel or matrix.
  - Lane 1: thermodynamic inputs.
  - Lane 2: project-location / process-integration inputs.
  - Output box: `screened case -> detailed chemistry -> process model`.
- Exact quantitative claims:
  - No new hard numbers are required on this slide beyond the basin variability established on Slide 1.
  - Use named sensitivity axes instead of invented ranges unless the ranges are later generated from a formal design-of-experiments table.
  - Add a literature-informed mini-table or callout row to prove these sensitivities are not hypothetical.
- Required sensitivity axes:

| Axis | Category | Why it belongs in the case study | Claim tag | Source |
|---|---|---|---|---|
| Li concentration | Thermodynamic | Directly drives whether the basin is concentration-limited or volume-limited | `external-source` | Basin literature on Slide 1 |
| TDS / NaCl load | Thermodynamic | Changes ionic strength, phase behavior, pretreatment load, and likely surrogate regime boundaries | `external-source` | Basin literature on Slide 1 |
| Competing ions | Thermodynamic | Mg, Ca, Sr, Ba, and Na change selectivity requirements and pretreatment sequence | `external-source` | Jang 2017 and basin-specific water chemistry literature |
| Solvent / extractant system | Process chemistry | Determines whether lithium-selective behavior is even plausible | `repo-derived` plus `external-source` | Gando and Jang workflows; repo scripts |
| O/A ratio | Operating variable | Directly affects stage transfer and is already exposed in repo-generated sweep assets | `repo-derived` | `data/multiphase/gando_2025_one_stage_assets/gando_2025_one_stage_assets.md` |
| Plant location / logistics | Deployment variable | Basin infrastructure, water handling, and pretreatment economics affect whether a chemistry win matters commercially | `external-source` | Basin setting and current produced-water management context |

- Case-selection conclusion to place on the slide:

| Screening conclusion | Why it follows from the literature | Claim tag | Source |
|---|---|---|---|
| `Use Smackover as the flagship premium-brine case.` | Smackover combines high lithium concentrations, very high salinity, lower major-metals-to-Li ratios than Bakken/Wolfcamp, and existing brine-processing infrastructure in southern Arkansas | `external-source` plus `zotero-local` | USGS Smackover publications and data release; Gerardo and Song, 2025; Arkansas bromine page |
| `Use Marcellus/Appalachian as the follow-on comparison case.` | Marcellus is attractive on lower secondary-cation burden and end-use geography, so it is the best contrast case once the premium-brine story is established | `zotero-local` | Gerardo and Song, 2025 |

- Recommended presenter framing for this slide:
  - `Smackover wins the first-case screen not because it is easy, but because it is both valuable and thermodynamically unforgiving. That combination is exactly where a physically grounded electrolyte EoS is worth the trouble.`

- Optional literature callout table for this slide:

| Literature anchor | Experimental lesson for the slide | Exact claim | Claim tag |
|---|---|---|---|
| Gerardo and Song, 2025 | Basin-scale lithium grade and siting both belong in the screening story | Wolfcamp averages about `14 ppm` Li and the main Permian water-producing formations fall in the `1-30 ppm` range; Marcellus was favored partly because of lower secondary-cation burden and geography | `zotero-local` |
| Jang et al., 2017 | Divalent-ion pretreatment belongs in the screening story | First-stage divalent removal exceeded `94.4%`; second-stage lithium extraction reached `41.2%`; total recovered lithium was `30.8%` after pretreatment loss | `zotero-local` |
| Lee and Chung, 2020 | Organics should be treated as a sensitivity axis, not ignored | Increasing alkane chain length and increasing `n`-hexane concentration both reduced final lithium recovery | `zotero-local` |
| Shan et al., 2025 | Conventional ligand chemistry can still be highly selective in actual field water | Table 1 is a simulated coexisting-ion feed, while the actual 15 L field-water process case reached above `97%` lithium extraction after impurity removal with HBTA/TOPO | `zotero-local` |
| Chen et al., 2025 | HBTA and DBM class chemistry give the conventional-ligand comparison frame | Use this as the secondary ligand-class bridge when explaining why the active benchmark is non-ionic rather than ionic-liquid-based | `zotero-local` |

- Speaker points:
  - The case study needs to show more than a single composition and one operating point.
  - Chemistry variables set the feasible separation regime; location variables determine whether that regime is worth deploying.
  - This framing also sets up why ALAMO and trust-region workflows matter later: not every part of the space deserves equal sampling density.
  - In the current project, O/A and salt effects are already visible in repo-generated one-stage assets.
  - The produced-water extraction literature makes the same point from another direction: divalents, organics, extractant choice, and siting all change the outcome materially.
- Asset sources:
  - Sensitivity matrix graphic: `to-be-generated`.
  - Optional small anchor plot from repo one-stage sweeps: `data/multiphase/gando_2025_one_stage_assets/gando_2025_one_stage_extraction_vs_salt.png` and `..._distribution_vs_oa.png`.

### Slide 3

- Title: `What We Could Not Do Before`
- Purpose: explicitly demote the old Jang-style placeholder case from showcase result to limitation slide.
- Visual concept:
  - Left: small chart of the old crossflow trend.
  - Right: three red limitation callouts.
  - Footer banner: `useful as a debugging scaffold, not as the flagship case study`.
- Exact quantitative claims:
  - Ten-contact crossflow placeholder case reaches only `39.96%` cumulative lithium extraction while sodium still reaches `38.05%` cumulative extraction. `repo-derived`
  - TBP and D2EHPA are modeled as fixed surrogates / placeholders rather than fitted, chemistry-faithful species. `repo-derived`
  - In the literature, stronger performance typically comes only after explicit pretreatment and chemistry-specific extractants, which the placeholder model does not represent faithfully. `zotero-local`
- Repo evidence:
  - Limitation summary recorded in `docs/.codex-journal/project_memory.md` under `2026-03-17 LLE Script Triage`.
  - Placeholder implementation at `scripts/lle/jang_2017_stage2_li_na_tbp_d2ehpa.py`.
- Speaker points:
  - The old example was useful for wiring the workflow and exercising the multiphase solver.
  - It did not preserve a convincing lithium-over-sodium separation advantage.
  - It relied on fixed surrogate assumptions, so it could not carry the “look what the package enables now” message.
  - This is the correct place to be candid: the old case is the baseline we outgrew.
  - The literature does not say lithium extraction is easy; it says the difficult parts are pretreatment, competing ions, organics, and extractant chemistry, which is exactly what the placeholder case compresses away.
- Asset sources:
  - Existing placeholder chart can be regenerated from `scripts/lle/jang_2017_stage2_li_na_tbp_d2ehpa.py` if needed. `to-be-generated`
  - If regeneration is not worth it, this slide can use a text-only comparison table.
  - Optional side table comparing placeholder behavior against literature anchors from Jang 2017, Shan 2025, and Chen 2025.

### Slide 4

- Title: `What We Can Do Now: One-Stage Reactive Produced-Water Split`
- Purpose: show the first credible lithium-selective result supported by the current source-regressed Li/Na workflow.
- Visual concept:
  - Main visual: species split chart plus small KPI table.
  - Supporting annotation: simple process cartoon showing `ePC-SAFT aqueous activity support + fitted HBTA/TOPO reactive-stage bridge`.
- Exact quantitative claims:
  - Selected MS-2 one-stage Li extraction at `O/A = 1` = `47.2846%`. `repo-derived`
  - Selected MS-2 one-stage Na extraction at `O/A = 1` = `0.0131%`. `repo-derived`
  - \(D_{Li} = 0.8970\). `repo-derived`
  - \(S_{Li/Na} = 6840.1071\). `repo-derived`
  - Raffinate after one stage: Li = `88.5619 mg/L`, Na = `64091.5953 mg/L`. `repo-derived`
  - Activity source label = `epcsaft_from_local_runtime_params`. `repo-derived`
  - This should be framed as a source-regressed Li/Na stage-model result, not a direct Smackover-well HBTA/TOPO experiment. `repo-derived`
- Repo evidence:
  - `data/reference/produced_water/hbta_topo_reactive_stage_results.csv`
  - `data/reference/produced_water/hbta_topo_reactive_prommis_stage_table.csv`
  - `data/reference/produced_water/hbta_topo_reactive_model_report.md`
- Required bridge statement for the deck:
  - Present this as the current `source-regressed Li/Na stage engine` for a source-backed Smackover feed, not as a claim that the Arkansas wells already have measured HBTA/TOPO extraction data.
  - The story should be: basin screening identifies Smackover as the premium target, and the current ePC-SAFT plus fitted HBTA/TOPO bridge is the first model in this project that is strong enough to generate process variables for that kind of brine without collapsing back to a nonselective placeholder.
- Speaker points:
  - This is the first point in the talk where the audience should feel a real step change versus the placeholder case.
  - The result is selective: lithium moves materially, sodium barely moves.
  - The chemistry is not claimed to arise from the bare flash alone; the fitted reaction stoichiometry and activity-informed transfer law are the point.
  - That makes this a better bridge to external-function or surrogate deployment because the selective chemistry is isolated, inspectable, and labeled by trust region.
  - A small benchmark inset can show that the literature also needs chemistry-specific tuning: Jang 2017 reached `41.2%` second-stage lithium extraction after pretreatment, Shan 2025 reached above `97%` after impurity removal with HBTA/TOPO in actual field water, and Chen 2025 keeps the HBTA/DBM conventional-ligand comparison frame visible.
- Asset sources:
  - Reactive-stage tables listed above.
  - Optional callout box summarizing fit basis from `data/reference/extraction_models/gando_2025/hbta_topo_reactive_fit.json`.
  - Optional benchmark inset: `to-be-generated` from Zotero-derived literature anchors.

### Slide 5

- Title: `What We Can Do Now: Multi-Stage Performance`
- Purpose: extend the one-stage selective story into a process-relevant multi-stage result.
- Visual concept:
  - Cumulative extraction line plot across stages.
  - Small stage summary table.
  - Right-side callout: `this is the “could not do before” slide`.
- Exact quantitative claims:
  - Stage 1 cumulative Li extraction = `47.2846%`. `repo-derived`
  - Stage 2 cumulative Li extraction = `89.5753%`. `repo-derived`
  - Stage 3 model cumulative Li extraction = `99.99999%`, labeled `outside_literature_capacity_envelope_near_total_transfer`. `repo-derived`
  - Stage 3 cumulative Na extraction = `0.1160%`. `repo-derived`
  - Stage 1 \(D_{Li} = 0.8970\). `repo-derived`
  - Stage 1 \(S_{Li/Na} = 6840.1071\). `repo-derived`
  - Formal costing uses the source-backed `97.17%` recovery cap instead of the near-total extrapolated model recovery. `repo-derived`
  - Paper comparison for cumulative Li extraction: Stage 1 `54.95%`, Stage 2 `85.60%`, Stage 3 `97.17%`. `repo-derived` from local summary of paper comparison
- Repo evidence:
  - `data/reference/produced_water/hbta_topo_reactive_stage_results.csv`
  - `data/reference/produced_water/hbta_topo_reactive_prommis_stage_table.csv`
  - `data/reference/produced_water/hbta_topo_formal_costing_results.csv`
- Speaker points:
  - The new workflow is not just a nicer one-stage spot result; it carries through a staged separation train.
  - By stage 3, lithium recovery is near complete while sodium remains low.
  - This is the clearest answer to `highlight what can be done now that we could not do before`.
  - If time is tight, this should be the single quantitative hero slide in the case-study section.
  - The produced-water literature mostly reports one- or two-stage experimental demonstrations; showing a clean staged selective progression is one of the strongest differentiators of the current project workflow.
- Asset sources:
  - Reactive-stage CSVs and generated Quarto tables.

### Slide 6

- Title: `Why This Matters For Process Design`
- Purpose: connect the chemistry case study to optimization, surrogates, and process integration.
- Visual concept:
  - Four-box workflow:
    1. basin screening,
    2. detailed chemistry model,
    3. trust-region sampling + ALAMO surrogate,
    4. PrOMMiS / IDAES stage or external-function deployment.
  - Small callout at bottom: `case study becomes reusable infrastructure, not just one plot`.
- Exact quantitative claims:
  - Current integration path already exists conceptually through `pcsaft-pse` into PrOMMiS. `repo-derived`
  - Slide should not invent surrogate fit metrics until they are actually generated.
- Required messaging:
  - The detailed chemistry model defines the trustworthy region.
  - Trust-region logic prevents the surrogate from being trained blindly in irrelevant or unstable regions.
  - ALAMO is the next surrogate upgrade to test rather than defaulting to low-order polynomials.
  - The source-regressed Li/Na stage model makes it natural to expose the model either as:
    - an algebraic surrogate inside PrOMMiS, or
    - an external-function-style block similar in spirit to the IAPWS integration pattern.
  - Do not say `best EoS available` unless a benchmark slide is added. Safer wording:
    - `the most capable model currently available in this project for mixed aqueous-organic-electrolyte extraction and multiphase equilibrium`
    - `the right thermodynamic backbone for a Smackover-like produced-water case because it can carry hypersaline brine chemistry, selective aqueous-organic partitioning, and later hydrocarbon/organic extensions on one framework`

- Why ePC-SAFT is the right backbone for this case:

| Modeling need in the Smackover case | Why ePC-SAFT + source-regressed Li/Na stage model fits | Why weaker alternatives are not enough for this project story |
|---|---|---|
| `Very high TDS electrolyte brine` | ePC-SAFT gives a physically structured thermodynamic basis for hypersaline electrolyte brines instead of treating salinity as a nuisance correction | A low-order polynomial surrogate or a fixed placeholder fit cannot be trusted outside its calibration window and does not explain why basin chemistry changes the split |
| `Aqueous-organic Li-selective extraction` | The current project already couples ePC-SAFT aqueous activity behavior to a fitted HBTA/TOPO reactive-stage law, which is exactly the architecture needed when bare equilibrium is not the whole story | The old Jang-style placeholder compressed chemistry into fixed factors and lost convincing Li-over-Na selectivity |
| `Potential organics / hydrocarbon carryover and follow-on VLE` | The same backbone can support mixed aqueous-organic-electrolyte and hydrocarbon cases, which keeps the workflow coherent as the case study expands | Simpler activity-coefficient placeholders tend to become regime-specific and fragment the story into disconnected models |
| `Process embedding and trust-region surrogates` | A mechanistic thermodynamic backbone is a better source model for ALAMO or external-function deployment because the surrogate can be trained around a physically meaningful region | Surrogating a weak placeholder just produces a faster weak placeholder |
- Speaker points:
  - The value of the case study is not only the separation number; it is the workflow it enables.
  - Once the case is framed by basin chemistry, the trust-region and surrogate story becomes much more credible.
  - This is where the audience should understand why a selective case matters for optimization and design, not just for validation.
  - Keep the wording conservative: the project has a clear integration path, but not yet a final ALAMO benchmark or production-grade external function.
- Asset sources:
  - New workflow diagram: `to-be-generated`.
  - Supporting context already present in current deck slide 19 and local project memory.

### Slide 7

- Title: `From Equilibrium To Transfer Variables`
- Purpose: explicitly connect the ePC-SAFT calculation to the variables PrOMMiS/IDAES solvent-extraction unit models need.
- Visual concept:
  - Left: ePC-SAFT box with inputs and equilibrium solve.
  - Middle: transfer-variable table.
  - Right: PrOMMiS/IDAES stage model box.
- Required variables to show:

| ePC-SAFT / reactive-stage bridge output | Process meaning | Presentation use |
|---|---|---|
| aqueous phase composition | raffinate equilibrium state | shows what remains after extraction |
| organic phase composition | loaded solvent equilibrium state | shows what the solvent carries forward |
| phase fraction / O:A relation | stage split basis | connects thermodynamics to material balance |
| \(D_{Li}\), \(D_{Na}\) | transfer strength | quantifies selectivity beyond percent extraction |
| \(S_{Li/Na}\) | lithium-over-sodium selectivity | proves the case is not just generic salt movement |
| convergence / validity diagnostics | trust-region flag | prevents bad equilibrium points from entering a surrogate |

- Speaker points:
  - Percent extraction is only the presentation-friendly output.
  - The process-model interface needs the underlying phase compositions and distribution behavior.
  - This is where the ePC-SAFT integration becomes concrete: it can provide equilibrium-derived transfer variables to a PrOMMiS/IDAES solvent-extraction block.

### Slide 8

- Title: `Why This Belongs In PrOMMiS / IDAES`
- Purpose: make the software ecosystem ask explicit.
- Visual concept:
  - Three deployment options shown as a maturity ladder:
    1. offline ePC-SAFT data generator;
    2. ALAMO / trust-region surrogate;
    3. direct external-function or property-package integration.
- Required messaging:
  - Start with an offline data-generation workflow because it is the lowest-risk route.
  - Use ALAMO/trust-region surrogates for optimization when direct ePC-SAFT calls are too slow or brittle.
  - Keep a direct external-function/property route as the long-term target for high-fidelity studies.
  - The integration should carry diagnostics, not only numbers.
- Speaker points:
  - PrOMMiS/IDAES already gives the process-modeling home; what is missing is a credible electrolyte LLE thermodynamic engine for produced-water solvent extraction.
  - A fixed placeholder recovery factor cannot support basin screening, solvent screening, or extrapolation.
  - ePC-SAFT integration lets the same case move from literature validation to flowsheet optimization.

### Slide 9

- Title: `What Still Needs To Be Finished`
- Purpose: be transparent about remaining work before presenting this as a complete case study.
- Visual concept:
  - checklist grouped by `must have`, `should have`, and `future upgrade`.
- Must-have items:
  - finalize the Smackover feed basis from a source-cited observed or percentile composition;
  - build the basin map and compact basin comparison table;
  - build the ePC-SAFT-to-PrOMMiS variable bridge diagram;
  - choose the one-stage and three-stage showcase figures for the main deck;
  - keep the disclaimer that the current showcase is Smackover-like, not a fully calibrated Arkansas-well flowsheet.
- Should-have items:
  - add one sensitivity slide over O/A and salt load from existing Gando one-stage assets;
  - add a compact literature benchmark inset;
  - add a trust-region/surrogate workflow slide;
  - render the Quarto deck and export PDF for review.
- Future upgrades:
  - calibrate a true Smackover composition;
  - add Mg/Ca/Sr/Ba competition;
  - test direct PrOMMiS/IDAES coupling through `pcsaft-pse`;
  - build an ALAMO surrogate and compare against direct ePC-SAFT calls.

## Backup Slides

### Backup A

- Title: `Basin Sensitivity Expansion`
- Purpose: show how the main case-study chemistry would be re-run across basin-style feeds without inventing unsupported results.
- Visual concept:
  - 2D matrix with basins on rows and sensitivity axes on columns.
  - Colored boxes indicating `screen now`, `later with new data`, `not a first-pass priority`.
- Proposed analysis grid:

| Basin style | Li basis | TDS basis | Secondary ions | Solvent / O:A knobs | Status |
|---|---|---|---|---|---|
| Appalachian-high-Li | Use Marcellus regional medians or percentiles | `>100,000 mg/L` baseline | Mg/Li split between NE and SW PA | O/A and solvent swap | `future case expansion` |
| Permian-volume-driven | Use `1-30 ppm` basin-grade range with `~14 ppm` Wolfcamp average as the default low-grade anchor | Wolfcamp low-to-high salinity window | NaCl-heavy first pass | O/A and pretreatment burden | `future case expansion` |
| Williston-high-TDS | Use `>100 to ~200 mg/L` working range | `308 g/L` average TDS basis | high Na/K/Cl | solvent robustness and pretreatment burden | `future case expansion` |
| Smackover-premium-Li | Use `100-400+ mg/L` hotspot framing | `156,000-340,000 mg/L` TDS with `305,000 mg/L` median from the current USGS 2022 southern-Arkansas observation set | bromine / high-salinity brine context | recovery/value benchmark | `future case expansion` |

- Optional literature-informed note box for this slide:
  - Jang 2017 shows the baseline placeholder problem and why pretreatment matters.
  - Lee 2020 shows organics deserve their own sensitivity row.
  - Shan 2025 shows that actual field water with conventional ligands can still be highly selective once impurity removal and chemistry are handled explicitly.

- Speaker points:
  - This slide is intentionally a roadmap, not a fake result slide.
  - The purpose is to show the next systematic screening campaign that the package makes possible.
  - This is where a trust-region design-of-experiments table would naturally live once the next model round starts.
- Asset sources:
  - Matrix graphic: `to-be-generated`.

### Backup B

- Title: `Extension Cases Enabled By This Work`
- Purpose: remind the audience that the package capability extends beyond this one produced-water LLE case.
- Visual concept:
  - Three-column collage:
    - produced-water selective LLE,
    - mixed-solvent / electrolyte multiphase equilibrium,
    - hydrocarbon VLE / organic-phase behavior.
- Exact quantitative claims:
  - Keep quantitative claims limited to already validated local examples or published validation figures already in the main deck.
  - Do not invent new extension metrics.
- Candidate extension examples:
  - Water + 1-butanol + NaCl/KCl multiphase benchmark already represented in the current deck. `repo-derived`
  - Yu 2024 reactive-wrapper reproduction for lithium extraction from magnesium-rich brine. `repo-derived`
  - Hubach 2024 / related organic-phase activity and extraction studies already used in local package validation. `repo-derived`
  - Hydrocarbon VLE and mixed aqueous-organic-electrolyte cases should be framed as `enabled by the same thermodynamic backbone`, not as a fully shown case study. `repo-derived`
- Speaker points:
  - The produced-water case is the lead example because it matches the project goal.
  - The broader point is that the same framework is not locked to one lithium-specific solvent system.
  - Keep CMM/REE discussion brief here unless a separate extension slide is later requested.
- Asset sources:
  - Collage: `to-be-generated` from existing validation figures and repo outputs.

## Build Handoff Table

| Slide | Visual needed | Source path / citation | New work required |
|---|---|---|---|
| 1 | U.S. basin map + basin table | External citations in Slide 1 | Build basin map, extract final basin percentile table, replace `to-confirm` entries |
| 2 | Sensitivity matrix / funnel | Slide 1 sources + repo sweep assets | Build clean matrix graphic; decide whether to include one mini-plot |
| 3 | Placeholder limitation chart or text table | `scripts/lle/jang_2017_stage2_li_na_tbp_d2ehpa.py`; project memory | Regenerate plot if desired; otherwise format text comparison table |
| 4 | One-stage split chart + KPI table | `data/multiphase/gando_2025_one_stage_assets/` | Mostly ready; choose best PNG pair and simplify annotations |
| 5 | Stagewise / cumulative chart + summary table | `data/multiphase/gando_2025_slide_assets/`; `data/multiphase/gando_2025_stage3_comparison.md` | Mostly ready; unify style with deck theme |
| 6 | Workflow diagram from chemistry to surrogate to PrOMMiS | Current deck integration slide + repo context | New diagram required |
| 7 | ePC-SAFT to transfer-variable bridge | This spec plus `data/multiphase/gando_2025_*` summaries | New diagram/table required |
| 8 | PrOMMiS/IDAES integration maturity ladder | This spec plus `pcsaft-pse` context from project memory | New slide required |
| 9 | Completion checklist | This spec | New slide required |
| Backup A | Basin sensitivity grid | Slide 1 sources | New grid required; no new calculations yet |
| Backup B | Capability collage | Existing validation figures and repo outputs | New collage required |

## External References Used In This Draft

1. Mackey, J., Bain, D.J., Lackey, G., Gardiner, J., Gulliver, D., and Kutchko, B., 2024, *Estimates of lithium mass yields from produced water sourced from the Devonian-aged Marcellus Shale*, Scientific Reports 14, 8813. [https://www.nature.com/articles/s41598-024-58887-x](https://www.nature.com/articles/s41598-024-58887-x)
2. McDevitt, B., Tasker, T.L., Coyte, R., Blondes, M.S., Stewart, B.W., Capo, R.C., Hakala, J.A., Vengosh, A., Burgos, W.D., and Warner, N.R., 2024, *Utica/Point Pleasant brine isotopic compositions elucidate mechanisms of lithium enrichment in the Appalachian Basin*. USGS publication page: [https://pubs.usgs.gov/publication/70255920](https://pubs.usgs.gov/publication/70255920)
3. Nicot, J.-P., Darvari, R., Eichhubl, P., Scanlon, B.R., Elliott, B.A., Bryndzia, L.T., Gale, J.F.W., and Fall, A., 2020, *Origin of low salinity, high volume produced waters in the Wolfcamp Shale (Permian), Delaware Basin, USA*, Applied Geochemistry 122, 104771. [https://doi.org/10.1016/j.apgeochem.2020.104771](https://doi.org/10.1016/j.apgeochem.2020.104771)
4. Peterman, Z.E., Thamke, J., Futa, K., and Oliver, T.A., 2017, *Characterization and origin of brines from the Bakken-Three Forks petroleum system in the Williston Basin, USA*, Mountain Geologist 54(3), 203-221. USGS page: [https://pubs.usgs.gov/publication/70190270](https://pubs.usgs.gov/publication/70190270)
5. U.S. Geological Survey, 2024, *Evaluation of oilfield brine lithium commodity resources of the Paradox and Williston basins* research opportunity page. [https://www.usgs.gov/index.php/centers/mendenhall-research-fellowship-program/23-04-evaluation-oilfield-brine-lithium-commodity](https://www.usgs.gov/index.php/centers/mendenhall-research-fellowship-program/23-04-evaluation-oilfield-brine-lithium-commodity)
6. Knierim, K.J., Masterson, A.L., Freeman, P.A., McDevitt, B., Herzberg, A.H., Li, P., Mills, C., Doolan, C., Jubb, A.M., Ausbrooks, S.M., and Chenault, J., 2024, *Lithium resource in the Smackover Formation brines of southern Arkansas*, U.S. Geological Survey Fact Sheet 2024-3052. [https://doi.org/10.3133/fs20243052](https://doi.org/10.3133/fs20243052)
7. Knierim, K.J., Blondes, M.S., Masterson, A.L., Freeman, P.A., McDevitt, B., Herzberg, A.S., Li, P., Mills, C., Doolan, C.A., Jubb, A.M., Ausbrooks, S., and Chenault, J., 2024, *Evaluation of the lithium resource in the Smackover Formation brines of southern Arkansas using machine learning*, Science Advances. USGS page: [https://www.usgs.gov/publications/evaluation-lithium-resource-smackover-formation-brines-southern-arkansas-using-machine](https://www.usgs.gov/publications/evaluation-lithium-resource-smackover-formation-brines-southern-arkansas-using-machine)
8. Jang, E., Jang, Y., and Chung, E., 2017, *Lithium recovery from shale gas produced water using solvent extraction*, Applied Geochemistry 78, 343-350. DOI: [https://doi.org/10.1016/J.APGEOCHEM.2017.01.016](https://doi.org/10.1016/J.APGEOCHEM.2017.01.016)
9. Lee, J., and Chung, E., 2020, *Lithium recovery by solvent extraction from simulated shale gas produced water – Impact of organic compounds*, Applied Geochemistry 116, 104571. DOI: [https://doi.org/10.1016/j.apgeochem.2020.104571](https://doi.org/10.1016/j.apgeochem.2020.104571)
10. Zante, G., Trébouet, D., and Boltoeva, M., 2020, *Solvent extraction of lithium from simulated shale gas produced water with a bifunctional ionic liquid*, Applied Geochemistry 123, 104783. DOI: [https://doi.org/10.1016/j.apgeochem.2020.104783](https://doi.org/10.1016/j.apgeochem.2020.104783)
11. Wang, X., Numedahl, N., and Jiang, C., 2024, *Direct lithium extraction from Canadian oil and gas produced water using functional ionic liquids – A preliminary study*, Applied Geochemistry 172, 106126. DOI: [https://doi.org/10.1016/j.apgeochem.2024.106126](https://doi.org/10.1016/j.apgeochem.2024.106126)
12. Gerardo, S., and Song, W., 2025, *Lithium recovery from U.S. oil and gas produced waters: resource quality and siting considerations*, Environmental Science: Water Research & Technology 11(3), 536-541. DOI: [https://doi.org/10.1039/d4ew00422a](https://doi.org/10.1039/d4ew00422a)
13. Kumar, A., Fukuda, H., Hatton, T.A., and Lienhard, J.H., 2019, *Lithium Recovery from Oil and Gas Produced Water: A Need for a Growing Energy Industry*, ACS Energy Letters 4(6), 1471-1474. DOI: [https://doi.org/10.1021/acsenergylett.9b00779](https://doi.org/10.1021/acsenergylett.9b00779)
14. Liu, Q., Yang, P., Tu, W., Sun, H., Li, S., and Zhang, Y., 2023, *Lithium recovery from oil and gas produced water: Opportunities, challenges, and future outlook*, Journal of Water Process Engineering 55, 104148. DOI: [https://doi.org/10.1016/j.jwpe.2023.104148](https://doi.org/10.1016/j.jwpe.2023.104148)
15. Arkansas Department of Energy and Environment, Arkansas Geological Survey, *Brine in Arkansas / Bromine (Brine)*. [https://www.geology.ar.gov/energy/brine-in-arkansas.html](https://www.geology.ar.gov/energy/brine-in-arkansas.html)
16. Knierim, K.J., Masterson, A.L., Freeman, P.A., McDevitt, B., Herzberg, A.H., Li, P., Mills, C., Doolan, C., Jubb, A.M., Ausbrooks, S.M., and Chenault, J., 2024, *Lithium observations, machine-learning predictions, and mass estimates from the Smackover Formation brines in southern Arkansas*, U.S. Geological Survey data release. DOI: [https://doi.org/10.5066/P9QPRYZN](https://doi.org/10.5066/P9QPRYZN)
17. TDS summary used in Slide 1 and Backup A was computed from the `southAR_brines_2022.txt` file inside Ref. 16 using rows with `FORMATION` or `FRM_GRP = Smackover`, after removing duplicate and blank samples and ignoring missing-code values.

## Repo References Used In This Draft

- `data/multiphase/gando_2025_one_stage_assets/gando_2025_one_stage_assets.md`
- `data/multiphase/gando_2025_stage3_comparison.md`
- `data/multiphase/gando_2025_slide_assets/gando_2025_slide_assets.md`
- `scripts/lle/jang_2017_stage2_li_na_tbp_d2ehpa.py`
- `docs/.codex-journal/project_memory.md`
