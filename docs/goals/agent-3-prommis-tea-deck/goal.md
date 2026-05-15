# Agent 3 PrOMMiS/IDAES TEA Deck

## Objective

Execute the Agent 3 process, screening-TEA, and presentation vertical slice from `docs/plans/AGENT_3_PROMMIS_TEA_DECK_PROMPT.md`, using `docs/plans/MASTER_CASE_STUDY_CONTEXT_ROADMAP.md`, Agent 1 outputs, and Agent 2 outputs as the controlling context.

## Original Request

Prep the GoalBuddy goal to follow the Agent 3 case prompt and read the master case-study plan for context, using the named research, writing, chemical-engineering, visual, and presentation-quality skills when they help.

## Intake Summary

- Input shape: `existing_plan`
- Audience: Internal KeyLogic/government-contracted technical management and project leads
- Authority: `requested`
- Proof type: `artifact`
- Completion proof: Agent 3 staged extraction, screening-TEA, deck, figures, readiness checklist, and changelog artifacts exist; validation/renders pass or blockers are documented; final audit confirms the deck is case-study-first and ready for internal escalation review.
- Likely misfire: Building an ePC-SAFT theory lecture or generic cost deck instead of a produced-water case-study package with reconciled transfer/process/TEA numbers.
- Blind spots considered: transfer-table and costing recovery mismatch, Marcellus missing major-ion chemistry, high-Na/Li extrapolation, direct ePC-SAFT overclaiming, divalent extraction leakage, PowerPoint source-of-truth drift, and screening-TEA overprecision.
- Existing plan facts: Preserve Agent 3 prompt scope, master roadmap story arc, Agent 1 feed/naming/range outputs, Agent 2 transfer/convention outputs, repo-local presentation policy, and chemical solvent naming.

## Goal Kind

`existing_plan`

## Current Tranche

Create the complete Agent 3 case-study package: PrOMMiS/IDAES-style staged extraction outputs, transfer-versus-process recovery reconciliation, screening-TEA scenarios, management-readable figures, a 10-12 slide text-first case-study deck with backup slides, final readiness checklist, and changelog.

The first `/goal` task validates that all Agent 1 and Agent 2 inputs are present and internally consistent before any process, costing, or presentation files are changed. After validation, the board should activate the largest safe Worker package that can produce the process/TEA/deck artifacts and verify them.

## Non-Negotiable Constraints

- Use `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`, `TBAC/DA DES + 10 wt% TOPO`, or `90 wt% TBAC/DA DES + 10 wt% TOPO` for the solvent system.
- Do not use the source-author name as a solvent-system label in new slides, reports, figure captions, executive summaries, or new artifact names.
- Use Agent 2 transfer variables as the extraction source of truth; do not invent extraction values in process or TEA artifacts.
- Label direct ePC-SAFT as unpromoted unless direct reactive-LLE validation passes.
- Treat divalent ions as pretreatment/cost/loss/guardrail variables, not active Li/Na extraction species.
- Keep all cost outputs labeled screening TEA; do not imply vendor-grade, design-grade, investment-grade, or commercialization readiness.
- Make the deck case-study-first for internal project formalization and integration funding; keep ePC-SAFT theory to one main slide plus backup.
- Preserve the repo presentation policy: prefer text-first sources, use the active case-study slide package, and do not edit or regenerate PPTX unless explicitly reopened.
- Use the requested skills only when they help the active `/goal` task: `chemical-engineer` for process/TEA assumptions and mass balances, `academic-researcher` for source-backed claims, `article-writer-latex-submission` for claim-safe technical prose, `uncodixfy` for avoiding generic deck/UI styling, and `imagegen` only if bitmap visuals are needed.
- Follow the output style restrictions in the Agent 3 prompt and roadmap.

## Stop Rule

Stop only when a final audit proves the full Agent 3 outcome is complete.

Do not stop after planning, discovery, or Judge selection if a safe Worker task can be activated.

Do not stop after a single verified Worker package when the broader Agent 3 package still has safe local follow-up work. Advance the board to the next highest-leverage safe Worker package unless a phase, risk, rejected-verification, ambiguity, or final-completion review is due.

## Slice Sizing

Safe means bounded, explicit, verified, and reversible. It does not mean tiny.

A good Worker package should produce a coherent Agent 3 artifact set or a meaningful vertical subset, such as process/TEA data plus reports, or deck/figure construction plus render checks. Avoid one task per chart, slide, or helper unless a narrow blocker requires it.

## Canonical Board

Machine truth lives at:

`docs/goals/agent-3-prommis-tea-deck/state.yaml`

If this charter and `state.yaml` disagree, `state.yaml` wins for task status, active task, receipts, verification freshness, and completion truth.

## Run Command

```text
/goal Follow docs/goals/agent-3-prommis-tea-deck/goal.md.
```

## PM Loop

On every `/goal` continuation:

1. Read this charter.
2. Read `state.yaml`.
3. Read `docs/plans/AGENT_3_PROMMIS_TEA_DECK_PROMPT.md`, `docs/plans/MASTER_CASE_STUDY_CONTEXT_ROADMAP.md`, Agent 1 outputs, Agent 2 outputs, and presentation policy before changing process, costing, or presentation files.
4. Work only on the active board task.
5. Use Scout/Judge/Worker/PM according to the task.
6. Write compact task receipts and keep `state.yaml` as board truth.
7. Verify generated data, reports, and deck renders before final audit.
8. Finish only with a Judge/PM audit receipt that maps receipts and verification back to the original Agent 3 outcome and records `full_outcome_complete: true`.
