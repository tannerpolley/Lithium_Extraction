# Zotero Organic-Solvents Literature Review For The Produced-Water Case Study

Last updated: 2026-05-07

## Purpose

This note records the current Zotero-backed evidence review for the non-ionic produced-water lithium solvent-extraction case study. It is intended to support the Phase 4-5 parameterization path and the Phase 9 presentation narrative.

The active benchmark rule remains unchanged: ionic-liquid systems are excluded from the flagship case study because of cost and implementation uncertainty. Ionic-liquid papers can still be used as ePC-SAFT modeling-method references, but not as the active solvent case.

## Bottom Line

HBTA/TOPO remains the strongest flagship chemistry because it is conventional ligand/synergist extraction, is already tied to oil-and-gas field water in the local case-study artifacts, and has direct stoichiometry/selectivity support from Zhang 2017 plus field-water process support from Shan/Gando 2025.

Rezaee 2026 is valuable, but it is not a complete solution to the HBTA/TOPO problem. It uses PC-SAFT for the organic DES/TOPO phase and ePC-SAFT for the aqueous electrolyte phase, with reaction-equilibrium bridging between phase-specific species. It therefore supports a parameter-fitting and modeling-method pilot, not a claim that full reactive ePC-SAFT for HBTA/TOPO has been solved.

## Evidence Table

| Topic | Zotero key | Source | DOI | Evidence status | Use in this case study |
|---|---|---|---|---|---|
| Produced-water flagship chemistry | `JUNBXVTI` | Gando-Ferreira/Shan 2025, oil-and-gas field-water HBTA/TOPO/sulfonated-kerosene study | `10.3390/w17152258` | Full-text evidence in Zotero; current repo artifacts already use it | Primary active benchmark and stage/costing anchor |
| HBTA/TOPO stoichiometry and selectivity | `9LJWDC7E` | Zhang 2017, HBTA-TOPO alkaline-brine extraction | `10.1016/j.seppur.2017.07.028` | Full-text evidence in Zotero | Mechanistic anchor for `2 HBTA : 1 TOPO : 1 Li` extraction complex and Li/Na selectivity |
| HBTA/TOPO process support | `AEL6ZEPG` | Zhang 2018, beta-diketone lithium extraction | `10.1016/j.hydromet.2017.10.029` | Full-text evidence in Zotero | Secondary HBTA/TOPO process and mixer-settler support |
| HBTA/TOPO and HTTA/TOPO physical properties | `GK598336` | Hanada 2021, synergistic deep eutectic solvents for lithium extraction | `10.1021/acssuschemeng.0c07606` | Full-text evidence in Zotero | Supports pseudo-component fitting targets and solvent-candidate ranking |
| PC-SAFT/ePC-SAFT modeling pilot | `3NMV5MF2` | Rezaee 2026, DES/TOPO lithium extraction modeling | `10.1016/j.fluid.2026.114737` | Full-text evidence in Zotero | Parameter-fitting smoke test and warning case: organic PC-SAFT plus aqueous ePC-SAFT, not full reactive ePC-SAFT |
| Conventional produced-water comparison | `BLUVRJ9Q` | Jang 2017, shale-gas produced-water lithium recovery | `10.1016/j.apgeochem.2017.01.016` | Full-text evidence in Zotero and local scripts | Comparison/limitation baseline |
| Conventional high-Mg brine comparison | `V7EN7V3S` | Kia 2024, TBP/FeCl3 high Mg/Li brine extraction | `10.1007/s11356-024-34617-8` | Zotero metadata/full text available | Optional comparison, not flagship due Fe/acid process burden |
| Review context | `CGJJSXYG` | Kanagasundaram 2024 review | `10.1016/j.ccr.2024.215727` | Zotero full text available | Broad solvent-class framing only |
| Produced-water and brine-review context | `DIRN6TP8`, `2GHKXGZ7`, `HGPATNIR`, `DSLJER2U`, `E92CSFXM` | Knapik 2023, Gerardo 2025, Karuppasamy 2024, Liu 2023, Kumar 2019 | see Zotero metadata | Zotero metadata/full text available depending on item | Siting, produced-water variability, process context |
| Ionic-liquid ePC-SAFT method reference | `FGAE94M4` | Hubach 2024 | `10.1021/acs.jced.4c00074` | Zotero full text/supporting info available | ePC-SAFT method reference only; excluded as active solvent chemistry |
| Ionic-liquid ePC-SAFT method reference | `SLMXCPZM` | Yu 2024 | `10.1016/j.ces.2023.119682` | Zotero full text available | ePC-SAFT method reference only; excluded as active solvent chemistry |

## Solvent-System Ranking After Organic-Solvents Review

