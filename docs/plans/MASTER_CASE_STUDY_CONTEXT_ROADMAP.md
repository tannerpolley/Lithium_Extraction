# Master Context, Roadmap, and Benchmarks: Produced-Water Lithium Extraction with ePC-SAFT

**Project:** Lithium Extraction with ePC-SAFT  
**Working case-study title:** Modeling Lithium Extraction from Produced Water Using ePC-SAFT, TBAC/DA DES + 10 wt% TOPO, and PrOMMiS/IDAES  
**Audience:** Internal KeyLogic/government-contracted technical management and project leads  
**Purpose:** Support internal project formalization, not commercialization funding  
**Status:** Case-study revision and implementation planning document for coding agents

---

## 1. One-sentence project mission

Demonstrate a produced-water lithium solvent-extraction workflow in which ePC-SAFT generates Li/Na extraction thermodynamics and surrogate transfer variables for PrOMMiS/IDAES staged-contactor and screening-TEA calculations.

---

## 2. Why this project exists

The prior presentation was correct for its original purpose: it explained the ePC-SAFT package, validation, multiphase-equilibrium capability, and possible PrOMMiS integration. The new task is not to reject that deck. The new task is to advance it into a concrete case study.

The revised case study must show that the ePC-SAFT package can support an official internal project by connecting:

1. a real produced-water source,
2. a defined solvent-extraction chemistry,
3. thermodynamic distribution/selectivity calculations,
4. surrogate variables for process models,
5. a PrOMMiS/IDAES staged extraction workflow,
6. screening-level cost numbers.

The target decision is internal escalation: approve an official project for ePC-SAFT-to-PrOMMiS/IDAES integration and produced-water lithium case-study development.

This is not a request for full commercialization, pilot-plant funding, or investment-grade TEA.

---

## 3. Required naming convention

Use the chemical solvent name.

**Approved solvent labels:**

- `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`
- `TBAC/DA DES + 10 wt% TOPO`
- `90 wt% TBAC/DA DES + 10 wt% TOPO`

**Do not use the source-author name as the solvent-system name.** The source-author name may appear only in a bibliography, citation list, or legacy file path already present in the repository. Do not use it in slide titles, executive summaries, figure captions, artifact names, or prompts as shorthand for the solvent system.

**New artifact naming:** use `tbac_da_topo`, not author-based names.

**Existing legacy paths:** existing repository folders may retain legacy names for compatibility. Do not rename existing folders unless the repo maintainers explicitly want that cleanup. Create new deck-facing and report-facing outputs with chemical names.

---

## 4. Final accepted case-study claim

Use this claim:

> This case study demonstrates lithium extraction from produced water using a source-backed produced-water feed, upstream divalent/organics pretreatment, TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO for Li/Na solvent extraction, ePC-SAFT-generated or ePC-SAFT-calibrated transfer variables, and PrOMMiS/IDAES staged extraction with screening-level TEA.

Do not claim:

- fully predictive direct reactive-LLE closure unless the direct model passes validation,
- experimental validation on Smackover brine unless such data are actually present,
- solved divalent extraction,
- REE recovery from the selected feed,
- investment-grade TEA,
- commercialization readiness,
- a general lithium-extraction platform for all brines without validity flags.

---

## 5. Final product definition

The final deliverable should look like a compact internal case-study package:

1. **Main presentation:** 10–12 slides, PowerPoint or Beamer, case-study-first.
2. **Backup appendix:** ePC-SAFT theory, literature scorecard, equation details, validation diagnostics, source tables.
3. **Source-backed report:** concise Markdown report with feed basis, solvent basis, model basis, PrOMMiS handoff, TEA assumptions, limitations, and next-phase work.
4. **Clean figures:** no clutter, no raw notebook dumps, no excessive theory figures.
5. **Generated data artifacts:** selected feeds, LHS/LHC input ranges, Li/Na transfer variables, staged-contactor results, screening-TEA results, readiness checklist.

The final presentation should read like a case study enabled by ePC-SAFT, not like a thermodynamics lecture.

---

## 6. Executive story arc for the final deck

Use this order.

