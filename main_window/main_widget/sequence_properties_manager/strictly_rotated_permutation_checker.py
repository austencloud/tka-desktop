from typing import TYPE_CHECKING

from data.constants import BLUE_ATTRIBUTES, RED_ATTRIBUTES


if TYPE_CHECKING:
    from .sequence_properties_manager import SequencePropertiesManager


class StrictlyRotatedPermutationChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager

    def check(self) -> bool:
        sequence = self.manager.sequence
        letter_sequence = [
            entry["letter"] for entry in sequence[1:] if "letter" in entry
        ]
        unique_letters = set(letter_sequence)
        for letter in unique_letters:
            occurrences = [i for i, x in enumerate(letter_sequence) if x == letter]
            if len(occurrences) > 1:
                for i in range(1, len(occurrences)):
                    prev = sequence[occurrences[i - 1]]
                    curr = sequence[occurrences[i]]
                    if not self._is_strictly_rotated_permutation(prev, curr):
                        return False
        return True

    def _is_strictly_rotated_permutation(self, prev, curr) -> bool:
        return (
            prev[BLUE_ATTRIBUTES]["motion_type"] == curr[BLUE_ATTRIBUTES]["motion_type"]
            and prev[BLUE_ATTRIBUTES]["prop_rot_dir"]
            == curr[BLUE_ATTRIBUTES]["prop_rot_dir"]
            and prev[RED_ATTRIBUTES]["motion_type"]
            == curr[RED_ATTRIBUTES]["motion_type"]
            and prev[RED_ATTRIBUTES]["prop_rot_dir"]
            == curr[RED_ATTRIBUTES]["prop_rot_dir"]
        )
