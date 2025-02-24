from typing import TYPE_CHECKING

from base_widgets.pictograph.hotkey_graph_adjuster.special_placement_data_updater.special_placement_data_updater import (
    SpecialPlacementDataUpdater,
)


from .attr_key_generator import AttrKeyGenerator


if TYPE_CHECKING:
    from placement_managers.arrow_placement_manager.arrow_placement_manager import (
        ArrowPlacementManager,
    )
    from base_widgets.pictograph.pictograph import Pictograph


class SpecialArrowPositioner:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.placement_manager = placement_manager
        self.pictograph: Pictograph = placement_manager.pictograph
        self.data_loader = self
        self.attr_key_generator = AttrKeyGenerator(self)
        self.data_updater = SpecialPlacementDataUpdater(
            self,
            self.attr_key_generator,
            self.pictograph.state,
            lambda arrow: self.placement_manager.default_positioner.get_default_adjustment(
                arrow
            ),
            self.pictograph.managers.get,
        )
