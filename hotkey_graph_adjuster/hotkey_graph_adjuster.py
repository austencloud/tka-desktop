from typing import TYPE_CHECKING

from hotkey_graph_adjuster.arrow_movement_manager import ArrowMovementManager
from hotkey_graph_adjuster.prop_placement_override_manager import (
    PropPlacementOverrideManager,
)
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)


from .arrow_rot_angle_override_manager import ArrowRotAngleOverrideManager

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )
    from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph import (
        GE_Pictograph,
    )


class HotkeyGraphAdjuster:
    def __init__(self, view: "GE_PictographView") -> None:
        self.view = view
        self.entry_remover = (
            self.view.get_current_pictograph().managers.arrow_placement_manager.data_updater.entry_remover
        )
        self.movement_manager = ArrowMovementManager(view)
        self.turns_tuple_generator = TurnsTupleGenerator()

        self.rotation_angle_override_manager = ArrowRotAngleOverrideManager(self)
        self.prop_placement_override_manager = PropPlacementOverrideManager(self)
