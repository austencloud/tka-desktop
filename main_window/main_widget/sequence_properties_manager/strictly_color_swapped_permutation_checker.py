from typing import TYPE_CHECKING

from data.constants import BLUE_ATTRIBUTES, RED_ATTRIBUTES


if TYPE_CHECKING:
    from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )


class StrictlyColorSwappedPermutationChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager

    def check(self) -> bool:
        sequence = self.manager.sequence[1:]  # Skip metadata
        length = len(sequence)
        if length % 2 != 0:
            return False

        half_length = length // 2
        first_half = sequence[:half_length]
        second_half = sequence[half_length:]

        for i in range(half_length):
            first_entry = first_half[i]
            second_entry = second_half[i]

            if not self._is_color_swapped(first_entry, second_entry):
                return False

        return True

    def _is_color_swapped(self, first_entry, second_entry) -> bool:
        # Strictly checks if the roles are swapped without any mirroring
        return (
            first_entry[BLUE_ATTRIBUTES] == second_entry[RED_ATTRIBUTES]
            and first_entry[RED_ATTRIBUTES] == second_entry[BLUE_ATTRIBUTES]
        )
