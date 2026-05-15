"""Minimal organic property package for TBAC/DA DES + TOPO Li/Na transfer."""

from __future__ import annotations

from pyomo.environ import Param, Set, Var, units

from idaes.core import (
    Component,
    MaterialFlowBasis,
    Phase,
    PhysicalParameterBlock,
    StateBlock,
    StateBlockData,
    declare_process_block_class,
)
from idaes.core.util.initialization import fix_state_vars


@declare_process_block_class("TbacDaTopoOrgParameters")
class TbacDaTopoOrgParameterData(PhysicalParameterBlock):
    def build(self):
        super().build()
        self.liquid = Phase()
        self.DES = Component()
        self.TOPO = Component()
        self.Li = Component()
        self.Na = Component()
        self.Cl = Component()

        self.concentration_elements = Set(initialize=["DES", "TOPO", "Li", "Na", "Cl"])
        self.mw = Param(
            self.component_list,
            units=units.kg / units.mol,
            initialize={
                "DES": 622.44e-3,
                "TOPO": 386.64e-3,
                "Li": 6.94e-3,
                "Na": 22.98976928e-3,
                "Cl": 35.45e-3,
            },
        )
        self._state_block_class = TbacDaTopoOrgStateBlock

    @classmethod
    def define_metadata(cls, obj):
        obj.add_default_units(
            {
                "time": units.hour,
                "mass": units.kg,
                "amount": units.mol,
                "length": units.m,
                "temperature": units.K,
            }
        )


class _TbacDaTopoOrgStateBlock(StateBlock):
    def fix_initialization_states(self):
        fix_state_vars(self)


@declare_process_block_class("TbacDaTopoOrgStateBlock", block_class=_TbacDaTopoOrgStateBlock)
class TbacDaTopoOrgStateBlockData(StateBlockData):
    def build(self):
        super().build()
        self.conc_mass_comp = Var(
            self.params.concentration_elements,
            units=units.mg / units.L,
            initialize=1e-7,
            bounds=(1e-20, None),
        )
        self.flow_vol = Var(units=units.L / units.hour, bounds=(1e-8, None))
        self.conc_mol_comp = Var(
            self.params.concentration_elements,
            units=units.mol / units.L,
            initialize=1e-5,
            bounds=(1e-20, None),
        )

        @self.Constraint(self.params.concentration_elements)
        def molar_concentration_constraint(b, j):
            return units.convert(
                b.conc_mol_comp[j] * b.params.mw[j],
                to_units=units.mg / units.litre,
            ) == b.conc_mass_comp[j]

    def get_material_flow_basis(self):
        return MaterialFlowBasis.molar

    def get_material_flow_terms(self, p, j):
        return units.convert(
            self.flow_vol * self.conc_mass_comp[j] / self.params.mw[j],
            to_units=units.mol / units.hour,
        )

    def get_material_density_terms(self, p, j):
        return units.convert(
            self.conc_mass_comp[j] / self.params.mw[j],
            to_units=units.mol / units.m**3,
        )

    def define_state_vars(self):
        return {"flow_vol": self.flow_vol, "conc_mass_comp": self.conc_mass_comp}
