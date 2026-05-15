# Master Specification: Produced-Water Lithium Extraction Case Study with ePC-SAFT, IDAES ALAMO, and PrOMMiS

**Document status:** controlling planning and execution specification for the next coding-agent run.  
**Project:** `tannerpolley/Lithium_Extraction`  
**Companion dependency:** `tannerpolley/prommis` installed as a pinned Git dependency.  
**Primary objective:** create a clean, successful, notebook-driven case study that demonstrates how lithium extraction from produced water can be modeled through a thermodynamics-to-process-model workflow.

This document replaces the earlier loose agent plans. When this document conflicts with older prompts, deck notes, task boards, or diagnostic handoffs, this document wins.

---

## 0. Executive intent

The case study is not intended to prove that a specific produced-water source and a specific solvent system are the commercially optimal lithium extraction process. The case study is intended to prove that the team can build the workflow:

```text
source-backed produced-water feed information
        → simplified Li/Na extraction input space
        → source-anchored stage-response data
        → IDAES ALAMO surrogate
        → IDAES SurrogateBlock / PrOMMiS SolventExtraction / MSContactor
        → staged Li/Na extraction results
        → screening TEA and UQ
        → management-ready case-study presentation
```

The project should show how ePC-SAFT-enabled thermodynamics can become a process-facing capability inside the PrOMMiS/IDAES ecosystem. The case study is a demonstration and internal project-escalation package, not a commercial engineering package.

---

## 1. Non-negotiable success-only rule

### 1.1 Required attitude toward validation

The final artifacts must be success artifacts only. Do not present diagnostic failures, unresolved residuals, failed direct closures, failed phase splits, failed regressions, or partial diagnostic outputs as acceptable deliverables.

Agents may use diagnostics privately while developing, but diagnostic failure is never a final deliverable.

### 1.2 Forbidden final-result language

The following terms and ideas must not appear in final deck/report/notebook-facing outputs except in this master specification or in internal scratch comments:

```text
failed
failure
source_mismatch
predictive_budget_exhausted
best-effort LLE
no accepted physical split
collapsed split
diagnostic failure
does not close
unresolved residual
convention scan failed
model failed
partial success
almost works
probably wrong
```

If a direct ePC-SAFT calculation does not produce a validated result, do not make a slide or final report section about the failure. Use the approved fallback path described below.

### 1.3 Completion rule

A coding agent may mark the work as done only if the final requested outputs pass their acceptance checks. If a deliverable cannot be made successful and the approved synthetic fallback does not apply, the agent must stop and report the blocker. It must not submit a diagnostic failure as completion.

### 1.4 The one and only permitted non-factual/synthetic allowance

The only part of the workflow that may use synthetic/fabricated demonstration data is the **stage-response data used to propagate the ALAMO/PrOMMiS/TEA workflow when the ePC-SAFT package is not yet ready**.

This synthetic path is allowed only under the following conditions:

1. The data must be clearly labeled as synthetic demonstration data.
2. The data must be source-paper anchored, not arbitrary random numbers.
3. The data must match the qualitative and approximate quantitative behavior expected from the TBAC/DA DES + TOPO literature.
4. The data must be used only to propagate the downstream workflow: ALAMO, SurrogateBlock, PrOMMiS/MSContactor, screening TEA, and presentation figures.
5. The data must not be presented as experimental evidence.
6. The data must not be presented as direct ePC-SAFT closure.
7. The data must not be used to claim that Smackover produced water has been experimentally validated with this solvent.
8. Every row must contain `row_type`, `model_basis`, `backend_name`, and `direct_epcsaft_closure` fields.
9. The synthetic data path must be deterministic and reproducible from a fixed seed.
10. All non-synthetic project claims, feed chemistry, source-paper facts, dependency statements, and PrOMMiS implementation claims must be correct.

Use these labels exactly:

```text
backend_name = synthetic_source_anchored_demo
model_basis = source_paper_anchored_synthetic_stage_response
row_type = source_anchor | generated_source_domain | generated_produced_water_domain | nominal | corner | validation
synthetic_demo_data = true
direct_epcsaft_closure = false
```

The correct public-facing description is:

```text
The workflow uses source-paper anchors and source-anchored generated stage-response data to demonstrate the ALAMO-to-PrOMMiS case-study pipeline while direct ePC-SAFT closure is being finalized.
```

Do not write that the workflow is using fabricated data in management-facing materials. Use the phrase **source-anchored generated demonstration data**.

---

## 2. Decisions already made

The following decisions are final for the next agent run.

| Decision | Final choice |
|---|---|
| Primary selection criterion | Model-readiness for ePC-SAFT / IDAES / PrOMMiS, not highest commercial extraction performance. |
| Main solvent chemistry | TBAC(1):DA(2) hydrophobic DES + TOPO. |
| Nominal TOPO loading | 10 wt% TOPO in the organic solvent phase. |
| TOPO UQ range | 5–15 wt% TOPO. |
| Main surrogate inputs | `li_mg_L`, `na_mg_L`, `o_to_a_ratio`, `topo_wt_pct`. |
| Fixed chemistry metadata | TBAC:DA = 1:2, temperature = 23 °C, pH = 10.4, divalents removed upstream. |
| Main surrogate path | IDAES Surrogates API with ALAMO. |
| ALAMO outputs | `logit_k_Li`, `logit_k_Na`. |
| ALAMO availability | Train if ALAMO is available; otherwise load frozen `AlamoSurrogate` JSON. |
| Training-data strategy | Source-paper anchors plus generated source-anchored design points. |
| Design domains | Two-domain design: source-paper-valid domain and produced-water-centered domain. |
| Preferred model if both work | Produced-water-centered result, if validation and boundedness are acceptable. |
| Repository strategy | Lithium-first sandbox. |
| PrOMMiS strategy | Install pinned PrOMMiS dependency. Do not copy PrOMMiS source into Lithium_Extraction. |
| Original notebook | Preserve original PrOMMiS notebook unchanged. Copy it into Lithium_Extraction and revise the copy. |
| TOP + hexane | Legacy tutorial / smoke-test chemistry only. Not the final case-study chemistry. |
| HBTA/TOPO | High-performance benchmark and future solvent path. Not first implementation. |
| Trust Region Framework | Completely excluded. Do not mention or implement. |

