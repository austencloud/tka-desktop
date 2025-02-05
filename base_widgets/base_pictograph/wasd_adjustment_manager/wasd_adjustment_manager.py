from typing import TYPE_CHECKING

from base_widgets.base_pictograph.wasd_adjustment_manager.prop_placement_override_manager import (
    PropPlacementOverrideManager,
)


from .arrow_movement_manager import ArrowMovementManager
from .rotation_angle_override_manager import RotationAngleOverrideManager

if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph import Pictograph


class WASD_AdjustmentManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.entry_remover = (
            self.pictograph.arrow_placement_manager.special_positioner.data_updater.entry_remover
        )
        self.movement_manager = ArrowMovementManager(pictograph)
        self.rotation_angle_override_manager = RotationAngleOverrideManager(self)
        self.prop_placement_override_manager = PropPlacementOverrideManager(self)

    def handle_special_placement_removal(self) -> None:
        selected_arrow = (
            self.pictograph.main_widget.sequence_workbench.graph_editor.selection_manager.selected_arrow
        )
        if not selected_arrow:
            return
        letter = self.pictograph.letter
        self.entry_remover.remove_special_placement_entry(letter, selected_arrow)
        self.pictograph.arrow_placement_manager.update_arrow_placements()
        self.pictograph.updater.update_pictograph()
        self.pictograph.view.repaint()
