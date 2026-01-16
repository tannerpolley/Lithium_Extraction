import numpy as np
from scipy.optimize import minimize, least_squares
from pcsaft import pcsaft_lnfugcoef, pcsaft_den

from pcsaft_models_polley.ePC_SAFT_properties import get_prop_dict

R = 8.314462618  # J/mol/K  (not used now, but kept in case you extend)

# ── helpers: partition, E-matrix, ξ-map, mean-ionic ───────────────────────────
def split_neutral_ionic(prop_dic):
    # which components are neutral vs ionic from "z" (charges) array
    charges = np.asarray(prop_dic["z"], dtype=float)
    idx_ions  = np.where(charges != 0.0)[0]
    idx_neuts = np.where(charges == 0.0)[0]
    ion_charges = charges[idx_ions]
    return idx_neuts, idx_ions, ion_charges

def build_E_matrix(z_feed_ions, ion_charges):
    """
    Create E of shape (Nch-1, Nch) for mean-ionic combos.
    Simple independent pairing: 'most-abundant major group' vs each of minor group.
    """
    z_feed_ions = np.asarray(z_feed_ions, dtype=float)
    ion_charges = np.asarray(ion_charges, dtype=float)
    Nch = len(ion_charges)

    idx_sorted = np.argsort(-z_feed_ions)

    q_sorted = ion_charges[idx_sorted]

    cat_idx = [idx_sorted[i] for i, s in enumerate(q_sorted) if s > 0]
    an_idx = [idx_sorted[i] for i, s in enumerate(q_sorted) if s < 0]

    if len(cat_idx) == 0 or len(an_idx) == 0:
        raise ValueError("Need at least one cation and one anion.")

    E_sorted = np.zeros((Nch-1, Nch), dtype=float)
    # weights 1/|z| (charge magnitude)
    if len(cat_idx) <= len(an_idx):
        ref = cat_idx[0]
        for k in range(len(an_idx)):
            row = min(k, Nch-2)
            E_sorted[row, ref]        = 1.0/abs(q_sorted[ref])
            E_sorted[row, an_idx[k]]  = 1.0/abs(q_sorted[an_idx[k]])

        if len(cat_idx) > 1:
            ref = an_idx[0]
            for k in range(len(cat_idx) - 1):
                row = k + len(an_idx)

                E_sorted[row, ref]        = 1.0/abs(q_sorted[ref])
                E_sorted[row, cat_idx[k+1]] = 1.0/abs(q_sorted[cat_idx[k+1]])


    # # unsort back to original ion order
    # P = np.zeros((Nch, Nch))
    # P[np.arange(Nch), idx_sorted] = 1.0
    # E = E_sorted @ P.T

    E = E_sorted


    if np.linalg.matrix_rank(E) != Nch-1:
        raise RuntimeError("E matrix not full rank; adjust pairing.")
    return E

def composition_from_vars(n_neut, xi, n0_ions, E):
    """
    (n_neut, xi) -> full composition x (neutrals + ions), normalized.
    Electrically neutral by construction via n_ch = n0_ions + E^T xi.
    """
    n_neut = np.asarray(n_neut, dtype=float)
    xi     = np.asarray(xi, dtype=float)
    n_ch   = n0_ions + E.T @ xi
    if np.any(n_neut < 0) or np.any(n_ch < 0):
        return None
    n_all = np.concatenate([n_neut, n_ch])
    tot = n_all.sum()
    if tot <= 0:
        return None
    return n_all / tot

def mean_ionic_combo(vec_ions, E):
    row_sums = E.sum(axis=1)
    return (E @ vec_ions) / row_sums

# ── lnphi(T,p,x,phase_id) that uses your pcsaft_den then pcsaft_lnfugcoef ─────
def make_lnphi_func(pcsaft_lnfugcoef, pcsaft_den,
                    prop_dic_phase1, prop_dic_phase2):
    """
    Returns lnphi(T,p,x,phase_id) using:
        rho = pcsaft_den(T, p, x, prop_dic_phase#)
        lnphi = pcsaft_lnfugcoef(T, rho, x, prop_dic_phase#)
    """
    def lnphi(T, p, x, phase_id):
        if phase_id == 1:
            prop = prop_dic_phase1
        elif phase_id == 2:
            prop = prop_dic_phase2
        else:
            # default to phase-1 context for scalar evals (e.g., g-hat-like)
            prop = prop_dic_phase1
        rho = pcsaft_den(T, p, x, prop)
        return np.asarray(pcsaft_lnfugcoef(T, rho, x, prop), dtype=float)
    return lnphi

