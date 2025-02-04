from typing import TYPE_CHECKING
from .handlers.beta_prop_positioner import BetaPropPositioner
from .handlers.default_prop_positioner import DefaultPropPositioner

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PropPlacementManager:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph

        # Positioners
        self.default_positioner = DefaultPropPositioner(self)
        self.beta_positioner = BetaPropPositioner(self)

    def update_prop_positions(self) -> None:
        for prop in self.pictograph.props.values():
            self.default_positioner.set_prop_to_default_loc(prop)

        if self.pictograph.check.ends_with_beta():
            self.beta_positioner.reposition_beta_props()
