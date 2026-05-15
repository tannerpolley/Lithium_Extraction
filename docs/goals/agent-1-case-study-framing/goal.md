# Agent 1 Case-Study Framing

## Objective

Execute the Agent 1 case-study framing slice for the produced-water lithium extraction package. Create or update the required storyboard, claims-and-boundaries, selected-feed, and LHS/LHC input-range artifacts using `docs/plans/AGENT_1_CASE_STUDY_FRAMING_PROMPT.md` and `docs/plans/MASTER_CASE_STUDY_CONTEXT_ROADMAP.md` as controlling context.

## Original Request

`/goal Follow the prompt in the agent 1 case md document and read the master case study plan for context. Be sure to use the correct language for the context of what is being created; use academic-researcher, article-writer-latex-submission, chemical-engineer, uncodixfy, and imagegen when they help.`

## Intake Summary

- Input shape: `existing_plan`
- Audience: internal KeyLogic/government-contracted technical management and project leads
- Authority: `requested`
- Proof type: `artifact`
- Completion proof: the four Agent 1 deliverables exist, use the required TBAC/DA/TOPO language, pass acceptance checks, and preserve the screening-TEA/internal-escalation boundary.
- Likely misfire: producing a package-first ePC-SAFT theory deck or author-name solvent framing instead of a case-study-first internal project package.
- Blind spots considered: stale HBTA/TOPO or author-name shorthand, Marcellus versus Smackover mixing, hidden pretreatment assumptions, overclaiming predictive ePC-SAFT closure, varying TOPO when the prompt fixes it at 10 wt%.
- Existing plan facts: read `MASTER_CASE_STUDY_CONTEXT_ROADMAP.md` first; implement only the Agent 1 vertical slice; do not implement ePC-SAFT model, PrOMMiS flowsheet, or TEA.

## Goal Kind

`existing_plan`

## Current Tranche

Complete the Agent 1 framing deliverables in one bounded local pass. The tranche is complete when the deliverables satisfy the prompt acceptance checks and validation confirms no source-author solvent label appears in executive-facing titles or new deck-facing artifact names.

## Non-Negotiable Constraints

- Use `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`, `TBAC/DA DES + 10 wt% TOPO`, or `90 wt% TBAC/DA DES + 10 wt% TOPO` for the solvent system.
- Do not use a source-author name as the solvent-system label in slide titles, executive summaries, figure captions, artifact names, or new prose shorthand.
- New user-facing artifact names must use `tbac_da_topo`.
- Keep the project framed as internal project escalation with screening-level TEA.
- Keep divalent ions as pretreatment/feed-context variables or residual-divalent guardrails, not active Li/Na extraction species.
- Do not claim experimental validation on Smackover brine, solved divalent extraction, investment-grade TEA, commercialization readiness, REE recovery from the selected feed, or fully predictive direct reactive-LLE closure unless separately validated.
- Do not edit PowerPoint artifacts in this tranche.

## Stop Rule

Stop only when a PM audit maps the written artifacts and verification back to the Agent 1 prompt and records that the tranche is complete.

## Canonical Board

Machine truth lives at:

`docs/goals/agent-1-case-study-framing/state.yaml`

If this charter and `state.yaml` disagree, `state.yaml` wins for task status, active task, receipts, verification freshness, and completion truth.

## Run Command

```text
/goal Follow docs/goals/agent-1-case-study-framing/goal.md.
```
