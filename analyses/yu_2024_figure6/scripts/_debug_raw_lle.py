from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

THIS_FILE = Path(__file__).resolve()
sys.path.insert(0, str(THIS_FILE.parent))
import yu_2024_figure6_replication as rep
import scripts.epcsaft_compat as pcs

runtime_mod = rep._load_pcsaft_runtime_module()
user_params, k_ij, k_hb, l_ij, user_options = rep._load_dataset(rep.DATASET_DIR)
matrices = {"k_ij": k_ij, "k_hb": k_hb, "l_ij": l_ij}
mw = {comp: float(user_params[comp]["MW"]) for comp in rep.SPECIES}
n_feed = rep._build_feed_moles(2.0, 1.9, mw)
z_feed = n_feed / float(np.sum(n_feed))
params = rep._build_params(rep.SPECIES, 298.15, user_params, matrices, user_options, runtime_mod)
res = pcs.pcsaft_multiphase_lle(298.15, 1.013e5, z_feed, params, rep.SPECIES, options=rep._solver_profiles()[0])
print('converged', res.get('converged'), 'n_phases', res.get('n_phases'), 'status', res.get('status'), 'message', res.get('message'))
for i,p in enumerate(res.get('phases', [])):
    print('phase', i, 'beta', p['beta'])
    print(np.array(p['x']))