# ── TPDF from ln(φ x) ─────────────────────────────────────────────────────────
def tpdf_lnfx(lnphi_func, T, p, x_trial, z_feed):
    lnphi_trial = lnphi_func(T, p, x_trial, 1)
    lnphi_feed  = lnphi_func(T, p, z_feed,  1)
    lnfx_trial  = lnphi_trial + np.log(np.clip(x_trial, 1e-300, 1.0))
    lnfx_feed   = lnphi_feed  + np.log(np.clip(z_feed,  1e-300, 1.0))
    return float(np.dot(x_trial, lnfx_trial - lnfx_feed))

# ── stability search to get a second-phase seed x2* (if unstable) ─────────────
def stability_seed(lnphi_func, T, p, z, Nneut, Nch, E, n0_ions, n_global=1500, rng=None):
    rng = np.random.default_rng() if rng is None else rng
    best_val, best_x = +np.inf, None

    for _ in range(n_global):
        n_neut = rng.random(Nneut)
        xi     = rng.random(Nch-1)
        x_try  = composition_from_vars(n_neut, xi, n0_ions, E)
        if x_try is None:
            continue
        val = tpdf_lnfx(lnphi_func, T, p, x_try, z)
        if val < best_val:
            best_val, best_x = val, x_try

    if best_x is None:
        return None, None

    # local polish
    n_total = 1.0
    n_neut0 = best_x[:Nneut] * n_total
    target  = best_x[Nneut:] * n_total - n0_ions
    res = least_squares(lambda xi: (E.T @ xi) - target,
                        x0=np.maximum(1e-8, np.ones(Nch-1)*0.1),
                        bounds=(0, np.inf))
    xi0 = res.x

    def obj(y):
        nn = np.maximum(y[:Nneut], 1e-12)
        xx = np.maximum(y[Nneut:], 1e-12)
        x_loc = composition_from_vars(nn, xx, n0_ions, E)
        if x_loc is None:
            return 1e6
        return tpdf_lnfx(lnphi_func, T, p, x_loc, z)

    y0  = np.concatenate([n_neut0, xi0])
    pol = minimize(obj, y0, method="Nelder-Mead",
                   options={"maxiter": 1000, "xatol": 1e-8, "fatol": 1e-10})
    if not pol.success:
        return best_val, best_x

    nn = np.maximum(pol.x[:Nneut], 1e-16)
    xx = np.maximum(pol.x[Nneut:], 1e-16)
    x_pol = composition_from_vars(nn, xx, n0_ions, E)
    val   = tpdf_lnfx(lnphi_func, T, p, x_pol, z)
    return val, x_pol

