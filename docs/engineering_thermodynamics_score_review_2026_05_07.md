# HBTA/TOPO Engineering Thermodynamics Score Review

Date: 2026-05-07

Scope: source-regressed Li/Na HBTA/TOPO stage model, ePC-SAFT/PSE bridge artifacts, PrOMMiS handoff, and downstream IDAES costing. These scores intentionally accept the current divalent-ion assumption: Ca/Mg/Sr/Ba are pretreatment/limitation species until enough source data exists to include competitive multication extraction without fabricating behavior.

## Current Scores And Improvements

| Category | Score | Review | Improvements To Raise Score |
|---|---:|---|---|
| Chemistry-set source relevance | 8.5/10 | HBTA/TOPO/sulfonated kerosene is well chosen for the field-water case. | Add direct Zhang 2017 distribution/capacity data; add source-backed solvent-loss and recycle data; preserve Gando/Shan as the field-water anchor. |
| Chemistry-set completeness | 6/10 | Li/Na is defensible; full Ca/Mg/Ba/Sr chemistry is not parameterized. | Digitize or table-extract Gando cation figures; add alkaline-earth BFA/HBTA/TOPO source records; keep divalents as pretreatment unless fitted independently. |
| Divalent-ion assumption | 8/10 | Pretreatment treatment is supported by Gando Table 2 and process logic. | Quantify residual Ca/Mg after precipitation; model pretreatment reagent needs; add uncertainty for Li loss during pretreatment. |
| Reaction stoichiometry basis | 7/10 | Zhang supports `2 HBTA : 1 TOPO : 1 Li`; Gando mechanism text is closer to `LiBTA.TOPO`, so this needs reconciliation. | Store both species-basis conventions; test whether Zhang's two-HBTA slope result is an apparent slope while Gando reports a saponified exchange form; document the chosen basis in the reaction network. |
| Li/Na fit residuals | 9/10 | Current Gando-stage residuals are about `-0.06`, `+0.12`, and `-0.13` percentage points. | Add independent Zhang 2017 `D_Li`, `D_Na`, O/A, and capacity points; reserve one source as validation if enough points are available. |
| Parameter identifiability | 4.5/10 | `saltout_gain` is weakly identified and the fit Jacobian is ill-conditioned. | Refit with direct distribution data; run profile likelihood or bounded sensitivity; reduce parameter count if the new data cannot identify salt-out separately. |
| Parameter physicality | 6/10 | Parameters are bounded and interpretable, but they are effective-stage constants rather than thermodynamic constants. | Add activity/reaction expressions from Zhang 2017; fit apparent equilibrium constants by basis; separate capacity, salt-out, and complexation effects. |
| Additional fit-data availability | 7.5/10 | Zhang 2017 adds real distribution, capacity, O/A, and temperature data. | Extract all Zhang 2017 tables and digitize Figures 1-5; use Zhang 2018 process data as a process-scale validation check. |
| Equilibrium formulation | 6/10 | The model is a staged mass-action surrogate, not full reactive LLE. | Add explicit reaction extents and component balances; connect aqueous activity and organic capacity consistently; map future full ePC-SAFT requirements. |
| Equilibrium convergence | 8.5/10 | Least-squares solve converges cleanly with low residual norm. | Add seed perturbation tests; add sensitivity over O/A, Li, Na, and TDS; report when stages hit capacity or near-total-transfer limits. |
| ePC-SAFT aqueous activity use | 6.5/10 | Aqueous activity coefficients are called when available; organic phase remains unresolved. | Cache and validate gamma values; compare ideal versus ePC-SAFT sensitivity; add tests for package fallback diagnostics. |
| Organic ePC-SAFT parameters | 3/10 | HBTA, TOPO, sulfonated kerosene, and Li-complex parameters are the main gap. | Search Zotero for density/VLE/SLE data; regress pseudo-components where defensible; use Rezaee 2026 only as method evidence, not chemistry closure. |
| Distribution coefficient treatment | 7/10 | Outputs `D_Li`, `D_Na`, and selectivity, but the current fit underuses Zhang's direct D table. | Replace derived Na point with direct `D_Na`; add `D_Li=33.7` and `D_Na=0.016` as direct targets; store D residuals separately from recovery residuals. |
| Selectivity treatment | 7.5/10 | Conservative Li/Na anchor works, but raw selectivity evidence is sparse. | Add direct Li/Na, Li/K, Li/Mg, and Li/Ca data where solvent chemistry matches; keep cross-solvent selectivity as qualitative comparison. |
| Smackover extrapolation honesty | 8/10 | Feed/extraction distinction is labeled clearly. | Add scenario labels to every exported row; add a one-page uncertainty note for Shan/Gando-to-Smackover transfer. |
| Surrogate-to-PrOMMiS handoff | 8/10 | Stage transfer, D, selectivity, raffinate, and extract values are machine-readable. | Add units and basis checks in tests; add scenario schema validation; pass uncertainty ranges, not only point estimates. |
| MSContactor realism | 5.5/10 | Handoff rows are useful, but not a rigorous PrOMMiS unit solve with hydraulics/residence/design constraints. | Build a true MSContactor example from the handoff table; add phase ratio and residence assumptions; test convergence in the PrOMMiS environment. |
| IDAES costing implementation | 7/10 | Formal Pyomo/IDAES expressions exist and run. | Add explicit flowsheet units or costing blocks where available; test solver-free expression build plus report generation; include provenance for every cost parameter. |
| Costing economic credibility | 4.5/10 | Scenario costing is still Class-5 style; vendor costs and solvent-loss data are missing. | Add solvent price/loss ranges, pretreatment reagent costs, acid/base regeneration costs, concentration energy, and vendor-style contactor scaling. |
| Overall thermodynamic-engine confidence | 6.5/10 | Strong Li/Na staged surrogate, weak full reactive ePC-SAFT closure. | Use Zhang 2017 as the next regression backbone; validate with Zhang 2018 and Gando/Shan; keep full ePC-SAFT as a staged upgrade rather than an implied current result. |

## Highest-Value Next Actions

1. Add Zhang 2017 direct distribution and capacity records to the regression dataset.
2. Digitize Zhang 2017 pH, O/A, temperature, and isotherm figures.
3. Refit the Li/Na model with direct `D_Li`, `D_Na`, capacity, and stage-recovery targets.
4. Add profile/sensitivity diagnostics for `saltout_gain` and capacity.
5. Convert the PrOMMiS handoff into a true MSContactor validation case with uncertainty bands.
6. Replace placeholder costing inputs with source-backed or vendor-style ranges for pretreatment, solvent makeup, acid/base regeneration, and contactor scale.

## Stored Follow-Up Evidence

- `data/reference/produced_water/zotero_lithium_recovery_deep_review_2026_05_07.md` stores the expanded Zotero-derived solvent review and candidate ranking.
- `data/reference/produced_water/zotero_lithium_recovery_candidate_expansion_2026_05_07.csv` stores the scored candidate table, including at least three added candidates beyond the active scorecard.
- `data/reference/produced_water/zotero_lithium_recovery_parameter_fit_opportunities_2026_05_07.csv` stores the parameter/data upgrades most likely to raise these scores.
- `data/reference/produced_water/zotero_lithium_recovery_figure_replication_opportunities_2026_05_07.csv` stores the figure and article-folder revalidation targets.
- `docs/case_study_completion_revalidation_2026_05_07.md` stores the command-level revalidation, MiKTeX finding, PrOMMiS/IDAES costing status, and remaining improvement actions.