1. **Internal project ask**  
   Approve an official internal project to integrate ePC-SAFT lithium-extraction thermodynamics into PrOMMiS/IDAES.

2. **Why produced water**  
   Produced water is a large, variable, lithium-bearing waste stream with existing water-handling infrastructure.

3. **Candidate screening**  
   Smackover, Marcellus, Bakken, and Permian are not equivalent. Chemistry and production rate both matter.

4. **Selected feed cases**  
   Smackover MS-2 is the flagship hard case. Marcellus NE PA is the lower-burden comparison. Bakken is a stress test.

5. **Pretreatment boundary**  
   Raw produced water is not the extraction feed. Ca/Mg/Sr/Ba and organics are pretreatment and guardrail variables.

6. **Solvent system**  
   TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO is selected because it has experimental extraction data, defined Li/Na reactions, and PC-SAFT/ePC-SAFT parameterization support.

7. **Thermodynamic role**  
   ePC-SAFT provides activities, distribution/selectivity diagnostics, density support, validity flags, and surrogate-transfer variables.

8. **Base extraction result**  
   Present the Smackover clean Li/Na extraction result with stage count and Na co-extraction.

9. **Surrogate and validity gate**  
   Show LHS/LHC variables, extrapolation flags, and what PrOMMiS consumes.

10. **PrOMMiS/IDAES workflow**  
    ePC-SAFT-PSE or surrogate block → staged contactor → flowsheet variables → costing.

11. **Screening TEA**  
    Show stress/base/favorable cases and sensitivity to solvent loss, pretreatment Li loss, and stage count.

12. **Roadmap and ask**  
    Fund the integration/validation sprint: direct ePC-SAFT closure, surrogate production, MSContactor implementation, and screening-TEA maturation.

---

## 7. Produced-water feed strategy

### 7.1 Main case: Smackover MS-2

Use Smackover MS-2 as the main flowsheet case.

Known basis:

- Li: `168 mg/L`
- TDS: `305,000 mg/L`
- Na: `64,100 mg/L`
- Ca: `36,900 mg/L`
- Mg: `3,310 mg/L`
- Na/Li mass ratio: approximately `381.5`

Why it is the flagship:

- source-backed row,
- high salinity,
- meaningful Li grade,
- difficult interference profile,
- good demonstration of why thermodynamics and pretreatment matter.

### 7.2 Comparison case: Marcellus NE PA

Use Marcellus NE PA as the lower-burden comparison case.

Current screening basis:

- Li: approximately `205 mg/L`
- TDS: approximately `100,000 mg/L`
- lower divalent/Li burden than Smackover in the screening table

Boundary:

- Fill missing Na/Ca/Sr/Ba from a source before treating this as a full process-simulation feed.
- If those values remain missing, use Marcellus only as a comparison card, not as a full TEA scenario.

### 7.3 Sensitivity case: Smackover high observed

Use as a high-Li Smackover sensitivity case.

Current screening basis:

- Li: approximately `252 mg/L`
- TDS: approximately `340,000 mg/L`
- strong candidate score

### 7.4 Stress case: Bakken high-Li / high-Na

Use as stress test only.

Current screening basis:

- Li: approximately `103 mg/L`
- TDS: approximately `258,193 mg/L`
- Na/Li mass ratio: approximately `771`

Why stress only:

- high salinity and high Na burden,
- useful for surrogate validity testing,
- not the cleanest management flagship.

### 7.5 Do not make Permian the main case

Permian matters because of produced-water volume and operations, but the current lithium grades are weaker. Use it only in the opportunity landscape or screening table unless new high-Li data are added.

---

## 8. Pretreatment boundary

The raw produced water is not the extraction feed.

The active Li/Na extraction model begins after pretreatment removes the divalent and organic burden. The pretreatment block must carry:

- Ca removal,
- Mg removal,
- Sr removal,
- Ba removal,
- suspended solids/oil/organics removal or guardrail,
- pretreatment chemical/cost placeholders,
- Li loss during pretreatment,
- residual-divalent leakage flag.

Divalent ions must not silently enter the Li/Na extraction model. If residual divalent ions are included, they must be labeled as a leakage/validity guardrail, not an active extraction species.

