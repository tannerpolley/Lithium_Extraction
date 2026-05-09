# Non-Ionic Produced-Water Lithium Case Study Dependency Roadmap

Last updated: 2026-05-07

> Superseded context, 2026-05-08: this roadmap is retained for provenance, but its HBTA/TOPO-first recommendation is no longer the active path. Current Phase 0-9 work uses the Rezaee DES/TOPO Li/Na bridge after divalent pretreatment, with HBTA/TOPO as comparison/future parameterization.

## Purpose

This document preserves the remaining work needed to turn the non-ionic produced-water lithium extraction case study into a presentation-ready and implementation-ready argument for adding ePC-SAFT into the PrOMMiS and IDAES ecosystem.

The roadmap is dependency ordered. Later phases should not be treated as blocked completely, but their final scientific claims depend on earlier phases being resolved.

## Core Boundary

True reactive HBTA/TOPO ePC-SAFT is not scientifically complete yet because the required parameter set and reaction-equilibrium constants were not found for HBTA, TOPO, sulfonated kerosene or a defensible diluent surrogate, and lithium-ligand complexes. Competing divalent complexes are not part of the active Li/Na-after-pretreatment objective.

The current bridge therefore must remain clearly labeled as a calibrated or structured fallback until those parameters and reaction data are sourced, fitted, or explicitly replaced with documented surrogate assumptions.

## Phase 0: Decide The Case-Study Strategy

Everything else depends on this phase.

### Required Decisions

1. Choose the flagship solvent case.
   - Default: HBTA/TOPO/sulfonated kerosene from Shan et al. 2025.
   - Backup candidates: DBM/TOPO, TBP+D2EHPA, TOP/FeCl3.
2. Decide the presentation standard.
   - Most scientifically real: real produced water plus real solvent paper plus explicit parameter gaps.
   - Easiest to showcase: existing repo scripts/artifacts plus acceptable assumptions.
3. Decide whether Smackover is:
   - the actual modeled feed, or
   - the siting motivation while Shan et al. 2025 supplies the extraction chemistry.
4. Decide how much uncertainty can be shown in the presentation.
   - Conservative audience: emphasize parameter gaps and model-readiness ladder.
   - Pitch audience: emphasize why ePC-SAFT is the missing backbone and show the staged artifacts as the implementation path.

### Output Of This Phase

- One selected flagship solvent system.
- One selected feed/siting basis.
- One explicit standard for what counts as presentation-ready.

## Phase 1: Source And Feed Data

Depends on Phase 0.

Some of this work realistically requires the user, because source access, data rights, and credibility of the chosen field basis matter.

### User-Owned Or User-Led Tasks

1. Choose or approve one real flagship produced-water source.
2. If possible, collect one actual well, field, operator, or basin dataset for the flagship case.
3. Confirm whether the source is southern Arkansas Smackover, Marcellus/Appalachian, or a generic oil-and-gas field water case.
4. Provide or approve any proprietary/non-public brine data that should be used.
5. Decide whether REE and other critical minerals are central to the pitch or secondary.

### Data Needed

1. Major cations: Li, Na, K, Mg, Ca, Sr, Ba.
2. Major anions: Cl, Br, SO4, HCO3 or alkalinity when available.
3. Bulk properties: TDS, pH, density, temperature, pressure, TOC or organic family data.
4. Trace metals and critical minerals: Mn, Fe, Zn, Cu, Ni, Al, B, and REE only if reported.
5. Sampling/source metadata: formation, basin, well/field if available, date, sample treatment, source DOI or report URL.
6. Pretreatment data: filtration, suspended solids, Ca/Mg removal, pH adjustment, organics removal, Fe/Mn removal.

### Rules

- Do not infer REE from nearby basins or generic produced-water claims.
- If REE are not reported for the selected feed, record `not_reported`.
- If REE are important but unavailable for the selected feed, build a separate parallel mineral-opportunity dataset.
- Do not claim Shan et al. 2025 establishes a Smackover-specific composition unless a Smackover-specific composition is actually found.

### Output Of This Phase

- A source-specific composition table.
- A source log for every number.
- A clear distinction between extraction-chemistry evidence and basin-siting evidence.

## Phase 2: Solvent-System Selection

