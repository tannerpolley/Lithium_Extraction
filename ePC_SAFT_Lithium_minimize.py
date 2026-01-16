import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, least_squares
from pcsaft import pcsaft_ares, pcsaft_den, pcsaft_p, pcsaft_fugcoef


species_dic = {
    'H2O': {'m': 1.2047, 's': 2.7852, 'e': 353.95, 'e_assoc': 2425.7, 'vol_a': .0451, 'z': 0., 'assoc_scheme': '2B',
            'dielc': 77.44},
    'TOP': {'m': 4.2032, 's': 5.4506, 'e': 280.4777, 'e_assoc': 6393.5, 'vol_a': .0001, 'z': 0., 'assoc_scheme': '2B',
            'dielc': 11},
    'IL': {'m': 4.073, 's': 4.6432, 'e': 434.6130, 'e_assoc': 5000, 'vol_a': .1, 'z': 0., 'assoc_scheme': '2B',
           'dielc': 11},
    'Li+': {'m': 1., 's': 2.8449, 'e': 360.00, 'e_assoc': 0., 'vol_a': 100, 'z': 1, 'assoc_scheme': '2B', 'dielc': 8},
    'Mg2+': {'m': 1., 's': 3.1327, 'e': 1500, 'e_assoc': 0., 'vol_a': 0, 'z': 2, 'assoc_scheme': None, 'dielc': 8},
    'Cl-': {'m': 1., 's': 2.7560, 'e': 170.00, 'e_assoc': 0., 'vol_a': 0, 'z': -1, 'assoc_scheme': None, 'dielc': 8},
}

prop_dic = {}

for k in species_dic['H2O'].keys():

    prop_list = []
    for sp in species_dic.keys():
        prop_list.append(species_dic[sp][k])
    if k == 'assoc_scheme':
        prop_dic[k] = prop_list
    elif k == 'dielc':
        continue
    else:
        prop_dic[k] = np.array(prop_list)

k_ij = np.zeros((6, 6))
k_ij[0, 2] = .007
k_ij[2, 0] = k_ij[0, 2]

k_ij[3, 1] = .3
k_ij[1, 3] = k_ij[3, 1]

k_ij[0, 1] = 1
k_ij[1, 0] = k_ij[0, 1]

k_ij[3, 2] = 1
k_ij[2, 3] = k_ij[3, 2]

k_ij[0, 3] = 1
k_ij[3, 0] = k_ij[0, 3]

k_ij[3, 5] = .669
k_ij[5, 3] = k_ij[3, 5]

prop_dic['k_ij'] = k_ij

T = 300  # K
P = 101325  # Pa
V1 = 1  # L

MW_Li = 6.941  # g/mol
MW_Mg = 24.305  # g/mol
MW_H2O = 18.01528  # g/mol
MW_Cl = 70.906  # g/mol

rho_Li = .766  # g/L
rho_Mg = 98.984  # g/L
rho_H2O = 1000  # g/L

C_Li = rho_Li / MW_Li  # mol/L
C_Mg = rho_Mg / MW_Mg  # mol/L
C_H2O = rho_H2O / MW_H2O

n_Li = C_Li * V1  # mol
n_Mg = C_Mg * V1  # mol
n_H2O = C_H2O * V1
n_Cl = n_Li + 2 * n_Mg

n_T = sum([n_Li, n_Mg, n_Cl, n_H2O])

x_Li, x_Mg, x_Cl, x_H2O = n_Li / n_T, n_Mg / n_T, n_Cl / n_T, n_H2O / n_T

m_Li = n_Li * MW_Li
m_Mg = n_Mg * MW_Mg
m_Cl = n_Cl * MW_Cl
m_ion_T = m_Li + m_Mg + m_Cl
w_Li, w_Mg, w_Cl = m_Li / m_ion_T, m_Mg / m_ion_T, m_Cl / m_ion_T

w = {'Li+': w_Li, 'Mg2+': w_Mg, 'Cl-': w_Cl}

dielectric = species_dic['H2O']['dielc'] * x_H2O + np.sum(
    [species_dic[s]['dielc'] * w[s] for s in ['Li+', 'Mg2+', 'Cl-']])

prop_dic['dielc'] = dielectric

x1 = np.array([x_H2O, 1e-9, 1e-9, x_Li, x_Mg, x_Cl])

V2 = 6  # L

rho_TOP = 920  # g/L

MW_TOP = 434.63  # g/mol
MW_IL = 395.3  # g/mol

C_IL = .09  # mol/L
C_TOP = rho_TOP / MW_TOP

n_IL = C_IL * V2
n_TOP = C_TOP * V2
n_T2 = n_IL + n_TOP
x_IL, x_TOP = n_IL / n_T2, n_TOP / n_T2

x2 = np.array([1e-9, x_TOP, x_IL, 1e-9, 1e-9, 1e-9])

K = x2 / x1

