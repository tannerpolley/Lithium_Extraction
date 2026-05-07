# Phase 9 Selected Produced-Water Feed Basis

## Selected Base Brine

The Phase 9 case uses the clean local USGS southern-Arkansas Smackover row:

- Source file: `build/smackover_sar_li/input/usgs_southAR/southAR_brines_2022.txt`
- `SITEID`: `MS-2`
- Well: `MSPU 4-W1`
- Field: `Magnolia Smackover Production Unit`
- County/state: `Columbia County, Arkansas`
- Formation: `Smackover`
- Sample date: `2022-08-24`
- Sample location: `WH`
- Depth interval: `7493-7495 ft`

This row is selected because its `TDS = 305,000 mg/L`, which matches the clean local Smackover median TDS, while `Li = 168 mg/L` gives a realistic premium-brine case without using the highest observed lithium row.

## Major Composition

| Quantity | Value |
|---|---:|
| Temperature | `61.67 degC` |
| pH | `5.77` |
| Specific gravity | `1.21` |
| TDS | `305,000 mg/L` |
| Li | `168 mg/L` |
| Na | `64,100 mg/L` |
| K | `2,300 mg/L` |
| Mg | `3,310 mg/L` |
| Ca | `36,900 mg/L` |
| Sr | `1,940 mg/L` |
| Ba | `8.39 mg/L` |
| Cl | `174,000 mg/L` |
| Br | `2,700 mg/L` |
| SO4 | `184 mg/L` |
| B | `163 mg/L` |

## Critical Minerals And REE Status

- Reported or threshold trace fields include Fe, Mn, Zn, and other metals tracked in `smackover_critical_minerals_ree_status.csv`.
- `B = 163 mg/L` is a source-backed minor/critical-mineral-adjacent value for the selected row.
- REE are `not_reported` in the local source table. They should not be inferred or presented as part of the selected feed.

## Chemistry Basis Boundary

This selected Smackover row is the source-composition basis.

The HBTA/TOPO extraction basis remains Shan/Gando 2025:

- HBTA extractant.
- TOPO synergist.
- Sulfonated kerosene diluent.
- 100% saponification.
- `O/A = 1:1`.
- `6 min` contact time.
- Three-stage field-water process anchor above 97% lithium extraction after impurity removal.

The current repository does not contain a Smackover-specific HBTA/TOPO extraction experiment. Therefore the deck should say:

> The source feed is Smackover-specific; the extraction chemistry is Shan/Gando HBTA/TOPO; the current model is a source-regressed Li/Na stage model coupled to a literature-backed non-ionic extraction chemistry.

## Phase 9 Use

Use this file to ground:

1. The selected-location slide.
2. The feed-composition slide.
3. The pretreatment slide.
4. The cost-basis and product-rate scaffold.
5. The limitation slide.

Do not use it to claim final full multication Smackover extraction performance until the HBTA/TOPO parameter and reaction-constant gaps are closed. The current source-regressed Li/Na stage model is acceptable for the case-study handoff only when labeled with its trust-region caveats.
