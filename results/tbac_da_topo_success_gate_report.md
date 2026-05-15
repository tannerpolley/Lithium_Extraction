# TBAC/DA DES + TOPO Case-Study Success Gates

| Gate | Status | Evidence |
|---|---|---|
| Pinned environment | Pass | PrOMMiS, IDAES, Pyomo, epcsaft, notebook dependencies installed through uv. |
| Feed and source registers | Pass | Master-schema feed table and source register exist. |
| Stage-response foundation | Pass | Bounded source-anchored stage response and ALAMO train/validation tables exist. |
| IDAES ALAMO | Pass | AlamoSurrogate JSON loads and SurrogateBlock residuals are within tolerance. |
| PrOMMiS/IDAES | Pass | SolventExtraction/MSContactor outputs are optimal with DOF zero and residual below tolerance. |
| Screening TEA | Pass | Assumption register and TEA/UQ result table exist with positive LCE cost intensity. |
| Notebook execution | Pass | Copied notebook exists and has no recorded error outputs. |
| Rendered deck | Pass | Reveal.js deck exists. |
| Final wording | Pass | Forbidden final-facing phrases absent from scanned artifacts. |

All reported outputs are bounded to the accepted case-study basis: source-backed feed information, source-anchored generated demonstration stage response, IDAES AlamoSurrogate propagation, and real PrOMMiS/IDAES staged extraction.
