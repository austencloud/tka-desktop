from typing import TYPE_CHECKING
from data.constants import BLUE_ATTRIBUTES, END_LOC, END_POS, RED_ATTRIBUTES, START_LOC, START_POS
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
        _dict[BLUE_ATTRIBUTES], _dict[RED_ATTRIBUTES] = (
            _dict[RED_ATTRIBUTES],
            _dict[BLUE_ATTRIBUTES],
        )

        for loc in [START_LOC, END_LOC]:
            if loc in _dict[BLUE_ATTRIBUTES] and loc in _dict[RED_ATTRIBUTES]:
                left_loc = _dict[BLUE_ATTRIBUTES][loc]
                right_loc = _dict[RED_ATTRIBUTES][loc]
                pos_key = START_POS if loc == START_LOC else END_POS
                _dict[pos_key] = positions_map.get((left_loc, right_loc))

        return _dict
