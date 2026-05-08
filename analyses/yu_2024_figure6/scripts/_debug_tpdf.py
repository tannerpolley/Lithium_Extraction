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
options = rep._solver_profiles()[1]
options['debug'] = True
res = pcs.pcsaft_multiphase_lle(298.15, 1.013e5, z_feed, params, rep.SPECIES, options=options)
print('tpdf_seed_x', np.array(res.get('tpdf_seed_x', [])))
print('tpdf_min', res.get('tpdf_min'))
if int(res.get('n_phases', 0)) == 2:
    print('split_norm', max(abs(np.array(res['phases'][0]['x'])-np.array(res['phases'][1]['x']))))
else:
    print('n_phases', res.get('n_phases'), 'status', res.get('status'), 'message', res.get('message'))
