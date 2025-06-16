from typing import TYPE_CHECKING
from data.constants import (
    BLUE_ATTRS,
    BOX,
    DIAMOND,
    END_LOC,
    GRID_MODE,
    RED_ATTRS,
    START_LOC,
)
from data.positions_maps import positions_map
from data.locations import cw_loc_order

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.grid_mode_checker import GridModeChecker
from main_window.main_widget.sequence_workbench.base_sequence_modifier import (
    BaseSequenceModifier,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from .sequence_workbench import SequenceWorkbench


class SequenceRotater(BaseSequenceModifier):
    error_message = "No sequence to rotate."
    success_message = "Sequence rotated!"

    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sequence_workbench = sequence_workbench

    def rotate_current_sequence(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if not self._check_length():
            QApplication.restoreOverrideCursor()
            return
        rotated_sequence = self._rotate_sequence()
        self.sequence_workbench.beat_frame.updater.update_beats_from(rotated_sequence)
        self._update_ui()
        QApplication.restoreOverrideCursor()

    def _rotate_sequence(self):

        metadata = (
            AppContext.json_manager().loader_saver.load_current_sequence()[0].copy()
        )
        metadata[GRID_MODE] = BOX if metadata[GRID_MODE] == DIAMOND else DIAMOND

        rotated_sequence = [metadata]

        start_pos_beat_data = (
            self.sequence_workbench.beat_frame.start_pos_view.start_pos.state.pictograph_data.copy()
        )
        self._rotate_dict(start_pos_beat_data)
        rotated_sequence.append(start_pos_beat_data)

        for beat_data in self.sequence_workbench.beat_frame.get.beat_datas():
            rotated_dict = beat_data.copy()
            self._rotate_dict(rotated_dict)
            rotated_sequence.append(rotated_dict)

        return rotated_sequence

    def _rotate_dict(self, _dict: dict):
        for color in [BLUE_ATTRS, RED_ATTRS]:
            if color in _dict:
                attributes = _dict[color]
                for loc in [START_LOC, END_LOC]:
                    if loc in attributes:
                        attributes[loc] = self._rotate_location(attributes[loc])

        if BLUE_ATTRS in _dict and RED_ATTRS in _dict:
            bl = _dict[BLUE_ATTRS]
            rl = _dict[RED_ATTRS]
            for loc in [START_LOC, END_LOC]:
                if loc in bl and loc in rl:
                    _dict[f"{loc.split('_')[0]}_pos"] = positions_map[
                        (bl[loc], rl[loc])
                    ]

        _dict[GRID_MODE] = GridModeChecker.get_grid_mode(_dict)
        return _dict

    def _rotate_location(self, location):
        if location not in cw_loc_order:
            return location
        idx = cw_loc_order.index(location)
        new_idx = (idx + 1) % len(cw_loc_order)
        return cw_loc_order[new_idx]
