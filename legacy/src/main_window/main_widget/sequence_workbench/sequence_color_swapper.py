from typing import TYPE_CHECKING
from data.constants import (
    BLUE_ATTRS,
    END_LOC,
    END_POS,
    RED_ATTRS,
    START_LOC,
    START_POS,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.sequence_workbench.base_sequence_modifier import (
    BaseSequenceModifier,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext
from data.positions_maps import positions_map

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
        self.sequence_workbench.beat_frame.updater.update_beats_from(swapped_sequence)
        self._update_ui()
        QApplication.restoreOverrideCursor()

    def _color_swap_sequence(self) -> list[dict]:
        self.sequence_workbench.button_panel.toggle_swap_colors_icon()
        metadata = (
            AppContext.json_manager().loader_saver.load_current_sequence()[0].copy()
        )
        swapped_sequence = [metadata]

        start_pos_beat_data: dict = (
            self.sequence_workbench.beat_frame.start_pos_view.start_pos.state.pictograph_data.copy()
        )

        self._color_swap_pictograph_data(start_pos_beat_data)
        swapped_sequence.append(start_pos_beat_data)

        beat_datas = self.sequence_workbench.beat_frame.get.beat_datas()

        for beat_data in beat_datas:
            swapped_beat_data = beat_data.copy()
            self._color_swap_pictograph_data(swapped_beat_data)

            swapped_sequence.append(swapped_beat_data)

        for beat_view in self.sequence_workbench.beat_frame.beat_views:
            beat = beat_view.beat
            red_reversal = beat.state.red_reversal
            blue_reversal = beat.state.blue_reversal
            beat.state.red_reversal = blue_reversal
            beat.state.blue_reversal = red_reversal

        return swapped_sequence

    def _color_swap_pictograph_data(self, beat_data):

        beat_data[BLUE_ATTRS], beat_data[RED_ATTRS] = (
            beat_data[RED_ATTRS],
            beat_data[BLUE_ATTRS],
        )

        for loc in [START_LOC, END_LOC]:
            if loc in beat_data[BLUE_ATTRS] and loc in beat_data[RED_ATTRS]:
                left_loc = beat_data[BLUE_ATTRS][loc]
                right_loc = beat_data[RED_ATTRS][loc]
                pos_key = START_POS if loc == START_LOC else END_POS
                mapped_pos = positions_map.get((left_loc, right_loc))

                if mapped_pos is None:
                    print(
                        f"⚠️ WARNING: positions_map.get(({left_loc}, {right_loc})) returned None!"
                    )

                beat_data[pos_key] = mapped_pos

        return beat_data
