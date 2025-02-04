from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE
from data.positions import mirrored_positions
from data.locations import vertical_loc_mirror_map
from main_window.main_widget.sequence_widget.base_sequence_modifier import (
    BaseSequenceModifier,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import (
        SequenceWorkbench,
    )


class SequenceReflector(BaseSequenceModifier):
    success_message = "Sequence mirrored!"
    error_message = "No sequence to mirror."

    vertical_mirror_positions = mirrored_positions["vertical"]

    def __init__(self, sequence_widget: "SequenceWorkbench"):
        self.sequence_widget = sequence_widget
        json_manager = self.sequence_widget.main_widget.json_manager
        self.json_loader = json_manager.loader_saver
        self.json_updater = json_manager.updater

    def reflect_current_sequence(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        mirrored_sequence = self._reflect_sequence()
        self.sequence_widget.beat_frame.updater.update_beats_from(mirrored_sequence)
        self._update_ui()
        QApplication.restoreOverrideCursor()

    def _reflect_sequence(self):
        if self._check_length():
            return

        metadata = self.json_loader.load_current_sequence_json()[0].copy()
        mirrored_sequence = [metadata]

        start_pos_beat_dict = (
            self.sequence_widget.beat_frame.start_pos_view.start_pos.pictograph_dict.copy()
        )
        self._reflect_dict(start_pos_beat_dict)
        mirrored_sequence.append(start_pos_beat_dict)

        for beat_dict in self.sequence_widget.beat_frame.get.beat_dicts():
            mirrored_dict = beat_dict.copy()
            self._reflect_dict(mirrored_dict)
            mirrored_sequence.append(mirrored_dict)
        for beat_view in self.sequence_widget.beat_frame.beat_views:
            if beat_view.is_filled:
                beat = beat_view.beat

                beat.red_motion.prop_rot_dir = self.swap_dir(
                    beat.red_motion.prop_rot_dir
                )
                beat.blue_motion.prop_rot_dir = self.swap_dir(
                    beat.blue_motion.prop_rot_dir
                )

        return mirrored_sequence

    def _reflect_dict(self, pictograph_dict):
        for key in ["start_pos", "end_pos"]:
            if key in pictograph_dict:
                pictograph_dict[key] = self.vertical_mirror_positions.get(
                    pictograph_dict[key], pictograph_dict[key]
                )

        for color in ["blue_attributes", "red_attributes"]:
            if color in pictograph_dict:
                attributes = pictograph_dict[color]
                for loc_key in ["start_loc", "end_loc"]:
                    if loc_key in attributes:
                        attributes[loc_key] = vertical_loc_mirror_map.get(
                            attributes[loc_key], attributes[loc_key]
                        )
                if "prop_rot_dir" in attributes:
                    prop_rot_dir = attributes["prop_rot_dir"]
                    attributes["prop_rot_dir"] = self.swap_dir(prop_rot_dir)

        return pictograph_dict

    def swap_dir(self, prop_rot_dir):
        return (
            COUNTER_CLOCKWISE
            if prop_rot_dir == CLOCKWISE
            else (CLOCKWISE if prop_rot_dir == COUNTER_CLOCKWISE else prop_rot_dir)
        )
