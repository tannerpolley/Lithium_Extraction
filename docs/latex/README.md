# Lithium Extraction LaTeX Manuscript

This folder is the source manuscript scaffold for the produced-water lithium extraction case study.

## Active Mirror

The mirror folder is:

```text
C:\Users\Tanner\Documents\git\LaTeX-Projects\Lithium-Extraction-LaTeX
```

Use `sync_to_latex_projects_mirror.ps1` from this folder to copy the source manuscript into the mirror. The sync script intentionally stays in the source folder and is not copied into the mirror.

## Build

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex
```

## Current Manuscript Boundary

The draft uses a Rezaee-calibrated distribution surrogate as the active process-screening basis. It should not claim a final accepted direct reactive ePC-SAFT LLE physical split until the direct solve and residual evidence are promoted.
