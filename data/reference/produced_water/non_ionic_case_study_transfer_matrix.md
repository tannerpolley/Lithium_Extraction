# Non-Ionic Case Study Transfer-Matrix Pack

Source of truth for the deck: these values are copied from generated local CSV artifacts and are intended for direct slide tables and sanity checks.

## Provenance

- One-stage KPI row: `data/multiphase/gando_2025_one_stage_assets/gando_2025_one_stage_nominal.csv`
- Three-stage KPI rows: `data/multiphase/gando_2025_slide_assets/gando_2025_stage_summary.csv`

## Exported Metrics

| Stage view | Li extraction (stage) | Li extraction (cumulative) | Na extraction (stage) | Na extraction (cumulative) | \(D_{Li}\) | \(S_{Li/Na}\) | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| One-stage nominal | `52.0047%` | `52.0047%` | `0.9067%` | `0.9067%` | `1.0835` | `118.4138` | Smackover-like non-ionic showcase basis |
| Three-stage stage 1 | `52.0047%` | `52.0047%` | `0.9067%` | `0.9067%` | `1.0835` | `118.4138` | Match to staged table row 1 |
| Three-stage stage 2 | `68.4342%` | `84.8499%` | `1.2021%` | `2.0979%` | `2.1680` | `178.1839` | Reused from staged comparison table |
| Three-stage stage 3 | `85.4948%` | `97.8025%` | `1.5166%` | `3.5827%` | `5.8941` | `382.7454` | Final staged transfer outcome |

## Deck-Ready Takeaway

- The story in this section should stay inside the non-ionic benchmark and use these values as process-transfer variables, not as standalone “best-case” claims.
- Keep each numeric claim traceable to one artifact row in this pack or the matching source CSV.

## Missing-or-Risk Notes

- These transfer values are workflow outputs from existing scripts under `scripts/lle/...`.
- Some values are rounded for slide readability; when precision is needed, cite the corresponding CSV in the artifact pack.
