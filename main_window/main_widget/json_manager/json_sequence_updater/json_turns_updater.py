from typing import TYPE_CHECKING, Union

from data.constants import DASH, FLOAT, NO_ROT, STATIC


if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )
    from objects.motion.motion import Motion


class JsonTurnsUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater"):
        self.json_updater = json_updater
        self.json_manager = json_updater.json_manager
        self.main_widget = self.json_manager.main_widget

    def update_turns_in_json_at_index(
        self, index: int, color: str, turns: Union[int, float]
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["turns"] = turns
        end_ori = self.json_manager.ori_calculator.calculate_end_ori(
            sequence[index], color
        )
        sequence[index][f"{color}_attributes"]["end_ori"] = end_ori
        beat_frame = self.json_manager.main_widget.sequence_widget.beat_frame
        if sequence[index][f"{color}_attributes"]["turns"] != "fl":
            if sequence[index][f"{color}_attributes"]["turns"] > 0:
                pictograph = beat_frame.beat_views[index - 2].beat
                if pictograph:
                    motion = pictograph.get.motion_by_color(color)
                    prop_rot_dir = motion.prop_rot_dir
                    sequence[index][f"{color}_attributes"][
                        "prop_rot_dir"
                    ] = prop_rot_dir
            if "prefloat_prop_rot_dir" in sequence[index][f"{color}_attributes"]:

                del sequence[index][f"{color}_attributes"]["prefloat_prop_rot_dir"]
        elif sequence[index][f"{color}_attributes"]["turns"] == "fl":
            pictograph = beat_frame.beat_views[index - 2].beat
            if pictograph:
                motion = pictograph.get.motion_by_color(color)

        if sequence[index][f"{color}_attributes"]["motion_type"] in [DASH, STATIC]:
            if sequence[index][f"{color}_attributes"]["turns"] == 0:
                prop_rot_dir = NO_ROT
                sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir

        self.json_manager.loader_saver.save_current_sequence(sequence)
        self.main_widget.sequence_properties_manager.update_sequence_properties()

    def set_turns_from_num_to_num_in_json(self, motion: "Motion", new_turns):
        current_beat = (
            self.main_widget.sequence_widget.beat_frame.get.currently_selected_beat_view()
        )
        current_beat_number = (
            current_beat.number
            + self.get_number_of_placeholders_before_current_beat(current_beat.number)
        )
        self.update_turns_in_json_at_index(
            current_beat_number + 1, motion.color, new_turns
        )
        self.json_updater.motion_type_updater.update_motion_type_in_json_at_index(
            current_beat_number + 1, motion.color, motion.motion_type
        )

        self.json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json_at_index(
            current_beat_number + 1, motion.color, motion.prop_rot_dir
        )

    def get_number_of_placeholders_before_current_beat(self, current_beat_number):
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        number_of_placeholders = 0
        for beat in sequence[2:]:
            if beat["beat"] < current_beat_number and beat.get("is_placeholder"):
                number_of_placeholders += 1
        return number_of_placeholders

    def set_turns_to_num_from_fl_in_json(self, motion: "Motion", new_turns):
        beat_index = (
            self.main_widget.sequence_widget.beat_frame.get.index_of_currently_selected_beat()
        )
        json_index = beat_index + 2
        motion.motion_type = (
            self.json_manager.loader_saver.get_prefloat_motion_type_from_json_at_index(
                json_index,
                motion.color,
            )
        )
        motion.prop_rot_dir = (
            self.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                json_index,
                motion.color,
            )
        )
        self.update_turns_in_json_at_index(json_index, motion.color, new_turns)
        self.json_updater.motion_type_updater.update_motion_type_in_json_at_index(
            json_index, motion.color, motion.motion_type
        )
        self.json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json_at_index(
            json_index, motion.color, motion.prop_rot_dir
        )

    def set_turns_to_fl_from_num_in_json(self, motion: "Motion", new_turns):
        beat_index = (
            self.main_widget.sequence_widget.beat_frame.get.index_of_currently_selected_beat()
        )
        json_index = beat_index + 2
        self.update_turns_in_json_at_index(json_index, motion.color, new_turns)
        self.json_updater.motion_type_updater.update_prefloat_motion_type_in_json(
            json_index,
            motion.color,
            self.json_manager.loader_saver.get_motion_type_from_json_at_index(
                json_index, motion.color
            ),
        )
        self.json_updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            json_index,
            motion.color,
            self.json_manager.loader_saver.get_prop_rot_dir_from_json(
                json_index, motion.color
            ),
        )
        self.json_updater.motion_type_updater.update_motion_type_in_json_at_index(
            json_index, motion.color, FLOAT
        )
        self.json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json_at_index(
            json_index, motion.color, NO_ROT
        )
