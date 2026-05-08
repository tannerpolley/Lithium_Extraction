from __future__ import annotations
import math
import numpy as np
from scipy.optimize import least_squares

LI_G_PER_L = 0.766
MG_G_PER_L = 98.984
MW_LI = 6.94
MW_MG = 24.31
N_LI0 = LI_G_PER_L / MW_LI
N_MG0 = MG_G_PER_L / MW_MG
C_IL = 0.09

target = {
    1: (37.0, 0.8),
    2: (75.0, 0.7),
    3: (83.2, 0.7),
    4: (87.3, 0.9),
    5: (88.7, 1.1),
    6: (89.0, 1.4),
}


def solve_extents(oa, logK_li, logK_mg, c_top, c_hoe0):
    V_aq = 1.0
    V_org = oa
    n_il0 = C_IL * V_org
    n_top0 = c_top * V_org
    K_li = 10**logK_li
    K_mg = 10**logK_mg

    def residual(y):
        xi_li = N_LI0 / (1.0 + math.exp(-y[0]))
        xi_mg = min(N_MG0, n_il0) / (1.0 + math.exp(-y[1]))
        if xi_li + xi_mg >= n_il0 or xi_li + xi_mg >= n_top0:
            return np.array([1e3, 1e3])
        n_li_aq = N_LI0 - xi_li
        n_mg_aq = N_MG0 - xi_mg
        n_il_org = n_il0 - xi_li - xi_mg
        n_top_org = n_top0 - xi_li - xi_mg
        n_hoe_aq = c_hoe0 * V_aq + xi_li + xi_mg
        if min(n_li_aq, n_mg_aq, n_il_org, n_top_org, n_hoe_aq) <= 0.0:
            return np.array([1e3, 1e3])
        c_li_aq = n_li_aq / V_aq
        c_mg_aq = n_mg_aq / V_aq
        c_il_org = n_il_org / V_org
        c_top_org = n_top_org / V_org
        c_hoe_aq = n_hoe_aq / V_aq
        c_licx_org = xi_li / V_org
        c_mgcx_org = xi_mg / V_org
        r1 = math.log10(c_hoe_aq * c_licx_org / (c_il_org * c_li_aq * c_top_org)) - logK_li
        r2 = math.log10(c_hoe_aq * c_mgcx_org / (c_il_org * c_mg_aq * c_top_org)) - logK_mg
        return np.array([r1, r2])

    sol = least_squares(residual, x0=np.array([0.0, -8.0]), bounds=(-20.0, 20.0), ftol=1e-12, xtol=1e-12, gtol=1e-12)
    xi_li = N_LI0 / (1.0 + math.exp(-sol.x[0]))
    xi_mg = min(N_MG0, n_il0) / (1.0 + math.exp(-sol.x[1]))
    return 100*xi_li/N_LI0, 100*xi_mg/N_MG0


def objective(p):
    logK_li, logK_mg, c_top, c_hoe0 = p
    errs = []
    for oa, (eli_t, emg_t) in target.items():
        eli, emg = solve_extents(oa, logK_li, logK_mg, c_top, c_hoe0)
        errs.append((eli - eli_t) / 2.5)
        errs.append((emg - emg_t) / 0.25)
    return np.array(errs)

sol = least_squares(objective, x0=np.array([0.2, -2.5, 1.9, 0.0056]), bounds=([-4.0, -10.0, 0.5, 1e-4], [6.0, 2.0, 4.0, 0.2]), ftol=1e-12, xtol=1e-12, gtol=1e-12, max_nfev=300)
print('sol', sol.x)
for oa in sorted(target):
    eli, emg = solve_extents(oa, *sol.x)
    print(oa, eli, emg, target[oa])
