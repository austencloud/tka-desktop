from typing import TYPE_CHECKING

from .attr_key_generator import AttrKeyGenerator
from .special_placement_data_updater.special_placement_data_updater import SpecialPlacementDataUpdater

if TYPE_CHECKING:
    from placement_managers.arrow_placement_manager.arrow_placement_manager import ArrowPlacementManager
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class SpecialArrowPositioner:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.placement_manager = placement_manager
        self.pictograph: BasePictograph = placement_manager.pictograph
        self.data_loader = self
        self.data_updater = SpecialPlacementDataUpdater(self)
        self.attr_key_generator = AttrKeyGenerator(self)