# ── main two-phase LLE flash (x1, x2, alpha1) ─────────────────────────────────
def two_phase_flash_lnphi_pcsaft(
    T, p, z_feed,
    prop_dic_phase1, prop_dic_phase2,
    pcsaft_lnfugcoef, pcsaft_den
):
    """
    Two-liquid LLE flash using ln(phi*x) equalities (neutrals and mean-ionic),
    with electroneutrality enforced via xi variables and with overall mass
    balance enforced exactly. Alpha (phase-1 fraction) is an explicit unknown.

    Requirements (already defined elsewhere in your script):
      - split_neutral_ionic(prop_dic)
      - build_E_matrix(z_feed_ions, ion_charges)
      - composition_from_vars(n_neut, xi, n0_ions, E)
      - mean_ionic_combo(vec_ions, E)
      - make_lnphi_func(pcsaft_lnfugcoef, pcsaft_den, prop_dic_phase1, prop_dic_phase2)
      - stability_seed(lnphi_func, T, p, z, Nneut, Nch, E, n0_ions, n_global=..., rng=None)
    """
    import numpy as np
    from scipy.optimize import minimize, least_squares

    # normalize feed
    z_feed = np.asarray(z_feed, dtype=float)
    z_feed = z_feed / z_feed.sum()

    # partitions (same ordering assumed in both prop dicts)
    idx_neut, idx_ion, charges_ion = split_neutral_ionic(prop_dic_phase1)
    Nneut, Nch = len(idx_neut), len(idx_ion)
    N = Nneut + Nch

    # E from feed ions; reference ion moles (unimolar basis)
    z_ions_feed = z_feed[idx_ion]
    E = build_E_matrix(z_ions_feed, charges_ion)
    n0_ions = z_ions_feed.copy()

    # lnphi(T,p,x,phase_id) using your density → lnphi chain
    lnphi_func = make_lnphi_func(pcsaft_lnfugcoef, pcsaft_den,
                                 prop_dic_phase1, prop_dic_phase2)

    # stability to get second-phase seed
    val, x2_seed_full = stability_seed(lnphi_func, T, p, z_feed, Nneut, Nch, E, n0_ions, n_global=3000)
    if (x2_seed_full is None) or (val >= 0.0):
        # single phase stable
        return {
            "stable": True,
            "x1": z_feed.copy(),
            "x2": None,
            "alpha1": 1.0,
            "alpha2": 0.0,
            "E": E,
            "success": True,
            "res_norm": 0.0
        }

    # crude complement seed for phase 1
    x1_seed_full = np.clip(z_feed + (z_feed - x2_seed_full), 1e-12, 1.0)
    x1_seed_full = x1_seed_full / x1_seed_full.sum()

    # helper: pack/unpack (includes alpha via a_raw -> sigmoid)
    def unpack_y(y):
        o = 0
        ln_n1  = y[o:o+Nneut];      o += Nneut
        ln_xi1 = y[o:o+Nch-1];      o += Nch-1
        ln_n2  = y[o:o+Nneut];      o += Nneut
        ln_xi2 = y[o:o+Nch-1];      o += Nch-1
        a_raw  = y[o]
        alpha = 1.0 / (1.0 + np.exp(-a_raw))  # sigmoid keeps 0<alpha<1
        return ln_n1, ln_xi1, ln_n2, ln_xi2, alpha

    def blocks_lnfx(x, phase_id):
        lnphi = lnphi_func(T, p, x, phase_id)
        lnfx  = lnphi + np.log(np.clip(x, 1e-300, 1.0))
        lnfxN = lnfx[idx_neut]
        lnfxI = lnfx[idx_ion]
        lnfxI_hat = mean_ionic_combo(lnfxI, E)
        return lnfxN, lnfxI_hat

    # residuals: neutrals equality + mean-ionic equality + (N-1) mass balances
    def eq_residuals(y):
        ln_n1, ln_xi1, ln_n2, ln_xi2, alpha = unpack_y(y)
        n_neut1 = np.exp(ln_n1);    xi1 = np.exp(ln_xi1)
        n_neut2 = np.exp(ln_n2);    xi2 = np.exp(ln_xi2)

        x1 = composition_from_vars(n_neut1, xi1, n0_ions, E)
        x2 = composition_from_vars(n_neut2, xi2, n0_ions, E)
        if (x1 is None) or (x2 is None):
            return 1e6*np.ones(Nneut + (Nch-1) + (N-1))

        # equilibrium equalities
        lnfxN1, lnfxI1 = blocks_lnfx(x1, phase_id=1)
        lnfxN2, lnfxI2 = blocks_lnfx(x2, phase_id=2)
        rN = lnfxN1 - lnfxN2
        rI = lnfxI1 - lnfxI2

        # strict overall mass balance (drop one row to avoid redundancy)
        z_fit = alpha*x1 + (1.0 - alpha)*x2
        rM = (z_feed - z_fit)[:-1]

        return np.concatenate([rN, rI, rM])

    # initialization: back out (n_neut, xi) from seeds, seed alpha from lever rule
    def init_from_x(x_seed_full):
        xN = x_seed_full[idx_neut]
        xI = x_seed_full[idx_ion]
        n_neut0 = np.maximum(xN, 1e-12)
        target  = xI - n0_ions
        res = least_squares(lambda xi: (E.T @ xi) - target,
                            x0=np.ones(Nch-1)*0.1, bounds=(0, np.inf))
        xi0 = np.maximum(res.x, 1e-12)
        return np.log(n_neut0), np.log(xi0)

    ln_n1, ln_xi1 = init_from_x(x1_seed_full)
    ln_n2, ln_xi2 = init_from_x(x2_seed_full)

    # lever-rule alpha seed
    d = x1_seed_full - x2_seed_full
    dd = float(np.dot(d, d))
    if dd < 1e-16:
        alpha0 = 0.5
    else:
        alpha0 = float(np.dot(z_feed - x2_seed_full, d) / dd)
        alpha0 = 0.0 if alpha0 < 0.0 else (1.0 if alpha0 > 1.0 else alpha0)
    a_raw0 = np.log(alpha0/(1.0 - alpha0 + 1e-16) + 1e-16)

    y0 = np.concatenate([ln_n1, ln_xi1, ln_n2, ln_xi2, [a_raw0]])

    # solve
    sol = least_squares(eq_residuals, y0, jac='2-point',
                        xtol=1e-10, ftol=1e-10, gtol=1e-10, max_nfev=5000)

    # unpack solution
    ln_n1, ln_xi1, ln_n2, ln_xi2, alpha = unpack_y(sol.x)
    n_neut1 = np.exp(ln_n1); xi1 = np.exp(ln_xi1)
    n_neut2 = np.exp(ln_n2); xi2 = np.exp(ln_xi2)
    x1_full = composition_from_vars(n_neut1, xi1, n0_ions, E)
    x2_full = composition_from_vars(n_neut2, xi2, n0_ions, E)
    alpha1  = float(alpha)
    alpha2  = 1.0 - alpha1

    # optional tiny polish of alpha only (keeps x1,x2 fixed)
    def ghat_like(alpha_scalar):
        a = 0.0 if alpha_scalar < 0.0 else (1.0 if alpha_scalar > 1.0 else alpha_scalar)
        x_mix = a*x1_full + (1.0 - a)*x2_full
        lnphi_mix = lnphi_func(T, p, x_mix, 1)
        lnfx_mix  = lnphi_mix + np.log(np.clip(x_mix, 1e-300, 1.0))
        return float(np.dot(x_mix, lnfx_mix))
    br = minimize(lambda a: ghat_like(a[0]), x0=np.array([alpha1]),
                  bounds=[(0.0,1.0)], method="L-BFGS-B", options={"maxiter": 50})
    alpha1 = float(np.clip(br.x[0], 0.0, 1.0))
    alpha2 = 1.0 - alpha1

    return {
        "stable": False,
        "x1": x1_full, "x2": x2_full,
        "alpha1": alpha1, "alpha2": alpha2,
        "E": E,
        "success": bool(sol.success),
        "res_norm": float(np.linalg.norm(sol.fun))
    }


