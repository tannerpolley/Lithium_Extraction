"""Minimal aqueous Li/Na/Cl property package for the TBAC/DA + TOPO case study."""

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


@declare_process_block_class("TbacDaTopoAqParameters")
class TbacDaTopoAqParameterData(PhysicalParameterBlock):
    def build(self):
        super().build()
        self.liquid = Phase()
        self.H2O = Component()
        self.Li = Component()
        self.Na = Component()
        self.Cl = Component()

        self.dissolved_elements = Set(initialize=["Li", "Na", "Cl"])
        self.mw = Param(
            self.component_list,
            units=units.kg / units.mol,
            initialize={"H2O": 18.015e-3, "Li": 6.94e-3, "Na": 22.98976928e-3, "Cl": 35.45e-3},
        )
        self.dens_mass = Param(
            initialize=1.0,
            units=units.kg / units.litre,
            mutable=True,
            doc="Bulk aqueous density used for the simplified concentration-state package.",
        )
        self._state_block_class = TbacDaTopoAqStateBlock

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


class _TbacDaTopoAqStateBlock(StateBlock):
    def fix_initialization_states(self):
        fix_state_vars(self)


@declare_process_block_class("TbacDaTopoAqStateBlock", block_class=_TbacDaTopoAqStateBlock)
class TbacDaTopoAqStateBlockData(StateBlockData):
    def build(self):
        super().build()
        self.conc_mass_comp = Var(
            self.params.dissolved_elements,
            units=units.mg / units.L,
            bounds=(1e-20, None),
        )
        self.flow_vol = Var(units=units.L / units.hour, bounds=(1e-8, None))
        self.conc_mol_comp = Var(
            self.params.dissolved_elements,
            units=units.mol / units.L,
            initialize=1e-5,
            bounds=(1e-20, None),
        )

        @self.Constraint(self.params.dissolved_elements)
        def molar_concentration_constraint(b, j):
            return units.convert(
                b.conc_mol_comp[j] * b.params.mw[j],
                to_units=units.mg / units.litre,
            ) == b.conc_mass_comp[j]

    def get_material_flow_basis(self):
        return MaterialFlowBasis.molar

    def get_material_flow_terms(self, p, j):
        if j == "H2O":
            return self.flow_vol * self.params.dens_mass / self.params.mw[j]
        return units.convert(
            self.flow_vol * self.conc_mass_comp[j] / self.params.mw[j],
            to_units=units.mol / units.hour,
        )

    def get_material_density_terms(self, p, j):
        if j == "H2O":
            return units.convert(
                self.params.dens_mass / self.params.mw[j],
                to_units=units.mol / units.m**3,
            )
        return units.convert(
            self.conc_mass_comp[j] / self.params.mw[j],
            to_units=units.mol / units.m**3,
        )

    def define_state_vars(self):
        return {"flow_vol": self.flow_vol, "conc_mass_comp": self.conc_mass_comp}
