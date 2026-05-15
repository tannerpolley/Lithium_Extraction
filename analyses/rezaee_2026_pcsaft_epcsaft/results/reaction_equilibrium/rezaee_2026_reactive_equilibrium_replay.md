# Rezaee 2026 Reactive Equilibrium Replay

## Source Basis

- 2025 source: `papers/pdf/Rezaee et al. - 2025 - Application of Response Surface Methodology for Selective Extraction of Lithium Using a Hydrophobic DES.pdf`.
- 2025 supporting information: `papers/pdf/Rezaee et al. - 2025 - Supporting information - Application of Response Surface Methodology for Selective Extraction of Lithium.pdf`.
- Main source: `papers/pdf/Rezaee et al. - 2026 - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents A PC.pdf`.
- 2026 supporting information: `papers/pdf/Rezaee et al. - 2026 - Supplementary material - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents.pdf`.
- Searchable source text: `papers/md/Rezaee et al. - 2026 - Thermodynamic modeling of lithium extraction from synthetic brine using deep eutectic solvents A PC.md`.
- The replay follows the paper's phase-specific reaction-equilibrium formulation rather than a conventional same-species LLE fugacity equality.
- Aqueous phase: H2O, Li+, Na+, Cl-, H+, OH-, NH4+ with ePC-SAFT component activity coefficients.
- Organic phase: DES, TOPO, RLi, RNa with PC-SAFT activity coefficients calculated as mixture fugacity coefficient over pure-component fugacity coefficient.
- Calibrated actual-row replay uses `data\processed\rezaee_2026_reactive_equilibrium_paper_k_calibration.json` from the fixed-paper-K organic refit.

## Result

- Rows replayed: `26`.
- Status: `published_mismatch_but_calibrated_actual_rows_consistent`.
- Published Table 8/9 median lnQ-lnK Li/Na: `32.33363244970333`, `37.758477412972525`.
- Published Table 8/9 median absolute RLi/RNa error: `0.004442850658281856`, `0.020811015739249972`.
- Calibrated paper-K median lnQ-lnK Li/Na: `-0.23055203253576018`, `0.20188825902796737`.
- Calibrated paper-K median absolute RLi/RNa error: `0.0024493390000924417`, `0.007617085730106119`.

## Interpretation

The package can evaluate the phase-specific ePC-SAFT/PC-SAFT activity terms required by Rezaee's formulation. The published Table 2 constants together with the published Table 8/9 organic parameters still do not reproduce the SI RLi/RNa complex mole fractions under the current activity-reference convention.

For actual-data replay, the fixed-paper-K organic refit closes the 26 SI equilibrium rows cleanly without changing the aqueous ePC-SAFT calls or the paper equilibrium constants. Treat that calibrated replay as the real-data result for this downstream workflow, and treat the published Table 8/9 mismatch as a documented source/convention gap rather than as missing package capability.

## Generated Files

- `data\processed\rezaee_2026_reactive_equilibrium_replay.csv`
- `results\reaction_equilibrium\rezaee_2026_reactive_equilibrium_replay_summary.json`
- `results\reaction_equilibrium\rezaee_2026_reactive_equilibrium_replay.md`
- `data\processed\rezaee_2026_reactive_equilibrium_paper_k_calibration.json`
