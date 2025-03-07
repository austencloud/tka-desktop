from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.arrow_movement_manager import (
    ArrowMovementManager,
)
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.prop_placement_override_manager import (
    PropPlacementOverrideManager,
)
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.special_placement_data_updater.special_placement_entry_remover import (
    SpecialPlacementEntryRemover,
)
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

        self.movement_manager = ArrowMovementManager(view)
        self.turns_tuple_generator = TurnsTupleGenerator()

        self.rot_angle_override_manager = RotAngleOverrideManager(self)
        self.prop_placement_override_manager = PropPlacementOverrideManager(self)
        self.entry_remover = SpecialPlacementEntryRemover(self)