---

## 3. Case-study claim

The final case-study claim is:

> This case study demonstrates a produced-water lithium extraction modeling workflow using source-backed produced-water feed information, a TBAC/DA hydrophobic DES + TOPO Li/Na extraction chemistry, IDAES ALAMO surrogate modeling, and a PrOMMiS/IDAES staged solvent-extraction model to propagate feed and operating uncertainty into extraction recovery and screening TEA.

The claim is deliberately about the workflow.

The case study does not claim:

- that this exact solvent is the best commercial solvent for produced water;
- that this exact solvent has been experimentally validated on Smackover produced water;
- that direct ePC-SAFT reactive-LLE closure is complete;
- that the TEA is commercial, vendor-grade, investment-grade, or plant-ready;
- that divalent extraction is solved by the Li/Na model;
- that REEs or other CMMs are implemented in the present case.

---

## 4. Why this solvent system remains the active first implementation

### 4.1 Active solvent system

Use the chemical name:

```text
TBAC(1):DA(2) hydrophobic DES + TOPO
```

or the short name:

```text
TBAC/DA DES + TOPO
```

Do not call the solvent system by author name.

### 4.2 Nominal formulation

```text
DES base: tetrabutylammonium chloride + decanoic acid
TBAC:DA molar ratio: 1:2
Nominal organic phase: 90 wt% TBAC/DA DES + 10 wt% TOPO
TOPO UQ range: 5–15 wt%
Temperature: 23 °C
Aqueous pH: 10.4
```

### 4.3 Literature facts to preserve

The source experimental paper reports:

- TBAC is the hydrogen-bond acceptor.
- Decanoic acid is the hydrogen-bond donor.
- TOPO is the coextractant.
- Response surface methodology was used to optimize lithium extraction and selectivity.
- The optimized condition is TBAC(1)/DA(2), 10 wt% TOPO, 23 °C, pH 10.4.
- One-stage lithium extraction at the optimized point is about 48.57%.
- Selectivity at the optimized point is about 4.41 by the paper’s definition.
- Model-brine lithium extraction is about 51.63%.
- Model-brine co-extraction values are much lower for Na, K, Mg, and Ca.
- FTIR supports Li/H ion-exchange behavior in the DES phase.
- Regeneration/reuse behavior is reported over multiple cycles.

The thermodynamic paper reports:

- The equilibrium system is aqueous Li/Na chloride solution plus organic DES/TOPO phase.
- Li and Na are solvated ions in the aqueous phase.
- In the organic phase, extracted Li and Na are represented as DES-associated neutral complexes RLi and RNa.
- The chemistry is ion exchange, not ordinary same-species LLE.
- PC-SAFT is used for the organic phase.
- ePC-SAFT is used for the aqueous electrolyte phase.
- DES, TOPO, RLi, and RNa have a thermodynamic parameterization path.
- Reported AARD values are about 7.89% for lithium extraction and 8.63% for Li/Na selectivity.
- The SI provides Gibbs-energy construction for TBAC, DA, DES, RLi, and RNa.
- The SI provides density data for DES and 10 wt% TOPO in DES.

### 4.4 Why not switch to TOP + hexane

TOP + hexane is retained only as the old PrOMMiS tutorial chemistry. It is not the final case-study chemistry because:

- TOP and TOPO are different compounds.
- TOP + hexane is not a DES.
- TOP + hexane does not represent the TBAC/DA DES ion-exchange chemistry.
- The existing PrOMMiS notebook used TOP + hexane as a compact interface demonstration.
- The new case study should preserve the interface style, not the chemistry.

### 4.5 Why not use HBTA/TOPO as first implementation

HBTA/TOPO is a strong performance benchmark and future path. It is not the first implementation because:

- it is less directly ready for ePC-SAFT/PrOMMiS integration;
- it requires additional parameterization and reaction modeling;
- kerosene and saponification/scrubbing/stripping introduce extra process complexity;
- the current project priority is model-readiness, not choosing the highest extraction system.

However, HBTA/TOPO should appear in the deck as the high-performance benchmark/future solvent option.

---

## 5. Produced-water source strategy

The case study must show produced-water variability, not just one brine.

### 5.1 Required produced-water roles

| Role | Source | Use |
|---|---|---|
| Main case | Smackover MS-2 | Main flowsheet and TEA case. |
| Sensitivity | Smackover high observed | High-Li sensitivity. |
| Comparison | Marcellus / Appalachian | Comparison card and possible lower-burden feed if chemistry is complete. |
| Stress | Bakken | High-Na/high-salinity stress case. |
| Context/caution | Permian / Wolfcamp | Large water volume but lower Li grade; do not make flagship. |
| Optional comparison | Salton Sea | Geothermal comparison only, not produced water. |

### 5.2 Feed-data rule

Every feed row must include:

```text
feed_id
basin
formation
region
source_type
Li_mg_L
Na_mg_L
K_mg_L
Mg_mg_L
Ca_mg_L
Sr_mg_L
Ba_mg_L
Cl_mg_L
TDS_mg_L
pH
TOC_mg_L
Na_Li_mass_ratio
divalent_Li_mass_ratio
data_quality_flag
simulation_allowed_flag
source_citation
notes
```

If major ions are missing, set:

```text
simulation_allowed_flag = false
```

A feed with missing Na/Ca/Sr/Ba may be shown as a comparison card, but it must not be used for PrOMMiS stage simulation or TEA unless the missing data are source-filled or explicitly isolated as synthetic demonstration data.

### 5.3 Required map and feed-variance visuals

The deck must include a U.S. basin map with at least:

```text
Smackover
Marcellus / Appalachian
Bakken / Williston
Permian / Wolfcamp
optional Salton Sea comparison
```

The map must communicate that:

- lithium concentration varies significantly by basin and formation;
- TDS varies significantly;
- high produced-water volume does not automatically mean a good lithium resource;
- location and proximity to lithium consumers matter.

The deck must include a feed-variance figure or table showing at least:

```text
Li_mg_L
TDS_mg_L
Na_Li_mass_ratio
divalent_Li_mass_ratio
data completeness flag
case-study role
```

---

## 6. Pretreatment boundary

The active extraction model is a Li/Na model after pretreatment.

### 6.1 Active extraction species

```text
Li
Na
```

### 6.2 Pretreatment/context species

```text
Ca
Mg
Sr
Ba
K
organics
oil
suspended solids
H2S if relevant
```

### 6.3 Pretreatment model role

The pretreatment block is not the main focus. It must exist as a mass-balance and cost/loss sensitivity layer. It should include:

```text
pretreatment_li_loss_pct
residual_divalent_flag
organics_pretreatment_flag
pretreatment_cost_usd_per_m3
```

The main deck must state:

```text
Raw produced water is not the Li/Na extraction feed. Divalent ions and organics are handled upstream as pretreatment, loss, and cost variables.
```

### 6.4 No hidden divalent extraction

Do not silently include Ca/Mg/Sr/Ba extraction in the Li/Na solvent extraction model. If divalent leakage is shown, it must be a guardrail/sensitivity variable, not part of the active extraction chemistry.

---

## 7. Simplified input-space philosophy

The original PrOMMiS notebook was valuable because it had a simple process-facing input interface. Preserve that philosophy.

### 7.1 Main ALAMO inputs

Use exactly:

```text
li_mg_L
na_mg_L
o_to_a_ratio
topo_wt_pct
```

### 7.2 Fixed metadata

Use:

```text
solvent_base = TBAC(1):DA(2) hydrophobic DES
TBAC_to_DA_molar_ratio = 1:2
temperature_C = 23
aqueous_pH = 10.4
pretreatment_basis = divalents removed upstream
chloride_transfer_allowed = false
```

### 7.3 Variables not in the main ALAMO input set

Do not include these in the main ALAMO input set:

```text
TDS
feed_id
Ca
Mg
Sr
Ba
K
TOC
pH
temperature
plant_location
stage_count
solvent_loss
pretreatment_li_loss
product_value
```

These belong to metadata, TEA sensitivity, process sensitivity, or backup analysis. Do not turn the main surrogate into a broad optimization problem.

---

## 8. Two-domain design

### 8.1 Purpose

Use two domains:

```text
Domain A: source-paper-valid domain
Domain B: produced-water-centered domain
```

Run both. Prefer the produced-water-centered domain if it passes validation, boundedness, and plausibility checks.

### 8.2 Domain A: source-paper-valid domain

This domain protects scientific credibility.

```text
li_mg_L: 1000–2000
na_li_mass_ratio: 5–25
o_to_a_ratio: 0.5–1.5
topo_wt_pct: 5–15
pH: fixed 10.4
temperature_C: fixed 23
```

Because the ALAMO input column must be `na_mg_L`, derive:

```text
na_mg_L = li_mg_L * na_li_mass_ratio
```

Then store `na_li_mass_ratio` as a derived metadata column.

### 8.3 Domain B: produced-water-centered domain

This domain supports the actual produced-water case-study narrative and UQ.

```text
li_mg_L: 80–300
na_mg_L: 10,000–90,000
o_to_a_ratio: 0.5–2.0
topo_wt_pct: 5–15
pH: fixed 10.4
temperature_C: fixed 23
```

### 8.4 Sampling

Generate:

```text
625 source-domain LHS rows
625 produced-water-domain LHS rows
all available source-anchor rows
nominal rows
16–32 corner/stress rows
```

Use Latin hypercube sampling with a fixed seed.

### 8.5 Required design columns

```text
design_id
domain
row_type
li_mg_L
na_mg_L
na_li_mass_ratio
o_to_a_ratio
topo_wt_pct
temperature_C
aqueous_pH
solvent_base
TBAC_to_DA_molar_ratio
source_anchor_flag
synthetic_demo_data
model_basis
backend_name
direct_epcsaft_closure
validity_flag
extrapolation_flag
```

---

## 9. Stage-response generation

### 9.1 Preferred path when ePC-SAFT is ready

If the ePC-SAFT package can generate accepted Li/Na transfer values successfully, use it. Accepted means:

- no model failure;
- no diagnostic-only result;
- physically bounded extraction fractions;
- finite outputs;
- reproducible results;
- source anchors reproduced within declared tolerance;
- no hidden unvalidated assumptions.

### 9.2 Approved fallback path when ePC-SAFT is not ready

If the ePC-SAFT package is not ready, use the synthetic source-anchored demonstration stage-response generator.

The generator must be deterministic and source-anchored.

Use source anchors such as:

```text
optimized condition: 10 wt% TOPO, 23 °C, pH 10.4
one-stage Li extraction near 48.57%
source-paper selectivity near 4.41 by source-paper definition
model-brine Li extraction near 51.63%
model-brine Na extraction near 9.97%
low K/Mg/Ca extraction in model-brine context
```

The generated data must show plausible monotonic and interaction behavior:

- Li extraction should generally improve with O/A ratio.
- Li extraction should generally improve near the 10 wt% TOPO optimum and not behave wildly outside 5–15 wt%.
- Na co-extraction should remain meaningfully lower than Li extraction.
- Higher Na burden should reduce selectivity and/or increase Na co-extraction pressure.
- Outputs must stay bounded.

### 9.3 Required output columns

The stage-response data must include:

```text
design_id
domain
row_type
li_mg_L
na_mg_L
na_li_mass_ratio
o_to_a_ratio
topo_wt_pct
k_Li
k_Na
logit_k_Li
logit_k_Na
Li_extraction_pct
Na_extraction_pct
D_Li
D_Na
Li_Na_selectivity_process
Li_Na_selectivity_source_definition
validity_flag
extrapolation_flag
synthetic_demo_data
model_basis
backend_name
direct_epcsaft_closure
```

### 9.4 Transformations

Use:

