# Presentation Workflow

This directory is the repo-local presentation workspace. The controlling policy
is `..\PRESENTATIONS.md`, which extends the global policy at
`C:\Users\Tanner\.codex\PRESENTATIONS.md`.

## Canonical Files

- `deck.qmd`: broad project deck source for Quarto iteration.
- `theme.scss`: shared revealjs styling and layout conventions.
- `_quarto.yml`: default Quarto revealjs render settings.
- `final_rezaee_calibrated_case_study_2026_05_08/`: active final case-study
  package with `deck.tex`, `references.bib`, `figures/`, and Beamer PDF output.

## Authoring Rules

- Edit text-first sources first: `.qmd` for drafting and `.tex` for final
  technical PDF decks.
- Do not touch `.pptx` files for the active Rezaee case-study package unless the
  user explicitly reopens PowerPoint work.
- Keep one slide concept per heading/frame.
- Keep speaker notes inline with `::: {.notes}` blocks when using Quarto.
- Reference figures and tables from tracked repo files or the presentation
  package `figures/` folder.
- Change deck-wide look and layout conventions in `theme.scss`, not slide by
  slide.

## Render Commands

Quarto is installed on this machine as a per-user install at:

`C:\Users\Tanner\AppData\Local\Apps\Quarto\bin\quarto.exe`

If a new shell session has refreshed `PATH`, use:

```powershell
quarto render .\slides\deck.qmd --to revealjs
```

If `quarto` is not yet visible on `PATH` in the current shell, use the installed binary directly:

```powershell
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\slides\deck.qmd --to revealjs
```

That generates the HTML slide deck next to `deck.qmd` unless you later add an output directory.

For PDF sharing from the broad Quarto deck, render the revealjs deck and print
the generated HTML deck to PDF from the browser.

## Current Validation Status

- Quarto `1.8.27` is installed and passes `quarto check`.
- The starter deck has been rendered successfully to `slides/deck.html`.
- The render required running Quarto outside the sandbox in this Codex session because Quarto spawns the system shell during project rendering.

## Default Workflow Decision

- First-draft source: Quarto.
- Final technical source: Beamer PDF when the presentation is engineering- or
  equation-heavy.
- PowerPoint: out of scope for the active Rezaee case-study package unless
  explicitly requested.
- Current final case-study package:
  `final_rezaee_calibrated_case_study_2026_05_08/`.

## Current Starter Deck

`deck.qmd` is the current produced-water lithium extraction deck source. As of 2026-05-08, the active case-study basis is the Rezaee DES/TOPO Li/Na bridge after divalent pretreatment. Older Gando/HBTA/TOPO figures remain comparison or historical assets only unless a slide explicitly marks them as current.
