from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from analyses.gando_2025_pcsaft_repro.scripts.gando_2025_selective_model import (
    DEFAULT_CONFIG_JSON,
    load_payload,
    load_selective_config,
    mg_L_to_mol_L,
    run_three_stage_crossflow,
    solve_selective_stage,
)

OUT_DIR = REPO_ROOT / 'data' / 'multiphase'
OUT_CSV = OUT_DIR / 'gando_2025_pcsaft_repro.csv'
OUT_MD = OUT_DIR / 'gando_2025_pcsaft_repro.md'
OUT_PNG = OUT_DIR / 'gando_2025_pcsaft_repro.png'

TABLE4_CUM = np.array([54.95, 85.60, 97.17], dtype=float)
FIG3_NA_MG_L = np.array([0.0, 2000.0, 4000.0, 6000.0, 8000.0, 10900.0], dtype=float)
FIG3_LI_TARGET = np.array([49.82, np.nan, np.nan, np.nan, np.nan, 51.82], dtype=float)
LI_FEED_MG_L = 60.0
NA_FEED_MG_L = 10900.0
TOP_MOL_L = 0.015
OA_RATIO = 1.0


def _compute_na_sweep(config):
    rows = []
    li_mol_L = mg_L_to_mol_L(LI_FEED_MG_L, 'Li+')
    for na_mg_L, li_target in zip(FIG3_NA_MG_L, FIG3_LI_TARGET, strict=True):
        na_mol_L = mg_L_to_mol_L(float(na_mg_L), 'Na+')
        stage = solve_selective_stage(
            li_mol_L=li_mol_L,
            na_mol_L=na_mol_L,
            top_mol_L=TOP_MOL_L,
            o_to_a_ratio=OA_RATIO,
            config=config,
        )
        rows.append(
            {
                'na_mg_L': float(na_mg_L),
                'paper_li_stage_pct': li_target,
                'calc_li_stage_pct': stage.li_extraction_pct,
                'calc_na_stage_pct': stage.na_extraction_pct,
                'calc_li_distribution_ratio': stage.li_distribution_ratio,
                'calc_li_na_selectivity': stage.li_na_selectivity,
                'saltout_factor': stage.saltout_factor,
            }
        )
    return rows


def _write_csv(sweep_rows, three_stage) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow([
            'section',
            'na_mg_L',
            'paper_li_stage_pct',
            'calc_li_stage_pct',
            'calc_na_stage_pct',
            'calc_li_distribution_ratio',
            'calc_li_na_selectivity',
            'saltout_factor',
            'stage',
            'paper_li_cumulative_pct',
            'calc_li_cumulative_pct',
            'calc_na_cumulative_pct',
        ])
        for row in sweep_rows:
            writer.writerow([
                'na_sweep',
                row['na_mg_L'],
                row['paper_li_stage_pct'],
                row['calc_li_stage_pct'],
                row['calc_na_stage_pct'],
                row['calc_li_distribution_ratio'],
                row['calc_li_na_selectivity'],
                row['saltout_factor'],
                '', '', '', '',
            ])
        for idx in range(3):
            writer.writerow([
                'three_stage',
                '', '',
                three_stage.li_stage_pct[idx],
                three_stage.na_stage_pct[idx],
                three_stage.li_distribution_ratio[idx],
                three_stage.li_na_selectivity[idx],
                '',
                idx + 1,
                TABLE4_CUM[idx],
                three_stage.li_cumulative_pct[idx],
                three_stage.na_cumulative_pct[idx],
            ])


