from typing import TYPE_CHECKING
from data.quartered_permutations import quartered_permutations
from data.halved_permutations import halved_permutations
from data.constants import (
    BEAT,
    BLUE,
    BLUE_ATTRIBUTES,
    CCW_HANDPATH,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    CW_HANDPATH,
    DASH,
    DIRECTION,
    EAST,
    END_LOC,
    END_ORI,
    END_POS,
    LETTER,
    MOTION_TYPE,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PROP_ROT_DIR,
    RED,
    RED_ATTRIBUTES,
    SEQUENCE_START_POSITION,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    START_LOC,
    START_ORI,
    START_POS,
    STATIC,
    TIMING,
    TURNS,
    WEST,
)
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

from objects.motion.managers.handpath_calculator import HandpathCalculator
from .permutation_executor_base import PermutationExecutor
from data.positions_map import positions_map

if TYPE_CHECKING:
    from ..circular_sequence_builder import CircularSequenceBuilder


class RotatedPermutationExecutor(PermutationExecutor):
    def __init__(self, circular_sequence_generator: "CircularSequenceBuilder"):
        self.circular_sequence_generator = circular_sequence_generator
        self.hand_rot_dir_calculator = HandpathCalculator()

    def create_permutations(self, sequence: list[dict]):
        start_position_entry = (
            sequence.pop(0) if SEQUENCE_START_POSITION in sequence[0] else None
        )
        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]

        new_entries = []
        next_beat_number = last_entry[BEAT] + 1
        halved_or_quartered = self.get_halved_or_quartered()

        sequence_workbench = (
            self.circular_sequence_generator.main_widget.sequence_workbench
        )
        entries_to_add = self.determine_how_many_entries_to_add(sequence_length)
        for _ in range(entries_to_add):
            next_pictograph = self.create_new_rotated_permutation_entry(
                sequence,
                last_entry,
                next_beat_number,
                sequence_length + entries_to_add,
                halved_or_quartered,
            )
            new_entries.append(next_pictograph)
            sequence.append(next_pictograph)

            sequence_workbench.sequence_beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                next_pictograph,
                override_grow_sequence=True,
                update_word=False,
                update_image_export_preview=False,
            )
            QApplication.processEvents()

            last_entry = next_pictograph
            next_beat_number += 1

        sequence_workbench.current_word_label.update_current_word_label_from_beats()

        if start_position_entry:
            start_position_entry[BEAT] = 0
            sequence.insert(0, start_position_entry)

    def determine_how_many_entries_to_add(self, sequence_length: int) -> int:
        if self.is_quartered_permutation():
            return sequence_length * 3
        elif self.is_halved_permutation():
            return sequence_length
        return 0

    def is_quartered_permutation(self) -> bool:
        sequence = (
            self.circular_sequence_generator.json_manager.loader_saver.load_current_sequence()
        )
        start_pos = sequence[1][END_POS]
        end_pos = sequence[-1][END_POS]
        return (start_pos, end_pos) in quartered_permutations

    def is_halved_permutation(self) -> bool:
        sequence = (
            self.circular_sequence_generator.json_manager.loader_saver.load_current_sequence()
        )
        start_pos = sequence[1][END_POS]
        end_pos = sequence[-1][END_POS]
        return (start_pos, end_pos) in halved_permutations

    def get_halved_or_quartered(self) -> str:
        if self.is_halved_permutation():
            return "halved"
        elif self.is_quartered_permutation():
            return "quartered"
        return ""

    def calculate_rotated_permuatation_new_loc(
        self, start_loc: str, hand_rot_dir: str
    ) -> str:
        loc_map_cw = {
            SOUTH: WEST,
            WEST: NORTH,
            NORTH: EAST,
            EAST: SOUTH,
            NORTHEAST: SOUTHEAST,
            SOUTHEAST: SOUTHWEST,
            SOUTHWEST: NORTHWEST,
            NORTHWEST: NORTHEAST,
        }
        loc_map_ccw = {
            SOUTH: EAST,
            EAST: NORTH,
            NORTH: WEST,
            WEST: SOUTH,
            NORTHEAST: NORTHWEST,
            NORTHWEST: SOUTHWEST,
            SOUTHWEST: SOUTHEAST,
            SOUTHEAST: NORTHEAST,
        }
        if hand_rot_dir == CW_HANDPATH:
            loc_map = loc_map_cw

        elif hand_rot_dir == CCW_HANDPATH:
            loc_map = loc_map_ccw

        elif hand_rot_dir == DASH:
            loc_map = {
                SOUTH: NORTH,
                NORTH: SOUTH,
                WEST: EAST,
                EAST: WEST,
                NORTHEAST: SOUTHWEST,
                SOUTHEAST: NORTHWEST,
                SOUTHWEST: NORTHEAST,
                NORTHWEST: SOUTHEAST,
            }

        elif hand_rot_dir == STATIC:
            loc_map = {
                SOUTH: SOUTH,
                NORTH: NORTH,
                WEST: WEST,
                EAST: EAST,
                NORTHEAST: NORTHEAST,
                SOUTHEAST: SOUTHEAST,
                SOUTHWEST: SOUTHWEST,
                NORTHWEST: NORTHWEST,
            }

        return loc_map[start_loc]

    def create_new_rotated_permutation_entry(
        self,
        sequence,
        previous_entry,
        beat_number: int,
        final_intended_sequence_length: int,
        halved_or_quartered: str,
    ) -> dict:
        previous_matching_beat = self.get_previous_matching_beat(
            sequence,
            beat_number,
            final_intended_sequence_length,
            halved_or_quartered,
        )

        new_entry = {
            BEAT: beat_number,
            LETTER: previous_matching_beat[LETTER],
            START_POS: previous_entry[END_POS],
            END_POS: self.calculate_new_end_pos(previous_matching_beat, previous_entry),
            TIMING: previous_matching_beat[TIMING],
            DIRECTION: previous_matching_beat[DIRECTION],
            BLUE_ATTRIBUTES: self.create_new_attributes(
                previous_entry[BLUE_ATTRIBUTES],
                previous_matching_beat[BLUE_ATTRIBUTES],
            ),
            RED_ATTRIBUTES: self.create_new_attributes(
                previous_entry[RED_ATTRIBUTES],
                previous_matching_beat[RED_ATTRIBUTES],
            ),
        }

        if previous_matching_beat[BLUE_ATTRIBUTES].get(PREFLOAT_MOTION_TYPE, ""):
            new_entry[BLUE_ATTRIBUTES][PREFLOAT_MOTION_TYPE] = previous_matching_beat[
                BLUE_ATTRIBUTES
            ][PREFLOAT_MOTION_TYPE]
        if previous_matching_beat[BLUE_ATTRIBUTES].get(PREFLOAT_PROP_ROT_DIR, ""):
            new_entry[BLUE_ATTRIBUTES][PREFLOAT_PROP_ROT_DIR] = previous_matching_beat[
                BLUE_ATTRIBUTES
            ][PREFLOAT_PROP_ROT_DIR]
        if previous_matching_beat[RED_ATTRIBUTES].get(PREFLOAT_MOTION_TYPE, ""):
            new_entry[RED_ATTRIBUTES][PREFLOAT_MOTION_TYPE] = previous_matching_beat[
                RED_ATTRIBUTES
            ][PREFLOAT_MOTION_TYPE]
        if previous_matching_beat[RED_ATTRIBUTES].get(PREFLOAT_PROP_ROT_DIR, ""):
            new_entry[RED_ATTRIBUTES][PREFLOAT_PROP_ROT_DIR] = previous_matching_beat[
                RED_ATTRIBUTES
            ][PREFLOAT_PROP_ROT_DIR]

        new_entry[BLUE_ATTRIBUTES][END_ORI] = (
            self.circular_sequence_generator.json_manager.ori_calculator.calculate_end_ori(
                new_entry, BLUE
            )
        )
        new_entry[RED_ATTRIBUTES][END_ORI] = (
            self.circular_sequence_generator.json_manager.ori_calculator.calculate_end_ori(
                new_entry, RED
            )
        )

        return new_entry

    def calculate_new_end_pos(
        self, previous_matching_beat: dict, previous_entry: dict
    ) -> str:
        blue_hand_rot_dir = self.hand_rot_dir_calculator.get_hand_rot_dir(
            previous_matching_beat[BLUE_ATTRIBUTES][START_LOC],
            previous_matching_beat[BLUE_ATTRIBUTES][END_LOC],
        )
        red_hand_rot_dir = self.hand_rot_dir_calculator.get_hand_rot_dir(
            previous_matching_beat[RED_ATTRIBUTES][START_LOC],
            previous_matching_beat[RED_ATTRIBUTES][END_LOC],
        )

        new_blue_end_loc = self.calculate_rotated_permuatation_new_loc(
            previous_entry[BLUE_ATTRIBUTES][END_LOC],
            blue_hand_rot_dir,
        )

        new_red_end_loc = self.calculate_rotated_permuatation_new_loc(
            previous_entry[RED_ATTRIBUTES][END_LOC],
            red_hand_rot_dir,
        )
        new_end_pos = positions_map.get((new_blue_end_loc, new_red_end_loc))
        return new_end_pos

    def get_hand_rot_dir_from_locs(self, start_loc: str, end_loc: str) -> str:
        hand_rot_dir_map = {
            (SOUTH, WEST): CLOCKWISE,
            (WEST, NORTH): CLOCKWISE,
            (NORTH, EAST): CLOCKWISE,
            (EAST, SOUTH): CLOCKWISE,
            (WEST, SOUTH): COUNTER_CLOCKWISE,
            (NORTH, WEST): COUNTER_CLOCKWISE,
            (EAST, NORTH): COUNTER_CLOCKWISE,
            (SOUTH, EAST): COUNTER_CLOCKWISE,
            (SOUTH, NORTH): DASH,
            (WEST, EAST): DASH,
            (NORTH, SOUTH): DASH,
            (EAST, WEST): DASH,
            (NORTH, NORTH): STATIC,
            (EAST, EAST): STATIC,
            (SOUTH, SOUTH): STATIC,
            (WEST, WEST): STATIC,
            (NORTHEAST, SOUTHEAST): CLOCKWISE,
            (SOUTHEAST, SOUTHWEST): CLOCKWISE,
            (SOUTHWEST, NORTHWEST): CLOCKWISE,
            (NORTHWEST, NORTHEAST): CLOCKWISE,
            (NORTHEAST, NORTHWEST): COUNTER_CLOCKWISE,
            (NORTHWEST, SOUTHWEST): COUNTER_CLOCKWISE,
            (SOUTHWEST, SOUTHEAST): COUNTER_CLOCKWISE,
            (SOUTHEAST, NORTHEAST): COUNTER_CLOCKWISE,
            (NORTHEAST, SOUTHWEST): DASH,
            (SOUTHEAST, NORTHWEST): DASH,
            (SOUTHWEST, NORTHEAST): DASH,
            (NORTHWEST, SOUTHEAST): DASH,
            (NORTHEAST, NORTHEAST): STATIC,
            (SOUTHEAST, SOUTHEAST): STATIC,
            (SOUTHWEST, SOUTHWEST): STATIC,
            (NORTHWEST, NORTHWEST): STATIC,
        }
        return hand_rot_dir_map.get((start_loc, end_loc))

    def get_previous_matching_beat(
        self,
        sequence: list[dict],
        beat_number: int,
        final_length: int,
        halved_or_quartered: str,
    ) -> dict:
        index_map = self.get_index_map(halved_or_quartered, final_length)
        return sequence[index_map[beat_number]]

    def get_index_map(self, halved_or_quartered: str, length: int) -> dict[int, int]:
        if halved_or_quartered == "quartered":
            return {
                i: i - (length // 4) + 1 for i in range((length // 4) + 1, length + 1)
            }
        elif halved_or_quartered == "halved":
            return {
                i: i - (length // 2) + 1 for i in range((length // 2) + 1, length + 1)
            }
        else:
            raise ValueError(
                "Invalid permutation type. Expected 'quartered' or 'halved'."
            )

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
        beat[BLUE_ATTRIBUTES], beat[RED_ATTRIBUTES] = (
            beat[RED_ATTRIBUTES],
            beat[BLUE_ATTRIBUTES],
        )
        return beat

    def create_new_attributes(
        self,
        previous_attributes: dict,
        previous_matching_beat_attributes: dict,
    ) -> dict:
        return {
            MOTION_TYPE: previous_matching_beat_attributes[MOTION_TYPE],
            START_ORI: previous_attributes[END_ORI],
            PROP_ROT_DIR: previous_matching_beat_attributes[PROP_ROT_DIR],
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
