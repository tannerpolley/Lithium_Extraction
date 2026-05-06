from __future__ import annotations
import copy
import sys
from pathlib import Path

import numpy as np

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
sys.path.insert(0, str(THIS_FILE.parent))
sys.path.insert(0, str(REPO_ROOT))

import yu_2024_figure6_replication as rep

runtime_mod = rep._load_pcsaft_runtime_module()
user_params, k_ij, k_hb, l_ij, user_options = rep._load_dataset(rep.DATASET_DIR)
matrices = {"k_ij": k_ij, "k_hb": k_hb, "l_ij": l_ij}
points = rep._load_exp_points(rep.DEFAULT_DIGITIZED_CSV)

def evaluate(li_top_kij, li_top_khb, li_il_khb, top_il_kij, li_dborn, mg_dborn, top_conc):
    up = copy.deepcopy(user_params)
    ms = {name: copy.deepcopy(val) for name, val in matrices.items()}
    up["Li+"]["d_born"] = li_dborn
    up["Mg2+"]["d_born"] = mg_dborn
    for a, b, val in [
        ("Li+", "TOP", li_top_kij),
        ("TOP", "Li+", li_top_kij),
        ("TOP", "[HOEMIM][Tf2N]", top_il_kij),
        ("[HOEMIM][Tf2N]", "TOP", top_il_kij),
    ]:
        ms["k_ij"][(a, b)] = val
    for a, b, val in [
        ("Li+", "TOP", li_top_khb),
        ("TOP", "Li+", li_top_khb),
        ("Li+", "[HOEMIM][Tf2N]", li_il_khb),
        ("[HOEMIM][Tf2N]", "Li+", li_il_khb),
    ]:
        ms["k_hb"][(a, b)] = val

    rows = []
    for point in points:
        row = rep._solve_point(
            oa_ratio=point.oa_ratio,
            e_li_exp_pct=point.e_li_exp_pct,
            e_mg_exp_pct=point.e_mg_exp_pct,
            top_conc_mol_per_l_org=top_conc,
            temp_k=298.15,
            pressure_pa=1.013e5,
            user_params=up,
            matrices=ms,
            user_options=user_options,
            runtime_mod=runtime_mod,
        )
        rows.append(row)
    li = np.array([r.e_li_calc_pct for r in rows], dtype=float)
    mg = np.array([r.e_mg_calc_pct for r in rows], dtype=float)
    conv = all(r.converged for r in rows)
    return conv, li, mg

candidates = [
    (0.3, 0.3, 1.0, 1.0, 2.784, 3.1327, 1.9),
    (0.1, 0.1, 1.0, 1.0, 3.2, 2.4, 1.9),
    (-0.1, 0.0, 1.0, 1.0, 3.6, 2.2, 1.9),
    (-0.2, -0.2, 1.0, 1.0, 4.0, 2.0, 1.9),
    (0.3, 0.3, 0.4, 1.0, 3.2, 2.4, 1.9),
    (0.1, 0.1, 0.0, 0.2, 3.6, 2.2, 1.9),
]

for cand in candidates:
    conv, li, mg = evaluate(*cand)
    print("cand", cand)
    print("converged", conv)
    print("li", np.round(li, 3))
    print("mg", np.round(mg, 3))
