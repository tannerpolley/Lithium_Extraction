from __future__ import annotations
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[3]
sys.path.insert(0, str(THIS_FILE.parent))
import yu_2024_figure6_replication as rep

runtime_mod = rep._load_pcsaft_runtime_module()
user_params, k_ij, k_hb, l_ij, user_options = rep._load_dataset(rep.DATASET_DIR)
matrices = {"k_ij": k_ij, "k_hb": k_hb, "l_ij": l_ij}
point = rep._load_exp_points(rep.DEFAULT_DIGITIZED_CSV)[1]
row = rep._solve_point(
    oa_ratio=point.oa_ratio,
    e_li_exp_pct=point.e_li_exp_pct,
    e_mg_exp_pct=point.e_mg_exp_pct,
    top_conc_mol_per_l_org=1.9,
    temp_k=298.15,
    pressure_pa=1.013e5,
    user_params=user_params,
    matrices=matrices,
    user_options=user_options,
    runtime_mod=runtime_mod,
)
print(row)

