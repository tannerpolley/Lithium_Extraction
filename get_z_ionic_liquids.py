from ePC_SAFT_properties import pcsaft_prop
import numpy as np


def get_z(V_aq_0, O_A):
    MW_Li = pcsaft_prop['Li+']['MW']  # g/mol
    MW_Mg = pcsaft_prop['Mg2+']['MW']
    MW_H2O = pcsaft_prop['H2O-2B-Li']['MW']
    MW_Cl = pcsaft_prop['Cl-']['MW']
    MW_TOP = pcsaft_prop['TOP']['MW']
    MW_IL = pcsaft_prop['IL']['MW']

    MWs = np.array([MW_H2O, MW_TOP, MW_IL, MW_Li, MW_Mg, MW_Cl])*1e-3 # kg/mol

    V_org_0 = V_aq_0 * O_A  # m3

    # Brine
    Mg_Li = 40.0

    ρ_Li_aq = .766  # kg/m3
    ρ_Mg_aq = 98.984  # kg/m3
    ρ_H2O_aq = 1000  # kg/m3

    Cl_H2O_aq_0 = ρ_H2O_aq / MW_H2O # mol/m3
    Cl_TOP_aq_0 = 0.0
    Cl_IL_aq_0 = 0.0
    Cl_Mg_aq_0 = ρ_Mg_aq / MW_Mg  # mol/m3
    Cl_Li_aq_0 = (Cl_Mg_aq_0 * V_aq_0 / Mg_Li) / V_aq_0
    Cl_Cl_aq_0 = (Cl_Li_aq_0*V_aq_0 + 2 * Cl_Mg_aq_0 * V_aq_0) / V_aq_0

    Cl_aq_0 = np.array([Cl_H2O_aq_0, Cl_TOP_aq_0, Cl_IL_aq_0, Cl_Li_aq_0, Cl_Mg_aq_0, Cl_Cl_aq_0])

    n_aq_0 = Cl_aq_0 * V_aq_0
    m_aq_0 = n_aq_0 * MWs

    n_aq_T_0 = np.sum(n_aq_0)
    m_aq_T_0 = np.sum(m_aq_0)

    x_aq_0 = n_aq_0 / n_aq_T_0
    w_aq_0 = m_aq_0 / m_aq_T_0

    # Organic Solvent/Ionic Liquid
    ρ_TOP_org = 930  # # kg/m3

    Cl_H2O_org_0 = 0.0
    Cl_TOP_org_0 = ρ_TOP_org / MW_TOP
    Cl_IL_org_0 = .09e3  # mol/m3

    Cl_Li_org_0 = 0.0
    Cl_Mg_org_0 = 0.0
    Cl_Cl_org_0 = 0.0

    Cl_org_0 = np.array([Cl_H2O_org_0, Cl_TOP_org_0, Cl_IL_org_0, Cl_Li_org_0, Cl_Mg_org_0, Cl_Cl_org_0])

    n_org_0 = Cl_org_0 * V_org_0
    m_org_0 = n_org_0 * MWs

    n_org_T_0 = np.sum(n_org_0)
    m_org_T_0 = np.sum(m_org_0)

    x_org_0 = n_org_0 / n_org_T_0
    w_org_0 = m_org_0 / m_org_T_0

    ξ_0 = n_org_T_0/n_aq_T_0

    n_0 = n_aq_0 + n_org_0
    n_T = np.sum(n_0)
    m_0 = n_0 * MWs
    w_0 = m_0 / np.sum(m_0)
    z = n_0 / np.sum(n_0)

    return z, n_T, x_aq_0, x_org_0, n_aq_0, n_org_0, Cl_aq_0, Cl_org_0, w_aq_0, w_org_0, MWs, ξ_0

def convert_models_rho(x, params, phase):
    m = params['m']
    s = params['s']
    e = params['e']

    params.pop('m')
    params.pop('s')
    params.pop('e')
    params.pop('assoc_scheme')

    return x, m, s, e, params, phase

def convert_models_phi(x, params):
    m = params['m']
    s = params['s']
    e = params['e']
    k_ij = params['k_ij']
    e_assoc = params['e_assoc']
    vol_a = params['vol_a']
    dipm = list(params['dipm'])
    dip_num = params['dip_num']
    z = params['z']
    dielc = params['dielc']
    return x, m, s, e, k_ij, e_assoc, vol_a, dipm, dip_num, z, dielc