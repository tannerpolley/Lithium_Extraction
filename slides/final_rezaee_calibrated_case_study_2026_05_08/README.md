# Final Rezaee-Calibrated Produced-Water Case Study

This folder is the source-first presentation package for the active Rezaee
DES/TOPO clean Li/Na produced-water case study.

## Source Of Truth

- Final technical source: `deck.tex`
- Citation/source registry: `references.bib`
- Figure assets: `figures/`

PowerPoint work is intentionally out of scope for this package unless the user
explicitly reopens a PPTX deliverable.

## Outputs

- `deck.pdf` - final technical Beamer PDF when built from `deck.tex`.

## Build

Build the Beamer PDF:

```powershell
cd .\slides\final_rezaee_calibrated_case_study_2026_05_08
pdflatex deck.tex
```

If MiKTeX reports a missing `translator.sty` package, install the package from
an explicit CTAN mirror before rebuilding:

```powershell
& "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64\mpm.exe" --repository=https://mirrors.mit.edu/CTAN/systems/win32/miktex/tm/packages/ --install=translator
```

## Current Narrative Boundary

- Current case-study basis: pretreated southern-Arkansas Smackover Li/Na stream.
- Active solvent bridge: Rezaee DES/TOPO.
- Current process bridge: calibrated distribution-coefficient surrogate.
- Main limitation: produced-water Na/Li rows are extrapolated beyond the
  original Rezaee DOE Na/Li domain.
- Archived HBTA/TOPO and Gando/Jang/Yu/Hubach work should stay outside the main
  chain unless clearly labeled as comparison or diagnostics.
