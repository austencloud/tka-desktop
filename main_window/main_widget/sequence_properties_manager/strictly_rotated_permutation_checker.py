from typing import TYPE_CHECKING


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
            prev["blue_attributes"]["motion_type"]
            == curr["blue_attributes"]["motion_type"]
            and prev["blue_attributes"]["prop_rot_dir"]
            == curr["blue_attributes"]["prop_rot_dir"]
            and prev["red_attributes"]["motion_type"]
            == curr["red_attributes"]["motion_type"]
            and prev["red_attributes"]["prop_rot_dir"]
            == curr["red_attributes"]["prop_rot_dir"]
        )
