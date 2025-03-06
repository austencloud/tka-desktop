from typing import TYPE_CHECKING
from data.quartered_CAPs import quartered_CAPs
from data.halved_CAPs import halved_CAPs
from data.constants import (
    BEAT,
    BLUE,
    BLUE_ATTRS,
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
    RED_ATTRS,
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
from PyQt6.QtWidgets import QApplication
from main_window.main_widget.generate_tab.circular.CAP_executors.CAP_type import CAPType
from objects.motion.managers.handpath_calculator import HandpathCalculator
from .CAP_executor import CAPExecutor
from data.positions_map import positions_map

if TYPE_CHECKING:
    from ..circular_sequence_builder import CircularSequenceBuilder


class StrictRotatedCAPExecutor(CAPExecutor):
    CAP_TYPE = CAPType.STRICT_ROTATED

    def __init__(self, circular_sequence_generator: "CircularSequenceBuilder"):
        super().__init__(circular_sequence_generator)
        self.hand_rot_dir_calculator = HandpathCalculator()

    def create_CAPs(self, sequence: list[dict]):
        """Creates rotated CAPs in a circular sequence."""
        start_position_entry = (
            sequence.pop(0) if SEQUENCE_START_POSITION in sequence[0] else None
        )
        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]
        new_entries = []
        next_beat_number = last_entry[BEAT] + 1
        cap_type = self.get_halved_or_quartered()

        sequence_workbench = (
            self.circular_sequence_generator.main_widget.sequence_workbench
        )
        entries_to_add = self.determine_how_many_entries_to_add(sequence_length)

        for _ in range(entries_to_add):
            next_pictograph = self.create_new_CAP_entry(
                sequence,
                last_entry,
                next_beat_number,
                sequence_length + entries_to_add,
                cap_type,
            )
            new_entries.append(next_pictograph)
            sequence.append(next_pictograph)

            sequence_workbench.beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
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
        """Determines how many beats to add based on CAP type."""
        if self.is_quartered_CAP():
            return sequence_length * 3
        elif self.is_halved_CAP():
            return sequence_length
        return 0

    def is_quartered_CAP(self) -> bool:
        """Checks if the sequence qualifies for a quartered CAP."""
        sequence = (
            self.circular_sequence_generator.json_manager.loader_saver.load_current_sequence()
        )
        return (sequence[1][END_POS], sequence[-1][END_POS]) in quartered_CAPs

    def is_halved_CAP(self) -> bool:
        """Checks if the sequence qualifies for a halved CAP."""
        sequence = (
            self.circular_sequence_generator.json_manager.loader_saver.load_current_sequence()
        )
        return (sequence[1][END_POS], sequence[-1][END_POS]) in halved_CAPs

    def get_halved_or_quartered(self) -> str:
        """Returns the CAP type as a string."""
        if self.is_halved_CAP():
            return "halved"
        elif self.is_quartered_CAP():
            return "quartered"
        return ""

    def create_new_CAP_entry(
        self,
        sequence,
        previous_entry,
        beat_number: int,
        final_intended_sequence_length: int,
        cap_type: str,
    ) -> dict:
        """Generates a new rotated CAP entry with updated attributes."""
        previous_matching_beat = self.get_previous_matching_beat(
            sequence, beat_number, final_intended_sequence_length, cap_type
        )

        new_entry = {
            BEAT: beat_number,
            LETTER: previous_matching_beat[LETTER],
            START_POS: previous_entry[END_POS],
            END_POS: self.calculate_new_end_pos(previous_matching_beat, previous_entry),
            TIMING: previous_matching_beat[TIMING],
            DIRECTION: previous_matching_beat[DIRECTION],
            BLUE_ATTRS: self.create_new_attributes(
                previous_entry[BLUE_ATTRS], previous_matching_beat[BLUE_ATTRS]
            ),
            RED_ATTRS: self.create_new_attributes(
                previous_entry[RED_ATTRS], previous_matching_beat[RED_ATTRS]
            ),
        }

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
        """Determines the new end position based on rotation direction."""
        blue_hand_rot_dir = self.hand_rot_dir_calculator.get_hand_rot_dir(
            previous_matching_beat[BLUE_ATTRS][START_LOC],
            previous_matching_beat[BLUE_ATTRS][END_LOC],
        )
        red_hand_rot_dir = self.hand_rot_dir_calculator.get_hand_rot_dir(
            previous_matching_beat[RED_ATTRS][START_LOC],
            previous_matching_beat[RED_ATTRS][END_LOC],
        )

        new_blue_end_loc = self.calculate_rotated_permutation_new_loc(
            previous_entry[BLUE_ATTRS][END_LOC], blue_hand_rot_dir
        )
        new_red_end_loc = self.calculate_rotated_permutation_new_loc(
            previous_entry[RED_ATTRS][END_LOC], red_hand_rot_dir
        )

        return positions_map.get((new_blue_end_loc, new_red_end_loc))

    def calculate_rotated_permutation_new_loc(
        self, start_loc: str, hand_rot_dir: str
    ) -> str:
        """Computes the new location based on rotational mappings."""
        rotation_maps = {
            CW_HANDPATH: {
                SOUTH: WEST,
                WEST: NORTH,
                NORTH: EAST,
                EAST: SOUTH,
                NORTHEAST: SOUTHEAST,
                SOUTHEAST: SOUTHWEST,
                SOUTHWEST: NORTHWEST,
                NORTHWEST: NORTHEAST,
            },
            CCW_HANDPATH: {
                SOUTH: EAST,
                EAST: NORTH,
                NORTH: WEST,
                WEST: SOUTH,
                NORTHEAST: NORTHWEST,
                NORTHWEST: SOUTHWEST,
                SOUTHWEST: SOUTHEAST,
                SOUTHEAST: NORTHEAST,
            },
            DASH: {
                SOUTH: NORTH,
                NORTH: SOUTH,
                WEST: EAST,
                EAST: WEST,
                NORTHEAST: SOUTHWEST,
                SOUTHEAST: NORTHWEST,
                SOUTHWEST: NORTHEAST,
                NORTHWEST: SOUTHEAST,
            },
            STATIC: {
                SOUTH: SOUTH,
                NORTH: NORTH,
                WEST: WEST,
                EAST: EAST,
                NORTHEAST: NORTHEAST,
                SOUTHEAST: SOUTHEAST,
                SOUTHWEST: SOUTHWEST,
                NORTHWEST: NORTHWEST,
            },
        }

        return rotation_maps.get(hand_rot_dir, {}).get(start_loc, start_loc)

    def get_previous_matching_beat(
        self, sequence: list[dict], beat_number: int, final_length: int, cap_type: str
    ) -> dict:
        """Fetches the previous matching beat using an index map."""
        index_map = self.get_index_map(cap_type, final_length)
        return sequence[index_map[beat_number]]

    def get_index_map(self, cap_type: str, length: int) -> dict[int, int]:
        """Generates index mappings for quartered or halved sequences."""
        step = length // 4 if cap_type == "quartered" else length // 2
        return {i: i - step + 1 for i in range(step + 1, length + 1)}

    def create_new_attributes(
        self, previous_attributes: dict, previous_matching_beat_attributes: dict
    ) -> dict:
        """Creates new attributes based on the previous matching beat."""
        return {
            MOTION_TYPE: previous_matching_beat_attributes[MOTION_TYPE],
            START_ORI: previous_attributes[END_ORI],
            PROP_ROT_DIR: previous_matching_beat_attributes[PROP_ROT_DIR],
            START_LOC: previous_attributes[END_LOC],
            END_LOC: self.calculate_rotated_permutation_new_loc(
                previous_attributes[END_LOC],
                previous_matching_beat_attributes[PROP_ROT_DIR],
            ),
            TURNS: previous_matching_beat_attributes[TURNS],
        }