Pretreatment must appear in both process and TEA logic. It cannot be a hidden assumption.

---

## 9. Solvent-system basis

Selected active solvent system:

- DES: tetrabutylammonium chloride and decanoic acid
- DES molar ratio: `TBAC:DA = 1:2`
- Coextractant: TOPO
- Organic formulation: `90 wt% TBAC/DA DES + 10 wt% TOPO`
- Nominal operating point: `23 °C`, `pH 10.4`, `O/A = 1` unless model/design specifies otherwise

Source-paper experimental benchmarks:

- one-stage Li extraction at optimized point: `48.57%`
- Li/Na selectivity at optimized point: `4.41`
- model-brine extraction: Li `51.63%`, Na `9.97%`, K `3.11%`, Mg `4.38%`, Ca `2.29%`
- extraction mechanism: Li/H ion exchange in the DES phase
- reuse/regeneration evidence exists, but should not be overclaimed as industrial solvent stability

Source-paper thermodynamic/model benchmarks:

- PC-SAFT/ePC-SAFT formulation for organic/aqueous phases
- organic phase contains DES, TOPO, RLi, and RNa
- aqueous phase contains Li/Na chloride chemistry with pH-related species
- reported AARD: approximately `7.89%` for Li extraction and `8.63%` for selectivity
- supporting data include Gibbs-energy formation details and density measurements for DES and 10 wt% TOPO-in-DES

---

## 10. ePC-SAFT role

Use ePC-SAFT as the thermodynamic engine, not as a slide topic by itself.

Main functions:

1. calculate aqueous activity coefficients,
2. calculate organic-phase activity/fugacity diagnostics,
3. support density and parameter regression,
4. produce or calibrate distribution coefficients,
5. generate Li/Na selectivity and extraction variables,
6. attach validity and extrapolation flags,
7. generate surrogate rows for PrOMMiS/IDAES.

The direct ePC-SAFT path is preferred. The calibrated Li/Na bridge is acceptable only when clearly labeled.

---

## 11. Phase-inventory / reaction-coordinate reference-state convention

Use this term:

> phase-inventory / reaction-coordinate reference-state convention

Do not call it the “weird inlet convention.”

Why it matters:

- The system is not ordinary same-species LLE.
- Aqueous Li and Na are ions.
- Organic Li and Na are neutral organic complexes, RLi and RNa.
- The transfer occurs through an ion-exchange reaction.
- Exact reproduction of source-paper extraction percentages requires the same initial inventory, phase amount, phase density, and reaction-coordinate basis used by the source authors.

The current diagnostic issue is chemically plausible: the aqueous rows can be charge balanced and pH-consistent while the organic RLi/RNa phase-inventory basis remains ambiguous.

Required diagnostic scans:

- O/A as mass ratio,
- O/A as volume ratio,
- equal phase masses,
- equal phase volumes,
- density-corrected O/A,
- pH-stoichiometric H/OH basis,
- NH4/OH buffer basis if already present,
- explicit phase-mass and phase-volume reporting.

Do not let agents keep flipping signs, reciprocals, activity-coefficient conventions, or arbitrary equation forms. The next step is phase-inventory closure.

---

## 12. Revised LHS/LHC input-space specification

The main surrogate design should cover Smackover, Marcellus-like lower-TDS brines, and Bakken stress without drifting into weak Permian cases.

| Variable | Range | Role |
|---|---:|---|
| `Li_feed_mg_L` | `80–300` | Produced-water Li grade range for active cases. |
| `TDS_feature_mg_L` | `80,000–360,000` | Salinity/process feature. |
| `Na_Li_mass_ratio` | `75–850` | Use log or stratified sampling. |
| `organic_to_aqueous_mass_ratio` | `0.5–2.0` | Stage capacity and recovery sensitivity. |
| `temperature_C` | `20–35` | Near experimental/model domain. |
| `aqueous_pH` | `9.5–10.8` | Avoid pH above 11 due to phase/emulsion risk. |
| `TOPO_wt_pct_in_organic` | fixed `10` | Fixed official solvent formulation. |
| `TBAC_to_DA_molar_ratio` | fixed `1:2` | Fixed DES formulation. |
| `stage_count` | integer `1–5` | Process/TEA variable. |
| `residual_divalent_mg_L` | `0–500` guardrail | Pretreatment leakage flag only. |
| `feed_id` | categorical | Smackover main, Marcellus comparison, Bakken stress. |

