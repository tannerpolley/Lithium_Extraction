# Quarto Slide Workflow

This directory is the repo-local **source of truth** for slide authoring.

## Canonical Files

- `deck.qmd`: slide content, structure, speaker notes, images, and commands
- `theme.scss`: shared revealjs styling and layout conventions
- `_quarto.yml`: default Quarto revealjs render settings

## Authoring Rules

- Edit the `.qmd`, not a `.pptx`, for first-pass deck creation.
- Keep one slide per heading.
- Keep speaker notes inline with `::: {.notes}` blocks.
- Reference figures and tables from files already tracked in the repo.
- Change deck-wide look and layout conventions in `theme.scss`, not slide by slide.

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

For PDF sharing, render the revealjs deck and print the generated HTML deck to PDF from the browser.

Optional later:

```powershell
quarto render .\slides\deck.qmd --to pptx
```

If PPTX becomes a real deliverable, add a branded `reference.pptx` template in this folder and wire it through Quarto instead of making PowerPoint the primary authoring surface.

## Current Validation Status

- Quarto `1.8.27` is installed and passes `quarto check`.
- The starter deck has been rendered successfully to `slides/deck.html`.
- The render required running Quarto outside the sandbox in this Codex session because Quarto spawns the system shell during project rendering.

## Default Workflow Decision

- Primary artifact: web slides and PDF sharing
- Canonical source: Markdown plus theme/template files
- PowerPoint: secondary export path only
- LaTeX/Beamer: only for formula-dense, PDF-first decks
- Marp: optional lighter alternative, but Quarto is the richer default

## Current Starter Deck

`deck.qmd` is seeded with the produced-water lithium extraction case study already being developed in this repo. It uses existing Gando selective-showcase figures under `data/multiphase/` so the Markdown-first workflow starts with real project content rather than placeholder slides.
