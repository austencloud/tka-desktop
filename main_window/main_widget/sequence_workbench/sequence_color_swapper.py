from typing import TYPE_CHECKING
from data.positions_map import positions_map
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.sequence_workbench.base_sequence_modifier import (
    BaseSequenceModifier,
)
from main_window.settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class SequenceColorSwapper(BaseSequenceModifier):
    success_message = "Colors swapped!"
    error_message = "No sequence to color swap."

    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sequence_workbench = sequence_workbench

    def swap_current_sequence(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if not self._check_length():
            QApplication.restoreOverrideCursor()
            return
        swapped_sequence = self._color_swap_sequence()
        self.sequence_workbench.sequence_beat_frame.updater.update_beats_from(
            swapped_sequence
        )
        self._update_ui()
        QApplication.restoreOverrideCursor()

    def _color_swap_sequence(self) -> list[dict]:

        self.sequence_workbench.button_panel.toggle_swap_colors_icon()
        metadata = (
            AppContext.json_manager().loader_saver.load_current_sequence()[0].copy()
        )
        swapped_sequence = []
        swapped_sequence.append(metadata)

        start_pos_beat_dict: dict = (
            self.sequence_workbench.sequence_beat_frame.start_pos_view.start_pos.state.pictograph_data.copy()
        )
        self._color_swap_dict(start_pos_beat_dict)
        swapped_sequence.append(start_pos_beat_dict)

        beat_dicts = self.sequence_workbench.sequence_beat_frame.get.beat_dicts()
        for beat_dict in beat_dicts:
            swapped_beat = beat_dict.copy()
            self._color_swap_dict(swapped_beat)
            swapped_sequence.append(swapped_beat)
        for beat_view in self.sequence_workbench.sequence_beat_frame.beat_views:
            beat = beat_view.beat

            red_reversal = beat.state.red_reversal
            blue_reversal = beat.state.blue_reversal
            beat.state.red_reversal = blue_reversal
            beat.state.blue_reversal = red_reversal

        return swapped_sequence

    def _color_swap_dict(self, _dict):
        _dict["blue_attributes"], _dict["red_attributes"] = (
            _dict["red_attributes"],
            _dict["blue_attributes"],
        )

        for loc in ["start_loc", "end_loc"]:
            if loc in _dict["blue_attributes"] and loc in _dict["red_attributes"]:
                left_loc = _dict["blue_attributes"][loc]
                right_loc = _dict["red_attributes"][loc]
                pos_key = "start_pos" if loc == "start_loc" else "end_pos"
                _dict[pos_key] = positions_map.get((left_loc, right_loc))

        return _dict
