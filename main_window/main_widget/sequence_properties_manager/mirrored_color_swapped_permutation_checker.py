from typing import TYPE_CHECKING
from data.positions import mirrored_positions

if TYPE_CHECKING:
    from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )


class MirroredColorSwappedPermutationChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager

    def check(self) -> bool:
        sequence = self.manager.sequence[1:]  # Skip metadata
        length = len(sequence)
        if length < 4 or length % 2 != 0:
            return False

        half_length = length // 2
        first_half = sequence[:half_length]
        second_half = sequence[half_length:]

        for i in range(half_length):
            first_entry = first_half[i]
            second_entry = second_half[i]

            if not (self._is_mirrored_and_color_swapped(first_entry, second_entry)):
                return False

        return True

    def _is_mirrored_and_color_swapped(self, first_entry, second_entry) -> bool:
        mirrored_vertical = self._get_mirrored_and_colorswapped_position(
            first_entry["end_pos"], "vertical"
        )
        mirrored_horizontal = self._get_mirrored_and_colorswapped_position(
            first_entry["end_pos"], "horizontal"
        )

        return second_entry["end_pos"] in [
            mirrored_vertical,
            mirrored_horizontal,
        ]

    def _is_color_swapped(self, first_entry, second_entry) -> bool:
        return (
            first_entry["blue_attributes"] == second_entry["red_attributes"]
            and first_entry["red_attributes"] == second_entry["blue_attributes"]
        )

    def _get_mirrored_and_colorswapped_position(self, position, direction):
        return mirrored_positions[direction][position]
