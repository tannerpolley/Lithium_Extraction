from __future__ import annotations
import copy
import random
import sys
from pathlib import Path
import numpy as np

THIS_FILE = Path(__file__).resolve()
sys.path.insert(0, str(THIS_FILE.parents[2]))
sys.path.insert(0, str(THIS_FILE.parent))
import scripts.epcsaft_compat as pcs
import yu_2024_figure6_replication as rep

runtime_mod = rep._load_pcsaft_runtime_module()
user_params, k_ij, k_hb, l_ij, user_options = rep._load_dataset(rep.DATASET_DIR)
base_matrices = {"k_ij": k_ij, "k_hb": k_hb, "l_ij": l_ij}
point = [p for p in rep._load_exp_points(rep.DEFAULT_DIGITIZED_CSV) if abs(p.oa_ratio - 3.0) < 1e-9][0]

random.seed(1234)

def eval_case(v):
    li_top_kij, li_top_khb, li_il_kij, li_il_khb, top_il_kij, li_dborn, mg_dborn = v
    up = copy.deepcopy(user_params)
    up["Li+"]["d_born"] = li_dborn
    up["Mg2+"]["d_born"] = mg_dborn
    ms = {k: copy.deepcopy(val) for k, val in base_matrices.items()}
    for a,b,val in [
        ("Li+","TOP",li_top_kij),("TOP","Li+",li_top_kij),
        ("Li+","[HOEMIM][Tf2N]",li_il_kij),("[HOEMIM][Tf2N]","Li+",li_il_kij),
        ("TOP","[HOEMIM][Tf2N]",top_il_kij),("[HOEMIM][Tf2N]","TOP",top_il_kij),
    ]:
        ms['k_ij'][(a,b)] = val
    for a,b,val in [
        ("Li+","TOP",li_top_khb),("TOP","Li+",li_top_khb),
        ("Li+","[HOEMIM][Tf2N]",li_il_khb),("[HOEMIM][Tf2N]","Li+",li_il_khb),
    ]:
        ms['k_hb'][(a,b)] = val
    mw = {comp: float(up[comp]['MW']) for comp in rep.SPECIES}
    n_feed = rep._build_feed_moles(point.oa_ratio, 1.9, mw)
    z_feed = n_feed / float(np.sum(n_feed))
    params = rep._build_params(rep.SPECIES, 298.15, up, ms, user_options, runtime_mod)
    out = pcs.pcsaft_multiphase_lle(298.15, 1.013e5, z_feed, params, rep.SPECIES, options=rep._solver_profiles()[0])
    if 'tpdf_seed_x' not in out:
        return float('inf'), float('nan'), float('nan'), float('nan'), np.full(len(rep.SPECIES), np.nan)
    xorg = np.asarray(out['tpdf_seed_x'], dtype=float)
    xorg = np.maximum(xorg, 1e-16)
    mask = xorg > 1e-12
    beta_max = float(np.min(z_feed[mask] / xorg[mask]) * 0.98)
    e_li = 100.0 * beta_max * xorg[rep.IDX['Li+']] / max(z_feed[rep.IDX['Li+']], 1e-30)
    e_mg = 100.0 * beta_max * xorg[rep.IDX['Mg2+']] / max(z_feed[rep.IDX['Mg2+']], 1e-30)
    mixed_org = float(xorg[rep.IDX['TOP']] + xorg[rep.IDX['[HOEMIM][Tf2N]']])
    score = abs(e_li - 83.2) + 10.0 * abs(e_mg - 0.7) + 20.0 * abs(mixed_org - 0.95)
    return score, e_li, e_mg, beta_max, xorg

best = []
for i in range(40):
    cand = (
        random.uniform(-1.0, 0.5),
        random.uniform(-1.0, 0.5),
        random.uniform(-1.0, 0.5),
        random.uniform(-1.0, 0.5),
        random.uniform(-0.5, 1.0),
        random.uniform(2.5, 5.0),
        random.uniform(1.5, 3.5),
    )
    try:
        score, e_li, e_mg, beta, xorg = eval_case(cand)
    except Exception as exc:
        print('fail', i, exc)
        continue
    best.append((score, cand, e_li, e_mg, beta, xorg[[rep.IDX['TOP'], rep.IDX['[HOEMIM][Tf2N]'], rep.IDX['Li+'], rep.IDX['Mg2+']]]))
    best.sort(key=lambda x: x[0])
    best = best[:8]
    print('done', i, 'best', round(best[0][0], 2), 'eli', round(best[0][2],2), 'emg', round(best[0][3],2), 'cand', tuple(round(v,3) for v in best[0][1]))

print('FINAL')
for row in best:
    print(row[0], tuple(round(v,4) for v in row[1]), row[2], row[3], row[4], np.round(row[5], 4))