```text
k_i = extraction fraction for species i
logit_k_i = log(k_i / (1 - k_i))
Li_extraction_pct = 100 * k_Li
Na_extraction_pct = 100 * k_Na
D_i = k_i / ((1 - k_i) * o_to_a_ratio)
process_selectivity = D_Li / D_Na
```

Clip only for numerical stability, and record clipping if used:

```text
eps = 1e-6
k_i_clipped = min(max(k_i, eps), 1 - eps)
```

---

## 10. IDAES ALAMO surrogate requirements

### 10.1 Main surrogate path

Use the IDAES Surrogates API, not a hand-coded polynomial as the main model.

The workflow is:

```text
training data DataFrame
        → AlamoTrainer
        → trained expressions
        → AlamoSurrogate
        → save JSON
        → load JSON if needed
        → SurrogateBlock
```

IDAES v2.6.0 documentation says the Surrogates API supports ALAMOPY, PySMO, and OMLT/Keras; it also describes loading/generated datasets as Pandas DataFrames, creating an `AlamoTrainer`, building an `AlamoSurrogate`, saving/loading JSON, and populating a `SurrogateBlock`.

### 10.2 Primary ALAMO inputs

```text
input_labels = ["li_mg_L", "na_mg_L", "o_to_a_ratio", "topo_wt_pct"]
```

### 10.3 Primary ALAMO outputs

```text
output_labels = ["logit_k_Li", "logit_k_Na"]
```

Do not train the primary ALAMO model directly on percent extraction or distribution ratios. Those are derived reporting quantities.

### 10.4 Output bounds and transformations

ALAMO predicts logit values. Convert to extraction fractions inside the process model or immediately after surrogate evaluation:

```text
k_i = 1 / (1 + exp(-logit_k_i))
```

This prevents the surrogate from producing negative extraction fractions or extraction fractions above 1.

### 10.5 ALAMO availability modes

The notebook and scripts must support two modes:

```text
train_alamo
load_frozen_alamo
```

#### train_alamo

Use when the ALAMO executable/license is available.

Required outputs:

```text
models/tbac_da_topo_alamo_surrogate.json
data/processed/tbac_da_topo_alamo_training_data.csv
data/processed/tbac_da_topo_alamo_validation_data.csv
results/tbac_da_topo_alamo_validation.md
figures/alamo_parity_logit_k_Li.png
figures/alamo_parity_logit_k_Na.png
figures/alamo_residual_logit_k_Li.png
figures/alamo_residual_logit_k_Na.png
```

#### load_frozen_alamo

Use when ALAMO is unavailable. Load:

```text
models/tbac_da_topo_alamo_surrogate.json
```

Do not require retraining to run the notebook.

### 10.6 License rule

Do not commit ALAMO license text, license keys, license files, email addresses, or license IDs. A local machine may have ALAMO licensed, but the repository must not contain license details.

### 10.7 Validation metrics

Report at minimum:

```text
R2_logit_k_Li
RMSE_logit_k_Li
MAE_logit_k_Li
R2_logit_k_Na
RMSE_logit_k_Na
MAE_logit_k_Na
max_abs_error_logit_k_Li
max_abs_error_logit_k_Na
boundedness_pass
source_anchor_agreement_pass
produced_water_domain_pass
selected_domain
```

### 10.8 No ALAMO failure artifacts

If ALAMO cannot train and no frozen JSON exists, the task is not complete. Do not create a report about ALAMO failure as the final deliverable.

---

## 11. PrOMMiS / IDAES implementation requirements

### 11.1 Repository approach

Develop in `Lithium_Extraction`. Install `prommis` as a pinned dependency. Do not copy PrOMMiS source into `Lithium_Extraction`.

### 11.2 Dependency pin

Add this to `Lithium_Extraction/pyproject.toml`:

```toml
"prommis @ git+https://github.com/tannerpolley/prommis.git@f2be79b8878edb2c6e56be6998f4d9388aa1a348",
```

Current `Lithium_Extraction` already pins `epcsaft` and includes numerical/scientific dependencies. Add PrOMMiS and notebook execution dependencies.

Recommended dependency block:

```toml
dependencies = [
    "epcsaft @ git+https://github.com/tannerpolley/ePC-SAFT.git@255ca07fbce7a2842aaea353fd626ab297af6067",
    "prommis @ git+https://github.com/tannerpolley/prommis.git@f2be79b8878edb2c6e56be6998f4d9388aa1a348",
    "matplotlib>=3.8",
    "numpy>=1.26",
    "pandas>=2.2",
    "scipy>=1.12",
    "nbformat>=5.10",
    "nbclient>=0.10",
    "ipykernel>=6.29",
]
```

PrOMMiS brings `idaes-pse` and `pyomo` through its own dependencies.

### 11.3 Local prototype namespace

If helper modules are needed, place them under:

```text
src/lithium_extraction/prommis_case_study/
```

Do not create:

```text
src/prommis/
```

inside `Lithium_Extraction`.

### 11.4 Real PrOMMiS claim requirement

A result can be called PrOMMiS/IDAES output only if it uses the real PrOMMiS/IDAES path:

```text
prommis.solvent_extraction.solvent_extraction.SolventExtraction
IDAES MSContactor
explicit material_transfer_term constraints
degrees_of_freedom(model) == 0
actual solve or successful initialization/evaluation
```

Algebraic postprocessing can be used only as a precheck. It must be labeled:

```text
algebraic_precheck
```

not PrOMMiS output.

### 11.5 Transfer convention

The PrOMMiS `MSContactor` consumes extraction fractions.

For each species `i`:

```text
material_transfer_term[t, stage, ("aqueous", "organic", i)]
    = - aqueous_inlet_material_flow_i * k_i
```

where:

```text
k_i = one-stage extraction fraction for species i
```

If only distribution ratio is available:

```text
k_i = D_i * o_to_a_ratio / (1 + D_i * o_to_a_ratio)
```

For this case study, the primary ALAMO surrogate predicts `logit_k_i`, so use:

```text
k_i = inverse_logit(logit_k_i)
```

