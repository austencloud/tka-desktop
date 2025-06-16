from data.constants import *
from main_window.main_widget.generate_tab.circular.CAP_type import CAPType
from .CAP_executor import CAPExecutor
from PyQt6.QtWidgets import QApplication
from enums.letter.complementary_letter_getter import ComplementaryLetterGetter


class StrictComplementaryCAPExecutor(CAPExecutor):

    def __init__(self, circular_sequence_generator):
        super().__init__(circular_sequence_generator)
        self.letter_determiner = (
            circular_sequence_generator.main_widget.letter_determiner
        )

    def create_CAPs(self, sequence: list[dict]):
        """Creates complementary CAPs for a circular sequence."""

        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]
        next_beat_number = last_entry[BEAT] + 1
        final_intended_sequence_length = (
            sequence_length + self.determine_how_many_entries_to_add(sequence_length)
        )

        for i in range(2, sequence_length + 2):  # Skip first two beats
            next_pictograph = self.create_new_CAP_entry(
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
                update_word=True,
                update_image_export_preview=False,
            )
            QApplication.processEvents()

    def can_perform_CAP(self, sequence: list[dict]) -> bool:
        """Ensures that the sequence can be complementary."""
        ends_at_start = sequence[-1][END_POS] == sequence[1][END_POS]
        return ends_at_start

    def create_new_CAP_entry(
        self,
        sequence,
        previous_entry,
        beat_number: int,
        final_intended_sequence_length: int,
    ) -> dict:
        """Generates a new complementary pictograph entry by flipping attributes."""
        previous_matching_beat = self.get_previous_matching_beat(
            sequence, beat_number, final_intended_sequence_length
        )

        new_entry = {
            BEAT: beat_number,
            LETTER: ComplementaryLetterGetter().get_complimentary_letter(
                previous_matching_beat[LETTER]
            ),
            START_POS: previous_entry[END_POS],
            END_POS: previous_matching_beat[END_POS],
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

        return new_entry

    def create_new_attributes(
        self, previous_entry_attributes: dict, previous_matching_beat_attributes: dict
    ) -> dict:
        """Creates complementary attributes by flipping relevant properties."""
        motion_type = self.get_other_motion_type(
            previous_matching_beat_attributes[MOTION_TYPE]
        )
        prop_rot_dir = self.get_other_prop_rot_dir(
            previous_matching_beat_attributes[PROP_ROT_DIR]
        )

        new_entry_attributes = {
            MOTION_TYPE: motion_type,
            START_ORI: previous_entry_attributes[END_ORI],
            PROP_ROT_DIR: prop_rot_dir,
            START_LOC: previous_entry_attributes[END_LOC],
            END_LOC: previous_matching_beat_attributes[END_LOC],
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

    def get_other_motion_type(self, motion_type: str) -> str:
        """Returns the other motion type."""
        if motion_type == PRO:
            return ANTI
        elif motion_type == ANTI:
            return PRO
        else:
            return motion_type

    def get_other_prop_rot_dir(self, prop_rot_dir: str) -> str:
        """Returns the other prop rot dir."""
        if prop_rot_dir == CLOCKWISE:
            return COUNTER_CLOCKWISE
        elif prop_rot_dir == COUNTER_CLOCKWISE:
            return CLOCKWISE
        else:
            return prop_rot_dir
