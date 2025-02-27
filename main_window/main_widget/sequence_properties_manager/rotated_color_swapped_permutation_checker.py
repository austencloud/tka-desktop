from typing import TYPE_CHECKING

from data.constants import END_POS


if TYPE_CHECKING:
    from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )


class RotatedColorSwappedPermutationChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager
        self.rotation_maps = self._initialize_rotation_maps()

    def _initialize_rotation_maps(self) -> dict[str, dict[str, dict[str, str]]]:
        return {
            "2_repetitions": {
                "1st-2nd": {
                    "alpha1": "alpha1",
                    "alpha3": "alpha3",
                    "alpha5": "alpha5",
                    "alpha7": "alpha7",
                    "beta1": "beta5",
                    "beta3": "beta7",
                    "beta5": "beta1",
                    "beta7": "beta3",
                    "gamma1": "gamma11",
                    "gamma3": "gamma13",
                    "gamma5": "gamma15",
                    "gamma7": "gamma11",
                    "gamma9": "gamma7",
                    "gamma11": "gamma1",
                    "gamma13": "gamma3",
                    "gamma15": "gamma5",
                },
            },
            "4_repetitions": {
                "1st-4th": {
                    "alpha1": "alpha7",
                    "alpha3": "alpha1",
                    "alpha5": "alpha3",
                    "alpha7": "alpha5",
                    "beta1": "beta7",
                    "beta3": "beta1",
                    "beta5": "beta3",
                    "beta7": "beta5",
                    "gamma1": "gamma7",
                    "gamma3": "gamma1",
                    "gamma5": "gamma3",
                    "gamma7": "gamma5",
                    "gamma9": "gamma15",
                    "gamma11": "gamma9",
                    "gamma13": "gamma11",
                    "gamma15": "gamma13",
                },
                "1st-3rd": {
                    "alpha1": "alpha5",
                    "alpha3": "alpha7",
                    "alpha5": "alpha1",
                    "alpha7": "alpha3",
                    "beta1": "beta5",
                    "beta3": "beta7",
                    "beta5": "beta1",
                    "beta7": "beta3",
                    "gamma1": "gamma5",
                    "gamma3": "gamma7",
                    "gamma5": "gamma1",
                    "gamma7": "gamma3",
                    "gamma9": "gamma13",
                    "gamma11": "gamma15",
                    "gamma13": "gamma9",
                    "gamma15": "gamma11",
                },
                "1st-2nd": {
                    "alpha1": "alpha3",
                    "alpha3": "alpha5",
                    "alpha5": "alpha7",
                    "alpha7": "alpha1",
                    "beta1": "beta3",
                    "beta3": "beta5",
                    "beta5": "beta7",
                    "beta7": "beta1",
                    "gamma1": "gamma3",
                    "gamma3": "gamma5",
                    "gamma5": "gamma7",
                    "gamma7": "gamma1",
                    "gamma9": "gamma11",
                    "gamma11": "gamma13",
                    "gamma13": "gamma15",
                    "gamma15": "gamma9",
                },
            },
        }

    def check(self) -> str:
        sequence = self.manager.sequence[1:]  # Skip metadata
        length = len(sequence)

        beats_per_repetition = self._determine_beats_per_repetition(sequence)
        if not beats_per_repetition:
            return False

        # Determine the number of repetitions
        repetitions = length // beats_per_repetition

        if repetitions == 2:
            return self._check_two_repetitions(sequence, beats_per_repetition)
        elif repetitions == 4:
            return self._check_four_repetitions(sequence, beats_per_repetition)

        return False

    def _determine_beats_per_repetition(self, sequence) -> int:
        sequence = [entry for entry in sequence if "is_placeholder" not in entry]
        length = len(sequence)

        # Extract the word pattern
        word_pattern = "".join([entry[LETTER] for entry in sequence])
        expected_word_pattern = word_pattern[
            : length // 4
        ]  # Expecting 4 repetitions of the pattern

        # Check if the pattern repeats four times
        if word_pattern == expected_word_pattern * 4:
            return length // 4

        # Fall back to checking for 2 repetitions
        if word_pattern == word_pattern[: length // 2] * 2:
            return length // 2

        return None  # No valid repetition pattern found

    def _check_two_repetitions(self, sequence, beats_per_repetition) -> str:
        first_part = sequence[:beats_per_repetition]
        second_part = sequence[beats_per_repetition : 2 * beats_per_repetition]

        if self._matches_rotated_and_color_swapped(
            first_part, second_part, "2_repetitions", "1st-2nd"
        ):
            return "First-Second Match"

        return False

    def _check_four_repetitions(self, sequence, beats_per_repetition) -> str:
        first_quarter = sequence[:beats_per_repetition]
        second_quarter = sequence[beats_per_repetition : 2 * beats_per_repetition]
        third_quarter = sequence[2 * beats_per_repetition : 3 * beats_per_repetition]
        fourth_quarter = sequence[3 * beats_per_repetition :]

        match_results = []
        if self._matches_rotated_and_color_swapped(
            first_quarter, fourth_quarter, "4_repetitions", "1st-4th"
        ):
            match_results.append("First-Fourth Match")
        if self._matches_rotated_and_color_swapped(
            first_quarter, third_quarter, "4_repetitions", "1st-3rd"
        ):
            match_results.append("First-Third Match")
        if self._matches_rotated_and_color_swapped(
            first_quarter, second_quarter, "4_repetitions", "1st-2nd"
        ):
            match_results.append("First-Second Match")

        # Prioritize matches
        if "First-Fourth Match" in match_results:
            return "First-Fourth Match"
        elif "First-Third Match" in match_results:
            return "First-Third Match"
        elif "First-Second Match" in match_results:
            return "First-Second Match"

        return False

    def _matches_rotated_and_color_swapped(
        self,
        first_part: list[dict],
        second_part: list[dict],
        repetition_type: str,
        match_type: str,
    ) -> bool:
        rotation_map = self.rotation_maps[repetition_type][match_type]
        if len(first_part) != len(second_part):
            return False

        for i in range(len(first_part)):
            if not self._is_rotated_and_color_swapped(
                first_part[i], second_part[i], rotation_map
            ):
                return False
        return True

    def _is_rotated_and_color_swapped(
        self, first_entry: dict, second_entry: dict, rotation_map: dict[str, str]
    ) -> bool:
        first_entry_rotated_pos = rotation_map.get(first_entry[END_POS])

        # Check if positions match after rotation and color swap
        if first_entry_rotated_pos != second_entry[END_POS]:
            return False

        return True
