# Phase 6-8 Smackover Reactive-Stage Outputs

## Scope

These outputs use the source-regressed Li/Na HBTA/TOPO reactive-stage model with 2 HBTA : 1 TOPO : 1 Li stoichiometry and ePC-SAFT aqueous activity coefficients when available. They assume divalent pretreatment and are transfer-variable and costing scaffold artifacts, not full organic-phase HBTA/TOPO ePC-SAFT LLE predictions.

## Generated Files

- `data\reference\produced_water\smackover_ms2_transfer_sensitivity.csv`
- `data\reference\produced_water\smackover_prommis_transfer_handoff.csv`
- `data\reference\produced_water\phase8_costing_scenarios_skeleton.csv`

## Selected Base Result

- Case: `smackover_clean_median_tds_proxy`
- O/A ratio: `1.0`
- Li feed: `168.000 mg/L`
- Na feed: `64100.000 mg/L`
- TDS: `305000.000 mg/L`
- One-stage Li extraction: `47.2846%`
- One-stage Na extraction: `0.0131%`
- Three-stage Li extraction: `99.99999%` (near-total extrapolated model result)
- Three-stage Na extraction: `0.1160%`
- Trust label: `outside_literature_capacity_envelope_near_total_transfer`

## Boundary

The high Smackover salinity and lithium concentration are outside the original Shan/Gando showcase calibration envelope. These rows are useful for process skeletons and reactive-stage surrogate design, but they must be labeled as extrapolative until the HBTA/TOPO organic-phase parameter and complex-parameter gaps are closed.
