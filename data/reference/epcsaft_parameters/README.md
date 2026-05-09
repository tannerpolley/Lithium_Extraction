# ePC-SAFT Parameter Payloads

This folder contains local Lithium_Extraction ePC-SAFT-style parameter payloads used by analysis scripts. It is not a complete predictive ePC-SAFT parameter library.

Use these status rules before running or extending an equilibrium workflow:

- `2024_Hubach/` is a local mirror of the package dataset `2024_Hubach` for the Hubach ionic-liquid method-reference case. The user options should match the package canonical `2024_Hubach` options.
- `2024_Yu/` is a method-reference payload for Yu Figure 6 workflows. It has pure and binary parameters for `H2O`, `TOP`, `[HOEMIM][Tf2N]`, `Li+`, `Mg2+`, and `Cl-`, plus an external reactive wrapper under `reaction/`. It is not a general HBTA/TOPO produced-water parameter set.

Non-package-ready parameter artifacts live outside this folder:

- `data/reference/epcsaft_parameter_catalog/legacy_epcsaft_properties/` contains the legacy copied package/default catalog used by `data/epcsaft_properties.py` for fallback components. It is not a complete scenario-specific runtime payload.
- `data/reference/extraction_models/gando_2025/` contains source-regressed HBTA/TOPO stage-model parameters, not pure-component ePC-SAFT parameters for HBTA, TOPO, diluent, or organic complexes.
- `data/reference/epcsaft_parameter_fits/rezaee_2026/` contains a diagnostic DES pseudo-component fit and reported Rezaee parameter notes. It is a regression smoke-test source, not a replacement for HBTA/TOPO/sulfonated-kerosene parameters.

For new full ePC-SAFT datasets, use the package layout:

```text
data/reference/epcsaft_parameters/<DatasetName>/
  user_options.json
  pure/any_solvent.csv
  mixed/binary_interaction/k_ij.csv
  mixed/binary_interaction/k_hb_ij.csv
  mixed/binary_interaction/l_ij.csv
```

Do not put runtime flags such as `debug` in `user_options.json`. Runtime/debug behavior belongs in scripts or CLI options.
