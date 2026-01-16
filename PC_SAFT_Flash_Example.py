import numpy as np
from pcsaft import pcsaft_den, pcsaft_fugcoef
from ePC_SAFT_properties import get_prop_dict
from pprint import pprint


species = ['Methane', 'Ethane', 'Propane']
z = np.array([.405, .257, .338])
T = 233.15
P = 1276369.47358564

prop_dic = get_prop_dict(species, z, T)

pprint(prop_dic)

def residuals(unknowns):

    """Return the 3 residuals (r1, r2, F) for given (K3, K4, ξ)"""
    K, ξ = np.array(unknowns[:-1]), unknowns[-1]

    x1 = z/(1 + ξ*(K - 1))
    x2 = K*x1

    x1 = np.array(x1) / sum(x1)
    x2 = np.array(x2) / sum(x2)

    # Liquid densities & fugacity coefficients
    ρ1 = pcsaft_den(t=T, p=P, x=x1, params=prop_dic, phase='liq')
    ρ2 = pcsaft_den(t=T, p=P, x=x2, params=prop_dic, phase='vap')

    ϕ1 = pcsaft_fugcoef(t=T, rho=ρ1, x=x1, params=prop_dic)
    ϕ2 = pcsaft_fugcoef(t=T, rho=ρ2, x=x2, params=prop_dic)

    residuals = []

    for i in range(len(z)):

        r = np.log(x1[i]) + np.log(ϕ1[i]) - np.log(x2[i]) - np.log(ϕ2[i])
        residuals.append(r)

    F = np.sum([(z[i]*(K[i] - 1))/(1 + (K[i] - 1)*ξ) for i in range(len(z))])
    residuals.append(F)
    return residuals


def objective(x):
    r = residuals(x)
    return 0.5 * np.dot(r, r)  # 1/2 * ||r||^2


if __name__ == "__main__":
    # Initial guess (same as original script)
    guesses = np.array([1, 1, 1, .5])  # K3, K4, ξ

    bnds = [(1e-8, 1e8), (1e-8, 1e8), (1e-5, 1e8), (1e-8, 1.0 - 1e-8)]

    # Use L-BFGS-B (handles simple bounds). You could also try 'TNC' or 'Powell'.
    # res = minimize(objective, guesses, method='L-BFGS-B', bounds=bnds, tol=1e-20, options={"maxiter": 500, "ftol": 1e-10})
    # res = root(residuals, res.x)
    #
    # K, ξ = res.x[:-1], res.x[-1]
    # r_opt = residuals(res.x)
    #
    # print("Optimization success:", res.success)
    # print("Message:", res.message)
    # print("Equilibrium", K)
    # print("Phase Fraction:", ξ)
    # print("Residuals", r_opt)
    # print("Objective", res.fun)

