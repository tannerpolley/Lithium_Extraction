# Produced-Water Lithium Case Study Charter

Last updated: 2026-05-07

## Decisions Locked For The Current Skeleton

| Decision | Selected path | Rationale |
|---|---|---|
| Flagship source | Southern Arkansas Smackover | High salinity, strong lithium signal, brine-handling infrastructure, and source-backed local USGS rows. |
| Base feed row | `MS-2 / MSPU 4-W1` | Actual clean Smackover row with median clean-set TDS `305,000 mg/L` and Li `168 mg/L`. |
| Active extraction chemistry | Shan/Gando 2025 HBTA/TOPO/sulfonated kerosene | Best current non-ionic oil-and-gas-field-water extraction anchor. |
| Comparison chemistry | Jang 2017 D2EHPA/TBP | Produced-water solvent-extraction baseline that shows pretreatment and placeholder limits. |
| Backup chemistry | DBM/TOPO | Conventional ligand candidate, but direct primary source remains missing locally. |
| Excluded chemistry | Ionic liquids | Explicitly out of active scope because of cost and uncertainty. |
| Modeling standard | Calibrated reactive-stage presentation case with explicit gaps | Good enough to present the why/how/what-for case, not a final predictive reactive ePC-SAFT LLE model. |
| ePC-SAFT role | Thermodynamic backend and transfer-variable generator | Computes or supports equilibrium, phase split, distribution ratios, selectivity, diagnostics, and surrogate training rows. |
| PrOMMiS/IDAES role | Process/costing layer | Consumes transfer variables in staged contactors, flowsheets, optimization, and costing hooks. |

## Boundary Statement

The selected feed is source-backed Smackover brine. The selected extraction chemistry is literature-backed Shan/Gando HBTA/TOPO. The current generated transfer-variable rows come from a calibrated reactive-stage HBTA/TOPO bridge with ePC-SAFT aqueous activity support when the local runtime can evaluate it. They are not true predictive reactive HBTA/TOPO ePC-SAFT LLE predictions because the HBTA, TOPO, diluent, complex, and reaction-equilibrium parameter set is still incomplete.

## Completion Standard For This Branch

This branch is considered presentation-prep complete when every phase has at least one local artifact, every nontrivial number is source-backed or labeled as an assumption, and the remaining hard scientific gaps are explicit.
