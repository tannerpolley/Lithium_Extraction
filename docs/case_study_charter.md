# Produced-Water Lithium Case Study Charter

Last updated: 2026-05-07

## Decisions Locked For The Current Skeleton

| Decision | Selected path | Rationale |
|---|---|---|
| Flagship source | Southern Arkansas Smackover | High salinity, strong lithium signal, brine-handling infrastructure, and source-backed local USGS rows. |
| Base feed row | `MS-2 / MSPU 4-W1` | Actual clean Smackover row with median clean-set TDS `305,000 mg/L` and Li `168 mg/L`. |
| Active extraction chemistry | Shan/Gando 2025 HBTA/TOPO/sulfonated kerosene | Best current non-ionic oil-and-gas-field-water extraction anchor. |
| Comparison chemistry | Jang 2017 D2EHPA/TBP | Produced-water solvent-extraction baseline that shows pretreatment and placeholder limits. |
| Backup chemistry | D2EHDTPA + BuPhen + octanol modifiers + n-dodecane | Best non-HBTA backup in the current Zotero-verified scorecard; strong multication selectivity, but no runnable local ePC-SAFT parameter payload yet. |
| Excluded chemistry | Ionic liquids | Explicitly out of active scope because of cost and uncertainty. |
| Modeling standard | Source-regressed Li/Na predictive stage model with explicit gaps | One shared HBTA/TOPO parameter payload is regressed from Zotero-verified Gando/Zhang anchors and reused across feed cases; full multication reactive ePC-SAFT LLE remains a future parameterization task. |
| ePC-SAFT role | Thermodynamic backend and transfer-variable generator | Computes or supports equilibrium, phase split, distribution ratios, selectivity, diagnostics, and surrogate training rows. |
| PrOMMiS/IDAES role | Process/costing layer | Consumes transfer variables in staged contactors, flowsheets, optimization, and the downstream formal IDAES/Pyomo costing module. |

## Boundary Statement

The selected feed is source-backed Smackover brine. The selected extraction chemistry is literature-backed Shan/Gando HBTA/TOPO. The current generated transfer-variable rows come from a source-regressed Li/Na HBTA/TOPO stage model with ePC-SAFT aqueous activity support when the local runtime can evaluate it. It is predictive inside the Li/Na staged-transfer closure because it uses one fitted parameter payload across feed and O/A cases, but it is not a full multication reactive HBTA/TOPO ePC-SAFT LLE model because the HBTA, TOPO, diluent, complex, and reaction-equilibrium parameter set is still incomplete.

The current solvent ranking is presentation-priority based: HBTA/TOPO is the flagship, D2EHDTPA/BuPhen is the best non-HBTA chemistry backup, Rezaee 2026 DES/TOPO is a parameter-regression smoke test, TBP/FeCl3 is a mechanistic backup, and D2EHPA/TBP remains a produced-water limitation baseline. DBM/TOPO remains an unresolved historical search target rather than the active backup.

## Completion Standard For This Branch

This branch is considered complete for the current case-study scope when every phase has a local artifact, every nontrivial number is source-backed or labeled as an assumption, the Li/Na model has regression residual and uncertainty artifacts, the PrOMMiS-side IDAES costing module has been run, and the remaining full multication/ePC-SAFT gaps are explicit.
