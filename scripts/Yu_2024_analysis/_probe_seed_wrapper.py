from __future__ import annotations
import copy
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
points = rep._load_exp_points(rep.DEFAULT_DIGITIZED_CSV)

def eval_case(li_top_kij, li_top_khb, li_il_kij, li_il_khb, top_il_kij, li_dborn, mg_dborn):
    up = copy.deepcopy(user_params)
    up["Li+"]["d_born"] = li_dborn
    up["Mg2+"]["d_born"] = mg_dborn
    ms = {k: copy.deepcopy(v) for k, v in base_matrices.items()}
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
    vals = []
    for point in points:
        n_feed = rep._build_feed_moles(point.oa_ratio, 1.9, mw)
        z_feed = n_feed / float(np.sum(n_feed))
        params = rep._build_params(rep.SPECIES, 298.15, up, ms, user_options, runtime_mod)
        out = pcs.pcsaft_multiphase_lle(298.15, 1.013e5, z_feed, params, rep.SPECIES, options=rep._solver_profiles()[1])
        if 'tpdf_seed_x' not in out:
            vals.append((point.oa_ratio, float('nan'), float('nan'), np.full(len(rep.SPECIES), np.nan)))
            continue
        xorg = np.asarray(out['tpdf_seed_x'], dtype=float)
        xorg = np.maximum(xorg, 1e-16)
        beta_max = float(np.min(z_feed[xorg > 1e-12] / xorg[xorg > 1e-12]) * 0.98)
        e_li = 100.0 * beta_max * xorg[rep.IDX['Li+']] / max(z_feed[rep.IDX['Li+']], 1e-30)
        e_mg = 100.0 * beta_max * xorg[rep.IDX['Mg2+']] / max(z_feed[rep.IDX['Mg2+']], 1e-30)
        vals.append((point.oa_ratio, e_li, e_mg, xorg))
    return vals

cands = [
    (0.3,0.3,1,1,1,2.784,3.1327),
    (-0.5,-0.5,-0.5,-0.5,1,4.0,2.0),
    (-0.8,-0.8,-0.8,-0.8,0.0,4.5,2.0),
    (-0.5,0.0,-0.5,0.0,0.5,4.0,2.0),
]
for cand in cands:
    print('cand', cand)
    vals = eval_case(*cand)
    for oa, eli, emg, xorg in vals:
        print(' oa', oa, 'Eli', round(eli,2), 'Emg', round(emg,2), 'xorg Li/Mg/TOP/IL', np.round(xorg[[rep.IDX['Li+'],rep.IDX['Mg2+'],rep.IDX['TOP'],rep.IDX['[HOEMIM][Tf2N]']]],4))
