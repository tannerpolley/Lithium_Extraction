# Case Study Full Implementation Goal

## Starter Command

```text
/goal Follow docs/goals/case_study_full_implementation/goal.md.
```

## Source Specification

Follow `docs/plans/MASTER_LITHIUM_CASE_STUDY_SUCCESS_ONLY_AGENT_SPEC.md` as the controlling plan. When it conflicts with older prompts, deck notes, task boards, diagnostics, or handoffs, the master specification wins.

## Requested Outcome

Fully implement the produced-water lithium extraction case study until it is complete, validated, and internally presentable:

```text
source-backed produced-water feed information
    -> TBAC/DA DES + TOPO Li/Na extraction chemistry
    -> ePC-SAFT-compatible or approved source-anchored stage-response data
    -> IDAES ALAMO surrogate
    -> IDAES SurrogateBlock
    -> real PrOMMiS/IDAES SolventExtraction/MSContactor path
    -> screening TEA and UQ
    -> executed notebook
    -> rendered management-ready deck
    -> all-success gate report
```

## Non-Negotiable Constraints

- Final deliverables must be success artifacts only. Diagnostic failures are not acceptable completion evidence.
- No fake final results. The only permitted synthetic/non-factual data is source-anchored generated demonstration stage-response data, and only when the ePC-SAFT package is not ready for accepted direct Li/Na transfer generation.
- Synthetic demonstration rows must be deterministic, source-paper anchored, explicitly labeled, and limited to propagating the ALAMO -> SurrogateBlock -> PrOMMiS -> TEA workflow.
- All feed chemistry, source-paper facts, dependency claims, PrOMMiS implementation claims, notebook behavior, and presentation content must be real, correct, passing, and traceable.
- Use real PrOMMiS/IDAES only when imports, unit construction, material-transfer constraints, degrees of freedom, outlet values, and mass balance checks pass.
- Do not copy PrOMMiS source into this repository. Install/import PrOMMiS as a pinned Git dependency.
- Preserve the original PrOMMiS notebook; create and revise a copy in `Lithium_Extraction`.
- Do not include Trust Region Framework content.
- Do not overclaim ePC-SAFT direct closure or commercial solvent/process readiness.
- Periodically check for new commits on `ePC-SAFT` `origin/main`; if the upstream PR has merged and accepted direct ePC-SAFT results are now possible, prefer the real accepted ePC-SAFT path over the synthetic demonstration backend.

## Completion Proof

The goal is complete only when a final Judge/PM audit proves all of the following:

- `uv sync` passes.
- `prommis`, `idaes`, `pyomo`, and `epcsaft` import in the project environment.
- Required source/feed registers and two-domain design artifacts exist and validate.
- Stage-response data is bounded, reproducible, and either accepted direct ePC-SAFT output or properly labeled source-anchored generated demonstration data.
- IDAES ALAMO trains or a frozen `AlamoSurrogate` JSON loads successfully.
- IDAES `SurrogateBlock` path is exercised.
- Real PrOMMiS/IDAES `SolventExtraction` and `MSContactor` objects are used for accepted PrOMMiS outputs.
- Li and Na material-transfer constraints are active; chloride transfer is absent or explicitly inactive.
- PrOMMiS model degrees of freedom are zero and mass-balance residuals are within tolerance.
- Copied notebook executes end to end with no failed cells.
- Screening TEA/UQ artifacts exist and are clearly screening-level.
- Deck renders and includes all required main and backup content.
- Forbidden diagnostic language is absent from final docs, deck, notebook markdown cells, and reports.
- `results/tbac_da_topo_success_gate_report.md` exists and contains only passing final gates.

## Likely Misfires To Avoid

- Submitting old Agent 1/2/3 diagnostic artifacts as if they satisfy the master success-only spec.
- Calling algebraic postprocessing "PrOMMiS output."
- Calling source-anchored generated demonstration data direct ePC-SAFT closure.
- Producing a deck/report about failed direct ePC-SAFT closure instead of using the approved fallback path.
- Treating an incomplete produced-water feed as simulation/TEA-ready.
- Letting older HBTA/TOPO, Gando, or TOP/hexane material drift back into the active TBAC/DA DES + TOPO implementation.
- Stopping at plan validation or partial artifacts without an executed notebook, real PrOMMiS pathway, rendered deck, and all-pass success report.

## Board Truth

`docs/goals/case_study_full_implementation/state.yaml` is the board truth. Keep exactly one active task. PM owns state updates. Worker tasks may write only inside their `allowed_files`.
