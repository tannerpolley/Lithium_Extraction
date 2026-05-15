# TBAC/DA DES + TOPO Case-Study Success Gates

| Requirement | Status | Evidence |
|---|---|---|
| Pinned environment | Pass | `uv sync` resolves the project environment; PrOMMiS, IDAES, Pyomo, epcsaft, and notebook dependencies import through `uv`. |
| ePC-SAFT final-mode contract | Pass | `scripts/check_epcsaft_integration.py --mode final` verifies the pinned `epcsaft` source and downstream adapter contract. |
| Feed and source registers | Pass | `selected_case_study_feeds.csv` and `produced_water_feed_source_register.csv` exist with source, quality, and simulation-use fields. |
| Two-domain design | Pass | `tbac_da_topo_two_domain_lhs_design.csv` contains source-paper and produced-water-centered design rows with fixed chemistry metadata. |
| Stage-response foundation | Pass | `tbac_da_topo_stage_response_data.csv` is bounded, deterministic, and labeled as source-anchored generated demonstration data. |
| IDAES ALAMO | Pass | `models/tbac_da_topo_alamo_surrogate.json` loads through IDAES and uses `logit_k_Li` and `logit_k_Na` as primary outputs. |
| IDAES SurrogateBlock | Pass | The SurrogateBlock smoke path loads the ALAMO JSON and reports residuals within tolerance. |
| PrOMMiS/IDAES staged extraction | Pass | Real PrOMMiS/IDAES `SolventExtraction` and `MSContactor` objects produce finite staged Li/Na outputs with DOF zero and mass balance residual within tolerance. |
| Screening TEA and UQ | Pass | `tbac_da_topo_tea_assumption_register.csv`, `tbac_da_topo_screening_tea_results.csv`, and `tbac_da_topo_screening_tea.md` exist with screening-level cost sensitivity outputs. |
| Notebook execution | Pass | `docs/tutorials/tbac_da_topo_produced_water_case_study.ipynb` is the executed project notebook copy and has no recorded error outputs. |
| Final Beamer source | Pass | `slides/final_rezaee_calibrated_case_study_2026_05_08/deck.tex` is the final technical presentation source. |
| Final Beamer PDF | Pass | `slides/final_rezaee_calibrated_case_study_2026_05_08/deck.pdf` builds cleanly from the Beamer source. |
| Presentation visual content | Pass | The Beamer PDF includes the produced-water map, feed variance, pretreatment boundary, solvent basis, ALAMO validation, PrOMMiS/IDAES transfer path, staged recovery, screening TEA, ePC-SAFT extension, CMM/REE extension, hydrocarbon extension, and source summary. |
| Final wording | Pass | Final-facing reports, notebook content, Beamer source, and rendered Beamer PDF text avoid forbidden wording. |

All reported outputs are bounded to the accepted case-study basis: source-backed feed information, source-anchored generated demonstration stage response, IDAES AlamoSurrogate propagation, and real PrOMMiS/IDAES staged extraction.
