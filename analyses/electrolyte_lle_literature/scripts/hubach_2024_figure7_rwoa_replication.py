from __future__ import annotations

import argparse
import copy
import csv
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.epcsaft_compat as pcs
from data.epcsaft_properties import get_prop_dict

DEFAULT_PAPER_MD = REPO_ROOT / 'papers' / 'md' / 'Li+ Extraction from Aqueous Medium Using Tetracyanoborate Ionic.md'
DEFAULT_SI_MD = REPO_ROOT / 'papers' / 'md' / 'Supporting Information for Li+ extraction from aqueous medium using tetracyanoborate ionic liquids -.md'
DEFAULT_DATASET_DIR = REPO_ROOT / 'data' / 'pcsaft_parameters' / 'huback_2024'
DEFAULT_OUT_CSV = REPO_ROOT / 'data' / 'multiphase' / 'hubach_2024_figure7_replication.csv'
DEFAULT_OUT_MD = REPO_ROOT / 'data' / 'multiphase' / 'hubach_2024_figure7_replication.md'
DEFAULT_OUT_PNG = REPO_ROOT / 'data' / 'multiphase' / 'hubach_2024_figure7_replication.png'

SPECIES = ['H2O', 'TBP', '[emim][tcb]', 'Li+', 'Cl-']
IDX = {sp: i for i, sp in enumerate(SPECIES)}
REQUIRED_PURE_COLUMNS = [
    'component',
    'MW',
    'm',
    's',
    'e',
    'e_assoc',
    'vol_a',
    'assoc_scheme',
    'dipm',
    'dip_num',
    'z',
    'dielc',
    'd_born',
    'f_solv',
]

W_TBP_ORG = 0.85
W_IL_ORG = 0.15
W_LI_PPM = 2000.0


@dataclass
class ParsedS11Row:
    rw_oa: float
    e_exp_pct: float
    e_calc_s11_pct: float


@dataclass
class SolveRow:
    rw_oa: float
    e_exp_pct: float
    e_calc_s11_pct: float
    e_pkg_mb_pct: float
    e_pkg_eq13_pct: float
    converged: bool
    status: Any
    message: str
    residual_norm: float
    tpdf_min: float
    beta_org: float
    beta_aq: float
    phi_eq13: float
    x_li_org: float
    x_li_feed: float
    phase_org: Any


