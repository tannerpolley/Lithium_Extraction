# Internet Parameter Source Search - HBTA/TOPO ePC-SAFT Case

Last updated: 2026-05-07

## Search Objective

Find public internet sources that could close or narrow the remaining HBTA/TOPO case-study gaps:

- HBTA pure-component PC-SAFT/ePC-SAFT parameters.
- TOPO pure-component PC-SAFT/ePC-SAFT parameters.
- Sulfonated kerosene or defensible diluent parameters.
- Li-BTA-TOPO complex parameters or stoichiometry.
- HBTA deprotonation/saponification and Li extraction reaction-equilibrium constants.

## Bottom Line

No public source found in this pass directly reports a complete predictive ePC-SAFT parameter set for the exact Shan/Gando produced-water system:

`H2O + Li+/Na+/Ca2+/Mg2+/Cl-/major brine ions + HBTA + TOPO + sulfonated kerosene + Li-BTA-TOPO complex`

The search did find useful sources that materially reduce the uncertainty:

1. A direct HBTA/TOPO stoichiometry and selectivity anchor for lithium extraction from alkaline brine.
2. HBTA/TOPO physical-property data that can support a fitted organic-phase pseudo-component or DES-style surrogate.
3. A PC-SAFT/ePC-SAFT lithium-extraction modeling paper with TOPO as co-extractant that should be reviewed for TOPO parameter-fitting workflow and possible parameter values.
4. General PC-SAFT alkane/diluent parameter sources that can support a kerosene surrogate.

## Priority Source Leads

| Priority | Source | What it appears to provide | Use in this project | Status |
|---:|---|---|---|---|
| 1 | Zhang et al. 2017, `Selective extraction of lithium from alkaline brine using HBTA-TOPO synergistic extraction system`, DOI: https://doi.org/10.1016/j.seppur.2017.07.028 | HBTA/TOPO/Li extraction complex stoichiometry `2:1:1`; Li/Na separation factor over `2100`; two-stage countercurrent extraction around `95%`; scrubbing, stripping, regeneration conditions. | Keep as the best stoichiometry/selectivity anchor for the current source-regressed Li/Na model; use figures/tables to regress apparent extraction constants if full text or digitized plots are available. | Strong mechanism/process source; not a complete ePC-SAFT parameter source. |
| 2 | Hanada and Goto 2021, `Synergistic Deep Eutectic Solvents for Lithium Extraction`, DOI: https://doi.org/10.1021/acssuschemeng.0c07606 | HBTA/TOPO and HTTA/TOPO DES physical properties; HBTA/TOPO at 2:1 molar ratio has reported melting point about `298 K`, density about `1.05 g/cm3`, viscosity about `13.2 mPa s`; spectroscopy supports synergistic Li complexation. | Use as organic-phase pseudo-component fitting data and mechanism support if the exact sulfonated-kerosene system cannot be parameterized directly. | Useful for fitted DES/pseudo-component; not the Shan/Gando diluent system. |
| 3 | Rezaee, Feyzi, and Miri 2026, `Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents: A PC-SAFT approach`, DOI: https://doi.org/10.1016/j.fluid.2026.114737 | PC-SAFT/ePC-SAFT lithium-extraction modeling with TOPO as co-extractant; reports DES/TOPO organic-phase PC-SAFT parameters from density data, reaction-product pseudo-species, fitted organic binary interactions, and aqueous electrolyte treatment with ePC-SAFT. | Highest-value modeling-method and regression-smoke-test lead. The full text now in Zotero includes tabulated DES/TOPO/RLi/RNa and binary-interaction values. | Not exact HBTA/TOPO/sulfonated-kerosene chemistry; importantly, it is a mixed PC-SAFT organic plus ePC-SAFT aqueous architecture, not a complete full reactive ePC-SAFT HBTA/TOPO closure. |
| 4 | Gross/Sadowski-style extended PC-SAFT parameter tables, e.g. DOI: https://doi.org/10.1016/j.fluid.2006.07.006 | Extended PC-SAFT pure-component parameter tables and group-contribution logic for nonassociating families, including hydrocarbons. | Use for n-alkane diluent surrogate selection when sulfonated kerosene is represented as n-dodecane, n-cetane, or a pseudo-component. | Good for diluent surrogate, not HBTA/TOPO chemistry. |
| 5 | Public PC-SAFT alkane parameter examples, e.g. n-decane/hexadecane tables in open literature | Example alkane parameters and validation contexts. | Use only as a temporary diluent surrogate source if local ePC-SAFT parameter tables do not already contain the chosen alkane. | Surrogate support only. |

## Evidence Notes

Zhang et al. 2017 is the most direct non-ionic HBTA/TOPO chemistry source found online. The publisher page reports that slope analysis identified the extraction complex as `HBTA:TOPO:Li = 2:1:1`, and reports Li/Na separation factor over `2100`.

Hanada and Goto 2021 is not the produced-water HBTA/TOPO/sulfonated-kerosene system, but it reports directly useful HBTA/TOPO physical-property data. Those density/viscosity values are enough to justify a pseudo-component fitting task if pure HBTA and TOPO PC-SAFT parameters remain unavailable.

Rezaee et al. 2026 is the strongest modeling lead found: it explicitly applies PC-SAFT/ePC-SAFT to a lithium extraction system with TOPO as co-extractant and says TOPO EOS parameters were obtained from density data. The Zotero full text has now been inspected and does include tabulated DES, TOPO, organic reaction-product pseudo-species, and organic binary-interaction values. It should still not be treated as proof that HBTA/TOPO parameters are solved, because the chemistry is TBAC/decanoic-acid DES plus TOPO, the organic phase is modeled with PC-SAFT, and the aqueous phase is modeled with ePC-SAFT.

## Recommended Next Actions

1. Use the retrieved Rezaee et al. 2026 full text as a package/regression smoke test and method reference, while preserving the full HBTA/TOPO parameter gap.
2. Digitize or extract Zhang et al. 2017 extraction curves for pH, HBTA concentration, TOPO concentration, temperature, and McCabe-Thiele data; fit apparent equilibrium constants for the current bridge.
3. Use Hanada and Goto 2021 HBTA/TOPO density and viscosity data to define a pseudo-component fitting target if a true pure-component HBTA/TOPO parameter set cannot be found.
4. Select a defensible kerosene surrogate from existing PC-SAFT alkane parameter tables, preferably n-dodecane, n-cetane/n-hexadecane, or a fitted pseudo-component.
5. Keep the current status label: `source_regressed_li_na_predictive_stage_model_limited_epcsaft`.

## Search Conclusion

The missing tasks are not fully complete from public internet sources alone. The most realistic path is now:

1. Treat Zhang 2017 as the HBTA/TOPO stoichiometry and selectivity source.
2. Treat Hanada 2021 as the HBTA/TOPO physical-property source.
3. Treat Rezaee 2026 as the PC-SAFT/ePC-SAFT modeling-method and diagnostic parameter source, not as a complete predictive HBTA/TOPO ePC-SAFT model.
4. Fit the missing constants/parameters explicitly and keep them labeled as source-regressed stage parameters until validated against independent extraction data.
