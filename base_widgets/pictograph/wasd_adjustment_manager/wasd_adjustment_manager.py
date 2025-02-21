from typing import TYPE_CHECKING

from base_widgets.pictograph.wasd_adjustment_manager.prop_placement_override_manager import (
    PropPlacementOverrideManager,
)
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)


from .arrow_movement_manager import ArrowMovementManager
from .rotation_angle_override_manager import RotationAngleOverrideManager

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class WASD_AdjustmentManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.entry_remover = (
            self.pictograph.managers.arrow_placement_manager.special_positioner.data_updater.entry_remover
        )
        self.movement_manager = ArrowMovementManager(pictograph)
        self.turns_tuple_generator = TurnsTupleGenerator()

        self.rotation_angle_override_manager = RotationAngleOverrideManager(self)
        self.prop_placement_override_manager = PropPlacementOverrideManager(self)
