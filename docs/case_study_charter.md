# Produced-Water Lithium Case Study Charter

Last updated: 2026-05-08

## Decisions Locked For The Current Skeleton

| Decision | Selected path | Rationale |
|---|---|---|
| Flagship source | Southern Arkansas Smackover | High salinity, strong lithium signal, brine-handling infrastructure, and source-backed local USGS rows. |
| Base feed row | `MS-2 / MSPU 4-W1` | Actual clean Smackover row with median clean-set TDS `305,000 mg/L` and Li `168 mg/L`. |
| Starting extraction feed | Pretreated clean Li+Na stream from the selected Smackover row | Ca/Mg/Sr/Ba are removed upstream and carried as pretreatment-cost/guardrail variables, not extraction species. |
| Active Li/Na bridge chemistry | Rezaee 2026 TBAC/decanoic-acid DES + TOPO | Best current package-facing evidence set: reported DES, TOPO, RLi, RNa, binary interactions, reaction constants, Li/Na extraction responses, and SI equilibrium-composition rows. |
| Comparison chemistry | Shan/Gando HBTA/TOPO/sulfonated kerosene | Remains the conventional field-water comparison and future parameterization lane, but no longer the Phase 0-9 flagship bridge. |
| Limitation baseline | Jang 2017 D2EHPA/TBP | Produced-water solvent-extraction baseline that shows pretreatment and placeholder limits. |
| Backup chemistry | D2EHDTPA + BuPhen + octanol modifiers + n-dodecane | Literature comparison only. The active demonstration is Li/Na after divalent pretreatment, not divalent extraction. |
| Excluded chemistry | Ionic liquids as the active benchmark | Out of active scope because of cost and uncertainty; method papers can still inform parameter fitting. |
| Modeling standard | Rezaee source-regressed Li/Na distribution bridge after divalent pretreatment | Distribution coefficients are derived from source-backed Rezaee extraction targets and SI equilibrium-composition evidence, with ePC-SAFT diagnostics and the Rezaee reactive convention scan carried as validity evidence. |
| ePC-SAFT role | Thermodynamic backend, parameter/regression support, and diagnostic transfer-variable generator | Supports density regression, electrolyte stability, bounded LLE diagnostics, distribution variables, selectivity, and surrogate-training rows. |
| PrOMMiS/IDAES role | Process/costing layer | Consumes transfer variables in staged contactors, flowsheets, optimization, and formal IDAES/Pyomo costing scenarios. |

## Boundary Statement

The selected site is source-backed Smackover brine, but the extraction model starts after a pretreatment block that removes the divalent cation burden. The active feed to the Rezaee extraction bridge is therefore a clean Li+Na stream with the selected MS-2 lithium and sodium concentrations. The selected Li/Na bridge is Rezaee 2026 DES/TOPO because it has source-backed extraction responses, equilibrium-composition rows, PC-SAFT-style organic parameters, binary interactions, and reaction constants. The current generated transfer-variable rows come from a Rezaee source-regressed Li/Na distribution bridge with ePC-SAFT density, stability, and bounded LLE diagnostic support.

This is not a claim that direct ePC-SAFT LLE has fully accepted aqueous/organic phase splits over the entire Smackover surrogate region, or that the published Rezaee constants close under the currently extracted Section 3.2 initial-mole/activity-reference convention. The accepted claim is narrower and stronger for the presentation: Rezaee supplies the data and parameter payload needed to derive Li/Na distribution coefficients, sensitivity rows over Na/TDS/OA, and PrOMMiS/IDAES transfer variables, while the direct thermodynamic closure gap is explicitly reported.

The active thermodynamic replication benchmark uses the 26 source-backed SI equilibrium rows. The direct Section 3.2 equation implementation starts after Table 8, uses Eqs. 14/15/17/18/19/20, and uses the ePC-SAFT package only for activity coefficients. Its first source-aligned Held-2014-S2/no-Born/Table-9 case does not reproduce the paper's post-Table-9 AARD values. The source-basis diagnostic also shows the organic total inferred from SI RLi is a median `3.64x` the organic total inferred from SI RNa when combined with Table 5 extraction percentages, so the missing source item is the exact initial-mole/phase-amount convention behind Eq. 17.

Ca/Mg/Sr/Ba and other divalent burdens are pretreated before extraction and retained only as feed-context, pretreatment-cost, and leakage-guardrail variables. This branch does not try to demonstrate divalent extraction or divalent equilibrium.

## Completion Standard For This Branch

This branch is considered complete for the current case-study scope when every phase has a local artifact, every nontrivial number is source-backed or labeled as an assumption, the Rezaee Li/Na bridge has distribution-coefficient and sensitivity artifacts, the clean Li+Na surrogate input space is documented, the PrOMMiS/IDAES handoff and costing input are generated, and remaining direct-LLE, surrogate-run, and TEA gaps are explicit.
