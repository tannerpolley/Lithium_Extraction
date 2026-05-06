from __future__ import annotations
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

THIS_FILE = Path(__file__).resolve()
sys.path.insert(0, str(THIS_FILE.parent))
import yu_2024_figure6_replication as rep
import scripts.epcsaft_compat as pcs


def softmax(v):
    v = np.asarray(v, dtype=float)
    m = np.max(v)
    ex = np.exp(v - m)
    return ex / np.sum(ex)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def logit(p):
    p = min(max(float(p), 1e-12), 1.0 - 1e-12)
    return np.log(p / (1.0 - p))


def phase_state(t, p, x, params):
    rho = float(pcs.pcsaft_den(t, p, x, params, phase='liq'))
    lnfugcoef = np.asarray(pcs.pcsaft_lnfugcoef(t, rho, x, params), dtype=float)
    return lnfugcoef + np.log(np.maximum(x, 1e-30)) + math.log(float(p))


runtime_mod = rep._load_pcsaft_runtime_module()
user_params, k_ij, k_hb, l_ij, user_options = rep._load_dataset(rep.DATASET_DIR)
matrices = {"k_ij": k_ij, "k_hb": k_hb, "l_ij": l_ij}
mw = {comp: float(user_params[comp]["MW"]) for comp in rep.SPECIES}
n_feed = rep._build_feed_moles(2.0, 1.9, mw)
z_feed = n_feed / float(np.sum(n_feed))
params = rep._build_params(rep.SPECIES, 298.15, user_params, matrices, user_options, runtime_mod)
base = pcs.pcsaft_multiphase_lle(298.15, 1.013e5, z_feed, params, rep.SPECIES, options=rep._solver_profiles()[1])
if 'tpdf_seed_x' not in base:
    print('No TPDF seed available:', base.get('status'), base.get('message'))
    raise SystemExit(0)
seed_x = np.asarray(base['tpdf_seed_x'], dtype=float)
print('seed', seed_x)

neutral_idx = np.array([rep.IDX['H2O'], rep.IDX['TOP'], rep.IDX['[HOEMIM][Tf2N]']], dtype=int)
charged_idx = np.array([rep.IDX['Li+'], rep.IDX['Mg2+'], rep.IDX['Cl-']], dtype=int)
z = np.asarray(params['z'], dtype=float)
E = np.array([
    [0.0, 0.5, 1.0],
    [1.0, 0.0, 1.0],
], dtype=float)

mask = seed_x > 1e-10
beta_hi = np.min(z_feed[mask] / seed_x[mask]) * 0.98
beta0 = min(0.08, float(beta_hi) * 0.9)
print('beta_hi', beta_hi, 'beta0', beta0)

def residual(y, weight):
    x1 = softmax(np.concatenate([y[:-1], [0.0]]))
    beta = beta0 * sigmoid(y[-1])
    x2 = (z_feed - beta * x1) / (1.0 - beta)
    if np.any(~np.isfinite(x2)) or np.any(x2 <= 1e-14):
        return np.full(8, 1e4)
    if abs(np.sum(x2) - 1.0) > 1e-8:
        return np.full(8, 1e4)
    try:
        l1 = phase_state(298.15, 1.013e5, x1, params)
        l2 = phase_state(298.15, 1.013e5, x2, params)
    except Exception:
        return np.full(8, 1e4)
    d = l1 - l2
    res = []
    res.extend(d[neutral_idx].tolist())
    res.extend((E.dot(d[charged_idx])).tolist())
    res.append(float(np.dot(z, x1)))
    res.append(weight * (x1[rep.IDX['TOP']] - seed_x[rep.IDX['TOP']]))
    res.append(weight * (x1[rep.IDX['H2O']] - seed_x[rep.IDX['H2O']]))
    return np.asarray(res, dtype=float)

xstart = np.maximum(seed_x, 1e-12)
xstart /= np.sum(xstart)
y0 = np.zeros(len(rep.SPECIES), dtype=float)
y0[:-1] = np.log(np.maximum(xstart[:-1], 1e-15) / xstart[-1])
y0[-1] = logit(beta0 / beta0)
for weight in [0.1, 1.0, 5.0, 20.0]:
    sol = least_squares(residual, y0, args=(weight,), method='trf', ftol=1e-10, xtol=1e-10, gtol=1e-10, max_nfev=400)
    x1 = softmax(np.concatenate([sol.x[:-1], [0.0]]))
    beta = beta0 * sigmoid(sol.x[-1])
    x2 = (z_feed - beta * x1) / (1.0 - beta)
    print('weight', weight, 'cost', sol.cost, 'beta', beta)
    print('x1', x1)
    print('x2', x2)
    print('split', np.max(np.abs(x1 - x2)))
