from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from scripts.gando_2025_pcsaft_repro.gando_2025_selective_model import (
    DEFAULT_CONFIG_JSON,
    load_payload,
    load_selective_config,
    run_three_stage_crossflow,
)

OUT_DIR = REPO_ROOT / 'data' / 'multiphase'
OUT_CSV = OUT_DIR / 'gando_2025_stage3_comparison.csv'
OUT_MD = OUT_DIR / 'gando_2025_stage3_comparison.md'
OUT_PNG = OUT_DIR / 'gando_2025_stage3_efficiency_plot.png'

TABLE4_CUM = np.array([54.95, 85.60, 97.17], dtype=float)
LI_FEED_MG_L = 60.0
NA_FEED_MG_L = 10900.0
TOP_MOL_L = 0.015
OA_RATIO = 1.0


def _write_csv(result) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow([
            'stage',
            'paper_li_cumulative_pct',
            'calc_li_stage_pct',
            'calc_li_cumulative_pct',
            'calc_na_stage_pct',
            'calc_na_cumulative_pct',
            'calc_li_distribution_ratio',
            'calc_li_na_selectivity',
        ])
        for idx in range(3):
            writer.writerow([
                idx + 1,
                TABLE4_CUM[idx],
                result.li_stage_pct[idx],
                result.li_cumulative_pct[idx],
                result.na_stage_pct[idx],
                result.na_cumulative_pct[idx],
                result.li_distribution_ratio[idx],
                result.li_na_selectivity[idx],
            ])


def _write_markdown(result, config_payload: dict) -> None:
    lines: list[str] = []
    lines.append('# Gando 2025 Three-Stage Crossflow Showcase')
    lines.append('')
    lines.append('## Basis')
    lines.append('')
    lines.append(f'- Config: `{DEFAULT_CONFIG_JSON}`')
    lines.append('- Mechanism: external Li-selective HBTA/TOPO chelation wrapper applied outside the bare PC-SAFT phase split.')
    lines.append('- Purpose: preserve lithium-specific extraction in the showcase chain while keeping sodium extraction low.')
    lines.append(f'- Feed: Li = {LI_FEED_MG_L:.3f} mg/L, Na = {NA_FEED_MG_L:.3f} mg/L, O/A = {OA_RATIO:.3f}, TOP = {TOP_MOL_L:.6f} mol/L.')
    lines.append('')
    lines.append('## Fitted Wrapper Parameters')
    lines.append('')
    params = config_payload['parameters']
    lines.append(f"- `log10(K_Li) = {params['log10_k_li']:.8f}`")
    lines.append(f"- `log10(K_Na) = {params['log10_k_na']:.8f}`")
    lines.append(f"- `log10(capacity factor) = {params['log10_capacity_factor']:.8f}`")
    lines.append(f"- `saltout gain = {params['saltout_gain']:.8f}`")
    lines.append(f"- `saltout ref = {params['saltout_ref_mol_L']:.6f} mol/L`")
    lines.append('')
    lines.append('## Stage Results')
    lines.append('')
    lines.append('| Stage | Paper $E_{Li,cum}$ (%) | Calc $E_{Li,stage}$ (%) | Calc $E_{Li,cum}$ (%) | Calc $E_{Na,stage}$ (%) | Calc $E_{Na,cum}$ (%) | $D_{Li}$ | $S_{Li/Na}$ |')
    lines.append('|---:|---:|---:|---:|---:|---:|---:|---:|')
    for idx in range(3):
        lines.append(
            f"| {idx + 1} | {TABLE4_CUM[idx]:.4f} | {result.li_stage_pct[idx]:.4f} | {result.li_cumulative_pct[idx]:.4f} | {result.na_stage_pct[idx]:.4f} | {result.na_cumulative_pct[idx]:.4f} | {result.li_distribution_ratio[idx]:.4f} | {result.li_na_selectivity[idx]:.4f} |"
        )
    lines.append('')
    lines.append('## Notes')
    lines.append('')
    lines.append('- This showcase intentionally uses an external reaction/selectivity wrapper because the bare ion-partitioning flash does not preserve the Li-over-Na selectivity seen in the HBTA/TOPO system.')
    lines.append('- Sodium extraction is kept near 1% per stage as a showcase calibration target; the paper reports sodium as non-specific and mildly promotive rather than strongly co-extracted.')
    OUT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _write_plot(result) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stages = np.array([1, 2, 3], dtype=float)
    fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=180)
    ax.plot(stages, TABLE4_CUM, color='black', marker='o', linewidth=2.0, label='Paper Li cumulative')
    ax.plot(stages, np.asarray(result.li_cumulative_pct, dtype=float), color='#d62728', marker='s', linewidth=2.0, label='Calc Li cumulative')
    ax.plot(stages, np.asarray(result.na_cumulative_pct, dtype=float), color='#1f77b4', marker='^', linewidth=2.0, label='Calc Na cumulative')
    ax.set_xlabel('Stage')
    ax.set_ylabel('Cumulative extraction (%)')
    ax.set_xticks(stages)
    ax.set_ylim(0.0, 100.0)
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc='lower right')
    fig.tight_layout()
    fig.savefig(OUT_PNG, bbox_inches='tight')
    plt.close(fig)


def run_stage3_showcase() -> tuple[Path, Path, Path]:
    config = load_selective_config(DEFAULT_CONFIG_JSON)
    payload = load_payload(DEFAULT_CONFIG_JSON)
    result = run_three_stage_crossflow(
        li_mg_L=LI_FEED_MG_L,
        na_mg_L=NA_FEED_MG_L,
        top_mol_L=TOP_MOL_L,
        o_to_a_ratio=OA_RATIO,
        config=config,
    )
    _write_csv(result)
    _write_markdown(result, payload)
    _write_plot(result)
    print(f'Saved CSV: {OUT_CSV}')
    print(f'Saved Markdown: {OUT_MD}')
    print(f'Saved Plot: {OUT_PNG}')
    return OUT_CSV, OUT_MD, OUT_PNG


def _parse_args() -> argparse.Namespace:
    return argparse.ArgumentParser(description='Gando 2025 three-stage selective-crossflow showcase.').parse_args()


def main() -> None:
    _parse_args()
    run_stage3_showcase()


if __name__ == '__main__':
    main()
