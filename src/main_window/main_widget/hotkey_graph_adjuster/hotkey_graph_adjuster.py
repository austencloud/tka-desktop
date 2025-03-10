# hotkey_graph_adjuster.py (modifications)
from typing import TYPE_CHECKING

from .arrow_movement_manager import ArrowMovementManager
from .prop_placement_override_manager import PropPlacementOverrideManager
from .data_updater.special_placement_entry_remover import SpecialPlacementEntryRemover
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from .rot_angle_override.rot_angle_override_manager import RotAngleOverrideManager

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


class HotkeyGraphAdjuster:
    def __init__(self, view: "GE_PictographView") -> None:
        self.ge_view = view
        self.graph_editor = view.graph_editor
        self.state = self.graph_editor.state  # Reference to centralized state

        self.movement_manager = ArrowMovementManager(view)
        self.turns_tuple_generator = TurnsTupleGenerator()

        self.rot_angle_override_manager = RotAngleOverrideManager(self)
        self.prop_placement_override_manager = PropPlacementOverrideManager(self)
        self.entry_remover = SpecialPlacementEntryRemover(self)
    
    def get_selected_arrow(self):
        """Get the currently selected arrow from centralized state."""
        return self.state.get_selected_arrow()
    
    def get_current_pictograph(self):
        """Get the currently editing pictograph from centralized state."""
        return self.state.get_pictograph()