### 11.6 Transfer species

For the active Li/Na model:

```text
transfer_species = ["Li", "Na"]
chloride_transfer_allowed = false
```

Do not transfer chloride unless a validated chemistry basis requires it.

### 11.7 Minimal local PrOMMiS wrapper components

Create only what is needed for the case-study wrapper:

```text
src/lithium_extraction/prommis_case_study/tbac_da_topo_aq_properties.py
src/lithium_extraction/prommis_case_study/tbac_da_topo_org_properties.py
src/lithium_extraction/prommis_case_study/tbac_da_topo_transfer_reactions.py
src/lithium_extraction/prommis_case_study/tbac_da_topo_mscontactor.py
src/lithium_extraction/prommis_case_study/alamo_bridge.py
```

These may import `prommis.solvent_extraction.solvent_extraction.SolventExtraction`.

### 11.8 Acceptance checks for PrOMMiS wrapper

The PrOMMiS wrapper must demonstrate:

```text
import prommis succeeds
import idaes succeeds
import pyomo succeeds
SolventExtraction object exists
MSContactor object exists
Li material transfer constraint active
Na material transfer constraint active
Cl transfer absent or inactive
degrees_of_freedom == 0
Li aqueous outlet decreases
Na aqueous outlet decreases less than Li in nominal case
organic outlet Li equivalent increases
mass balance residual is reported and within tolerance
```

Do not accept a result without these checks.

---

## 12. Notebook requirements

### 12.1 Original notebook preservation

Do not edit:

```text
prommis/docs/tutorials/pcsaft_lithium_sodium_case_study.ipynb
```

Create the revised copy in `Lithium_Extraction`:

```text
docs/tutorials/tbac_da_topo_produced_water_case_study.ipynb
```

### 12.2 Notebook purpose

The notebook must demonstrate the complete successful workflow:

```text
source-backed case-study basis
        → two-domain design
        → source-anchored stage-response generation
        → ALAMO training or frozen JSON loading
        → SurrogateBlock
        → PrOMMiS SolventExtraction / MSContactor
        → staged results
        → screening TEA / UQ outputs
```

### 12.3 Notebook sections

Use this notebook structure:

1. Case-study purpose and scope.
2. Original notebook preservation statement.
3. Imports and backend selection.
4. Source-backed solvent and feed basis.
5. Simplified four-variable input interface.
6. Source anchors.
7. Two-domain generated design.
8. Stage-response generation.
9. ALAMO training or frozen ALAMO loading.
10. ALAMO validation plots.
11. SurrogateBlock embedding.
12. PrOMMiS single-stage model.
13. PrOMMiS 1–5 stage sensitivity.
14. Produced-water source sensitivity.
15. Screening TEA / UQ.
16. Figures exported for deck.
17. Final success summary.

### 12.4 Notebook success requirement

The notebook must execute end to end in either:

```text
train_alamo
```

or:

```text
load_frozen_alamo
```

mode.

No failed cell output may remain in the notebook.

---

## 13. Screening TEA and UQ requirements

### 13.1 TEA framing

All economics are screening-level.

Allowed language:

```text
screening TEA
screening breakeven
screening margin
reference-value margin
hypothetical margin
```

Avoid:

```text
profit
commercial TEA
bankable economics
plant-ready economics
investment-grade economics
```

If the word profit is used at all, it must be explicitly qualified as hypothetical screening profit. Prefer margin.

### 13.2 TEA variables

Separate chemistry/process variables from TEA variables.

Chemistry/process variables:

```text
li_mg_L
na_mg_L
o_to_a_ratio
topo_wt_pct
stage_count
```

TEA/UQ variables:

```text
feed_flow_m3_day
pretreatment_li_loss_pct
solvent_loss_rate
solvent_makeup_cost_usd_kg
stripping_regeneration_cost_usd_m3
plant_location_case
product_value_usd_kg_Li2CO3
fixed_cost_multiplier
operating_cost_multiplier
```

### 13.3 Required TEA assumptions register

Create:

```text
data/reference/tea/tbac_da_topo_tea_assumption_register.csv
```

Required columns:

```text
assumption_id
assumption_name
value
units
source_type
source_reference
status
notes
```

Allowed `source_type` values:

```text
source_backed
engineering_assumption
placeholder_for_screening
synthetic_demo_only
```

### 13.4 Required TEA output columns

```text
case_id
feed_id
location_case
stage_count
li_recovery_pct
na_recovery_pct
pretreatment_li_loss_pct
topo_wt_pct
o_to_a_ratio
feed_flow_m3_day
Li2CO3_equiv_kg_year
solvent_loss_rate
screening_cost_usd_year
screening_breakeven_usd_kg_Li2CO3
reference_value_usd_kg_Li2CO3
screening_margin_usd_year
synthetic_demo_data
model_basis
backend_name
validity_flag
```

### 13.5 Plant-location sensitivity

Use simple location multipliers rather than a full GIS model.

Required location cases:

```text
smackover_south_arkansas
appalachian_marcellus
bakken_williston
permian_wolfcamp
salton_sea_reference
```

Location variables:

```text
brine_handling_multiplier
transport_shipping_multiplier
disposal_reinjection_credit
energy_operating_multiplier
proximity_to_battery_manufacturing_score
```

---

## 14. Presentation requirements

### 14.1 Core message

The deck must become a case-study / workflow demonstration deck, not an ePC-SAFT lecture.

The old March presentation was correct for its prior context: it was a package-capability and integration-status deck. The revised product is a case-study deck.

### 14.2 Main deck size

```text
main deck: 12–14 slides
backup: 8–12 slides
```

### 14.3 Required main-deck slide sequence

Use this sequence:

1. Internal project ask.
2. Case-study description.
3. Why produced water and why source variability matters.
4. U.S. basin map and feed-variance summary.
5. Selected feed cases and pretreatment boundary.
6. Solvent-system choice and why it is model-ready.
7. What ePC-SAFT enables now that was not possible before.
8. ALAMO surrogate workflow and two-domain design.
9. PrOMMiS/IDAES MSContactor workflow.
10. Base staged extraction result.
11. Sensitivity/UQ: concentration, O/A, TOPO, source/location.
12. Screening TEA and margin/breakeven sensitivity.
13. External-function / ePC-SAFT-PSE roadmap.
14. Roadmap and ask.

