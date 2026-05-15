# Agent 2 ePC-SAFT Surrogate

## Objective

Prepare and execute the Agent 2 ePC-SAFT, phase-inventory diagnostics, and transfer-variable slice for the produced-water lithium extraction case study. The `/goal` run must follow `docs/plans/AGENT_2_EPCSAFT_SURROGATE_PROMPT.md` and use `docs/plans/MASTER_CASE_STUDY_CONTEXT_ROADMAP.md` as controlling context.

## Original Request

`Prep the goal to Follow the prompt in the agent 2 case md document and read the master case study plan for context. Be sure to use the correct language for the context of what is being created; use academic-researcher, article-writer-latex-submission, chemical-engineer, uncodixfy, and imagegen when they help.`

## Intake Summary

- Input shape: `existing_plan`
- Audience: internal KeyLogic/government-contracted technical management and project leads
- Authority: `requested`
- Proof type: `artifact`
- Completion proof: the Agent 2 deliverables from the prompt exist, the ePC-SAFT or calibrated-transfer basis is explicitly labeled, phase-inventory and validity flags are reported, validation commands pass or blockers are recorded, and the outputs are ready for Agent 3 PrOMMiS/IDAES and screening-TEA consumption.
- Likely misfire: jumping directly into model edits or surrogate generation before reading the Agent 2 prompt, validating the post-Agent-1 framing, and fixing the source-of-truth boundaries.
- Blind spots considered: direct reactive-LLE may remain bounded rather than closed; high-Na/Li produced-water rows are outside the source-paper design space; the phase-inventory / reaction-coordinate reference-state convention may be unresolved; transfer-table and costing-stage recoveries may not agree; author-name solvent shorthand must not appear in new executive-facing outputs.
- Existing plan facts: Agent 1 froze chemical solvent labels, selected feed roles, and fixed LHS/LHC ranges; Agent 2 owns ePC-SAFT diagnostics, phase-inventory scans, and Li/Na transfer variables; Agent 3 owns PrOMMiS/IDAES staged extraction, screening TEA, and deck revision.

## Goal Kind

`existing_plan`

## Current Tranche

The current tranche is GoalBuddy preparation only. The next `/goal` run should read the Agent 2 prompt and master roadmap first, validate the Agent 2 scope against Agent 1 outputs, then execute the largest safe local work package needed to produce the ePC-SAFT diagnostics and transfer-variable artifacts.

## Non-Negotiable Constraints

- Use chemical solvent labels in user-facing outputs: `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`, `TBAC/DA DES + 10 wt% TOPO`, or `90 wt% TBAC/DA DES + 10 wt% TOPO`.
- Source-paper author names may appear only in bibliography/source notes or existing legacy paths, not as solvent-system shorthand.
- Preserve the accepted case-study claim boundary: internal project escalation, post-pretreatment Li/Na extraction, ePC-SAFT-generated or ePC-SAFT-calibrated transfer variables, PrOMMiS/IDAES handoff, and screening-level TEA.
- Do not claim full commercialization readiness, investment-grade TEA, experimental validation on Smackover brine, solved divalent extraction, REE recovery, or fully predictive direct reactive-LLE closure unless the Agent 2 evidence closes it.
- Treat Ca/Mg/Sr/Ba as pretreatment/feed-context variables or residual-divalent leakage guardrails, not active Li/Na extraction species.
- Use the `epcsaft-cross-repo` stable/final contract policy when validating package source state; do not silently switch to a mutable local ePC-SAFT worktree.
- Use named skills during execution only when they help: `academic-researcher` for source discipline, `article-writer-latex-submission` for submission-safe language, `chemical-engineer` for equations/model/input verification, `uncodixfy` for any visual/deck-facing artifact language or layout critique, and `imagegen` only if a bitmap visual asset is explicitly needed.

## Stop Rule

Stop prep after the board is created, locally visible, and valid. During the later `/goal` run, stop only when a final audit proves that Agent 2 deliverables satisfy the prompt and are ready for Agent 3.

## Canonical Board

Machine truth lives at:

`docs/goals/agent-2-epcsaft-surrogate/state.yaml`

If this charter and `state.yaml` disagree, `state.yaml` wins for task status, active task, receipts, verification freshness, and completion truth.

## Run Command

```text
/goal Follow docs/goals/agent-2-epcsaft-surrogate/goal.md.
```
