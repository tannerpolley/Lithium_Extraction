# TBAC/DA DES + 10 wt% TOPO PrOMMiS/IDAES-Style Stage Results

## Decision

The process layer consumes the Agent 2 transfer variables directly. The staged process value reported for the deck is overall Li recovery after pretreatment Li loss, while the transfer-table value remains the extraction-step recovery on the clean Li/Na feed.

## Base Case

- Case: `smackover_ms2_main_anchor`.
- Solvent system: `TBAC(1):DA(2) hydrophobic DES + 10 wt% TOPO`.
- Transfer-table Li recovery: `87.988%`.
- Overall staged Li recovery after pretreatment loss: `85.348%`.
- Na co-extraction across the staged contactor: `16.056%`.
- Li2CO3-equivalent placeholder output at `1000 m3/day`: `254439 kg/year`.

## Recovery Reconciliation

| scenario | transfer_table_cumulative_Li_recovery_pct | prommis_idaes_staged_Li_recovery_pct | absolute_difference_pct_points | reason_for_difference | chosen_deck_value |
| --- | --- | --- | --- | --- | --- |
| base_smackover_ms2 | 87.988 | 85.348 | 2.640 | same stage count as transfer table; PrOMMiS/IDAES-style recovery includes pretreatment Li loss. | 85.348% overall recovery after pretreatment loss |
| stress_bakken_high_na | 90.198 | 85.688 | 4.510 | same stage count as transfer table; PrOMMiS/IDAES-style recovery includes pretreatment Li loss. | 85.688% overall recovery after pretreatment loss |
| favorable_smackover_high_li | 86.928 | 85.189 | 1.739 | same stage count as transfer table; PrOMMiS/IDAES-style recovery includes pretreatment Li loss. | 85.189% overall recovery after pretreatment loss |
| comparison_marcellus_card | 81.679 | 79.229 | 2.450 | same stage count as transfer table; PrOMMiS/IDAES-style recovery includes pretreatment Li loss. | comparison card only until missing Na/Ca/Sr/Ba source values are filled |
| sensitivity_pretreatment_li_loss | 87.988 | 80.949 | 7.039 | same stage count as transfer table; PrOMMiS/IDAES-style recovery includes pretreatment Li loss. | sensitivity value; base deck value remains Smackover MS-2 |
| sensitivity_solvent_loss | 87.988 | 85.348 | 2.640 | same stage count as transfer table; PrOMMiS/IDAES-style recovery includes pretreatment Li loss. | sensitivity value; base deck value remains Smackover MS-2 |
| sensitivity_stage_count_5 | 87.988 | 94.163 | 6.176 | different stage-count definition; PrOMMiS/IDAES-style recovery includes pretreatment Li loss. | sensitivity value; base deck value remains Smackover MS-2 |

## Boundary

Divalent ions appear as pretreatment removal and residual-leakage guardrails. They are not active Li/Na extraction species in this stage model.
