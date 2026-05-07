# Non-Ionic Produced-Water Case Study Sources

This file records the evidence basis for the non-ionic solvent-extraction case study. It stays conservative on purpose: if the local OCR markdown did not report a value, the companion CSV uses `not_reported` rather than filling a gap from memory.

## Primary benchmark paper

- Shan, Q.; Zhu, G.; Fan, P.; Liang, M.; Zhang, X.; Liu, J.; Wu, G. 2025. *Influence Mechanism of Coexisting Ions on the Extraction Efficiency of Lithium from Oil and Gas Field Water*. Water 17, 2258. DOI: `10.3390/w17152258`. Zotero key: `JUNBXVTI`.
- Local repository evidence: `papers/md/Gando-Ferreira et al. - 2025 - Influence Mechanism of Coexisting Ions on the Extraction Efficiency o.md`.

## Local Zotero/API verification update

The Zotero MCP wrapper was not stable during the 2026-05-07 continuation, but the local Zotero HTTP API at `http://localhost:23119/api/` was reachable with `curl.exe`. Verified local metadata records:

- `JUNBXVTI` / `Gando-Ferreira2025`: Shan/Gando 2025, DOI `10.3390/W17152258`.
- `AEL6ZEPG` / `Zhang2018`: Zhang et al. 2018, *Recovery of lithium from alkaline brine by solvent extraction with beta-diketone*, DOI `10.1016/j.hydromet.2017.10.029`.
- `BLUVRJ9Q` / `Jang2017`: Jang et al. 2017, *Lithium recovery from shale gas produced water using solvent extraction*, DOI `10.1016/J.APGEOCHEM.2017.01.016`.
- `V7EN7V3S` / `Kia2024`: Kia et al. 2024, *Solvent extraction of lithium from brines with high magnesium/lithium ratios: investigation on parameter interactions*, DOI `10.1007/s11356-024-34617-8`.
- `NDEBX6D2` / `Almousa2025`: Almousa et al. 2025, *Comparative feasibility of lithium extraction technologies in U.S. oilfields*, DOI `10.1016/j.dwt.2025.101128`.

The direct DBM/TOPO unconventional-oilfield-brine primary paper was not found in the local Zotero pass. It remains a backup search target, not a source-backed active claim.

## Extracted values used in the CSV

- Simulated feed composition from Table 1:
  - Li = `60 mg/L`
  - Na = `10,900 mg/L`
  - K = `560 mg/L`
  - Ca = `8,600 mg/L`
  - Mg = `820 mg/L`
  - Ba = `560 mg/L`
  - Cl = `47,220 mg/L`
  - pH = `6`
- Organic system and process basis:
  - In the coexisting-ion experiments, HBTA and TOPO were each used at `0.015 mol/L`
  - HBTA extractant
  - TOPO synergist
  - sulfonated kerosene diluent
  - 100% saponification
  - `O/A = 1:1`
  - `6 min` contact time
- Actual 15 L field-water extraction case:
  - HBTA and TOPO were each used at `0.15 mol/L`
  - `O/A = 1:1`
  - `6 min` contact time
- Actual 15 L field-water case:
  - Actual water volume = `15 L`
  - TOC = `2160 mg/L`
  - Organic chemistry listed in the local OCR markdown includes benzene series, phenols, polycyclic aromatic hydrocarbons, organic acids, and long-chain alkanes
  - Three-stage cross-flow extraction after impurity removal reached just over `97%` lithium extraction
  - Reported lithium carbonate purity = `99.28%`
  - Average lithium transfer efficiency in the 15 L case = `91.35%`

## Evidence And Assumptions

- Simulated/coexisting-ion feed: Table 1 is a simulated oil-and-gas-field-water composition used for ion-interference experiments. The equal-concentration Li/Ca/Mg table in the OCR markdown is also a simulated selectivity test, not an actual field-water sample.
- Actual field-water process case: the 15 L extraction and carbonate-preparation sequence is the actual field-water validation case. The OCR markdown reports the operating conditions, the fifth-recycle extraction drop to `87.11%`, the average transfer efficiency of `91.35%`, and the final `99.28%` Li2CO3 purity. The actual field-water composition itself was not fully enumerated there, so the CSV keeps those analytes as `not_reported`.
- Smackover siting motivation: Smackover is a separate basin-screening argument supported by USGS and literature sources elsewhere in the repo. Shan 2025 is the process-evidence anchor for the HBTA/TOPO benchmark, but it does not establish a Smackover-specific feed composition.
- Smackover source data: the local USGS-derived file `build/smackover_sar_li/input/usgs_southAR/southAR_brines_2022.txt` has clean Smackover major-ion rows after excluding duplicate and blank rows. The summary file `data/reference/produced_water/smackover_usgs_clean_observation_summary.csv` records `13` clean rows with Li from `11.7` to `252 mg/L`, median Li `98.7 mg/L`, TDS from `156,000` to `340,000 mg/L`, and median TDS `305,000 mg/L`.
- Smackover sensitivity basis: `data/reference/produced_water/smackover_li_tds_sensitivity_basis.csv` separates actual observed clean rows from slide-friendly screening rows. The screening rows are for sensitivity only and should not be presented as direct well samples.
- Critical minerals and REE: `data/reference/produced_water/smackover_critical_minerals_ree_status.csv` records trace-metal fields available in the local Smackover source table and explicitly marks REE as `not_reported_in_local_usgs_file`. Censored values are summarized as threshold values for screening only, not as exact measured concentrations.

## Important exclusions

- Ionic-liquid systems are not treated as active case-study candidates in this repository branch.
- They may remain in the literature background only if needed to explain why the case study intentionally pivots to conventional ligand chemistry.
- The active ligand-chemistry comparison in the planning doc is HBTA/TOPO, with DBM/TOPO kept as a secondary class-level comparison for later retrieval or discussion.

## Gaps kept explicit

- The actual 15 L field-water composition was not enumerated in the local OCR markdown, so the CSV marks those analytes as `not_reported`.
- No Smackover-specific non-ionic solvent-extraction feed composition was verified in this task, so the case-study composition file stays anchored to the Shan 2025 oil-and-gas-field-water benchmark instead of inventing a basin-specific feed.

## Transfer-Metric Artifacts

Use these companion outputs for deck-ready tables and KPIs:

- `data/reference/produced_water/non_ionic_case_study_transfer_matrix.md`
- `data/reference/produced_water/non_ionic_case_study_transfer_matrix.csv`

## Companion Planning And Gap Artifacts

- `data/reference/produced_water/non_ionic_solvent_literature_matrix.csv`: ranked non-ionic solvent evidence matrix with Zotero keys and active/backup roles.
- `data/reference/produced_water/hbta_topo_model_gap_table.csv`: explicit parameter, reaction-constant, and source-composition gaps for the HBTA/TOPO case.
- `data/reference/produced_water/smackover_usgs_clean_observation_summary.csv`: summary statistics for the local clean Smackover observation set.
- `data/reference/produced_water/smackover_li_tds_sensitivity_basis.csv`: observed and presentation-sensitivity Li/TDS rows.
- `data/reference/produced_water/smackover_critical_minerals_ree_status.csv`: trace-metal and REE reporting-status table for the local clean Smackover source set.
