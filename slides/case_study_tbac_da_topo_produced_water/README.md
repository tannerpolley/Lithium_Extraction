# TBAC/DA/TOPO Produced-Water Case-Study Deck

## Source Of Truth

- Canonical source: `deck.qmd`.
- Generated review output: `deck.html` after Quarto render.
- Figures: `figures/`.

## Build

```powershell
& "$env:LOCALAPPDATA\Apps\Quarto\bin\quarto.exe" render .\deck.qmd --to revealjs
```

PowerPoint is out of scope unless explicitly reopened.
