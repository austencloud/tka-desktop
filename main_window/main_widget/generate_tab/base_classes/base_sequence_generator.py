from copy import deepcopy
import random
from typing import TYPE_CHECKING
from Enums.letters import Letter, LetterConditions
from data.constants import (
    ANTI,
    BLUE,
    BOX,
    DIAMOND,
    END_ORI,
    FLOAT,
    IN,
    MOTION_TYPE,
    PRO,
    PROP_ROT_DIR,
    RED,
    DASH,
    START_ORI,
    STATIC,
    NO_ROT,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    TURNS,
)
from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat import (
    StartPositionBeat,
)
from main_window.main_widget.sequence_widget.sequence_widget import SequenceWorkbench

if TYPE_CHECKING:
    from .base_sequence_generator_frame import BaseSequenceGeneratorFrame


class BaseSequenceGenerator:
    def __init__(self, sequence_generator_frame: "BaseSequenceGeneratorFrame"):
        self.sequence_generator_frame = sequence_generator_frame
        self.sequence_widget: "SequenceWorkbench" = None

        self.main_widget = sequence_generator_frame.tab.main_widget
        self.validation_engine = self.main_widget.json_manager.ori_validation_engine
        self.json_manager = self.main_widget.json_manager
        self.ori_calculator = self.main_widget.json_manager.ori_calculator

    def _initialize_sequence(self, length):
        if not self.sequence_widget:
            self.sequence_widget = self.main_widget.sequence_widget
        self.sequence = self.json_manager.loader_saver.load_current_sequence_json()

        if len(self.sequence) == 1:
            self.add_start_pos_pictograph()
            self.sequence = self.json_manager.loader_saver.load_current_sequence_json()

        self.sequence_widget.beat_frame.populator.modify_layout_for_chosen_number_of_beats(
            int(length)
        )

    def add_start_pos_pictograph(self) -> None:
        """Add a starting position pictograph to the sequence."""
        grid_mode = DIAMOND
        if grid_mode == DIAMOND:
            start_pos_keys = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
        elif grid_mode == BOX:
            start_pos_keys = ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]
        position_key = random.choice(start_pos_keys)
        self._add_start_position_to_sequence(position_key)

    def _add_start_position_to_sequence(self, position_key: str) -> None:
        start_pos, end_pos = position_key.split("_")
        letters = deepcopy(self.sequence_widget.main_widget.pictograph_dicts)
        for _, pictograph_dicts in letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict["start_pos"] == start_pos
                    and pictograph_dict["end_pos"] == end_pos
                ):
                    self.set_start_pos_to_in_orientation(pictograph_dict)
                    start_position_beat = StartPositionBeat(
                        self.main_widget.sequence_widget.beat_frame
                    )
                    start_position_beat.updater.update_pictograph(
                        deepcopy(pictograph_dict)
                    )

                    self.main_widget.json_manager.start_pos_handler.set_start_position_data(
                        start_position_beat
                    )
                    self.sequence_widget.beat_frame.start_pos_view.set_start_pos(
                        start_position_beat
                    )
                    return

    def set_start_pos_to_in_orientation(self, pictograph_dict: dict) -> None:
        """Set the start position pictograph to the in orientation."""
        pictograph_dict["blue_attributes"][START_ORI] = IN
        pictograph_dict["red_attributes"][START_ORI] = IN
        pictograph_dict["blue_attributes"][END_ORI] = IN
        pictograph_dict["red_attributes"][END_ORI] = IN

    def _update_start_oris(self, next_pictograph_dict, last_pictograph_dict):
        next_pictograph_dict["blue_attributes"][START_ORI] = last_pictograph_dict[
            "blue_attributes"
        ][END_ORI]
        next_pictograph_dict["red_attributes"][START_ORI] = last_pictograph_dict[
            "red_attributes"
        ][END_ORI]

    def _update_end_oris(self, next_pictograph_dict):
        next_pictograph_dict["blue_attributes"][END_ORI] = (
            self.ori_calculator.calculate_end_ori(next_pictograph_dict, BLUE)
        )
        next_pictograph_dict["red_attributes"][END_ORI] = (
            self.ori_calculator.calculate_end_ori(next_pictograph_dict, RED)
        )

    def _update_dash_static_prop_rot_dirs(
        self,
        next_beat: dict,
        is_continuous_rot_dir: bool,
        blue_rot_dir: str,
        red_rot_dir: str,
    ):
        def update_prop_rot_dir(color, rot_dir):
            attributes = next_beat[f"{color}_attributes"]
            if attributes[MOTION_TYPE] in [DASH, STATIC]:
                if is_continuous_rot_dir:
                    if attributes[TURNS] > 0:
                        attributes[PROP_ROT_DIR] = rot_dir
                    else:
                        attributes[PROP_ROT_DIR] = NO_ROT
                else:
                    if attributes[TURNS] > 0:
                        self._set_random_prop_rot_dir(next_beat, color)
                    else:
                        attributes[PROP_ROT_DIR] = NO_ROT

        update_prop_rot_dir(BLUE, blue_rot_dir)
        update_prop_rot_dir(RED, red_rot_dir)

    def _set_random_prop_rot_dir(self, next_pictograph_dict: dict, color: str) -> None:
        """Set a random prop rotation direction for the given color."""
        next_pictograph_dict[f"{color}_attributes"][PROP_ROT_DIR] = random.choice(
            [CLOCKWISE, COUNTER_CLOCKWISE]
        )

    def _update_beat_number_depending_on_sequence_length(
        self, next_pictograph_dict, sequence
    ):
        next_pictograph_dict["beat"] = len(sequence) - 1
        return next_pictograph_dict

    def _filter_options_by_rotation(
        self, options: list[dict], blue_rot_dir, red_rot_dir
    ) -> list[dict]:
        """Filter options to match the rotation direction for both hands."""
        filtered_options = [
            option
            for option in options
            if option["blue_attributes"][PROP_ROT_DIR] in [blue_rot_dir, NO_ROT]
            and option["red_attributes"][PROP_ROT_DIR] in [red_rot_dir, NO_ROT]
        ]
        return filtered_options if filtered_options else options

    def _set_turns(self, next_beat: dict, turn_blue: float, turn_red: float) -> dict:
        """Set the turns for blue and red attributes, adjusting motion types if necessary."""
        # Set blue turns
        if turn_blue == "fl" or turn_red == "fl":
            if Letter.get_letter(
                next_beat["letter"]
            ) in Letter.get_letters_by_condition(LetterConditions.TYPE1_HYBRID):
                return next_beat
        if turn_blue == "fl":

            if next_beat["blue_attributes"][MOTION_TYPE] in [PRO, ANTI]:
                next_beat["blue_attributes"][TURNS] = "fl"
                next_beat["blue_attributes"]["prefloat_motion_type"] = next_beat[
                    "blue_attributes"
                ][MOTION_TYPE]
                next_beat["blue_attributes"]["prefloat_prop_rot_dir"] = next_beat[
                    "blue_attributes"
                ][PROP_ROT_DIR]
                next_beat["blue_attributes"][MOTION_TYPE] = FLOAT
                next_beat["blue_attributes"][PROP_ROT_DIR] = NO_ROT

            elif next_beat["blue_attributes"][MOTION_TYPE] not in [PRO, ANTI]:
                next_beat["blue_attributes"][TURNS] = 0
        else:
            next_beat["blue_attributes"][TURNS] = turn_blue

        # Set red turns
        if turn_red == "fl":
            if next_beat["red_attributes"][MOTION_TYPE] in [PRO, ANTI]:
                next_beat["red_attributes"][TURNS] = "fl"
                next_beat["red_attributes"]["prefloat_motion_type"] = next_beat[
                    "red_attributes"
                ][MOTION_TYPE]
                next_beat["red_attributes"]["prefloat_prop_rot_dir"] = next_beat[
                    "red_attributes"
                ][PROP_ROT_DIR]
                next_beat["red_attributes"][MOTION_TYPE] = FLOAT
                next_beat["red_attributes"][PROP_ROT_DIR] = NO_ROT
            elif next_beat["red_attributes"][MOTION_TYPE] not in [PRO, ANTI]:
                next_beat["red_attributes"][TURNS] = 0
        else:
            next_beat["red_attributes"][TURNS] = turn_red

        return next_beat
