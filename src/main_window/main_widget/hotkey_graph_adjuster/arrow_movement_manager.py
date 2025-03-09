# arrow_movement_manager.py (modifications)
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


class ArrowMovementManager:
    def __init__(self, ge_view: "GE_PictographView") -> None:
        self.ge_view = ge_view
        self.graph_editor = ge_view.graph_editor
        self.state = self.graph_editor.state  # Reference to centralized state

    def handle_arrow_movement(self, key, shift_held, ctrl_held) -> None:
        self.ge_pictograph = self.ge_view.pictograph
        self.data_updater = (
            self.ge_pictograph.managers.arrow_placement_manager.data_updater
        )

        # Get selected arrow from centralized state
        selected_arrow = self.state.get_selected_arrow()
        if not selected_arrow:
            return

        adjustment_increment = 5
        if shift_held:
            adjustment_increment = 20
        if shift_held and ctrl_held:
            adjustment_increment = 200

        adjustment = self.get_adjustment(key, adjustment_increment)
        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(self.ge_pictograph)
        self.data_updater.update_arrow_adjustments_in_json(adjustment, turns_tuple)
        self.data_updater.mirrored_entry_manager.update_mirrored_entry_in_json()

        # Update all pictographs with the same letter
        for (
            pictograph
        ) in (
            self.ge_pictograph.main_widget.pictograph_collector.collect_all_pictographs()
        ):
            if pictograph.state.letter == self.ge_pictograph.state.letter:
                pictograph.managers.updater.placement_updater.update()

        QApplication.processEvents()

    def get_adjustment(self, key, increment) -> tuple[int, int]:
        direction_map = {
            Qt.Key.Key_W: (0, -1),
            Qt.Key.Key_A: (-1, 0),
            Qt.Key.Key_S: (0, 1),
            Qt.Key.Key_D: (1, 0),
        }
        dx, dy = direction_map.get(key, (0, 0))
        return dx * increment, dy * increment
