from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.pictograph_collector import PictographCollector
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)


if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph
    from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph import GE_Pictograph


from PyQt6.QtCore import Qt


class ArrowMovementManager:
    def __init__(self, pictograph: "GE_Pictograph") -> None:
        self.pictograph = pictograph
        self.data_updater = (
            self.pictograph.managers.arrow_placement_manager.special_positioner.data_updater
        )

    def handle_arrow_movement(
        self, GE_pictograph: "GE_Pictograph", key, shift_held, ctrl_held
    ) -> None:
        self.pictograph = GE_pictograph
        self.graph_editor = GE_pictograph.main_widget.sequence_workbench.graph_editor
        selected_arrow = self.graph_editor.selection_manager.selected_arrow

        if not selected_arrow:
            return

        adjustment_increment = 5
        if shift_held:
            adjustment_increment = 20
        if shift_held and ctrl_held:
            adjustment_increment = 200

        adjustment = self.get_adjustment(key, adjustment_increment)
        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(self.pictograph)
        self.data_updater.update_arrow_adjustments_in_json(adjustment, selected_arrow, turns_tuple)
        self.data_updater.mirrored_entry_manager.update_mirrored_entry_in_json(
            selected_arrow
        )
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