Depends on Phases 0 and 1.

The goal is to choose the solvent/extractant chemistry that gives the best combination of real evidence, non-ionic relevance, ePC-SAFT teachability, and PrOMMiS/IDAES implementation value.

## Solvent Candidate Ranking

| Rank | Solvent system | Evidence realism | Implementation ease | Current repo support | Recommendation |
|---:|---|---|---|---|---|
| 1 | HBTA/TOPO/sulfonated kerosene | Highest current fit: actual oil-and-gas field-water process, non-ionic ligand chemistry, strong multistage extraction evidence | Medium-hard because direct ePC-SAFT parameters and reaction constants are missing | Strong: current plan, transfer matrix, PrOMMiS artifact, ePCSAFT-PSE bridge scaffold | Best flagship case |
| 2 | DBM/TOPO | Potentially strong conventional ligand chemistry; review notes suggest actual unconventional oil-and-gas brine use | Medium; original paper and full data still need retrieval | Mentioned in current plan, but not deeply implemented | Best backup if HBTA/TOPO parameterization stalls |
| 3 | TBP+D2EHPA | Real Jang 2017 produced-water context and repo script exists | Easier to demo, but current model is placeholder-heavy and weakly selective | Strong local artifact: `data/multiphase/jang_2017_stage2_li_na_summary.md` | Good limitation/comparison case |
| 4 | TOP/FeCl3 | Conventional extraction class with strong reported selectivity in literature notes | Medium-hard; acid/corrosion/Fe handling and different chemistry complicate process story | Not yet a primary repo workflow | Possible alternate case, not first choice |
| 5 | Ionic-liquid systems | Literature and repo work exist | Excluded by project rule because cost and uncertainty are too high | Yu/Hubach artifacts exist but are out of active scope | Background only, not active benchmark |

### Additional Search Tasks

1. Run a fresh Zotero search for non-ionic produced-water lithium solvent extraction once the Zotero connector is available.
2. Use Rezaee et al. 2026 as a DES/TOPO PC-SAFT/ePC-SAFT regression-smoke-test source, while keeping it out of the active flagship chemistry.
3. Search for original DBM/TOPO unconventional oil-and-gas field brine paper cited by Chen et al. 2025.
4. Search for TOP/FeCl3 oilfield-brine extraction details and whether it can be made compatible with the pitch.
5. Re-scan the repo scripts and `data/multiphase/` outputs for any other non-ionic solvent systems already implemented or partially implemented.

### Output Of This Phase

- A ranked solvent selection table.
- A primary case and one backup case.
- A short explanation of why ionic liquids are excluded from active benchmarking.

## Phase 3: Literature Extraction

Depends on the selected solvent system from Phase 2.

### Required Tasks

1. Retrieve original papers for the selected solvent, not only reviews.
2. Extract feed composition, solvent composition, O/A ratio, pH, contact time, saponification degree, stage count, stripping conditions, and precipitation conditions.
3. Extract or digitize missing curves where tables are insufficient.
4. Build a source log with citation key, DOI/URL, source type, values extracted, and claims supported.
5. Add a `not found` table for searched-but-unavailable data.

### HBTA/TOPO-Specific Extraction Tasks

1. Extract the Shan et al. 2025 simulated feed composition.
2. Extract Na effect data.
3. Extract K effect data.
4. Extract Ca and Mg inhibition data.
5. Extract organic-matter effect data.
6. Extract three-stage extraction data.
7. Extract the 15 L field-water process result.
8. Extract Li2CO3 precipitation and purity data.

### Backup-Solvent Extraction Tasks

1. For DBM/TOPO, retrieve the original actual-brine source and extract feed/solvent/stage data.
2. For TBP+D2EHPA, compare against the current Jang 2017 placeholder artifact.
3. For TOP/FeCl3, extract selectivity, stripping, corrosion/acid, Fe loss, and precipitation limitations.

### Output Of This Phase

- Literature extraction tables.
- Figure digitization outputs if needed.
- A verified claim/source map for the deck.

## Phase 4: ePC-SAFT Parameter Work

Depends on Phases 2 and 3.

### Required Tasks

