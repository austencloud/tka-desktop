from typing import TYPE_CHECKING
from data.quartered_CAPs import quartered_CAPs
from data.halved_CAPs import halved_CAPs
from data.constants import (
    ANTI,
    BEAT,
    BLUE,
    BLUE_ATTRS,
    CCW_HANDPATH,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    CW_HANDPATH,
    DASH,
    DIRECTION,
    END_LOC,
    END_ORI,
    END_POS,
    LETTER,
    MOTION_TYPE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
    SEQUENCE_START_POSITION,
    START_LOC,
    START_ORI,
    START_POS,
    STATIC,
    TIMING,
    TURNS,
)
from data.CAP_executors.rotated_loc_maps import (
    loc_map_cw,
    loc_map_ccw,
    loc_map_dash,
    loc_map_static,
    hand_rot_dir_map,
)
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.generate_tab.circular.CAP_type import CAPType
from objects.motion.managers.handpath_calculator import HandpathCalculator
from .CAP_executor import CAPExecutor
from data.positions_maps import positions_map

if TYPE_CHECKING:
    from ..circular_sequence_builder import CircularSequenceBuilder


class RotatedSwappedCAPExecutor(CAPExecutor):

    def __init__(self, circular_sequence_generator: "CircularSequenceBuilder"):
        self.circular_sequence_generator = circular_sequence_generator
        self.hand_rot_dir_calculator = HandpathCalculator()

    def create_CAPs(self, sequence: list[dict]):
        start_position_entry = (
            sequence.pop(0) if SEQUENCE_START_POSITION in sequence[0] else None
        )
        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]

        new_entries = []
        next_beat_number = last_entry[BEAT] + 1

        sequence_workbench = (
            self.circular_sequence_generator.main_widget.sequence_workbench
        )
        for _ in range(sequence_length):
            next_pictograph = self.create_new_rotated_CAP_entry(
                sequence,
                last_entry,
                next_beat_number,
                sequence_length + sequence_length,
            )
            new_entries.append(next_pictograph)
            sequence.append(next_pictograph)

            sequence_workbench.beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                next_pictograph,
                override_grow_sequence=True,
                update_word=True,
                update_image_export_preview=False,
            )
            QApplication.processEvents()

            last_entry = next_pictograph
            next_beat_number += 1

        sequence_workbench.current_word_label.update_current_word_label()

        if start_position_entry:
            start_position_entry[BEAT] = 0
            sequence.insert(0, start_position_entry)

    def calculate_rotated_permuatation_new_loc(
        self, start_loc: str, hand_rot_dir: str
    ) -> str:
        if hand_rot_dir == CW_HANDPATH:
            loc_map = loc_map_cw
        elif hand_rot_dir == CCW_HANDPATH:
            loc_map = loc_map_ccw
        elif hand_rot_dir == DASH:
            loc_map = loc_map_dash
        elif hand_rot_dir == STATIC:
            loc_map = loc_map_static
        return loc_map[start_loc]

    def create_new_rotated_CAP_entry(
        self,
        sequence,
        previous_entry,
        beat_number: int,
        final_intended_sequence_length: int,
    ) -> dict:
        previous_matching_beat = self.get_previous_matching_beat(
            sequence,
            beat_number,
            final_intended_sequence_length,
        )

        new_entry = {
            BEAT: beat_number,
            LETTER: previous_matching_beat[LETTER],
            START_POS: previous_entry[END_POS],
            END_POS: self.calculate_new_end_pos(previous_matching_beat, previous_entry),
            TIMING: previous_matching_beat[TIMING],
            DIRECTION: previous_matching_beat[DIRECTION],
            BLUE_ATTRS: self.create_new_attributes(
                previous_entry[BLUE_ATTRS], previous_matching_beat[RED_ATTRS]
            ),
            RED_ATTRS: self.create_new_attributes(
                previous_entry[RED_ATTRS], previous_matching_beat[BLUE_ATTRS]
            ),
        }

        if previous_matching_beat[BLUE_ATTRS].get(PREFLOAT_MOTION_TYPE, ""):
            new_entry[BLUE_ATTRS][PREFLOAT_MOTION_TYPE] = previous_matching_beat[
                BLUE_ATTRS
            ][PREFLOAT_MOTION_TYPE]
        if previous_matching_beat[BLUE_ATTRS].get(PREFLOAT_PROP_ROT_DIR, ""):
            new_entry[BLUE_ATTRS][PREFLOAT_PROP_ROT_DIR] = previous_matching_beat[
                BLUE_ATTRS
            ][PREFLOAT_PROP_ROT_DIR]
        if previous_matching_beat[RED_ATTRS].get(PREFLOAT_MOTION_TYPE, ""):
            new_entry[RED_ATTRS][PREFLOAT_MOTION_TYPE] = previous_matching_beat[
                RED_ATTRS
            ][PREFLOAT_MOTION_TYPE]
        if previous_matching_beat[RED_ATTRS].get(PREFLOAT_PROP_ROT_DIR, ""):
            new_entry[RED_ATTRS][PREFLOAT_PROP_ROT_DIR] = previous_matching_beat[
                RED_ATTRS
            ][PREFLOAT_PROP_ROT_DIR]

        new_entry[BLUE_ATTRS][END_ORI] = (
            self.circular_sequence_generator.json_manager.ori_calculator.calculate_end_ori(
                new_entry, BLUE
            )
        )
        new_entry[RED_ATTRS][END_ORI] = (
            self.circular_sequence_generator.json_manager.ori_calculator.calculate_end_ori(
                new_entry, RED
            )
        )

        return new_entry

    def calculate_new_end_pos(
        self, previous_matching_beat: dict, previous_entry: dict
    ) -> str:
        blue_hand_rot_dir = self.hand_rot_dir_calculator.get_hand_rot_dir(
            previous_matching_beat[BLUE_ATTRS][START_LOC],
            previous_matching_beat[BLUE_ATTRS][END_LOC],
        )
        red_hand_rot_dir = self.hand_rot_dir_calculator.get_hand_rot_dir(
            previous_matching_beat[RED_ATTRS][START_LOC],
            previous_matching_beat[RED_ATTRS][END_LOC],
        )

        new_blue_end_loc = self.calculate_rotated_permuatation_new_loc(
            previous_entry[BLUE_ATTRS][END_LOC],
            blue_hand_rot_dir,
        )

        new_red_end_loc = self.calculate_rotated_permuatation_new_loc(
            previous_entry[RED_ATTRS][END_LOC],
            red_hand_rot_dir,
        )
        new_end_pos = positions_map.get((new_blue_end_loc, new_red_end_loc))
        return new_end_pos

    def get_hand_rot_dir_from_locs(self, start_loc: str, end_loc: str) -> str:
        return hand_rot_dir_map.get((start_loc, end_loc))

    def get_previous_matching_beat(
        self,
        sequence: list[dict],
        beat_number: int,
        final_length: int,
    ) -> dict:
        index_map = self.get_index_map(final_length)
        return sequence[index_map[beat_number]]

    def get_index_map(self, length: int) -> dict[int, int]:
        if length < 2:
            return {i: max(i - 1, 0) for i in range(1, length + 1)}

        return {i: i - (length // 2) + 1 for i in range((length // 2) + 1, length + 1)}

    def get_previous_matching_beat_mirrored(
        self,
        sequence: list[dict],
        beat_number: int,
        final_length: int,
        color_swap: bool,
    ) -> dict:
        mid_point = final_length // 2
        mirrored_beat_number = (final_length - beat_number) % mid_point
        mirrored_beat = sequence[mirrored_beat_number]
        if color_swap:
            mirrored_beat = self.swap_colors(mirrored_beat)
        return mirrored_beat

    def swap_colors(self, beat: dict) -> dict:
        beat[BLUE_ATTRS], beat[RED_ATTRS] = (
            beat[RED_ATTRS],
            beat[BLUE_ATTRS],
        )
        return beat

    def create_new_attributes(
        self,
        previous_attributes: dict,
        previous_matching_beat_attributes: dict,
    ) -> dict:
        motion_type = previous_matching_beat_attributes[MOTION_TYPE]
        prop_rot_dir = previous_matching_beat_attributes[PROP_ROT_DIR]
        new_entry_attributes = {
            MOTION_TYPE: motion_type,
            START_ORI: previous_attributes[END_ORI],
            PROP_ROT_DIR: prop_rot_dir,
            START_LOC: previous_attributes[END_LOC],
            END_LOC: self.calculate_rotated_permuatation_new_loc(
                previous_attributes[END_LOC],
                self.hand_rot_dir_calculator.get_hand_rot_dir(
                    previous_matching_beat_attributes[START_LOC],
                    previous_matching_beat_attributes[END_LOC],
                ),
            ),
            TURNS: previous_matching_beat_attributes[TURNS],
        }

        # Handle floating states
        if previous_matching_beat_attributes.get(PREFLOAT_MOTION_TYPE):
            new_entry_attributes[PREFLOAT_MOTION_TYPE] = (
                previous_matching_beat_attributes[PREFLOAT_MOTION_TYPE]
            )
            new_entry_attributes[PREFLOAT_PROP_ROT_DIR] = (
                previous_matching_beat_attributes[PREFLOAT_PROP_ROT_DIR]
            )
        return new_entry_attributes
