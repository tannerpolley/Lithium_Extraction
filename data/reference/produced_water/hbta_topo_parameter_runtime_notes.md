# HBTA/TOPO Parameter Runtime Notes

Last updated: 2026-05-07

## Runtime Path

The current local runtime path does not treat every broad catalog entry as available. The practical order is:

1. `pcsaft_properties.py` / `pcsaft_prop`
2. local ePC-SAFT parameter catalog if wired by the helper
3. scenario-specific parameter CSVs under `data/pcsaft_parameters/`

`data/all_pcsaft_fluids.json` is useful as a broad reference, but a species appearing there should not be presented as runtime-ready unless it is wired into the helper or a scenario parameter file.

## Coverage Correction

| Species | Current interpretation |
|---|---|
| water, Li+, Na+, K+, Mg2+, Cl-, Br- | Covered or expected covered in the local runtime path. |
| Ca2+ | Reference-only in broad library during this pass; not confirmed as default runtime-ready. |
| Sr2+, Ba2+ | Gaps. |
| SO4/SO42- | Partial reference-only status; not confirmed as runtime-ready for this case. |
| HBTA | Gap. |
| TOPO | Gap. |
| TOP | Runtime proxy available, but TOP is not TOPO and must be labeled if used as a surrogate. |
| TBP | Scenario-specific availability in older Hubach/Jang-style parameter files, not the HBTA/TOPO flagship chemistry. |
| hexane | Covered and usable as a simple organic surrogate. |
| n-dodecane / n-hexadecane | Broad reference candidates, not automatically runtime-ready. |
| Li-ligand and divalent-ligand complexes | Gaps for predictive ePC-SAFT parameters; current workflow uses a fitted reactive-stage HBTA/TOPO bridge. |

## Recommendation

For the current presentation skeleton, do not claim the HBTA/TOPO case has a complete predictive ePC-SAFT parameter set. Use:

- source-backed feed chemistry;
- literature-backed HBTA/TOPO process evidence;
- fitted reactive-stage transfer variables from `hbta_topo_reactive_stage_results.csv`;
- the formal Class-5 costing cap from `hbta_topo_formal_costing_results.csv`;
- this parameter table as the reason the next scientific step is parameterization and reaction-constant fitting.