def _write_markdown(sweep_rows, three_stage, payload: dict) -> None:
    params = payload['parameters']
    lines: list[str] = []
    lines.append('# Gando 2025 Selective-Chelation Reproduction')
    lines.append('')
    lines.append('## Basis')
    lines.append('')
    lines.append(f'- Config: `{DEFAULT_CONFIG_JSON}`')
    lines.append('- Mechanism: Li-selective HBTA/TOPO chelation wrapper outside the direct PC-SAFT flash.')
    lines.append(f'- Nominal feed: Li = {LI_FEED_MG_L:.3f} mg/L, Na = {NA_FEED_MG_L:.3f} mg/L, O/A = {OA_RATIO:.3f}, TOP = {TOP_MOL_L:.6f} mol/L.')
    lines.append('')
    lines.append('## Wrapper Parameters')
    lines.append('')
    lines.append(f"- `log10(K_Li) = {params['log10_k_li']:.8f}`")
    lines.append(f"- `log10(K_Na) = {params['log10_k_na']:.8f}`")
    lines.append(f"- `log10(capacity factor) = {params['log10_capacity_factor']:.8f}`")
    lines.append(f"- `saltout gain = {params['saltout_gain']:.8f}`")
    lines.append(f"- `saltout ref = {params['saltout_ref_mol_L']:.6f} mol/L`")
    lines.append('')
    lines.append('## Figure 3 Style Na Sweep')
    lines.append('')
    lines.append('| Na (mg/L) | Paper $E_{Li}$ (%) | Calc $E_{Li}$ (%) | Calc $E_{Na}$ (%) | $D_{Li}$ | $S_{Li/Na}$ | Salt-out factor |')
    lines.append('|---:|---:|---:|---:|---:|---:|---:|')
    for row in sweep_rows:
        paper = '' if np.isnan(row['paper_li_stage_pct']) else f"{row['paper_li_stage_pct']:.4f}"
        lines.append(
            f"| {row['na_mg_L']:.0f} | {paper} | {row['calc_li_stage_pct']:.4f} | {row['calc_na_stage_pct']:.4f} | {row['calc_li_distribution_ratio']:.4f} | {row['calc_li_na_selectivity']:.4f} | {row['saltout_factor']:.4f} |"
        )
    lines.append('')
    lines.append('## Table 4 Style Three-Stage Result')
    lines.append('')
    lines.append('| Stage | Paper $E_{Li,cum}$ (%) | Calc $E_{Li,stage}$ (%) | Calc $E_{Li,cum}$ (%) | Calc $E_{Na,stage}$ (%) | Calc $E_{Na,cum}$ (%) |')
    lines.append('|---:|---:|---:|---:|---:|---:|')
    for idx in range(3):
        lines.append(
            f"| {idx + 1} | {TABLE4_CUM[idx]:.4f} | {three_stage.li_stage_pct[idx]:.4f} | {three_stage.li_cumulative_pct[idx]:.4f} | {three_stage.na_stage_pct[idx]:.4f} | {three_stage.na_cumulative_pct[idx]:.4f} |"
        )
    lines.append('')
    lines.append('## Interpretation')
    lines.append('')
    lines.append('- The wrapper keeps lithium extraction near the paper range while keeping sodium extraction low enough to demonstrate lithium-specific solvent extraction in the surrogate showcase chain.')
    lines.append('- Sodium is modeled as weakly co-extracted and mildly promotive; the large Li-over-Na selectivity comes from the external chelation law rather than bare ion partitioning.')
    OUT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _write_plot(sweep_rows) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    x = np.asarray([row['na_mg_L'] for row in sweep_rows], dtype=float)
    y_li = np.asarray([row['calc_li_stage_pct'] for row in sweep_rows], dtype=float)
    y_na = np.asarray([row['calc_na_stage_pct'] for row in sweep_rows], dtype=float)
    fig, ax = plt.subplots(figsize=(7.4, 4.8), dpi=180)
    ax.plot(x, y_li, color='#d62728', marker='o', linewidth=2.0, label='Calc Li extraction')
    ax.plot(x, y_na, color='#1f77b4', marker='s', linewidth=2.0, label='Calc Na extraction')
    finite = ~np.isnan(FIG3_LI_TARGET)
    ax.scatter(x[finite], FIG3_LI_TARGET[finite], facecolors='white', edgecolors='black', s=50, linewidths=1.2, label='Paper Li points')
    ax.set_xlabel('Na concentration in aqueous feed (mg/L)')
    ax.set_ylabel('Single-stage extraction (%)')
    ax.set_ylim(0.0, 60.0)
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc='lower right')
    fig.tight_layout()
    fig.savefig(OUT_PNG, bbox_inches='tight')
    plt.close(fig)


def run_reproduction() -> tuple[Path, Path, Path]:
    config = load_selective_config(DEFAULT_CONFIG_JSON)
    payload = load_payload(DEFAULT_CONFIG_JSON)
    sweep_rows = _compute_na_sweep(config)
    three_stage = run_three_stage_crossflow(
        li_mg_L=LI_FEED_MG_L,
        na_mg_L=NA_FEED_MG_L,
        top_mol_L=TOP_MOL_L,
        o_to_a_ratio=OA_RATIO,
        config=config,
    )
    _write_csv(sweep_rows, three_stage)
    _write_markdown(sweep_rows, three_stage, payload)
    _write_plot(sweep_rows)
    print(f'Wrote {OUT_CSV}')
    print(f'Wrote {OUT_MD}')
    print(f'Wrote {OUT_PNG}')
    return OUT_CSV, OUT_MD, OUT_PNG


def parse_args() -> argparse.Namespace:
    return argparse.ArgumentParser(description='Selective Gando 2025 showcase reproduction.').parse_args()


def main() -> int:
    parse_args()
    run_reproduction()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

