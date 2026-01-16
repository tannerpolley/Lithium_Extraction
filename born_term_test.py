from ePC_SAFT_properties import get_prop_dict
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(formatter={'float': '{:0.8f}'.format})
# from pcsaft_electrolyte_py_polley import pcsaft_den, pcsaft_ares, pcsaft_lnfugcoef
from pcsaft import pcsaft_den, pcsaft_lnfugcoef

# species_aq = ['H2O', 'Na+']
# species_org = ['Methanol', 'Na+']

cation = ['Na+']
anion = ['Cl-']
aqueous_solvent = ['H2O-2B-Li']
organic_solvent = ['Ethanol']

species_aq = aqueous_solvent + cation + anion
species_org = aqueous_solvent + organic_solvent + cation + anion

# species_aq = ['H2O', 'Li+', 'Na+', 'K+', 'F-', 'Cl-', 'Br-', 'I-']
# species_org = [organic_solvent, 'Li+', 'Na+', 'K+', 'F-', 'Cl-', 'Br-', 'I-']


T = 298.15  # K
P = 101325
R = .008314 #kJ/mol-K

ϵ = 0.0
n_ions = len(species_aq) - 1
y_data_Li = np.array([2.9, 2.3, 0.9, 1.1, 2.5, 3.9, 5.2, 6.4, 8.1, 10.3])

x_data = np.arange(.1, 1.1, .1)
y_data_Na = np.array([2.8, 3.2, 3.4, 4.0, 5.2, 6.4, 7.7, 9.9, 12.4, 14.9])

x_aq_0 = np.array([1.0 - ϵ*n_ions] + list(np.zeros(n_ions) + ϵ))

x_org = 1.0

x_org_array = np.linspace(0, 1)
ΔG_Tr_array = []
for x_org in x_org_array:
    x_org_0 = np.array([1-x_org, x_org, 0.0, 0.0])

    prop_dic_aq = get_prop_dict(species_aq, T)
    prop_dic_org = get_prop_dict(species_org, T)

    ρ_aq_0 = pcsaft_den(T, P, x_aq_0, prop_dic_aq)
    ρ_org_0 = pcsaft_den(T, P, x_org_0, prop_dic_org)

    lnϕ_aq = pcsaft_lnfugcoef(T, ρ_aq_0, x_aq_0, prop_dic_aq)[1]
    lnϕ_org = pcsaft_lnfugcoef(T, ρ_org_0, x_org_0, prop_dic_org)[2]

    ΔG_Hyd = R * T * lnϕ_aq
    ΔG_Org = R * T * lnϕ_org
    ΔG_Tr = ΔG_Org - ΔG_Hyd
    ΔG_Tr_array.append(ΔG_Tr)

ΔG_Tr_array = np.array(ΔG_Tr_array)

plt.plot(x_data, y_data_Na, 'o')
plt.plot(x_org_array, ΔG_Tr_array)
plt.show()


