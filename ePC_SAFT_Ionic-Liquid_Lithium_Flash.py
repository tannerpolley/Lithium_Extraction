import numpy as np
from scipy.optimize import root, minimize
from pcsaft import pcsaft_den, pcsaft_lnfugcoef
from ePC_SAFT_properties import get_prop_dict
from get_z_ionic_liquids import get_z

np.set_printoptions(formatter={'float': '{:0.8f}'.format})


def get_stuff(K_Li, K_Mg, ξ):
    x_TOP_aq = 1e-16
    x_IL_aq = 1e-16
    x_Li_aq = z[3] / (1 + ξ * (K_Li - 1))
    x_Mg_aq = z[4] / (1 + ξ * (K_Mg - 1))
    x_Cl_aq = x_Li_aq + 2 * x_Mg_aq
    x_H2O_aq = 1 - (x_TOP_aq + x_IL_aq + x_Li_aq + x_Mg_aq + x_Cl_aq)
    x_aq = np.array([x_H2O_aq, x_TOP_aq, x_IL_aq, x_Li_aq, x_Mg_aq, x_Cl_aq])

    x_H2O_org = 1e-16
    x_TOP_org = z[1] / ξ
    x_IL_org = z[2] / ξ
    x_Li_org = K_Li * x_aq[3]
    x_Mg_org = K_Mg * x_aq[4]
    x_Cl_org = (z[5] - (1 - ξ) * x_aq[5]) / ξ

    x_org = np.array([x_H2O_org, x_TOP_org, x_IL_org, x_Li_org, x_Mg_org, x_Cl_org])

    x_aq = np.array(x_aq) / sum(x_aq)
    x_org = np.array(x_org) / sum(x_org)

    K = x_org / x_aq

    return x_aq, x_org, K


def residuals(unknowns, scales):
    unknowns = unknowns * scales
    print(unknowns)
    K_Li, K_Mg, ξ = unknowns

    x_aq, x_org, K = get_stuff(K_Li, K_Mg, ξ)

    prop_dic_aq = get_prop_dict(species, T)
    prop_dic_org = get_prop_dict(species, T)

    # Liquid densities & fugacity coefficients
    ρ_aq = pcsaft_den(T, P, x_aq, prop_dic_aq)
    ρ_org = pcsaft_den(T, P, x_org, prop_dic_org)

    lnϕ_aq = pcsaft_lnfugcoef(T, ρ_aq, x_aq, prop_dic_aq)
    lnϕ_org = pcsaft_lnfugcoef(T, ρ_org, x_org, prop_dic_org)

    residuals = []

    for i in range(3, 5):
        r = np.log(x_aq[i]) + lnϕ_aq[i] - np.log(x_org[i]) - lnϕ_org[i]
        residuals.append(r)

    F = np.sum([(z[i] * (K[i] - 1)) / (1 + (K[i] - 1) * ξ) for i in range(3, 5)])
    F += z[1] / ξ + z[2] / ξ - z[0] / (1 - ξ)
    residuals.append(F)
    print(residuals)
    # print()
    return residuals


def objective(x, scales):
    r = residuals(x, scales)
    obj = 0.5 * np.dot(r, r)  # 1/2 * ||r||^2
    return obj