n_total = n_H2O + n_TOP + n_IL + n_Li + n_Mg + n_Cl
z = np.array([n_H2O / n_total, n_TOP / n_total, n_IL / n_total, n_Li / n_total, n_Mg / n_total, n_Cl / n_total])


def residuals(x):
    """Return the 3 residuals (r1, r2, F) for given (K3, K4, ξ)"""
    K3, K4, K5, ξ = x
    K0, K1, K2 = 0.0, 0.0, 0.0

    # Guard against division-by-zero or invalid compositions
    eps = 1e-12
    ξ = np.clip(ξ, eps, 1.0 - eps)

    K = np.array([K0, K1, K2, K3, K4, K5])

    x = z/(1 + ξ*(K - 1))
    x[1] = 0.0
    x[2] = 0.0
    y = K*x
    y[0] = 0.0
    y[1] = z[1]/ξ
    y[2] = z[2] / ξ

    x = np.array(x)/np.sum(x)
    y = np.array(y) / np.sum(y)

    # Liquid densities & fugacity coefficients
    rho_alpha = pcsaft_den(t=T, p=P, x=x, params=prop_dic, phase='liq')
    phi_alpha = pcsaft_fugcoef(t=T, rho=rho_alpha, x=x, params=prop_dic)

    rho_beta = pcsaft_den(t=T, p=P, x=y, params=prop_dic, phase='liq')
    phi_beta = pcsaft_fugcoef(t=T, rho=rho_beta, x=y, params=prop_dic)

    r1 = np.log(x[3] + eps) + np.log(phi_alpha[3] + eps) - np.log(y[3] + eps) - np.log(phi_beta[3] + eps)
    r2 = np.log(x[4] + eps) + np.log(phi_alpha[4] + eps) - np.log(y[4] + eps) - np.log(phi_beta[4] + eps)
    r3 = K[5] - (1 + (z[5]/x[5] - 1)/ξ)

    # Material balance residual on splits (Rachford-Rice-like) + equality of fugacities for Li+, Mg2+
    F = np.sum([(z[i]*(K[i] - 1))/(1 + (K[i] - 1)*ξ) for i in range(len(z))])

    return np.array([r1, r2, r3, F])


def objective(x):
    r = residuals(x)
    return 0.5 * np.dot(r, r)  # 1/2 * ||r||^2


if __name__ == "__main__":
    # Initial guess (same as original script)
    guesses = np.array([100, 1e-5, 1.0, 0.60])  # K3, K4, ξ

    # Bounds: K3>=0, K4>=0, ξ in [eps, 1-eps] to avoid division-by-zero
    eps = 1e-8

    print(z)
    bnds = [(0.0, None), (0.0, None), (0.0, None), (0.0, 1.0)]

    # Use L-BFGS-B (handles simple bounds). You could also try 'TNC' or 'Powell'.
    res = minimize(objective, guesses, method='L-BFGS-B', bounds=bnds, options={"maxiter": 500, "ftol": 1e-10})

    K3_opt, K4_opt, K5_opt, xi_opt = res.x
    r_opt = residuals(res.x)

    print("Optimization success:", res.success)
    print("Message:", res.message)
    print("Iterations:", res.nit)
    print("K3, K4, K5, ξ:", K3_opt, K4_opt, K5_opt, xi_opt)
    print("Residuals [r1, r2, F]:", r_opt)
    print("Objective (0.5*||r||^2):", res.fun)

    K3, K4, K5, ξ = res.x
    K0, K1, K2 = 0.0, 0.0, 0.0
    ξ
    # Guard against division-by-zero or invalid compositions
    eps = 1e-12
    ξ = np.clip(ξ, eps, 1.0 - eps)

    K = np.array([K0, K1, K2, K3, K4, K5])

    x = z / (1 + ξ * (K - 1))
    x[1] = 0.0
    x[2] = 0.0
    y = K * x
    y[0] = 0.0
    y[1] = z[1]/ξ
    y[2] = z[2] / ξ

    x = np.array(x)/np.sum(x)
    y = np.array(y) / np.sum(y)

    print(x)
    print(y)

    # Liquid densities & fugacity coefficients
    rho_alpha = pcsaft_den(t=T, p=P, x=x, params=prop_dic, phase='liq')
    phi_alpha = pcsaft_fugcoef(t=T, rho=rho_alpha, x=x, params=prop_dic)

    rho_beta = pcsaft_den(t=T, p=P, x=y, params=prop_dic, phase='liq')
    phi_beta = pcsaft_fugcoef(t=T, rho=rho_beta, x=y, params=prop_dic)

    # print(x)
    # print(y)
    # print(z)

    Φ = ξ/(1 - ξ)
    print(ξ)
    print(Φ)

    print(Φ*y[3]/z[3])
    print(Φ * y[4] / z[4])


    # print(phi_alpha)
    # print(phi_beta)