1. Build a species inventory for the chosen solvent system.
2. Find existing ePC-SAFT/PC-SAFT parameters for:
   - water;
   - Li+, Na+, K+, Mg2+, Ca2+, Ba2+, Cl-;
   - TOPO or TOP;
   - diluent or diluent surrogate;
   - extractant;
   - neutral or charged complexes.
3. Choose the diluent representation.
   - sulfonated kerosene;
   - kerosene pseudo-component;
   - n-dodecane;
   - n-cetane;
   - hexane;
   - mixed alkane surrogate.
4. Find or fit pure-component parameters for missing neutral organics.
5. Define binary interaction parameters.
6. Define association parameters if needed.
7. Define uncertainty ranges.
8. Run the Rezaee 2026 DES/TOPO diagnostic fit as an ePC-SAFT package plumbing check, not as flagship HBTA/TOPO closure.

### Parameter Hierarchy

1. Existing ePC-SAFT package parameter tables.
2. Local repo parameter files.
3. Peer-reviewed ePC-SAFT/PC-SAFT parameter literature.
4. Closest defensible surrogate species.
5. Fitted pseudo-parameters, clearly labeled as case-study calibration.
6. Diagnostic literature smoke tests, such as Rezaee 2026, clearly labeled when they use a different chemistry or mixed PC-SAFT/ePC-SAFT architecture.

### Rule

If a parameter is missing, do not silently invent it. Record the missing parameter, choose a documented surrogate or reduced model, and continue with a visible limitation.

### Output Of This Phase

- Parameter inventory.
- Parameter-gap table.
- Chosen surrogate/diluent strategy.
- Parameter uncertainty notes.

## Phase 5: Reactive Chemistry

Depends on Phase 4.

### Required Tasks

1. Resolve the current core boundary: true reactive HBTA/TOPO ePC-SAFT is incomplete until parameters and reaction constants exist.
2. Define the minimum reaction network.
3. Find or fit equilibrium constants.
4. Decide whether the implementation is:
   - homogeneous reactive speciation followed by phase handoff;
   - reactive LLE;
   - external reaction wrapper plus phase split;
   - calibrated surrogate only.
5. Build a small reactive-speciation smoke test before full LLE.
6. Add phase-handoff logic from reactive speciation to aqueous/organic stage outputs.
7. Validate against trends, not only one nominal point.

### HBTA/TOPO Minimum Reaction Network

1. HBTA deprotonation or saponification.
2. Li+ + BTA- + nTOPO complexation.
3. Ca2+ and Mg2+ competing complexation if supported by data.
4. Acid stripping/back-extraction as a later process step.

### Output Of This Phase

- Reaction network definition.
- Reaction constants or explicit gaps.
- Reactive-speciation smoke test.
- Decision on whether the active model is predictive, fitted, or fallback.

## Phase 6: `epcsaft-pse` Bridge

Depends on Phases 4 and 5.

Some development can proceed now, but final scientific claims depend on Phase 5.

### Required Tasks

1. Replace current structured blocker diagnostics with a real reactive payload once parameters exist.
2. Add a documented parameter-set file for the selected solvent system.
3. Add tests for missing-parameter diagnostics.
4. Add a Rezaee 2026 package-smoke-test artifact to prove parameter-regression and electrolyte phase-equilibrium calls can execute for a literature-derived DES/TOPO pilot.
5. Add tests for successful reactive speciation.
6. Add phase-handoff tests.
7. Add Li/Na/Mg/Ca selectivity tests.
8. Generate surrogate training data.
9. Add trust-region bounds and validity diagnostics.
10. Preserve calibrated fallback as comparison only.

### Output Of This Phase

- Reactive bridge path.
- Surrogate generation path.
- Tests proving when ePC-SAFT is actually used and when fallback is used.
- Transfer-variable outputs ready for PrOMMiS.

## Phase 7: PrOMMiS / IDAES Integration

Depends on Phase 6 for final form, but partial artifact work can continue now.

### Required Tasks

1. Convert the artifact generator into a real MSContactor solve where possible.
2. Wire transfer terms for Li, Na, K, Mg, Ca, Ba, and Cl.
3. Add explicit pretreatment unit model or transparent placeholder block.
4. Add stripping/back-extraction.
5. Add solvent recycle.
6. Add solvent makeup/loss accounting.
7. Add concentration step.
8. Add Li2CO3 precipitation stoichiometry.
9. Add process-level mass-balance reports.
10. Add component recovery reports.
11. Add IDAES costing hooks.

