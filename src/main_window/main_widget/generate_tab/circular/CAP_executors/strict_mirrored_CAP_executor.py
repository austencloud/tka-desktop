from data.constants import *
from .CAP_executor_base import CAPExecutor
from PyQt6.QtWidgets import QApplication
from data.locations import vertical_loc_mirror_map, horizontal_loc_mirror_map


class StrictMirroredCAPExecutor(CAPExecutor):
    def __init__(self, circular_sequence_generator, color_swap_second_half: bool):
        super().__init__(circular_sequence_generator)
        self.color_swap_second_half = color_swap_second_half

    def create_CAPs(self, sequence: list[dict], vertical_or_horizontal: str):
        """Creates mirrored CAPs for a circular sequence."""
        if not self.can_perform_mirrored_CAP(sequence):
            return

        self.vertical_or_horizontal = vertical_or_horizontal
        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]
        next_beat_number = last_entry[BEAT] + 1
        final_intended_sequence_length = (
            sequence_length + self.determine_how_many_entries_to_add(sequence_length)
        )

        for i in range(2, sequence_length + 2):  # Skip first two beats
            next_pictograph = self.create_new_mirrored_CAP_entry(
                sequence,
                last_entry,
                next_beat_number + i - 2,
                final_intended_sequence_length,
            )
            sequence.append(next_pictograph)
            last_entry = next_pictograph

            # Add to UI
            sequence_workbench = self.circular_sequence_generator.sequence_workbench
            sequence_workbench.beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                next_pictograph,
                override_grow_sequence=True,
                update_word=False,
                update_image_export_preview=False,
            )
            QApplication.processEvents()

    def create_new_mirrored_CAP_entry(
        self,
        sequence,
        previous_entry,
        beat_number: int,
        final_intended_sequence_length: int,
    ) -> dict:
        """Generates a new mirrored pictograph entry by flipping attributes."""
        previous_matching_beat = self.get_previous_matching_beat(
            sequence, beat_number, final_intended_sequence_length
        )

        new_entry = {
            BEAT: beat_number,
            LETTER: previous_matching_beat[LETTER],
            START_POS: previous_entry[END_POS],
            END_POS: self.get_mirrored_position(previous_matching_beat),
            TIMING: previous_matching_beat[TIMING],
            DIRECTION: previous_matching_beat[DIRECTION],
            BLUE_ATTRS: self.create_new_attributes(
                previous_entry[BLUE_ATTRS], previous_matching_beat[BLUE_ATTRS]
            ),
            RED_ATTRS: self.create_new_attributes(
                previous_entry[RED_ATTRS], previous_matching_beat[RED_ATTRS]
            ),
        }

        # Ensure orientations are set properly
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

        # Swap colors at the midpoint of the sequence
        if (
            self.color_swap_second_half
            and beat_number >= final_intended_sequence_length // 2
        ):
            new_entry = self.swap_colors(new_entry)

        return new_entry

    def can_perform_mirrored_CAP(self, sequence: list[dict]) -> bool:
        """Ensures that the sequence can be mirrored."""
        return sequence[1][END_POS] == sequence[-1][END_POS]

    def get_mirrored_position(self, previous_matching_beat) -> str:
        """Handles mirroring based on the grid mode."""
        mirrored_positions = {
            VERTICAL: vertical_loc_mirror_map,
            HORIZONTAL: horizontal_loc_mirror_map,
        }
        return mirrored_positions[self.vertical_or_horizontal].get(
            previous_matching_beat[END_POS],
            previous_matching_beat[END_POS],  # Fallback to original position
        )

    def create_new_attributes(
        self, previous_entry_attributes: dict, previous_matching_beat_attributes: dict
    ) -> dict:
        """Creates mirrored attributes by flipping relevant properties."""
        motion_type = previous_matching_beat_attributes[MOTION_TYPE]
        prop_rot_dir = self.get_mirrored_prop_rot_dir(
            previous_matching_beat_attributes[PROP_ROT_DIR]
        )

        new_entry_attributes = {
            MOTION_TYPE: motion_type,
            START_ORI: previous_entry_attributes[END_ORI],
            PROP_ROT_DIR: prop_rot_dir,
            START_LOC: previous_entry_attributes[END_LOC],
            END_LOC: self.calculate_mirrored_CAP_new_loc(
                previous_matching_beat_attributes[END_LOC]
            ),
            TURNS: previous_matching_beat_attributes[TURNS],
        }

        # Handle floating states
        if previous_matching_beat_attributes.get(PREFLOAT_MOTION_TYPE):
            new_entry_attributes[PREFLOAT_MOTION_TYPE] = (
                previous_matching_beat_attributes[PREFLOAT_MOTION_TYPE]
            )
            new_entry_attributes[PREFLOAT_PROP_ROT_DIR] = (
                self.get_mirrored_prop_rot_dir(
                    previous_matching_beat_attributes[PREFLOAT_PROP_ROT_DIR]
                )
            )

        return new_entry_attributes

    def get_mirrored_prop_rot_dir(self, prop_rot_dir: str) -> str:
        """Mirrors prop rotation direction."""
        if prop_rot_dir == CLOCKWISE:
            return COUNTER_CLOCKWISE
        elif prop_rot_dir == COUNTER_CLOCKWISE:
            return CLOCKWISE
        return NO_ROT

    def calculate_mirrored_CAP_new_loc(
        self, previous_matching_beat_end_loc: str
    ) -> str:
        """Finds the new mirrored location based on grid mode."""
        if self.vertical_or_horizontal == VERTICAL:
            return vertical_loc_mirror_map.get(
                previous_matching_beat_end_loc, previous_matching_beat_end_loc
            )
        elif self.vertical_or_horizontal == HORIZONTAL:
            return horizontal_loc_mirror_map.get(
                previous_matching_beat_end_loc, previous_matching_beat_end_loc
            )
        return previous_matching_beat_end_loc  # Fallback
