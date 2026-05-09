# Lithium_Extraction Presentation Policy

This repository follows the global presentation workflow in
`C:\Users\Tanner\.codex\PRESENTATIONS.md`, with the project-specific choices
below.

## Source Of Truth

- Use text-first sources for maintainable presentation work.
- Use `slides/deck.qmd` for the broad project deck and fast Quarto iteration.
- Use `slides/final_rezaee_calibrated_case_study_2026_05_08/deck.tex` as the
  active final Rezaee-calibrated case-study presentation source.
- Treat PowerPoint decks as out of scope for this case-study overhaul unless the
  user explicitly reopens PowerPoint work.

## PowerPoint Boundary

- Do not edit, regenerate, or export PPTX files for the active Rezaee case-study
  package unless the user explicitly asks for a PowerPoint deliverable.
- If PowerPoint work is later reopened, copy
  `docs/Slides/Codex Presentation Template.pptx` first; never edit the template
  directly.

## Current Active Case Study

The active presentation chain is:

1. Pretreated southern-Arkansas Smackover Li/Na feed basis.
2. Rezaee DES/TOPO chemistry and calibrated Li/Na distribution bridge.
3. TDS/Li/O/A surrogate screening matrix.
4. PrOMMiS/IDAES transfer-table and costing handoff.
5. Explicit validation boundary for high-Na/Li extrapolation.

Archived HBTA/TOPO, Gando, Jang, Yu, and Hubach materials are comparison or
diagnostic material unless a slide explicitly labels them as current.

## Completion Checklist

- Text-first source exists and is referenced in the README.
- Figures used in the deck are collected in the presentation package `figures/`
  folder or referenced from a documented analysis output.
- The Beamer source builds to `deck.pdf` with local MiKTeX.
- The generated Beamer PDF is visually checked for text overflow, broken
  figures, equation rendering, section order, and citation/source consistency.
