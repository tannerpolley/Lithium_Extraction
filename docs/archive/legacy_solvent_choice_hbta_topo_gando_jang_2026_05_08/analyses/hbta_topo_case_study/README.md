# HBTA/TOPO Case Study

This analysis owns the Shan/Gando HBTA/TOPO case-study bridge, solvent candidate scorecard, Zotero review artifacts, Smackover handoff tables, and the current ePC-SAFT hard-case retry matrix. The Rezaee 2026 package-validation smoke now lives in `analyses/rezaee_2026_pcsaft_epcsaft`.

## ePC-SAFT Use

- Required for the Hubach/Jang retry matrix through direct `ePCSAFTMixture.equilibrium(kind="electrolyte_lle")` calls.
- Used as an aqueous activity/diagnostic support layer in the HBTA/TOPO bridge.
- The current HBTA/TOPO staged extraction model is source-regressed and limited to Li/Na transfer after divalent pretreatment; it is not a divalent extraction or divalent equilibrium model.

## Test Commands

```powershell
uv run python analyses\hbta_topo_case_study\scripts\hbta_topo_reactive_stage_solve.py
uv run python analyses\hbta_topo_case_study\scripts\solvent_candidate_scorecard.py
uv run python analyses\hbta_topo_case_study\scripts\epcsaft_equilibrium_retry_matrix_2026_05_07.py --timeout-seconds 25
```

The equivalent legacy `scripts\case_study\*.py` commands are wrappers.
