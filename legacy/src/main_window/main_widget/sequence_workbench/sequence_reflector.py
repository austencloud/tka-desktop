from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from data.constants import (
    BLUE_ATTRS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    END_LOC,
    END_POS,
    PROP_ROT_DIR,
    RED_ATTRS,
    START_LOC,
    START_POS,
    VERTICAL,
)
from data.positions_maps import mirrored_positions
from data.locations import vertical_loc_mirror_map
from main_window.main_widget.sequence_workbench.base_sequence_modifier import (
    BaseSequenceModifier,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class SequenceReflector(BaseSequenceModifier):
    success_message = "Sequence reflected!"
    error_message = "No sequence to reflect."

    vertical_mirror_positions = mirrored_positions[VERTICAL]

    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sequence_workbench = sequence_workbench
        json_manager = AppContext.json_manager()
        self.json_loader = json_manager.loader_saver
        self.json_updater = json_manager.updater

    def reflect_current_sequence(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if not self._check_length():
            QApplication.restoreOverrideCursor()
            return
        mirrored_sequence = self._reflect_sequence()
        self.sequence_workbench.beat_frame.updater.update_beats_from(mirrored_sequence)
        self._update_ui()
        QApplication.restoreOverrideCursor()

    def _reflect_sequence(self):

        metadata = self.json_loader.load_current_sequence()[0].copy()
        mirrored_sequence = [metadata]

        start_pos_beat_data = (
            self.sequence_workbench.beat_frame.start_pos_view.start_pos.state.pictograph_data.copy()
        )
        self._reflect_dict(start_pos_beat_data)
        mirrored_sequence.append(start_pos_beat_data)

        for beat_data in self.sequence_workbench.beat_frame.get.beat_datas():
            mirrored_dict = beat_data.copy()
            self._reflect_dict(mirrored_dict)
            mirrored_sequence.append(mirrored_dict)
        for beat_view in self.sequence_workbench.beat_frame.beat_views:
            if beat_view.is_filled:
                beat = beat_view.beat

                beat.elements.red_motion.state.prop_rot_dir = self.swap_dir(
                    beat.elements.red_motion.state.prop_rot_dir
                )
                beat.elements.blue_motion.state.prop_rot_dir = self.swap_dir(
                    beat.elements.blue_motion.state.prop_rot_dir
                )

        return mirrored_sequence

    def _reflect_dict(self, pictograph_data):
        for key in [START_POS, END_POS]:
            if key in pictograph_data:
                pictograph_data[key] = self.vertical_mirror_positions.get(
                    pictograph_data[key], pictograph_data[key]
                )

        for color in [BLUE_ATTRS, RED_ATTRS]:
            if color in pictograph_data:
                attributes = pictograph_data[color]
                for loc_key in [START_LOC, END_LOC]:
                    if loc_key in attributes:
                        attributes[loc_key] = vertical_loc_mirror_map.get(
                            attributes[loc_key], attributes[loc_key]
                        )
                if PROP_ROT_DIR in attributes:
                    prop_rot_dir = attributes[PROP_ROT_DIR]
                    attributes[PROP_ROT_DIR] = self.swap_dir(prop_rot_dir)

        return pictograph_data

    def swap_dir(self, prop_rot_dir):
        return (
            COUNTER_CLOCKWISE
            if prop_rot_dir == CLOCKWISE
            else (CLOCKWISE if prop_rot_dir == COUNTER_CLOCKWISE else prop_rot_dir)
        )