def check_equilibrium_from_paper(T, P, z_feed, x1, x2, lnphi1, lnphi2, charges, prop_dic):
    """
    Diagnostic: evaluate ghat for each phase and the equilibrium residuals
    given the paper's reported lnphi values and compositions.

    """

    z_feed = np.asarray(z_feed, dtype=float)
    z_feed = z_feed / z_feed.sum()

    # partitions (same ordering assumed in both prop dicts)
    idx_neut, idx_ion, charges_ion = split_neutral_ionic(prop_dic)
    Nneut, Nch = len(idx_neut), len(idx_ion)
    N = Nneut + Nch

    # E from feed ions; reference ion moles (unimolar basis)
    z_ions_feed = z_feed[idx_ion]
    E = build_E_matrix(z_ions_feed, charges_ion)

    idx_neut = [i for i,q in enumerate(charges) if q==0]
    idx_ion  = [i for i,q in enumerate(charges) if q!=0]

    # 1. ghat for each phase
    def ghat(lnphi, x):
        return np.dot(x, lnphi + np.log(x))

    ghat1 = ghat(lnphi1, x1)
    ghat2 = ghat(lnphi2, x2)
    ghat1_Jmol = ghat1 * 8.314 * T
    ghat2_Jmol = ghat2 * 8.314 * T
    print(f"ghat1 = {ghat1_Jmol:.3f} J/mol,  ghat2 = {ghat2_Jmol:.3f} J/mol")

    # 2. equilibrium residuals
    lnfx1 = lnphi1 + np.log(x1)
    lnfx2 = lnphi2 + np.log(x2)
    # neutrals equalities
    rN = lnfx1[idx_neut] - lnfx2[idx_neut]
    # ionic mean equalities
    lnfxI1_hat = (E @ lnfx1[idx_ion]) / E.sum(axis=1)
    lnfxI2_hat = (E @ lnfx2[idx_ion]) / E.sum(axis=1)
    rI = lnfxI1_hat - lnfxI2_hat

    print("Neutral equalities Δ(lnφx):", rN)
    print("Mean-ionic equalities Δ(lnφx):", rI)

    # 3. overall lever rule check
    # compute α from lever rule
    d = x1 - x2
    alpha = np.dot(z_feed - x2, d) / np.dot(d, d)
    z_check = alpha*x1 + (1-alpha)*x2
    print("alpha (from lever rule) =", alpha)
    print("mass-balance deviation =", np.max(np.abs(z_check - z_feed)))