def _must_exist(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f'Missing required file: {path}')


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    _must_exist(path)
    with path.open('r', encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError(f'CSV is missing a header row: {path}')
        rows = list(reader)
    if not rows:
        raise ValueError(f'CSV has no data rows: {path}')
    return rows


def _strip_math(text: str) -> str:
    t = text
    for token in ('$', '\\mathrm', '\\text', '\\left', '\\right', '{', '}', '^', '_', '±'):
        t = t.replace(token, '')
    return t.strip()


def _parse_float(raw: str) -> float:
    s = _strip_math(raw).replace('\u2212', '-').replace('\u2013', '-')
    s = re.sub(r'\s+', '', s)
    m = re.search(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', s)
    if not m:
        raise ValueError(f'Could not parse float from {raw!r}')
    return float(m.group(0))


def _sigma_water(temp_k: float) -> float:
    return 2.7927 + (10.11 * np.exp(-0.01775 * temp_k) - 1.417 * np.exp(-0.01146 * temp_k))


def _parse_scalar(raw: str, field: str, comp: str) -> Any:
    txt = (raw or '').strip()
    if field == 'assoc_scheme':
        return None if txt == '' or txt.lower() in {'none', 'null', 'nan'} else txt
    if field == 's' and comp == 'H2O':
        low = txt.lower().replace(' ', '')
        if low.startswith('sigma=') and 'exp(-0.01775*t)' in low and 'exp(-0.01146*t)' in low:
            return _sigma_water
    if txt == '':
        raise ValueError(f'Missing value for {comp}.{field}')
    val = float(txt)
    if not math.isfinite(val):
        raise ValueError(f'Non-finite value for {comp}.{field}: {txt}')
    return val


def _load_user_params(dataset_dir: Path) -> tuple[dict[str, dict[str, Any]], dict[str, float]]:
    rows = _read_csv_rows(dataset_dir / 'pure.csv')
    hdr = set(rows[0].keys())
    missing_cols = [c for c in REQUIRED_PURE_COLUMNS if c not in hdr]
    if missing_cols:
        raise ValueError(f'pure.csv missing required columns {missing_cols}')

    by_comp = {str(r['component']).strip(): r for r in rows if str(r.get('component', '')).strip()}
    missing_comp = [c for c in SPECIES if c not in by_comp]
    if missing_comp:
        raise ValueError(f'pure.csv missing required components {missing_comp}')

    user_params: dict[str, dict[str, Any]] = {}
    mw: dict[str, float] = {}
    for comp in SPECIES:
        row = by_comp[comp]
        entry = {
            'MW': _parse_scalar(row['MW'], 'MW', comp),
            'm': _parse_scalar(row['m'], 'm', comp),
            's': _parse_scalar(row['s'], 's', comp),
            'e': _parse_scalar(row['e'], 'e', comp),
            'e_assoc': _parse_scalar(row['e_assoc'], 'e_assoc', comp),
            'vol_a': _parse_scalar(row['vol_a'], 'vol_a', comp),
            'assoc_scheme': _parse_scalar(row['assoc_scheme'], 'assoc_scheme', comp),
            'dipm': _parse_scalar(row['dipm'], 'dipm', comp),
            'dip_num': _parse_scalar(row['dip_num'], 'dip_num', comp),
            'z': _parse_scalar(row['z'], 'z', comp),
            'dielc': _parse_scalar(row['dielc'], 'dielc', comp),
            'd_born': _parse_scalar(row['d_born'], 'd_born', comp),
            'f_solv': _parse_scalar(row['f_solv'], 'f_solv', comp),
        }
        user_params[comp] = entry
        mw[comp] = float(entry['MW'])
    return user_params, mw


def _load_user_options(dataset_dir: Path) -> dict[str, Any]:
    path = dataset_dir / 'user_options.json'
    _must_exist(path)
    payload = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise ValueError(f'user_options.json must be an object: {path}')
    opts = payload.get('canonical_user_options', payload)
    if not isinstance(opts, dict):
        raise ValueError(f'user_options.json must define canonical_user_options object: {path}')
    if 'elec_model' not in opts:
        raise ValueError(f'user_options.json is missing canonical_user_options.elec_model: {path}')
    return opts


def _load_matrix(dataset_dir: Path, file_name: str) -> dict[tuple[str, str], float]:
    rows = _read_csv_rows(dataset_dir / 'binary_interaction' / file_name)
    cols = [c for c in rows[0].keys() if c != 'component']
    if set(cols) != set(SPECIES):
        raise ValueError(f'{file_name} columns must match {SPECIES}; got {cols}')

    seen: set[str] = set()
    out: dict[tuple[str, str], float] = {}
    for row in rows:
        rc = str(row.get('component', '')).strip()
        if rc not in SPECIES:
            raise ValueError(f'{file_name} has unexpected row component {rc}')
        seen.add(rc)
        for cc in cols:
            txt = str(row.get(cc, '0')).strip() or '0'
            val = float(txt)
            if not math.isfinite(val):
                raise ValueError(f'Non-finite value in {file_name} for ({rc},{cc})')
            out[(rc, cc)] = val

    missing_rows = [c for c in SPECIES if c not in seen]
    if missing_rows:
        raise ValueError(f'{file_name} missing row components {missing_rows}')
    return out


def _parse_table_s11(si_md: str) -> list[ParsedS11Row]:
    lines = si_md.splitlines()
    starts = [i for i, line in enumerate(lines) if 'Table S11' in line]
    if not starts:
        raise ValueError('Missing Table S11 section in supporting-information markdown')

    start = starts[-1]
    rows: list[str] = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith('|'):
            rows.append(stripped)
            continue
        if rows:
            break

    if not rows:
        raise ValueError('No markdown table found under Table S11 section')

    out: list[ParsedS11Row] = []
    for row in rows:
        cells = [c.strip() for c in row.split('|')][1:-1]
        if len(cells) < 3:
            continue
        if cells[0].startswith(':---') or 'exp' in cells[0].lower():
            continue
        if not re.match(r'^[-+]?\d', _strip_math(cells[0])):
            continue
        try:
            rw = _parse_float(cells[0])
            e_exp = _parse_float(cells[1])
            e_calc = _parse_float(cells[2])
        except ValueError:
            continue
        out.append(ParsedS11Row(rw_oa=rw, e_exp_pct=e_exp, e_calc_s11_pct=e_calc))

    if len(out) < 5:
        raise ValueError(f'Expected at least 5 Table S11 rows; parsed {len(out)}')
    return sorted(out, key=lambda r: r.rw_oa)


def _build_feed_moles(rw_oa: float, mw: dict[str, float]) -> np.ndarray:
    m_aq = 1.0
    m_li = W_LI_PPM * 1e-6 * m_aq
    n_li = m_li / mw['Li+']
    m_cl = n_li * mw['Cl-']
    m_water = m_aq - m_li - m_cl
    if m_water <= 0.0:
        raise ValueError('Non-positive water mass in feed basis; check ppm interpretation')

    m_org = rw_oa * m_aq
    m_tbp = W_TBP_ORG * m_org
    m_il = W_IL_ORG * m_org

    n = np.zeros(len(SPECIES), dtype=float)
    n[IDX['H2O']] = m_water / mw['H2O']
    n[IDX['TBP']] = m_tbp / mw['TBP']
    n[IDX['[emim][tcb]']] = m_il / mw['[emim][tcb]']
    n[IDX['Li+']] = n_li
    n[IDX['Cl-']] = n_li
    return n


def _apply_matrix(params: dict[str, Any], key: str, values: dict[tuple[str, str], float]) -> None:
    for (a, b), val in values.items():
        params[key][IDX[a], IDX[b]] = float(val)


def _solver_options(profile: str) -> list[dict[str, Any]]:
    if profile != 'stable':
        raise ValueError(f'Unknown solver profile: {profile}')
    return [
        {
            'tpdf_global_trials': 1200,
            'tpdf_local_trials': 600,
            'solver_tol': 1e-8,
            'max_nfev': 300,
            'split_tol': 1e-4,
            'debug': False,
        },
        {
            'tpdf_global_trials': 4000,
            'tpdf_local_trials': 2000,
            'solver_tol': 1e-9,
            'max_nfev': 1000,
            'charge_weight': 5000.0,
            'solver_accept_norm': 0.5,
            'split_tol': 1e-4,
            'debug': False,
        },
    ]


def _organic_solvent_mass_fraction(x: np.ndarray, mw: dict[str, float]) -> float:
    masses = np.asarray([x[IDX[s]] * mw[s] for s in SPECIES], dtype=float)
    mtot = float(np.sum(masses))
    if mtot <= 0.0:
        return float('nan')
    return float((masses[IDX['TBP']] + masses[IDX['[emim][tcb]']]) / mtot)


def _solve_point(rw_row: ParsedS11Row, t_k: float, p_pa: float, mw: dict[str, float], user_params: dict[str, dict[str, Any]], kij: dict[tuple[str, str], float], khb: dict[tuple[str, str], float], lij: dict[tuple[str, str], float], user_options: dict[str, Any], solver_profile: str) -> SolveRow:
    n_feed = _build_feed_moles(rw_row.rw_oa, mw)
    n_tot = float(np.sum(n_feed))
    z_feed = n_feed / n_tot

    params = get_prop_dict(SPECIES, z_feed, t_k, user_params=user_params, user_options=user_options)
    _apply_matrix(params, 'k_ij', kij)
    _apply_matrix(params, 'k_hb', khb)
    _apply_matrix(params, 'l_ij', lij)

    last: dict[str, Any] | None = None
    for opt in _solver_options(solver_profile):
        res = pcs.pcsaft_multiphase_lle(t_k, p_pa, z_feed, params, SPECIES, options=opt)
        last = res
        if bool(res.get('converged', False)) and int(res.get('n_phases', 0)) == 2:
            break

    if last is None:
        return SolveRow(rw_row.rw_oa, rw_row.e_exp_pct, rw_row.e_calc_s11_pct, float('nan'), float('nan'), False, None, 'No solver result', float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float(z_feed[IDX['Li+']]), None)

    if int(last.get('n_phases', 0)) != 2:
        return SolveRow(rw_row.rw_oa, rw_row.e_exp_pct, rw_row.e_calc_s11_pct, float('nan'), float('nan'), bool(last.get('converged', False)), last.get('status'), str(last.get('message', 'No 2-phase split')), float(last.get('residual_norm', float('nan'))), float(last.get('tpdf_min', float('nan'))), float('nan'), float('nan'), float('nan'), float('nan'), float(z_feed[IDX['Li+']]), None)

    p0, p1 = last['phases'][0], last['phases'][1]
    x0, x1 = np.asarray(p0['x'], dtype=float), np.asarray(p1['x'], dtype=float)

    if float(np.max(np.abs(x0 - x1))) < 1e-10 and abs(float(p0['beta']) - float(p1['beta'])) < 1e-10:
        return SolveRow(rw_row.rw_oa, rw_row.e_exp_pct, rw_row.e_calc_s11_pct, float('nan'), float('nan'), False, last.get('status'), 'Degenerate two-phase split (identical phase compositions)', float(last.get('residual_norm', float('nan'))), float(last.get('tpdf_min', float('nan'))), float('nan'), float('nan'), float('nan'), float('nan'), float(z_feed[IDX['Li+']]), None)

    org0 = _organic_solvent_mass_fraction(x0, mw)
    org1 = _organic_solvent_mass_fraction(x1, mw)
    if org0 >= org1:
        org, aq, org_idx = p0, p1, 0
    else:
        org, aq, org_idx = p1, p0, 1

    beta_org = float(org['beta'])
    beta_aq = float(aq['beta'])
    x_li_org = float(org['x'][IDX['Li+']])
    x_li_feed = float(z_feed[IDX['Li+']])

    n_li_init = float(n_feed[IDX['Li+']])
    n_li_org = beta_org * x_li_org * n_tot
    e_mb = 100.0 * n_li_org / max(n_li_init, 1e-300)

    phi = beta_org / max(beta_aq, 1e-300)
    e_eq13 = 100.0 * phi * x_li_org / max(x_li_feed, 1e-300)
    if beta_aq < 1e-10:
        e_eq13 = float('nan')

    return SolveRow(rw_row.rw_oa, rw_row.e_exp_pct, rw_row.e_calc_s11_pct, float(e_mb), float(e_eq13), bool(last.get('converged', False)), last.get('status'), str(last.get('message', '')), float(last.get('residual_norm', float('nan'))), float(last.get('tpdf_min', float('nan'))), beta_org, beta_aq, float(phi), x_li_org, x_li_feed, org_idx)


def _ard_aad(model: list[float], ref: list[float]) -> tuple[float, float]:
    pairs = [(m, r) for m, r in zip(model, ref) if np.isfinite(m) and np.isfinite(r)]
    if not pairs:
        return float('nan'), float('nan')
    arr_m = np.array([p[0] for p in pairs], dtype=float)
    arr_r = np.array([p[1] for p in pairs], dtype=float)
    ard = 100.0 * float(np.mean(np.abs(1.0 - arr_m / np.maximum(arr_r, 1e-300))))
    aad = float(np.mean(np.abs(arr_m - arr_r)))
    return ard, aad


def _fmt(x: Any, n: int = 6) -> str:
    if isinstance(x, (float, np.floating)):
        if not np.isfinite(x):
            return 'nan'
        return f'{float(x):.{n}g}'
    return str(x)


def _write_csv(path: Path, rows: list[SolveRow], ard_exp: float, aad_exp: float, ard_s11: float, aad_s11: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as fh:
        fields = [
            'section',
            'rw_oa',
            'e_exp_pct',
            'e_calc_s11_pct',
            'e_pkg_mb_pct',
            'e_pkg_eq13_pct',
            'residual_vs_exp_pct',
            'residual_vs_s11_calc_pct',
            'converged',
            'status',
            'message',
            'residual_norm',
            'tpdf_min',
            'beta_org',
            'beta_aq',
            'phi_eq13',
            'x_li_org',
            'x_li_feed',
            'phase_org',
        ]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({
                'section': 'point',
                'rw_oa': r.rw_oa,
                'e_exp_pct': r.e_exp_pct,
                'e_calc_s11_pct': r.e_calc_s11_pct,
                'e_pkg_mb_pct': r.e_pkg_mb_pct,
                'e_pkg_eq13_pct': r.e_pkg_eq13_pct,
                'residual_vs_exp_pct': r.e_pkg_mb_pct - r.e_exp_pct if np.isfinite(r.e_pkg_mb_pct) else '',
                'residual_vs_s11_calc_pct': r.e_pkg_mb_pct - r.e_calc_s11_pct if np.isfinite(r.e_pkg_mb_pct) else '',
                'converged': r.converged,
                'status': r.status,
                'message': r.message,
                'residual_norm': r.residual_norm,
                'tpdf_min': r.tpdf_min,
                'beta_org': r.beta_org,
                'beta_aq': r.beta_aq,
                'phi_eq13': r.phi_eq13,
                'x_li_org': r.x_li_org,
                'x_li_feed': r.x_li_feed,
                'phase_org': r.phase_org,
            })
        w.writerow({'section': 'summary', 'message': 'ARD/AAD vs exp', 'e_pkg_mb_pct': ard_exp, 'e_pkg_eq13_pct': aad_exp})
        w.writerow({'section': 'summary', 'message': 'ARD/AAD vs S11 calc', 'e_pkg_mb_pct': ard_s11, 'e_pkg_eq13_pct': aad_s11})


def _write_md(path: Path, rows: list[SolveRow], ard_exp: float, aad_exp: float, ard_s11: float, aad_s11: float, args: argparse.Namespace, user_options: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append('# Hubach 2024 Figure 7 Replication (Dataset-Driven)')
    lines.append('')
    lines.append('## Basis')
    lines.append('')
    lines.append(f'- Paper markdown: {args.paper_md}')
    lines.append(f'- Supporting-info markdown: {args.si_md}')
    lines.append(f'- Dataset directory: {args.dataset_dir}')
    lines.append(f'- Solver profile: {args.solver_profile}')
    lines.append(f'- Effective user_options: {json.dumps(user_options, sort_keys=True)}')
    lines.append('')
    lines.append('## Definitions')
    lines.append('')
    lines.append('- Primary efficiency: $E_{Li+}^{mb} = 100\\cdot n_{Li+,org}/n_{Li+,init}$')
    lines.append('- Diagnostic Eq. (13)-style: $E_{Li+}^{(13)} = 100\\cdot \\phi \\cdot x_{Li+,org}/x_{Li+,feed}$ with $\\phi=\\beta_{org}/\\beta_{aq}$')
    lines.append('')
    lines.append('## Pointwise Comparison')
    lines.append('')
    lines.append('| $R^w(O/A)$ | $E_{Li+,exp}$ (%) | $E_{Li+,calc}^{S11}$ (%) | $E_{Li+}^{mb}$ (%) | $E_{Li+}^{(13)}$ (%) | delta vs exp | delta vs S11-calc | converged | status |')
    lines.append('|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for r in rows:
        de = r.e_pkg_mb_pct - r.e_exp_pct if np.isfinite(r.e_pkg_mb_pct) else float('nan')
        ds = r.e_pkg_mb_pct - r.e_calc_s11_pct if np.isfinite(r.e_pkg_mb_pct) else float('nan')
        lines.append(f'| {_fmt(r.rw_oa,4)} | {_fmt(r.e_exp_pct,5)} | {_fmt(r.e_calc_s11_pct,5)} | {_fmt(r.e_pkg_mb_pct,5)} | {_fmt(r.e_pkg_eq13_pct,5)} | {_fmt(de,5)} | {_fmt(ds,5)} | {r.converged} | {_fmt(r.status,4)} |')
    lines.append('')
    lines.append('## Aggregated Deviations')
    lines.append('')
    lines.append(f'- ARD vs Table S11 experimental (%): {_fmt(ard_exp,6)}')
    lines.append(f'- AAD vs Table S11 experimental (pct-pts): {_fmt(aad_exp,6)}')
    lines.append(f'- ARD vs Table S11 calc (%): {_fmt(ard_s11,6)}')
    lines.append(f'- AAD vs Table S11 calc (pct-pts): {_fmt(aad_s11,6)}')
    lines.append('')
    lines.append('## Notes')
    lines.append('')
    lines.append('- Line in Figure uses package-computed values; symbols use Table S11 experimental values.')
    lines.append('- If package output differs from S11-calculated values, this report keeps true package output and reports mismatch transparently.')
    path.write_text('\n'.join(lines), encoding='utf-8')


def _write_plot(path: Path, rows: list[SolveRow], dense_grid: bool, dense_rows: Any = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    x = np.array([r.rw_oa for r in rows], dtype=float)
    y_exp = np.array([r.e_exp_pct for r in rows], dtype=float)
    y_pkg = np.array([r.e_pkg_mb_pct for r in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(7.4, 4.8), dpi=180)
    ax.scatter(x, y_exp, color='black', marker='o', s=32, label='Exp. (Table S11)')
    if dense_grid and dense_rows is not None:
        xd = np.array([r.rw_oa for r in dense_rows], dtype=float)
        yd = np.array([r.e_pkg_mb_pct for r in dense_rows], dtype=float)
        mask = np.isfinite(yd)
        ax.plot(xd[mask], yd[mask], color='#1f77b4', linewidth=2.0, label='PC-SAFT model')
    else:
        mask = np.isfinite(y_pkg)
        ax.plot(x[mask], y_pkg[mask], color='#1f77b4', linewidth=2.0, marker=None, label='PC-SAFT model')

    ax.set_xlabel(r'$R^w(O/A)$')
    ax.set_ylabel(r'$E_{Li+}$ (%)')
    ax.set_title('Hubach 2024 Figure 7 Replication')
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc='lower right')
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)


def _runtime_banner() -> None:
    print(f'Python: {sys.executable}')
    print(f'pcsaft module: {Path(pcs.__file__).resolve()}')
    print(f'pcsaft_multiphase_lle available: {hasattr(pcs, "pcsaft_multiphase_lle")}')


def _dense_rows_if_needed(dense_grid: bool, rows_s11: list[ParsedS11Row], t_k: float, p_pa: float, mw: dict[str, float], user_params: dict[str, dict[str, Any]], kij: dict[tuple[str, str], float], khb: dict[tuple[str, str], float], lij: dict[tuple[str, str], float], user_options: dict[str, Any], solver_profile: str) -> Any:
    if not dense_grid:
        return None
    rmin = min(r.rw_oa for r in rows_s11)
    rmax = max(r.rw_oa for r in rows_s11)
    grid = np.linspace(rmin, rmax, 33)
    dense: list[SolveRow] = []
    for rw in grid:
        dummy = ParsedS11Row(rw_oa=float(rw), e_exp_pct=float('nan'), e_calc_s11_pct=float('nan'))
        dense.append(_solve_point(dummy, t_k, p_pa, mw, user_params, kij, khb, lij, user_options, solver_profile))
    return dense


def run(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    _runtime_banner()

    _must_exist(Path(args.paper_md))
    si_md = Path(args.si_md).read_text(encoding='utf-8')
    s11_rows = _parse_table_s11(si_md)

    dataset_dir = Path(args.dataset_dir)
    user_params, mw = _load_user_params(dataset_dir)
    kij = _load_matrix(dataset_dir, 'k_ij.csv')
    khb = _load_matrix(dataset_dir, 'k_hb_ij.csv')
    lij = _load_matrix(dataset_dir, 'l_ij.csv')
    user_options = _load_user_options(dataset_dir)

    if args.elec_model is not None:
        user_options = copy.deepcopy(user_options)
        if isinstance(user_options.get('elec_model'), dict):
            user_options['elec_model']['base'] = args.elec_model
        else:
            user_options['elec_model'] = args.elec_model

    t_k = 294.15
    p_pa = 1.013e5

    solved_rows: list[SolveRow] = []
    for r in s11_rows:
        solved_rows.append(_solve_point(r, t_k, p_pa, mw, user_params, kij, khb, lij, user_options, args.solver_profile))

    model_mb = [r.e_pkg_mb_pct for r in solved_rows]
    s11_exp = [r.e_exp_pct for r in solved_rows]
    s11_calc = [r.e_calc_s11_pct for r in solved_rows]
    ard_exp, aad_exp = _ard_aad(model_mb, s11_exp)
    ard_s11, aad_s11 = _ard_aad(model_mb, s11_calc)

    dense_rows = _dense_rows_if_needed(bool(args.dense_grid), s11_rows, t_k, p_pa, mw, user_params, kij, khb, lij, user_options, args.solver_profile)

    _write_csv(Path(args.out_csv), solved_rows, ard_exp, aad_exp, ard_s11, aad_s11)
    _write_md(Path(args.out_md), solved_rows, ard_exp, aad_exp, ard_s11, aad_s11, args, user_options)
    _write_plot(Path(args.out_png), solved_rows, dense_grid=bool(args.dense_grid), dense_rows=dense_rows)

    print(f'Saved CSV: {args.out_csv}')
    print(f'Saved Markdown: {args.out_md}')
    print(f'Saved Plot: {args.out_png}')

    return Path(args.out_csv), Path(args.out_md), Path(args.out_png)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Replicate Hubach 2024 Figure 7 from dataset-sourced parameters using PC-SAFT.')
    p.add_argument('--paper-md', default=str(DEFAULT_PAPER_MD))
    p.add_argument('--si-md', default=str(DEFAULT_SI_MD))
    p.add_argument('--dataset-dir', default=str(DEFAULT_DATASET_DIR))
    p.add_argument('--out-csv', default=str(DEFAULT_OUT_CSV))
    p.add_argument('--out-md', default=str(DEFAULT_OUT_MD))
    p.add_argument('--out-png', default=str(DEFAULT_OUT_PNG))
    p.add_argument('--elec-model', default=None, choices=['legacy_default', '2020', '2014_s1', '2014_s2', '2005', '2008'])
    p.add_argument('--solver-profile', default='stable', choices=['stable'])
    p.add_argument('--dense-grid', action='store_true')
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    run(args)


if __name__ == '__main__':
    main()