### Sensitivity Cases

1. No pretreatment.
2. Partial Ca/Mg removal.
3. Full Ca/Mg removal.
4. High/low Li feed.
5. High/low TDS.
6. Different O/A ratios.
7. Different extractant/synergist concentrations.

### Output Of This Phase

- PrOMMiS/IDAES staged flowsheet or staged artifact.
- Process mass-balance table.
- Costing hook table.
- Sensitivity outputs.

## Phase 8: Costing / TEA

Depends on Phase 7 and user-approved assumptions.

### User-Owned Or User-Led Tasks

1. Define process basis.
   - feed flowrate;
   - annual operating hours;
   - recovery target;
   - product basis;
   - site location.
2. Approve or provide cost assumptions.
   - HBTA/DBM/TBP/D2EHPA/TOPO/TOP price;
   - diluent price;
   - NaOH price;
   - HCl price;
   - carbonate reagent price;
   - solvent loss rate;
   - utilities;
   - waste disposal;
   - Li2CO3 price.
3. Decide whether avoided disposal credit is allowed.
4. Decide whether this is a pitch-level TEA or a more formal techno-economic analysis.

### Modeling Tasks

1. Add CAPEX placeholders for pretreatment, extraction contactors, settlers, stripping, concentration, precipitation, tanks, and pumps.
2. Add OPEX placeholders for reagents, solvent loss, utilities, waste handling, maintenance, and labor if needed.
3. Calculate Li2CO3 production rate.
4. Calculate revenue proxy.
5. Run conservative/base/optimistic scenarios.
6. Keep economics labeled as case-study economics, not investment-grade TEA.

### Output Of This Phase

- Cost basis table.
- Scenario table.
- Revenue/cost summary.
- Clear caveat level.

## Phase 9: Final Presentation

Depends on Phases 1 through 8.

### Required Slides

1. Why this location.
2. Why this solvent.
3. Why ePC-SAFT changes the question.
4. Process-flow diagram:
   - pretreatment;
   - extraction;
   - stripping;
   - concentration;
   - Li2CO3 precipitation.
5. ePC-SAFT to PrOMMiS/IDAES transfer-variable map.
6. Evidence ladder:
   - feed evidence;
   - solvent evidence;
   - model evidence;
   - process evidence;
   - costing evidence.
7. Limitation slide:
   - missing parameters;
   - calibrated bridge;
   - reactive chemistry still incomplete;
   - next parameterization step.
8. Implementation ask:
   - ePC-SAFT as thermodynamic backend;
   - ePC-SAFT as surrogate generator;
   - ePC-SAFT as external function;
   - PrOMMiS/IDAES as process/costing layer.

### Acceptance Criteria

1. Every number points to a source, generated artifact, or explicit assumption.
2. Ionic liquids are excluded from the active benchmark.
3. Smackover is supported by real composition evidence or clearly labeled as siting motivation.
4. HBTA/TOPO extraction chemistry is separated from Smackover composition unless a matching source is found.
5. ePC-SAFT's role is precise:
   - equilibrium;
   - activity/fugacity;
   - phase split;
   - distribution ratios;
   - selectivity;
   - validity diagnostics.
6. PrOMMiS/IDAES's role is precise:
   - staged unit models;
   - flowsheet;
   - optimization;
   - costing;
   - process reporting.
7. The audience can see what is complete, what is calibrated, what is assumed, and what still needs parameterization.

## Recommended Path

Use HBTA/TOPO as the flagship case, TBP+D2EHPA as the older/weak-placeholder comparison, and DBM/TOPO as the backup solvent candidate.

This gives the clearest story:

1. HBTA/TOPO provides the strongest non-ionic produced-water extraction anchor.
2. TBP+D2EHPA shows why older fixed-assumption placeholders are not enough.
3. DBM/TOPO gives a credible backup if HBTA/TOPO parameterization stalls.
4. ePC-SAFT remains the thermodynamic backbone needed to turn chemistry and basin composition into PrOMMiS/IDAES transfer variables.