def massfrac_to_molefrac(w, MW_water=0.01801528, MW_buoh=0.07412, MW_Na=0.02298, MW_K=0.0390983, MW_Cl=0.03545):

    MW_NaCl = MW_Na + MW_Cl
    MW_KCl  = MW_K  + MW_Cl
    # moles in 1 kg feed (any total mass works; it cancels after normalization)
    nH2O  = w[0]/ MW_water
    nBuOH = w[1] / MW_buoh
    nNaCl = w[2]  / MW_NaCl
    nKCl  = w[3]  / MW_KCl
    # split salts into ions (1:1)

    n_all_salt = np.array([nH2O, nBuOH, nNaCl, nKCl], dtype=float)
    z_salt = n_all_salt / n_all_salt.sum()
    return z_salt

def ion_to_salt(x_cat, x_an, z_cat, z_an):
    result = (x_cat ** (1 / np.abs(z_cat)) * x_an ** (1 / np.abs(z_an)))**(1 / ((1 / np.abs(z_cat)) + (1 / np.abs(z_an))))
    if x_cat < 0 and x_an < 0:
        return -result
    else:
        return result

def salt_x_to_ionic_x(x):

    n_sum = 1
    n_H2O, n_But, n_NaCl, n_KCl = x*n_sum

    n_Na = n_NaCl
    n_K = n_KCl
    n_Cl = n_NaCl + n_KCl
    n_all_ionic = np.array([n_H2O, n_But, n_Na, n_K, n_Cl], dtype=float)
    x_ionic = n_all_ionic / n_all_ionic.sum()
    return x_ionic

def salt_x_to_ionic_x_2(x):

    n_sum = 1
    n_H2O, n_But, n_KCl, n_Na2SO4 = x*n_sum


    n_K = n_KCl
    n_Cl = n_KCl
    n_Na = n_Na2SO4*2
    n_SO4 = n_Na2SO4
    n_all_ionic = np.array([n_H2O, n_But, n_K, n_Cl, n_Na, n_SO4], dtype=float)
    x_ionic = n_all_ionic / n_all_ionic.sum()
    return x_ionic