Important:

- Do not vary TOPO from 10–30 wt% in the main case-study surrogate.
- Do not vary TBAC:DA in the main case-study surrogate.
- Optional backup sensitivity can test TOPO `10–15 wt%`, but not as the official case basis.

---

## 13. Current numeric layers to reconcile

Existing artifacts contain multiple result layers. Agents must label them instead of blending them.

| Layer | Meaning | Use |
|---|---|---|
| `bridge_v0_source_regressed` | Earlier source-regressed Li/Na bridge | Backup validation layer. |
| `surrogate_v1_calibrated_surface` | Current process handoff table | Main result unless direct ePC-SAFT replaces it. |
| `idaes_costing_v1` | PrOMMiS/IDAES costing implementation | Screening TEA output. |

Known values to reconcile:

- `bridge_v0_source_regressed`: one-stage Li extraction about `45.366%`, one-stage Na extraction about `8.978%`, three-stage Li recovery about `83.693%`.
- `surrogate_v1_calibrated_surface`: nominal Smackover clean Li/Na row about `50.659%` one-stage Li extraction, `5.667%` one-stage Na extraction, `87.988%` three-stage Li recovery, Li/Na selectivity about `17.09`.
- `idaes_costing_v1`: nominal Smackover costing mirror reports about `82.85%` Li recovery.

Required handling:

- Use one source of truth for the main deck.
- If the IDAES/costing value differs from the transfer-table value, explain whether this is due to stage implementation, recovery definition, numerical mirror, or stale artifact.
- Do not mix the three numbers on one slide without labels.

---

## 14. Benchmarks and acceptance criteria

### 14.1 Literature/source benchmarks

The model workflow should be checked against:

- optimized one-stage extraction around `48.57%` Li under source-paper conditions,
- optimized Li/Na selectivity around `4.41`,
- model-brine multication extraction values: Li `51.63%`, Na `9.97%`, K `3.11%`, Mg `4.38%`, Ca `2.29%`,
- thermodynamic paper AARD targets around `7.89%` Li extraction and `8.63%` selectivity,
- process literature showing that staged solvent extraction can reach high recovery in other chemistries,
- produced-water literature showing that divalent and organic interferences must be handled upstream.

### 14.2 Feed benchmarks

The selected feed artifacts must include:

- Smackover MS-2 main case,
- Smackover high observed sensitivity,
- Marcellus NE PA comparison,
- Bakken stress point,
- missing-value flags where source chemistry is incomplete.

### 14.3 Modeling benchmarks

Each ePC-SAFT or calibrated model row must include:

- mass balance residual,
- charge balance residual where applicable,
- phase-inventory convention label,
- direct/reduced/calibrated model basis,
- extrapolation flag,
- validity flag.

### 14.4 PrOMMiS/IDAES benchmarks

The process handoff must include:

- `D_Li`,
- `D_Na`,
- one-stage Li extraction,
- one-stage Na extraction,
- cumulative Li recovery,
- cumulative Na recovery,
- Li/Na selectivity,
- O/A ratio,
- stage count,
- feed ID,
- solvent formulation,
- validity flags.

### 14.5 Screening TEA benchmarks

The TEA artifact must include:

- stress/base/favorable cases,
- feed flowrate,
- annual operating hours,
- solvent loss assumption,
- pretreatment cost assumption,
- Li loss during pretreatment,
- stage count,
- Li2CO3 equivalent output,
- breakeven cost or equivalent cost metric,
- sensitivity to solvent loss and pretreatment Li loss.

The TEA must be labeled screening-level only.

---

## 15. Three-agent vertical-slice plan

Use three agents max. Do not split into many narrow agents. Each agent owns a vertical slice and must deliver complete, coherent artifacts.

### Agent 1: Case-study framing, feed choices, naming, and storyboard

Why this agent exists:

