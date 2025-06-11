from typing import TYPE_CHECKING

from data.constants import BLUE_ATTRS, RED_ATTRS, LETTER, MOTION_TYPE, PROP_ROT_DIR


if TYPE_CHECKING:
    from .sequence_properties_manager import SequencePropertiesManager


class StrictRotatedCAPChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager

    def check(self) -> bool:
        sequence = self.manager.sequence
        letter_sequence = [entry[LETTER] for entry in sequence[1:] if LETTER in entry]
        unique_letters = set(letter_sequence)
        for letter in unique_letters:
            occurrences = [i for i, x in enumerate(letter_sequence) if x == letter]
            if len(occurrences) > 1:
                for i in range(1, len(occurrences)):
                    prev = sequence[occurrences[i - 1]]
                    curr = sequence[occurrences[i]]
                    if not self._is_strict_rotated_CAP(prev, curr):
                        return False
        return True

    def _is_strict_rotated_CAP(self, prev, curr) -> bool:
        return (
            prev[BLUE_ATTRS][MOTION_TYPE] == curr[BLUE_ATTRS][MOTION_TYPE]
            and prev[BLUE_ATTRS][PROP_ROT_DIR] == curr[BLUE_ATTRS][PROP_ROT_DIR]
            and prev[RED_ATTRS][MOTION_TYPE] == curr[RED_ATTRS][MOTION_TYPE]
            and prev[RED_ATTRS][PROP_ROT_DIR] == curr[RED_ATTRS][PROP_ROT_DIR]
        )
