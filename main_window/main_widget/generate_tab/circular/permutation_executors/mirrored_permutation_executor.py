from typing import TYPE_CHECKING

from data.constants import BLUE_ATTRIBUTES, RED_ATTRIBUTES
from .permutation_executor_base import PermutationExecutor
from PyQt6.QtWidgets import QApplication
from data.locations import vertical_loc_mirror_map, horizontal_loc_mirror_map

if TYPE_CHECKING:
    from ..circular_sequence_builder import CircularSequenceBuilder


class MirroredPermutationExecutor(PermutationExecutor):
    def __init__(
        self,
        circular_sequence_generator: "CircularSequenceBuilder",
        color_swap_second_half: bool,
    ):
        self.circular_sequence_generator = circular_sequence_generator
        self.color_swap_second_half = color_swap_second_half

    def create_permutations(self, sequence: list[dict], vertical_or_horizontal: str):
        if not self.can_perform_mirrored_permutation(sequence):
            return
        self.vertical_or_horizontal = vertical_or_horizontal
        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]
        new_entries = []
        next_beat_number = last_entry["beat"] + 1
        entries_to_add = self.determine_how_many_entries_to_add(sequence_length)
        final_intended_sequence_length = sequence_length + entries_to_add

        for i in range(sequence_length + 2):
            if i in [0, 1]:
                continue
            next_pictograph = self.create_new_mirrored_permutation_entry(
                sequence,
                last_entry,
                next_beat_number + i - 2,
                self.color_swap_second_half,
                vertical_or_horizontal,
                final_intended_sequence_length,
            )
            new_entries.append(next_pictograph)
            sequence.append(next_pictograph)

            sequence_workbench = self.circular_sequence_generator.sequence_workbench
            sequence_workbench.sequence_beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                next_pictograph, override_grow_sequence=True, update_word=False
            )
            self.validation_engine.validate_last_pictograph()
            QApplication.processEvents()

            last_entry = next_pictograph

    def determine_how_many_entries_to_add(self, sequence_length: int) -> int:
        return sequence_length

    def can_perform_mirrored_permutation(self, sequence: list[dict]) -> bool:
        return sequence[1]["end_pos"] == sequence[-1]["end_pos"]

    def create_new_mirrored_permutation_entry(
        self,
        sequence,
        previous_entry,
        beat_number: int,
        color_swap_second_half: bool,
        vertical_or_horizontal: str,
        final_intended_sequence_length: int,
    ) -> dict:

        previous_matching_beat = self.get_previous_matching_beat(
            sequence,
            beat_number,
            final_intended_sequence_length,
        )

        new_entry = {
            "beat": beat_number,
            "letter": previous_matching_beat["letter"],
            "start_pos": previous_entry["end_pos"],
            "end_pos": self.get_mirrored_position(
                previous_matching_beat, vertical_or_horizontal
            ),
            "timing": previous_matching_beat["timing"],
            "direction": previous_matching_beat["direction"],
            BLUE_ATTRIBUTES: self.create_new_attributes(
                previous_entry[BLUE_ATTRIBUTES],
                previous_matching_beat[BLUE_ATTRIBUTES],
            ),
            RED_ATTRIBUTES: self.create_new_attributes(
                previous_entry[RED_ATTRIBUTES],
                previous_matching_beat[RED_ATTRIBUTES],
            ),
        }

        new_entry[BLUE_ATTRIBUTES]["end_ori"] = (
            self.circular_sequence_generator.json_manager.ori_calculator.calculate_end_ori(
                new_entry, "blue"
            )
        )
        new_entry[RED_ATTRIBUTES]["end_ori"] = (
            self.circular_sequence_generator.json_manager.ori_calculator.calculate_end_ori(
                new_entry, "red"
            )
        )
        if color_swap_second_half:
            new_entry[BLUE_ATTRIBUTES], new_entry[RED_ATTRIBUTES] = (
                new_entry[RED_ATTRIBUTES],
                new_entry[BLUE_ATTRIBUTES],
            )
        return new_entry

    def get_previous_matching_beat(
        self,
        sequence: list[dict],
        beat_number: int,
        final_intended_sequence_length: int,
    ) -> dict:
        index_map = self.get_index_map(final_intended_sequence_length)
        return sequence[index_map[beat_number]]

    def get_index_map(self, length: int) -> dict[int, int]:
        return {i: i - (length // 2) + 1 for i in range((length // 2) + 1, length + 1)}

    def get_mirrored_position(
        self, previous_matching_beat, vertical_or_horizontal
    ) -> str:
        mirrored_positions = {
            "vertical": {
                "alpha1": "alpha1",
                "alpha3": "alpha7",
                "alpha5": "alpha5",
                "alpha7": "alpha3",
                "beta1": "beta1",
                "beta3": "beta7",
                "beta5": "beta5",
                "beta7": "beta3",
                "gamma1": "gamma9",
                "gamma3": "gamma15",
                "gamma5": "gamma13",
                "gamma7": "gamma11",
                "gamma9": "gamma1",
                "gamma11": "gamma7",
                "gamma13": "gamma5",
                "gamma15": "gamma3",
            },
            "horizontal": {
                "alpha1": "alpha5",
                "alpha3": "alpha3",
                "alpha5": "alpha1",
                "alpha7": "alpha7",
                "beta1": "beta5",
                "beta3": "beta3",
                "beta5": "beta1",
                "beta7": "beta7",
                "gamma1": "gamma13",
                "gamma3": "gamma11",
                "gamma5": "gamma9",
                "gamma7": "gamma15",
                "gamma9": "gamma5",
                "gamma11": "gamma3",
                "gamma13": "gamma1",
                "gamma15": "gamma7",
            },
        }
        return mirrored_positions[vertical_or_horizontal][
            previous_matching_beat["end_pos"]
        ]

    def get_mirrored_prop_rot_dir(self, prop_rot_dir: str) -> str:
        if prop_rot_dir == "cw":
            return "ccw"
        elif prop_rot_dir == "ccw":
            return "cw"
        elif prop_rot_dir == "no_rot":
            return "no_rot"

    def create_new_attributes(
        self,
        previous_entry_attributes: dict,
        previous_matching_beat_attributes: dict,
    ) -> dict:
        new_entry_attributes = {
            "motion_type": previous_matching_beat_attributes["motion_type"],
            "start_ori": previous_entry_attributes["end_ori"],
            "prop_rot_dir": self.get_mirrored_prop_rot_dir(
                previous_matching_beat_attributes["prop_rot_dir"]
            ),
            "start_loc": previous_entry_attributes["end_loc"],
            "end_loc": self.calculate_mirrored_permuatation_new_loc(
                previous_matching_beat_attributes["end_loc"]
            ),
            "turns": previous_matching_beat_attributes["turns"],
        }

        return new_entry_attributes

    def calculate_mirrored_permuatation_new_loc(
        self, previous_matching_beat_end_loc: str
    ) -> str:
        if self.vertical_or_horizontal == "vertical":
            return self.get_vertical_mirrored_location(previous_matching_beat_end_loc)
        elif self.vertical_or_horizontal == "horizontal":
            return self.get_horizontal_mirrored_location(previous_matching_beat_end_loc)

    def get_mirrored_rotation(self, rotation: str) -> str:
        if rotation == "cw":
            return "ccw"
        elif rotation == "ccw":
            return "cw"
        return rotation

    def get_vertical_mirrored_location(self, location: str) -> str:
        return vertical_loc_mirror_map.get(location, location)

    def get_horizontal_mirrored_location(self, location: str) -> str:
        return horizontal_loc_mirror_map.get(location, location)