### 14.4 Required backup slides

Include backup slides for:

- source-paper anchors;
- solvent scorecard: TBAC/DA DES + TOPO, HBTA/TOPO, TOP + hexane, IL systems, FeCl3 systems;
- ALAMO training/validation details;
- PrOMMiS transfer convention;
- TEA assumption register;
- CMM/REE extension table;
- hydrocarbon VLE/LLE and produced-water organics;
- ePC-SAFT theory details;
- feed table and data-completeness flags.

### 14.5 Mentor-feedback coverage

The deck must address all of the following, except trust regions:

| Mentor feedback item | Required treatment |
|---|---|
| Case study description | Opening workflow slide. |
| Produced-water source sensitivity | Map and feed-variance slide. |
| Li concentration and TDS variation | Feed-variance figure. |
| Concentration sensitivity | ALAMO/UQ results with `li_mg_L` and `na_mg_L`. |
| Solvent sensitivity | `topo_wt_pct` UQ range 5–15 and solvent scorecard in backup. |
| Plant location | Location multiplier sensitivity and map. |
| Use better surrogates / ALAMO | IDAES ALAMO main surrogate path. |
| Trust Region Framework | Excluded. Do not include. |
| External function / IAPWS / REAKTORO-PSE analogy | Roadmap slide only. |
| CMM/REE extension | Table/collage readiness tiers. |
| What can be done now | ePC-SAFT gap slide. |
| Best EoS | Phrase as best fit for this problem class, not universal best. |
| Activity coefficient limitations | Explain transferability/data limits. |
| Hydrocarbon VLE | Backup slide as adjacent enabled case. |

### 14.6 ePC-SAFT gap slide

The slide must explain why ePC-SAFT fills a gap where other thermodynamic models are weaker.

Use this comparison:

| Before / with conventional approaches | With ePC-SAFT + ALAMO + PrOMMiS |
|---|---|
| Literature extraction efficiencies stay isolated from process simulation. | Literature chemistry becomes process-facing transfer variables. |
| Activity-coefficient models often need system-specific binary data. | ePC-SAFT provides a molecular EoS basis for aqueous electrolyte + organic/DES phases. |
| Empirical distribution coefficients are difficult to transfer across feeds and solvents. | ePC-SAFT provides a path to activity, density, ion transfer, and phase-equilibrium variables. |
| Produced-water variability is hard to propagate through a flowsheet. | ALAMO and PrOMMiS propagate Li, Na, O/A, and TOPO uncertainty to recovery and cost. |
| Non-aqueous electrolyte behavior is hard to generalize. | Born/dielectric ePC-SAFT creates a physical path for ion solvation and transfer. |
| Thermodynamics and process modeling are disconnected. | SurrogateBlock/MSContactor connects stage chemistry to process and TEA. |

Do not say ePC-SAFT is universally the best EoS. Say:

```text
ePC-SAFT is the best-fit thermodynamic engine for this problem class because it can connect high-salinity aqueous electrolytes, non-aqueous organic/DES phases, ion transfer, and process-facing surrogate variables in one molecular EoS framework.
```

### 14.7 CMM/REE extension table

Use readiness tiers:

| Tier | Species/examples | Message |
|---|---|---|
| Implemented case | Li, Na | Active workflow demonstration. |
| Produced-water interferents | K, Mg, Ca, Sr, Ba, Mn | Feed/pretreatment/sensitivity layer. |
| Near-term ePC-SAFT ion-parameter path | V3+, VO2+, common salts | Extension route shown by recent ePC-SAFT parameter work. |
| Future CMM/REE | Co, Ni, Mn, Sc, Y, La–Lu | Requires parameters, solvent chemistry, and validation data. |
| Organic/produced-water contaminants | hydrocarbons, H2S, TOC species | Relevant to pretreatment and solvent loss. |

### 14.8 Hydrocarbon VLE/LLE backup slide

Add one backup slide:

```text
Adjacent cases enabled by the same thermodynamic infrastructure:
- hydrocarbon/water/brine VLE and LLE;
- CO2/H2S-containing brines;
- produced-water organics and solvent contamination;
- solvent loss to hydrocarbon/aqueous phases;
- oil/brine/organic partitioning;
- extraction-process solvent management.
```

Do not make hydrocarbon VLE a main lithium case-study claim.

---

## 15. External-function / ePC-SAFT-PSE roadmap

### 15.1 Current implementation

```text
source-anchored generated stage-response data
        → IDAES ALAMO
        → AlamoSurrogate JSON
        → IDAES SurrogateBlock
        → PrOMMiS SolventExtraction / MSContactor
```

### 15.2 Near-term roadmap

```text
ePC-SAFT-PSE / external-function-style block
        → direct property/equilibrium calls
        → IDAES-compatible variables
        → PrOMMiS unit models
```

### 15.3 Analogy

It is acceptable to compare the architecture to:

```text
IAPWS-style property solver coupling
REAKTORO-PSE-style external equilibrium coupling
```

But do not claim the ePC-SAFT external-function package already exists unless it is actually implemented and tested.

---

## 16. File and artifact plan

### 16.1 Required new or revised files in Lithium_Extraction