if __name__ == "__main__":

    run = True
    # run = False

    solve = True
    # solve = False

    if run:
        species = ['H2O-2B-Li', 'IL', 'TOP', 'Li+', 'Mg2+', 'Cl-']
        # species_aq = ['H2O', 'Li+', 'Mg2+', 'Cl-']
        # species_org = ['IL', 'TOP', 'Li+', 'Mg2+', 'Cl-']
        species_aq = ['H2O-2B-Li', 'Li+', 'Mg2+', 'Cl-']
        species_org = ['IL', 'TOP']
        species_org_2 = ['H2O-2B-Li', 'IL', 'TOP', 'Mg2+', 'Cl-']

        T = 298.15  # K
        P = 101325
        R = .008314
        O_A_0 = 2
        V_aq_0 = 5e-6  # m^3
        V_org_0 = O_A_0 * V_aq_0
        V_T = V_aq_0 + V_org_0

        z, n_T, x_aq_0, x_org_0, n_aq_0, n_org_0, Cl_aq_0, Cl_org_0, w_aq_0, w_org_0, MWs, ξ_0 = get_z(V_aq_0, O_A_0)

        prop_dic_aq = get_prop_dict(species, T)
        prop_dic_org = get_prop_dict(species, T)

        ρ_aq_0 = pcsaft_den(T, P, x_aq_0, prop_dic_aq)
        ρ_org_0 = pcsaft_den(T, P, x_org_0, prop_dic_org)

        lnϕ_aq_0 = pcsaft_lnfugcoef(T, ρ_aq_0, x_aq_0, prop_dic_aq)
        lnϕ_org_0 = pcsaft_lnfugcoef(T, ρ_org_0, x_org_0, prop_dic_org)

        print(lnϕ_aq_0)
        print(lnϕ_org_0)

        ΔG_Tr = R*T*(lnϕ_org_0 - lnϕ_aq_0)

        K_0 = lnϕ_org_0 - lnϕ_aq_0

        # Initial guess (same as original script)
        # guesses = np.append(np.ones(3), .5)  # K3, K4, K5, ξ
        guesses = np.array(list(K_0[3:-1]) + [ξ_0])
        scales = guesses
        ϵ = 1e-15
        bnds = [(ϵ, 1 / ϵ)] * (len(guesses) - 1)
        bnds.append((ϵ, 1.0 - ϵ))

        if solve:

            # Use L-BFGS-B (handles simple bounds). You could also try 'TNC' or 'Powell'.
            res = minimize(objective, guesses / scales, args=(scales,), method='L-BFGS-B', bounds=bnds, tol=1e-10,
                           options={"maxiter": 10000, "ftol": 1e-10})

            print(res.success, res.message)

            res = root(residuals, np.array(res.x), args=(scales,))
            r_opt = residuals(res.x, scales) * scales
            solution = res.x * scales

            K_Li, K_Mg, ξ_1 = solution

            x_aq_1, x_org_1, K = get_stuff(K_Li, K_Mg, ξ_1)

            Φ = ξ_1 / (1 - ξ_1)

            x_aq_1 = np.array(x_aq_1) / sum(x_aq_1)
            x_org_1 = np.array(x_org_1) / sum(x_org_1)

            # Liquid densities & fugacity coefficients

            prop_dic_aq = get_prop_dict(species, T)
            prop_dic_org = get_prop_dict(species, T)

            ρ_aq_1 = pcsaft_den(T, P, x_aq_1, prop_dic_aq)  # moles/m^3
            ρ_org_1 = pcsaft_den(T, P, x_org_1, prop_dic_org)  # moles/m^3

            lnϕ_aq_1 = pcsaft_lnfugcoef(T, ρ_aq_1, x_aq_1, prop_dic_aq)
            lnϕ_org_1 = pcsaft_lnfugcoef(T, ρ_org_1, x_org_1, prop_dic_org)

            n_aq_T_1 = n_T * (1 - ξ_1)  # moles
            n_org_T_1 = ξ_1 * n_T  # moles

            n_aq_1 = x_aq_1 * n_aq_T_1  # moles
            n_org_1 = x_org_1 * n_org_T_1  # moles

            m_aq = n_aq_1 * MWs
            m_org = n_org_1 * MWs

            m_aq_T = np.sum(m_aq)
            m_org_T = np.sum(m_org)

            w_aq_1 = m_aq / m_aq_T
            w_org_1 = m_org / m_org_T

            V_aq_1 = n_aq_T_1 / ρ_aq_1  # m^3
            V_org_1 = n_org_T_1 / ρ_org_1  # m^3

            O_A_1 = V_org_1 / V_aq_1
            V_aq_org = 1 / O_A_1

            Cl_aq_1 = n_aq_1 / V_aq_1
            Cl_org_1 = n_org_1 / V_org_1

            Cl_Li_aq_0 = Cl_aq_0[3]
            Cl_Mg_aq_0 = Cl_aq_0[4]

            Cl_Li_aq_1 = Cl_aq_1[3]
            Cl_Mg_aq_1 = Cl_aq_1[4]

            Cl_Li_org_0 = Cl_org_0[3]
            Cl_Mg_org_0 = Cl_org_0[4]

            Cl_Li_org_1 = Cl_org_1[3]
            Cl_Mg_org_1 = Cl_org_1[4]

            E_Li = (Cl_Li_aq_0 - Cl_Li_aq_1) / Cl_Li_aq_0
            E_Mg = (Cl_Mg_aq_0 - Cl_Mg_aq_1) / Cl_Mg_aq_0

            D_Li = Cl_Li_org_1 / Cl_Li_aq_1
            D_Mg = Cl_Mg_org_1 / Cl_Mg_aq_1

            β_Li_Mg = D_Li / D_Mg

            D_Li2 = (Cl_Li_aq_0 - Cl_Li_aq_1) / Cl_Li_aq_1 * V_aq_org
            D_Mg2 = (Cl_Mg_aq_0 - Cl_Mg_aq_1) / Cl_Mg_aq_1 * V_aq_org

            print(f'''
            Optimization success: {res.success}
            Message: {res.message}
            Residuals: {r_opt}
            Objective: {res.fun}

            Phase Fraction: {ξ_1}
            Equilibrium {K}

            Initial Mole Fraction: {z}
            Aqueous Phase Mole Fraction: {x_aq_1}
            Organic Phase Mole Fraction: {x_org_1}

            Aqueous Phase Fug Coeff: {lnϕ_aq_1}
            Organic Phase Fug Coeff: {lnϕ_org_1}

            Lithium Extraction Efficiency: {E_Li}
            Magnesium Extraction Efficiency: {E_Mg}

            Lithium Distribution Coefficient: {D_Li}
            Magnesium Distribution Coefficient: {D_Mg}

            Separation Selectivity: {β_Li_Mg}

            Lithium Distribution Coefficient: {D_Li2}
            Magnesium Distribution Coefficient: {D_Mg2}
            ''')
