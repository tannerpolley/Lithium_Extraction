import numpy as np
from scipy.optimize import minimize
# from pcsaft_electrolyte_py_polley import pcsaft_den, pcsaft_lnfugcoef
from pcsaft import pcsaft_den, pcsaft_lnfugcoef
from ePC_SAFT_properties import get_prop_dict

np.set_printoptions(formatter={'float': '{:0.8f}'.format})

def ion_to_salt(x_cat, x_an, z_cat, z_an):
    return ((x_cat)**(1/np.abs(z_cat)) * (x_an)**(1/np.abs(z_an)))**(1/((1/np.abs(z_cat)) + (1/np.abs(z_an))))


def residuals(unknowns, scales):
    unknowns = unknowns * scales

    K, ξ = unknowns[:-1], unknowns[-1]

    x_aq = z / (1 + ξ * (K - 1))
    x_org = K * x_aq

    x_aq = x_aq/np.sum(x_aq)
    x_org = x_org/np.sum(x_org)

    prop_dic_aq = get_prop_dict(species, T)
    prop_dic_org = get_prop_dict(species, T)

    # Liquid densities & fugacity coefficients
    ρ_aq = pcsaft_den(T, P, x_aq, prop_dic_aq)
    ρ_org = pcsaft_den(T, P, x_org, prop_dic_org)

    lnϕ_aq = pcsaft_lnfugcoef(T, ρ_aq, x_aq, prop_dic_aq)
    lnϕ_org = pcsaft_lnfugcoef(T, ρ_org, x_org, prop_dic_org)

    lnf_aq = lnϕ_aq + np.log(x_aq)
    lnf_org = lnϕ_org + np.log(x_org)

    residuals = [lnf_aq - lnf_org]

    F = np.sum([(z[i] * (K[i] - 1)) / (1 + (K[i] - 1) * ξ) for i in range(len(K))])
    residuals.append(F)
    print(residuals)
    return residuals


def objective(x, scales):
    r = residuals(x, scales)
    obj = 0.5 * np.dot(r, r)  # 1/2 * ||r||^2
    print(obj)
    return obj


if __name__ == "__main__":

    run = True
    # run = False

    # solve = True
    solve = False

    if run:
        species = ['H2O-2B-Li', 'Butanol', 'Na+', 'K+', 'Cl-']

        T = 298.15  # K
        P = 101325
        R = .008314

        z = np.array([0.94037406, 0.04879523, 0.00193402, 0.00348133, 0.00541535])
        ξ_0 = .067
        x_aq_0 = np.array([0.93931115, 0.01190360, 0.00741536, 0.01697727, 0.02439262])
        x_org_0 = np.array([0.44236864, 0.55670884, 0.0000414783, 0.000419780, 0.000461259])
        K_0 = x_org_0/x_aq_0

        prop_dic_aq = get_prop_dict(species, T)
        prop_dic_org = get_prop_dict(species, T)

        # Liquid densities & fugacity coefficients
        ρ_aq = pcsaft_den(T, P, x_aq_0, prop_dic_aq)
        ρ_org = pcsaft_den(T, P, x_org_0, prop_dic_org)

        lnϕ_aq = pcsaft_lnfugcoef(T, ρ_aq, x_aq_0, prop_dic_aq)
        lnϕ_org = pcsaft_lnfugcoef(T, ρ_org, x_org_0, prop_dic_org)

        lnf_aq = lnϕ_aq + np.log(x_aq_0)
        lnf_org = lnϕ_org + np.log(x_org_0)

        lnf_aq_H2O, lnf_aq_But, lnf_aq_Na, lnf_aq_K, lnf_aq_Cl = lnf_aq
        lnf_org_H2O, lnf_org_But, lnf_org_Na, lnf_org_K, lnf_org_Cl = lnf_org
        
        lnf_aq_NaCl = ion_to_salt(lnf_aq_Na, lnf_aq_Cl, 1, -1)
        lnf_aq_KCl = ion_to_salt(lnf_aq_K, lnf_aq_Cl, 1, -1)

        lnf_org_NaCl = ion_to_salt(lnf_org_Na, lnf_org_Cl, 1, -1)
        lnf_org_KCl = ion_to_salt(lnf_org_K, lnf_org_Cl, 1, -1)
        #
        print(lnf_org_H2O, lnf_aq_H2O)
        print(lnf_org_But, lnf_aq_But)
        print(lnf_org_KCl, lnf_aq_KCl)
        print(lnf_org_NaCl, lnf_aq_NaCl)
        print()
        print(lnf_org_Na, lnf_aq_Na)
        print(lnf_org_K, lnf_aq_K)
        print(lnf_org_Cl, lnf_aq_Cl)

        

        if solve:

            guesses = np.array(list(K_0) + [ξ_0])
            scales = guesses
            ϵ = 1e-15
            bnds = [(ϵ, 1 / ϵ)] * (len(guesses) - 1)
            bnds.append((ϵ, 1.0 - ϵ))

            # Use L-BFGS-B (handles simple bounds). You could also try 'TNC' or 'Powell'.
            res = minimize(objective, guesses / scales, args=(scales,), method='L-BFGS-B', bounds=bnds, tol=1e-10,
                           options={"maxiter": 10000, "ftol": 1e-10})
            
            # res = root(residuals, np.array(res.x), args=(scales,))
            print(res.success, res.message)

            r_opt = residuals(res.x, scales) * scales
            solution = res.x * scales

            K_1, ξ_1 = solution[:-1], solution[-1]

            Φ = ξ_1 / (1 - ξ_1)

            x_aq_1 = z / (1 + ξ_1 * (K_1 - 1))
            x_org_1 = K_1 * x_aq_1

            print(x_org_1)
            print(x_aq_1)
