# ePC-SAFT Parameter Readiness Audit

Date: 2026-05-07

> Superseded context, 2026-05-08: this audit predates the Rezaee pivot and still describes HBTA/TOPO as the flagship. The current Phase 0-9 basis is Rezaee DES/TOPO as a source-regressed Li/Na bridge with ePC-SAFT/PC-SAFT diagnostics. HBTA/TOPO remains a comparison and future parameterization lane.

Scope: Lithium_Extraction ePC-SAFT-facing datasets, options, and case-study components.

## Verdict

The flagship HBTA/TOPO produced-water case still needs organic parameter work before it can be claimed as a full predictive reactive ePC-SAFT LLE model. The current presentation-ready model is a source-regressed Li/Na staged-transfer bridge with ePC-SAFT aqueous activity support when available and an explicit divalent-pretreatment assumption.

Hubach 2024 and Yu 2024 are useful method-reference systems, but they do not close the HBTA/TOPO parameter gap.

## Runtime Environment Gate

This project should use Python 3.13 for local path installs against `C:\Users\Tanner\Documents\git\ePC-SAFT`. The upstream package build currently provides a CPython 3.13 native extension in the source checkout. A Python 3.12 Lithium environment can fail before any parameter or solver test runs.

## Component Coverage

| Component or group | Current status | Source/path | Needs regression or curation? |
|---|---|---|---|
| `H2O` | Available | Package datasets and local Hubach/Yu payloads | No, but use the correct dataset basis. |
| `Li+`, `Na+`, `K+`, `Cl-`, `Br-` | Available in package defaults/reference sets | ePC-SAFT package parameter catalog and defaults | No for basic aqueous support; validate selected set for each case. |
| `Mg2+` | Pretreatment/feed-context species for the active case | Source feed tables and Yu method-reference payload | No for the active Li/Na showcase; only needed if a future branch claims divalent extraction. |
| `Ca2+`, `Sr2+`, `Ba2+`, `SO4--` | Pretreatment/feed-context species for the active case | Source feed tables and gap inventories under `data/reference/produced_water/` | No for the active Li/Na showcase; document pretreatment/pass-through assumptions. |
| `TBP`, `[emim][tcb]` | Available for Hubach method-reference case | Package `2024_Hubach`; local `data/reference/epcsaft_parameters/2024_Hubach/` mirror | No for Hubach; not a HBTA/TOPO substitute. |
| `TOP`, `[HOEMIM][Tf2N]` | Available for Yu method-reference case | `data/reference/epcsaft_parameters/2024_Yu/` | Use only in Yu scope; not TOPO/HBTA. |
| `TOPO` | Missing for flagship model | Rezaee 2026 reports a TOPO-style parameter lead, but it is not converted into a canonical runtime payload | Yes. |
| `HBTA` | Missing/unverified | Zhang 2017 and Hanada 2021 support chemistry/physical-property fitting, not direct ePC-SAFT closure | Yes. |
| Sulfonated kerosene/diluent | Missing/unverified | Case-study source uses a solvent mixture, not a single pure component | Yes, or choose and document a surrogate such as an alkane/pseudo-component. |
| `Li(BTA)(TOPO)n` | Missing | No runtime parameter payload | Yes after reaction-network choice. |
| Divalent complexes | Out of active scope | Divalent ions are assumed pretreated away | No for the active Li/Na showcase. |
| `D2EHPA-SURR`, `TBP-SURR` | Script-local placeholders | Jang diagnostic script | Yes before treating as predictive. |
| `Rezaee_DES`, `RLi`, `RNa` | Diagnostic notes/fits only | `data/reference/epcsaft_parameter_fits/rezaee_2026/des_nonassoc_fit.json` | Convert to a complete runtime payload before production use. |

## Provenance

- Hubach 2024: `2024_Hubach` package dataset and local `huback_2024/` mirror, DOI `10.1021/acs.jced.4c00074`.
- Yu 2024: local method-reference payload, DOI `10.1016/j.ces.2023.119682`.
- Shan/Gando 2025: stage/case-study anchor for HBTA/TOPO produced-water extraction, DOI `10.3390/W17152258`.
- Zhang 2017: HBTA/TOPO/Li stoichiometry and selectivity anchor, DOI `10.1016/j.seppur.2017.07.028`.
- Hanada 2021: HBTA/TOPO physical-property lead for pseudo-component fitting, DOI `10.1021/acssuschemeng.0c07606`.
- Rezaee 2026: PC-SAFT/ePC-SAFT modeling-method and TOPO/DES parameter lead, DOI `10.1016/j.fluid.2026.114737`.

## Dataset Organization Findings

- The local `data/reference/epcsaft_parameters/2024_Hubach/` and `data/reference/epcsaft_parameters/2024_Yu/` folders now use the package-style layout with `pure/any_solvent.csv` and `mixed/binary_interaction/*.csv`.
- Source-regressed extraction-model payloads that are not complete ePC-SAFT datasets live in `data/reference/extraction_models/`.
- Diagnostic parameter-fit payloads that are not complete ePC-SAFT datasets live in `data/reference/epcsaft_parameter_fits/`.
- `data/reference/epcsaft_parameter_catalog/legacy_epcsaft_properties/` is the legacy copied default catalog used by `data/epcsaft_properties.py` for fallback/default components. It is intentionally separated from complete runtime-style datasets under `data/reference/epcsaft_parameters/<DatasetName>/`.
- New reusable datasets should live in the package-style `data/reference/epcsaft_parameters/<DatasetName>/` layout or under analysis-local `data/input/parameters/` when not reusable.
- Generated retry/debug outputs should move out of `data/multiphase/` over time and into analysis-local `results/<plot_set_or_run>/`.

## User Options Findings

- Hubach local options were updated to match the package `2024_Hubach` canonical settings: combined relative-permittivity rule, analytical derivatives, fitted Born diameter, solvation-shell model, and dielectric saturation.
- Yu options are package-canonical after removing the runtime `debug` key from the dataset file.
- Runtime flags belong in scripts/CLI options, not in `user_options.json`.

## Next Parameter Work

1. Keep the active target to Li over Na after divalent pretreatment. Do not add Mg/Ca/Sr/Ba extraction or equilibrium work to this branch.
2. Use Rezaee 2026 as a parameter-regression smoke path, not as a direct HBTA/TOPO closure.
3. Use Zhang 2017 and Hanada 2021 to fit apparent Li/Na reaction constants and organic pseudo-component properties if direct parameters remain unavailable.
4. Keep Hubach/Yu as method-reference diagnostics for the package electrolyte LLE solver, not as the flagship produced-water chemistry.