```text
pyproject.toml

docs/tutorials/tbac_da_topo_produced_water_case_study.ipynb

docs/plans/tbac_da_topo_success_only_case_study_spec.md

data/reference/produced_water/selected_case_study_feeds.csv
data/reference/produced_water/produced_water_feed_source_register.csv
data/reference/tea/tbac_da_topo_tea_assumption_register.csv

data/processed/tbac_da_topo_two_domain_lhs_design.csv
data/processed/tbac_da_topo_stage_response_data.csv
data/processed/tbac_da_topo_alamo_training_data.csv
data/processed/tbac_da_topo_alamo_validation_data.csv
data/processed/tbac_da_topo_prommis_stage_results.csv
data/processed/tbac_da_topo_screening_tea_results.csv

models/tbac_da_topo_alamo_surrogate.json

results/tbac_da_topo_alamo_validation.md
results/tbac_da_topo_prommis_stage_results.md
results/tbac_da_topo_screening_tea.md
results/tbac_da_topo_success_gate_report.md

src/lithium_extraction/prommis_case_study/__init__.py
src/lithium_extraction/prommis_case_study/backend.py
src/lithium_extraction/prommis_case_study/stage_response_generator.py
src/lithium_extraction/prommis_case_study/alamo_surrogate.py
src/lithium_extraction/prommis_case_study/tbac_da_topo_aq_properties.py
src/lithium_extraction/prommis_case_study/tbac_da_topo_org_properties.py
src/lithium_extraction/prommis_case_study/tbac_da_topo_transfer_reactions.py
src/lithium_extraction/prommis_case_study/tbac_da_topo_mscontactor.py
src/lithium_extraction/prommis_case_study/screening_tea.py

slides/case_study_tbac_da_topo_produced_water/deck.qmd
slides/case_study_tbac_da_topo_produced_water/figures/
```

### 16.2 Tests

Create tests under:

```text
tests/test_tbac_da_topo_stage_response.py
tests/test_tbac_da_topo_alamo_contract.py
tests/test_tbac_da_topo_prommis_mscontactor.py
tests/test_tbac_da_topo_tea_schema.py
tests/test_case_study_no_forbidden_diagnostics.py
```

### 16.3 Required success report

Create:

```text
results/tbac_da_topo_success_gate_report.md
```

It must contain only success checks and pass/fail status. If a required check fails, the final task is not done.

---

## 17. Success gates

### 17.1 Environment gate

Commands must pass:

```text
uv sync
uv run python -c "import prommis, idaes, pyomo; print('imports ok')"
uv run python -c "import epcsaft; print('epcsaft import ok')"
```

If `epcsaft` imports but direct calculations are not ready, use the approved synthetic demonstration data path.

### 17.2 Data gate

Pass if:

- selected feed table exists;
- every feed row has source/data-quality fields;
- incomplete feeds have `simulation_allowed_flag=false`;
- no incomplete feed is used in TEA unless explicitly synthetic demonstration mode;
- two-domain design exists;
- generated stage-response data is bounded and deterministic.

### 17.3 ALAMO gate

Pass if:

- ALAMO trains and saves JSON, or frozen JSON loads successfully;
- `models/tbac_da_topo_alamo_surrogate.json` exists;
- validation data exists;
- validation report exists;
- all outputs are finite;
- `logit_k_Li` and `logit_k_Na` are the primary outputs.

### 17.4 PrOMMiS gate

Pass if:

- real PrOMMiS import works;
- real `SolventExtraction` object is used;
- `MSContactor` object exists;
- Li and Na transfer constraints are active;
- degrees of freedom are zero;
- one-stage nominal run produces finite outlet streams;
- staged 1–5 results are produced;
- mass balance residual is within tolerance;
- chloride transfer is absent or explicitly inactive.

### 17.5 Notebook gate

Pass if:

- copied notebook exists;
- original PrOMMiS notebook is not edited;
- copied notebook executes end to end;
- no failed cell outputs remain;
- notebook exports training, ALAMO, PrOMMiS, TEA, and figures.

### 17.6 Deck gate

Pass if:

- deck renders;
- map figure exists;
- feed-variance figure exists;
- ALAMO figure exists;
- PrOMMiS workflow figure exists;
- screening TEA/UQ figure exists;
- CMM/REE table exists;
- hydrocarbon VLE backup exists;
- Trust Region Framework is absent;
- diagnostic failure terms are absent.

### 17.7 Forbidden diagnostic scan gate

Run a scan over final docs, deck, notebook markdown cells, and reports for forbidden terms listed in Section 1.2.

The scan must pass.

Do not scan raw scratch logs or developer-only temporary files if they are not committed or delivered.

---

## 18. Agent execution plan

Use one agent or up to three agents, but vertical slices must preserve the success-only rule.

### Agent Slice 1 — Setup, source data, notebook copy, and design

Scope:

- update `pyproject.toml` with pinned PrOMMiS;
- copy original notebook into Lithium_Extraction;
- create source/feed registers;
- create two-domain design generator;
- create synthetic/source-anchored stage-response generator if ePC-SAFT not ready;
- create tests for schemas and bounded outputs.

Done only if:

- environment imports pass;
- notebook copy exists;
- source and design data exist;
- bounded stage-response data exists.

### Agent Slice 2 — ALAMO and PrOMMiS wrapper

Scope:

- build IDAES ALAMO trainer/loader path;
- train or load `AlamoSurrogate` JSON;
- build `SurrogateBlock` integration;
- build local PrOMMiS wrapper using real `SolventExtraction` and `MSContactor`;
- produce single-stage and multistage process results.

Done only if:

- ALAMO JSON exists and loads;
- PrOMMiS model has DOF 0;
- Li/Na transfer constraints are active;
- stage results exist and pass mass-balance checks.

### Agent Slice 3 — TEA, deck, notebook execution, and success gate

Scope:

- execute copied notebook;
- build TEA assumption register;
- generate screening TEA/UQ;
- revise deck;
- add mentor-feedback slides;
- render deck;
- create success-gate report.

Done only if:

- notebook executes;
- deck renders;
- success report passes all gates;
- forbidden diagnostic scan passes.

---

## 19. Exact agent prompt block

Use this block to start the next coding agent:

```text
You are implementing the Lithium_Extraction produced-water lithium extraction case study. Read docs/plans/tbac_da_topo_success_only_case_study_spec.md first and treat it as the controlling specification.

Hard rule: final deliverables must be success artifacts only. Diagnostic failures are not acceptable deliverables. Failed direct ePC-SAFT calculations, failed phase splits, failed regressions, convention-scan failures, or partial diagnostic outputs cannot be used as completion evidence.

The only permitted synthetic/non-factual data is source-anchored generated demonstration stage-response data used to propagate the ALAMO → PrOMMiS → TEA workflow if the ePC-SAFT package is not ready. That data must be clearly labeled with backend_name=synthetic_source_anchored_demo, model_basis=source_paper_anchored_synthetic_stage_response, synthetic_demo_data=true, and direct_epcsaft_closure=false. All other project claims, dependencies, feed data, process-model claims, notebook behavior, and presentation content must be correct and passing.

Implement the Lithium-first sandbox. Do not copy the PrOMMiS source tree into Lithium_Extraction. Install/import PrOMMiS through a pinned Git dependency. Preserve the original PrOMMiS notebook and create a revised copy in Lithium_Extraction.

Use the active solvent system TBAC(1):DA(2) hydrophobic DES + TOPO. Nominal TOPO is 10 wt%; UQ range is 5–15 wt%. The main ALAMO inputs are li_mg_L, na_mg_L, o_to_a_ratio, and topo_wt_pct. Fixed metadata are pH=10.4, temperature=23 C, TBAC:DA=1:2, and divalents removed upstream.

Use IDAES ALAMO as the main surrogate path. Primary ALAMO outputs are logit_k_Li and logit_k_Na. Train ALAMO if available; otherwise load the frozen AlamoSurrogate JSON. Save/load via IDAES AlamoSurrogate JSON and embed through IDAES SurrogateBlock.

Use a two-domain design: source-paper-valid domain and produced-water-centered domain. Prefer the produced-water-centered result if validation and boundedness are acceptable.

Use real PrOMMiS/IDAES only if the model imports prommis, builds SolventExtraction/MSContactor, has active Li/Na material_transfer_term constraints, has degrees_of_freedom == 0, and reports successful mass balance. Algebraic postprocessing is only a precheck and must not be called PrOMMiS output.

Do not include Trust Region Framework content. Do include a produced-water basin map, feed-variance sensitivity, ALAMO surrogate slide, ePC-SAFT gap slide, external-function/ePC-SAFT-PSE roadmap, CMM/REE extension table, screening TEA/UQ, and hydrocarbon VLE/LLE backup slide.

Completion requires a rendered deck, executed notebook, ALAMO JSON, PrOMMiS stage results, screening TEA outputs, and a success-gate report with all gates passing. If any gate fails and the synthetic stage-response fallback does not apply, stop and report the blocker instead of submitting diagnostic failure outputs.
```

---

## 20. Final product definition

At the end of the successful run, the project should contain:

1. A copied and revised notebook in `Lithium_Extraction/docs/tutorials/`.
2. A reproducible environment with pinned PrOMMiS dependency.
3. Source-backed produced-water feed and source registers.
4. A two-domain design table.
5. Stage-response data that is either accepted ePC-SAFT output or clearly labeled source-anchored generated demonstration data.
6. An IDAES ALAMO surrogate JSON.
7. An ALAMO validation report and plots.
8. A real PrOMMiS/IDAES `SolventExtraction` / `MSContactor` wrapper and results.
9. Screening TEA/UQ outputs and assumption register.
10. A case-study deck that covers mentor feedback, without trust regions.
11. A success-gate report that contains only passing final gates.

The management message should be:

> This project demonstrates that produced-water lithium extraction chemistry can be converted into a process-facing ALAMO surrogate and PrOMMiS/IDAES staged extraction workflow, using ePC-SAFT-compatible chemistry as the long-term thermodynamic engine. The immediate ask is an internal integration and validation sprint, not commercial plant funding.

---

## 21. Source basis and literature roles

Use the attached papers as evidence. Do not invent source-paper facts.

| Source group | Role in this case study |
|---|---|
| TBAC/DA DES + TOPO experimental RSM paper | Main solvent selection, source anchors, RSM behavior, optimum point, regeneration support. |
| TBAC/DA DES + TOPO PC-SAFT/ePC-SAFT paper and SI | Thermodynamic model path, DES/TOPO/RLi/RNa parameterization, density/Gibbs-energy basis. |
| Shan oil and gas field water paper | Pretreatment and interference evidence; Ca/Mg must be removed before Li extraction. |
| Zhang HBTA/TOPO/kerosene paper | High-performance process benchmark and mixer-settler analog. |
| Hanada synergistic DES paper | Alternative DES concept and future chemistry option. |
| Jang shale gas produced-water paper | Produced-water pretreatment baseline and Li-loss caution. |
| Lee organic-compound paper | Produced-water organics/TOC risk and pretreatment rationale. |
| Gerardo & Song produced-water siting paper | Produced-water map, basin comparison, location/siting logic. |
| Almousa oilfield feasibility paper | Produced-water opportunity and DLE technology framing. |
| Yang low-quality brines review | Low-quality-brine motivation and DLE context. |
| Kanagasundaram solvent extraction review | Definitions, Li coordination challenge, extraction metrics. |
| Yu and Hubach IL/ePC-SAFT papers | ePC-SAFT credibility only; not final solvent if ILs remain excluded. |
| Bülow/Ascani/Held ePC-SAFT advanced papers | Why Born/dielectric ePC-SAFT fills the non-aqueous electrolyte gap. |
| Figiel/Yu/Held modified Born paper | Package-upgrade and future CMM ion-parameter path. |
| Raiguel D2EHDTPA/BuPhen paper | Future high-selectivity solvent option. |
| Ji/Kia FeCl3/TBP-type papers | Comparator chemistry; not the first implementation. |

---

## 22. Final reminders for agents

- This is a process-demonstration case study.
- Do not overclaim the solvent.
- Do not overclaim ePC-SAFT direct closure.
- Do not submit diagnostic failure as a deliverable.
- Use synthetic source-anchored stage-response data only if needed to propagate the workflow.
- Everything else must be real, correct, passing, and traceable.
- Use ALAMO.
- Use real PrOMMiS imports and unit models.
- Preserve the old notebook.
- Remove trust-region content completely.
- Make the final story clean enough for internal KeyLogic/project escalation.