- aligns the story before code changes,
- prevents wrong solvent naming,
- freezes feed choices and LHS/LHC scope,
- converts the old package deck into a case-study storyboard.

### Agent 2: ePC-SAFT, phase-inventory diagnostics, and transfer variables

Why this agent exists:

- connects chemistry to model outputs,
- resolves or bounds the phase-inventory issue,
- produces the transfer variables consumed by PrOMMiS/IDAES.

### Agent 3: PrOMMiS/IDAES staged extraction, screening TEA, and deck revision

Why this agent exists:

- turns transfer variables into a process case study,
- reconciles stage/cost numbers,
- creates the management-facing case-study deck.

Execution order:

1. Agent 1 freezes story, feeds, naming, and ranges.
2. Agent 2 generates validated transfer variables.
3. Agent 3 consumes transfer variables and updates process/TEA/deck.
4. Human review checks claim discipline and management usefulness.

---

## 16. Output style restrictions for all agents

Agents must follow these style restrictions in generated documents, reports, slide text, and changelogs.

Do not write:

- conversational filler,
- apologies,
- “as an AI,”
- “I will,”
- “I have completed,”
- “this document aims to,”
- “as requested,”
- “the agent,”
- vague progress narration,
- generic literature-review prose detached from the case study,
- local-user-path references in user-facing deliverables,
- raw uncurated code output in reports,
- inflated claims.

Use:

- direct technical statements,
- compact paragraphs,
- tables for decisions and assumptions,
- source-backed numbers,
- explicit uncertainty labels,
- artifact paths,
- clear pass/fail acceptance checks,
- management-relevant implications.

Every generated paragraph must support one of these: decision, assumption, benchmark, artifact, model result, risk, or next action.

---

## 17. Restricted claims and required caveats

Required caveats:

- The current project is for internal project escalation and screening TEA.
- The active extraction model starts after pretreatment.
- Divalent ions are pretreatment/feed-context variables unless explicitly modeled as leakage guardrails.
- High produced-water Na/Li cases are extrapolations beyond the source-paper low-Na/Li design space unless new validation data are added.
- Direct reactive-LLE closure must pass validation before it is presented as the model of record.
- Cost values are scenario scaffolds until solvent loss, reagent use, flowrate, and equipment assumptions are approved.

Restricted terms in main deck:

- “commercial-ready”
- “validated for Smackover brine”
- “fully predictive”
- “REE recovery”
- “solved divalent extraction”
- “investment-grade TEA”
- author-name shorthand for the solvent system

---

## 18. Required final artifact set

Minimum final artifacts:

- `docs/case_study_tbac_da_topo_storyboard.md`
- `docs/case_study_claims_and_boundaries.md`
- `data/reference/produced_water/selected_case_study_feeds.csv`
- `data/reference/produced_water/tbac_da_topo_lhs_input_ranges.csv`
- `data/processed/tbac_da_topo_lhs_design.csv`
- `data/processed/tbac_da_topo_phase_inventory_convention_scan.csv`
- `results/tbac_da_topo_phase_inventory_convention_scan.md`
- `data/processed/tbac_da_topo_li_na_transfer_variables.csv`
- `results/tbac_da_topo_li_na_surrogate_report.md`
- `data/processed/tbac_da_topo_prommis_stage_results.csv`
- `results/tbac_da_topo_prommis_stage_results.md`
- `data/processed/tbac_da_topo_screening_tea_results.csv`
- `results/tbac_da_topo_screening_tea.md`
- `slides/case_study_tbac_da_topo_produced_water/deck.qmd` or `deck.tex`
- `docs/final_case_study_readiness_checklist.md`

---

## 19. Readiness checklist

The final package is ready when:

- the main story is case-study-first,
- solvent naming is chemical and consistent,
- Smackover and Marcellus are not conflated,
- the extraction feed is clearly post-pretreatment,
- direct ePC-SAFT or calibrated-bridge basis is explicitly labeled,
- the phase-inventory convention is resolved or bounded,
- transfer-table and costing-stage recoveries are reconciled,
- screening TEA caveats are visible,
- every key number has a source or generated artifact,
- final deck has 10–12 main slides plus backup,
- project ask is internal formalization and integration funding, not commercialization.