| Rank | Solvent system | Evidence realism | ePC-SAFT readiness | Recommendation |
|---:|---|---|---|---|
| 1 | HBTA/TOPO/sulfonated kerosene | Highest for the current objective: actual oil-and-gas field water, conventional extractant/synergist, direct stage/process evidence | Missing pure-component, complex, binary-interaction, and reaction-equilibrium payloads | Keep as flagship; use the current calibrated reactive bridge until parameters are fitted |
| 2 | HBTA/TOPO or HTTA/TOPO DES | Strong selectivity and useful physical-property data; not the same as sulfonated kerosene field-water system | Better pseudo-component fitting path because density/viscosity data exist, but still not full reactive ePC-SAFT | Use as an alternate fitting target and mechanism support |
| 3 | Rezaee DES/TOPO | Strongest immediate parameter/regression pilot because it reports PC-SAFT-style parameters and organic/aqueous modeling workflow | Good for smoke-testing regression and phase-equilibrium plumbing; not the same active chemistry and not full ePC-SAFT | Use as method pilot, not flagship |
| 4 | TBP+D2EHPA | Real produced-water literature and existing local scripts | Current local model remains placeholder-heavy and less selective | Keep as comparison/limitation baseline |
| 5 | TBP/FeCl3 or TOP/FeCl3 | Conventional extraction class with useful selectivity literature | Process burdens and different acid/Fe chemistry complicate the presentation story | Optional backup only |
| 6 | Ionic-liquid systems | Strong modeling literature exists | Excluded by project rule | Background only |

## Rezaee 2026 Modeling Interpretation

Rezaee 2026 should be cited carefully. Its value is that it demonstrates how a lithium extraction system can be linked to PC-SAFT/ePC-SAFT thermodynamic calculations and fitted interaction parameters. The unusual feature is that the organic phase is treated with PC-SAFT, while the aqueous electrolyte phase is treated with ePC-SAFT. This is useful for this project because it creates a bridge example, but it does not prove that a single full reactive ePC-SAFT LLE model is already available for HBTA/TOPO extraction.

Extracted parameter information to carry forward:

- DES pseudo-component PC-SAFT values are reported for the TBAC/decanoic-acid DES.
- TOPO PC-SAFT-style values are reported for the TOPO-containing organic phase.
- Organic reaction-product pseudo-species and binary interaction parameters are fitted against extraction data.
- The authors acknowledge limitations from density-only fitting, group-contribution reaction energetics, and temperature-independent reaction constants.

Case-study implication:

Rezaee is the best immediate package/regression smoke test because the required inputs are sufficiently tabulated. HBTA/TOPO remains the better pitch case, but its missing parameter set must be fitted or sourced before the model can be called predictive.

## Parameterization Path

1. Preserve the current HBTA/TOPO fitted bridge as `calibrated_reactive_hbta_topo_not_full_predictive_epcsaft`.
2. Use Rezaee 2026 as a regression and phase-equilibrium smoke test for the new ePC-SAFT package.
3. Use Hanada 2021 density/viscosity values to justify a future HBTA/TOPO or HTTA/TOPO pseudo-component fitting attempt if direct pure-component parameters remain unavailable.
4. Digitize Zhang 2017 and Shan/Gando 2025 curves if fitted reaction constants are needed beyond the current stage-anchor calibration.
5. Choose a diluent surrogate explicitly, preferably from existing alkane PC-SAFT/ePC-SAFT parameter sources, if sulfonated kerosene cannot be parameterized directly.
6. Keep ionic-liquid ePC-SAFT papers in a separate method-reference bucket.

## Open Data Requests For The User

These are the items most likely to require user access or judgment:

- Original source data or supporting information for any HBTA, TOPO, sulfonated kerosene, or Li-BTA-TOPO pure-component parameters not found in Zotero.
- Extraction-equilibrium tables behind figures in Zhang 2017, Zhang 2018, Hanada 2021, and Shan/Gando 2025 if the figures cannot be cleanly digitized.
- Any proprietary or source-specific Smackover/field brine composition that should replace the current public MS-2/USGS basis.
- Market/cost assumptions for HBTA, TOPO, sulfonated kerosene, NaOH, HCl, solvent loss, and lithium carbonate product value.

## Current Claim Boundary

The presentation can already defend this statement:

> ePC-SAFT is the thermodynamic layer needed to convert source-specific brine chemistry, organic-phase extraction chemistry, and competing-ion nonideality into transfer variables for PrOMMiS/IDAES.

The presentation should not yet claim this:

> A complete predictive reactive ePC-SAFT model for HBTA/TOPO/sulfonated-kerosene lithium extraction has been fully parameterized and validated.

That second claim requires the missing parameter and reaction-equilibrium work to be completed.
