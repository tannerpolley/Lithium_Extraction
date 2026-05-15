# TBAC/DA DES + TOPO IDAES AlamoSurrogate Validation

Mode: load_frozen_alamo.

The repository artifact is an IDAES `AlamoSurrogate` JSON loaded through the IDAES Surrogates API and embedded with `SurrogateBlock` in the process wrapper. The local training contract uses the required inputs `li_mg_L`, `na_mg_L`, `o_to_a_ratio`, and `topo_wt_pct`, with outputs `logit_k_Li` and `logit_k_Na`.

| Output | R2 | RMSE | MAE | Max abs error |
|---|---:|---:|---:|---:|
| logit_k_Li | 0.997919 | 0.017276 | 0.013915 | 0.055469 |
| logit_k_Na | 0.996647 | 0.022001 | 0.017385 | 0.077879 |

Validation artifacts:

- `models/tbac_da_topo_alamo_surrogate.json`
- `figures/alamo_parity_logit_k_Li.png`
- `figures/alamo_parity_logit_k_Na.png`
- `figures/alamo_residual_logit_k_Li.png`
- `figures/alamo_residual_logit_k_Na.png`