if __name__ == "__main__":

    # zf_salt = np.array([.4, .4, .110, .090])
    # zf_ionic = salt_x_to_ionic_x_2(zf_salt)
    # print(zf_ionic)
    # z_charge = np.array([1, -1, 1, -2])
    # print(build_E_matrix(zf_ionic[2:], z_charge))

    R = 8.31415
    T = 298.15
    P = 101325
    species = ['H2O', 'Butanol', 'Na+', 'K+', 'Cl-']
    species_salt = ['H2O', 'Butanol', 'NaCl', 'KCl']

    w = np.array([.8094, .1728, .0054, .0124])

    z_0_salt = massfrac_to_molefrac(w)

    print(z_0_salt)

    z_0_ionic = salt_x_to_ionic_x(z_0_salt)

    prop_dic = get_prop_dict(species, z_0_ionic, T)

    ρ_0 = pcsaft_den(T, P, z_0_ionic, prop_dic)

    lnϕ_0_ionic = pcsaft_lnfugcoef(T, ρ_0, z_0_ionic, prop_dic)

    lnf_0_ionic = lnϕ_0_ionic + np.log(z_0_ionic)

    E = np.array([[1.0, 0.0, 1.0],  # “NaCl” row  (Na⁺ + Cl⁻)
                  [0.0, 1.0, 1.0]])  # “KCl” row  (K⁺  + Cl⁻)
    rowsum = E.sum(axis=1)  # = [2, 2] for 1:1 salts

    z_0_salt_1 = np.array(list(z_0_ionic[:2]) + list((E @ z_0_ionic[2:]) / rowsum))

    z_0_salt_1 = z_0_salt_1/np.sum(z_0_salt_1)

    lnf_0_salt = np.array(list(lnf_0_ionic[:2]) + list((E @ lnf_0_ionic[2:]) / rowsum))

    ghat_0 = R*T*np.dot(z_0_salt_1, lnf_0_salt)

    print('ghat feed', ghat_0)

    # print(ghat_salt)
    # print(ghat_ionic)
    # print(2*((ghat_salt + ghat_ionic)/2))

    alpha_org = .03
    alpha_aq = 1 - alpha_org

    x_aq_salt = np.array([0.9627, 0.0122, 0.0076, 0.0174])
    x_org_salt = np.array([0.4426, 0.5570, 4.15e-5, 4.20e-4])

    x_aq_ionic = np.array([0.93931115, 0.01190360, 0.00741536, 0.01697727, 0.02439262])
    x_org_ionic = np.array([0.44236864, 0.55670884, 0.0000414783, 0.000419780, 0.000461259])

    prop_dic_aq = get_prop_dict(species, x_aq_ionic, T)
    prop_dic_org = get_prop_dict(species, x_org_ionic, T)

    # Liquid densities & fugacity coefficients
    ρ_aq = pcsaft_den(T, P, x_aq_ionic, prop_dic_aq)
    ρ_org = pcsaft_den(T, P, x_org_ionic, prop_dic_org)

    lnϕ_aq_ionic = pcsaft_lnfugcoef(T, ρ_aq, x_aq_ionic, prop_dic_aq)
    lnϕ_org_ionic = pcsaft_lnfugcoef(T, ρ_org, x_org_ionic, prop_dic_org)

    lnf_org_ionic = lnϕ_org_ionic + np.log(x_org_ionic)
    lnf_aq_ionic = lnϕ_aq_ionic + np.log(x_aq_ionic)

    E = np.array([[1.0, 0.0, 1.0],  # “NaCl” row  (Na⁺ + Cl⁻)
                  [0.0, 1.0, 1.0]])  # “KCl” row  (K⁺  + Cl⁻)
    rowsum = E.sum(axis=1)  # = [2, 2] for 1:1 salts

    x_aq_salt = np.array(list(x_aq_ionic[:2]) + list((E @ x_aq_ionic[2:]) / rowsum))
    x_org_salt = np.array(list(x_org_ionic[:2]) + list((E @ x_org_ionic[2:]) / rowsum))

    x_aq_salt = x_aq_salt/np.sum(x_aq_salt)
    x_org_salt = x_org_salt/np.sum(x_org_salt)

    lnf_aq_salt = np.array(list(lnf_aq_ionic[:2]) + list((E @ lnf_aq_ionic[2:]) / rowsum))
    lnf_org_salt = np.array(list(lnf_org_ionic[:2]) + list((E @ lnf_org_ionic[2:]) / rowsum))

    ghat = R * T * (alpha_org * (np.dot(x_org_salt, lnf_org_salt)) + alpha_aq * (np.dot(x_aq_salt, lnf_aq_salt)))

    print('ghat', ghat)

    x_aq_salt = np.array([0.9627, 0.0122, 0.0076, 0.0174])
    x_org_salt = np.array([0.4426, 0.5570, 4.15e-5, 4.20e-4])

    lnf_org_salt = np.array([-3.521, -5.088, -206.733, -244.891])
    lnf_aq_salt = np.array([-3.521, -5.088, -206.733, -244.891])

    ghat = R * T * (alpha_org * (np.dot(x_org_salt, lnf_org_salt)) + alpha_aq * (np.dot(x_aq_salt, lnf_aq_salt)))

    print('ghat paper', ghat)

    #
    # ghat_salt = R*T*np.dot(x_aq_salt, lnf_aq_salt)*alpha_aq + R*T*np.dot(x_org_salt, lnf_org_salt)*alpha_org
    # ghat_ionic = R*T*np.dot(x_aq_ionic, lnf_aq_ionic)*alpha_aq + R*T*np.dot(x_org_ionic, lnf_org_ionic)*alpha_org
    #
    #
    # print('ghat ionic', ghat_ionic)
    # print('ghat average', (ghat_salt + ghat_ionic)/2)
    #
    # prop_dic = get_prop_dict(species, z_feed, T)
    # check_equilibrium_from_paper(T, P, z_feed, x_aq_ionic, x_org_ionic, lnϕ_aq_ionic, lnϕ_org_ionic, prop_dic_aq['z'], prop_dic_aq)
    #
    # out = two_phase_flash_lnphi_pcsaft(
    #     T, P, z_feed,
    #     prop_dic, prop_dic,  # use same dict for both phases (or different if needed)
    #     pcsaft_lnfugcoef,
    #     pcsaft_den,  # or provide rho_fn_* instead
    # )
    #
    # print("stable:", out["stable"])
    # print("x1:", out["x1"])
    # print("x2:", out["x2"])
    # print("alpha1:", out["alpha1"])