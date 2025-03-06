from typing import TYPE_CHECKING
from data.constants import *
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from ..circular_sequence_builder import CircularSequenceBuilder


class CAPExecutor:
    """Base class for all CAP executors, handling shared logic."""

    def __init__(self, circular_sequence_generator: "CircularSequenceBuilder"):
        self.circular_sequence_generator = circular_sequence_generator

    def create_CAPs(self, sequence: list[dict]):
        """Must be implemented by subclasses."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    def determine_how_many_entries_to_add(self, sequence_length: int) -> int:
        """Determines how many entries need to be added for full circularity."""
        return sequence_length  # Default: equal length

    def get_previous_matching_beat(
        self, sequence: list[dict], beat_number: int, final_length: int
    ) -> dict:
        """Fetch the previous matching beat using an index map."""
        index_map = self.get_index_map(final_length)
        return sequence[index_map[beat_number]]

    def get_index_map(self, length: int) -> dict[int, int]:
        """Generate index mapping for retrieving mirrored/rotated beats."""
        return {i: i - (length // 2) + 1 for i in range((length // 2) + 1, length + 1)}

    def swap_colors(self, beat: dict) -> dict:
        """Swaps blue and red attributes if needed."""
        beat[BLUE_ATTRS], beat[RED_ATTRS] = beat[RED_ATTRS], beat[BLUE_ATTRS]
        return beat

    def create_new_attributes(
        self, previous_entry_attributes: dict, previous_matching_beat_attributes: dict
    ) -> dict:
        """Creates new attributes for a transformed beat."""
        return {
            MOTION_TYPE: previous_matching_beat_attributes[MOTION_TYPE],
            START_ORI: previous_entry_attributes[END_ORI],
            PROP_ROT_DIR: previous_matching_beat_attributes[PROP_ROT_DIR],
            START_LOC: previous_entry_attributes[END_LOC],
            END_LOC: self.calculate_new_end_loc(
                previous_entry_attributes[END_LOC], previous_matching_beat_attributes
            ),
            TURNS: previous_matching_beat_attributes[TURNS],
        }

    def calculate_new_end_loc(self, start_loc: str, beat_attributes: dict) -> str:
        """Handles how the end location is mapped during transformation."""
        raise NotImplementedError("Subclasses must implement calculate_new_end_loc().")
