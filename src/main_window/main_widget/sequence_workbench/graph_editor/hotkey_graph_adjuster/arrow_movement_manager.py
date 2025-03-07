# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_movement_manager.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import GE_PictographView

class ArrowMovementManager:
    _DIRECTION_MAP = {
        Qt.Key.Key_W: (0, -1),
        Qt.Key.Key_A: (-1, 0),
        Qt.Key.Key_S: (0, 1),
        Qt.Key.Key_D: (1, 0),
    }

    def __init__(self, ge_view: "GE_PictographView") -> None:
        self._ge_view = ge_view
        self._ge_pictograph = ge_view.pictograph
        self._data_updater = self._ge_pictograph.managers.arrow_placement_manager.data_updater
        self._turns_generator = TurnsTupleGenerator()

    def handle_arrow_movement(self, key: Qt.Key, shift_held: bool, ctrl_held: bool) -> None:
        increment = self._calculate_increment(shift_held, ctrl_held)
        adjustment = self._calculate_adjustment(key, increment)
        self._update_arrow_positions(adjustment)
        self._refresh_ui()

    def _calculate_increment(self, shift: bool, ctrl: bool) -> int:
        if shift and ctrl:
            return 200
        return 20 if shift else 5

    def _calculate_adjustment(self, key: Qt.Key, increment: int) -> tuple[int, int]:
        dx, dy = self._DIRECTION_MAP.get(key, (0, 0))
        return dx * increment, dy * increment

    def _update_arrow_positions(self, adjustment: tuple[int, int]) -> None:
        turns_data = self._turns_generator.generate_turns_tuple(self._ge_pictograph)
        self._data_updater.update_arrow_adjustments_in_json(adjustment, turns_data)
        self._data_updater.mirrored_entry_manager.update_mirrored_entry_in_json()

    def _refresh_ui(self) -> None:
        target_letter = self._ge_pictograph.state.letter
        collector = self._ge_pictograph.main_widget.pictograph_collector
        
        for pictograph in collector.collect_all_pictographs():
            if pictograph.state.letter == target_letter:
                pictograph.managers.updater.placement_updater.update()
        
        QApplication.processEvents()