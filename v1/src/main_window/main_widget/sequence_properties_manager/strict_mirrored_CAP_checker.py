from tkinter import HORIZONTAL
from typing import TYPE_CHECKING
from data.constants import END_POS, VERTICAL
from data.positions_maps import mirrored_positions

if TYPE_CHECKING:
    from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )


class StrictMirroredCAPChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager

    def check(self) -> bool:
        sequence = self.manager.sequence[1:]
        length = len(sequence)
        if length < 4:
            return False
        if length % 2 != 0:
            return False

        half_length = length // 2
        first_half = sequence[0:half_length]
        second_half = sequence[half_length:]

        for i in range(half_length):
            first_entry = first_half[i]
            second_entry = second_half[half_length - i - 2]

            if not self._is_mirrored(first_entry, second_entry):
                return False

        return True

    def _is_mirrored(self, first_entry, second_entry) -> bool:
        mirrored_vertical = self._get_mirrored_position(first_entry[END_POS], VERTICAL)
        mirrored_horizontal = self._get_mirrored_position(
            first_entry[END_POS], HORIZONTAL
        )

        return second_entry[END_POS] in [
            mirrored_vertical,
            mirrored_horizontal,
        ]

    def _get_mirrored_position(self, position, direction):
        return mirrored_positions[direction][position]
