"""Transfer-reaction shim for explicit Li/Na MSContactor material transfer."""

from __future__ import annotations

from pyomo.common.config import ConfigValue
from pyomo.environ import Set, units

from idaes.core import ProcessBlock, ProcessBlockData, declare_process_block_class
from idaes.core.base import property_meta
from idaes.core.util.misc import add_object_reference


@declare_process_block_class("TbacDaTopoTransferReactions")
class TbacDaTopoTransferReactionsData(ProcessBlockData, property_meta.HasPropertyClassMetadata):
    def build(self):
        super().build()
        self._reaction_block_class = TbacDaTopoTransferReactionBlock
        self.element_list = Set(initialize=[])
        self.reaction_idx = Set(initialize=[])
        self.reaction_stoichiometry = {}

    @classmethod
    def define_metadata(cls, obj):
        obj.add_default_units(
            {
                "time": units.hour,
                "length": units.m,
                "mass": units.kg,
                "amount": units.mol,
                "temperature": units.K,
            }
        )

    @property
    def reaction_block_class(self):
        return self._reaction_block_class

    def build_reaction_block(self, *args, **kwargs):
        default = kwargs.pop("default", {})
        initialize = kwargs.pop("initialize", {})
        if initialize == {}:
            default["parameters"] = self
        else:
            for index in initialize:
                initialize[index]["parameters"] = self
        return self.reaction_block_class(*args, **kwargs, **default, initialize=initialize)


class _TbacDaTopoTransferReactionBlock(ProcessBlock):
    pass


@declare_process_block_class(
    "TbacDaTopoTransferReactionBlock",
    block_class=_TbacDaTopoTransferReactionBlock,
)
class TbacDaTopoTransferReactionBlockData(ProcessBlockData):
    CONFIG = ProcessBlockData.CONFIG()
    CONFIG.declare("parameters", ConfigValue(description="TBAC/DA + TOPO transfer parameter block."))

    def build(self):
        super().build()
        add_object_reference(self, "_params", self.config.parameters)

    @property
    def params(self):
        return self._params
