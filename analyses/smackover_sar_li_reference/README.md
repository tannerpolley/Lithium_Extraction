# Smackover SAR Lithium Reference Workflow

This analysis contains the reusable scripts from the Southern Arkansas
Smackover lithium mapping bundle. It is retained as a reference-data curation
workflow, not as an active generated-output location.

Durable source inputs live under `data/reference/smackover_sar_li/`. Generated
rasters, uncertainty grids, and prediction CSVs should be recreated locally when
needed and should not be committed back under `build/`.

## Scripts

- `prepare_sar_li_data.py` - source-data preparation.
- `train_sar_li_random_forest.R` - random-forest model training.
- `estimate_sar_li_uncertainty.py` - uncertainty estimation.
- `estimate_sar_li_grid.py` - grid prediction workflow.

## Validation

This workflow is not part of the default smoke suite. Before reusing it, inspect
the source bundle notes under `data/reference/smackover_sar_li/` and run the
scripts in order in a dedicated local output directory.
