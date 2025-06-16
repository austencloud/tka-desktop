from typing import TYPE_CHECKING

from data.constants import *


if TYPE_CHECKING:
    from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )


class RotatedSwappedCAPChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager
        self.rotation_maps = self._initialize_rotation_maps()

    def _initialize_rotation_maps(self) -> dict[str, dict[str, dict[str, str]]]:
        return {
            "2_repetitions": {
                "1st-2nd": {
                    ALPHA1: ALPHA1,
                    ALPHA3: ALPHA3,
                    ALPHA5: ALPHA5,
                    ALPHA7: ALPHA7,
                    BETA1: BETA5,
                    BETA3: BETA7,
                    BETA5: BETA1,
                    BETA7: BETA3,
                    GAMMA1: GAMMA11,
                    GAMMA3: GAMMA13,
                    GAMMA5: GAMMA15,
                    GAMMA7: GAMMA11,
                    GAMMA9: GAMMA7,
                    GAMMA11: GAMMA1,
                    GAMMA13: GAMMA3,
                    GAMMA15: GAMMA5,
                },
            },
            "4_repetitions": {
                "1st-4th": {
                    ALPHA1: ALPHA7,
                    ALPHA3: ALPHA1,
                    ALPHA5: ALPHA3,
                    ALPHA7: ALPHA5,
                    BETA1: BETA7,
                    BETA3: BETA1,
                    BETA5: BETA3,
                    BETA7: BETA5,
                    GAMMA1: GAMMA7,
                    GAMMA3: GAMMA1,
                    GAMMA5: GAMMA3,
                    GAMMA7: GAMMA5,
                    GAMMA9: GAMMA15,
                    GAMMA11: GAMMA9,
                    GAMMA13: GAMMA11,
                    GAMMA15: GAMMA13,
                },
                "1st-3rd": {
                    ALPHA1: ALPHA5,
                    ALPHA3: ALPHA7,
                    ALPHA5: ALPHA1,
                    ALPHA7: ALPHA3,
                    BETA1: BETA5,
                    BETA3: BETA7,
                    BETA5: BETA1,
                    BETA7: BETA3,
                    GAMMA1: GAMMA5,
                    GAMMA3: GAMMA7,
                    GAMMA5: GAMMA1,
                    GAMMA7: GAMMA3,
                    GAMMA9: GAMMA13,
                    GAMMA11: GAMMA15,
                    GAMMA13: GAMMA9,
                    GAMMA15: GAMMA11,
                },
                "1st-2nd": {
                    ALPHA1: ALPHA3,
                    ALPHA3: ALPHA5,
                    ALPHA5: ALPHA7,
                    ALPHA7: ALPHA1,
                    BETA1: BETA3,
                    BETA3: BETA5,
                    BETA5: BETA7,
                    BETA7: BETA1,
                    GAMMA1: GAMMA3,
                    GAMMA3: GAMMA5,
                    GAMMA5: GAMMA7,
                    GAMMA7: GAMMA1,
                    GAMMA9: GAMMA11,
                    GAMMA11: GAMMA13,
                    GAMMA13: GAMMA15,
                    GAMMA15: GAMMA9,
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

        if self._matches_rotated_and_swapped(
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
        if self._matches_rotated_and_swapped(
            first_quarter, fourth_quarter, "4_repetitions", "1st-4th"
        ):
            match_results.append("First-Fourth Match")
        if self._matches_rotated_and_swapped(
            first_quarter, third_quarter, "4_repetitions", "1st-3rd"
        ):
            match_results.append("First-Third Match")
        if self._matches_rotated_and_swapped(
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

    def _matches_rotated_and_swapped(
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
            if not self._is_rotated_and_swapped(
                first_part[i], second_part[i], rotation_map
            ):
                return False
        return True

    def _is_rotated_and_swapped(
        self, first_entry: dict, second_entry: dict, rotation_map: dict[str, str]
    ) -> bool:
        first_entry_rotated_pos = rotation_map.get(first_entry[END_POS])

        # Check if positions match after rotation and color swap
        if first_entry_rotated_pos != second_entry[END_POS]:
            return False

        return True
