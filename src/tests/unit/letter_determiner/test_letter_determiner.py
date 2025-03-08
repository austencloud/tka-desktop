import pytest
from enums.letter.letter import Letter
from letter_determination.core import LetterDeterminer
from .dataclasses import LetterDeterminationCase

@pytest.mark.parametrize(
    "test_case",
    [
        LetterDeterminationCase(
            name="Dual Float Motion - Expected Letter B",
            pictograph_data={
                "beat": 1,
                "letter": None,  # Initially unknown
                "letter_type": "dual_float",
                "duration": 1,
                "start_pos": "north",
                "end_pos": "east",
                "timing": "even",
                "direction": "same",
                "blue_attributes": {
                    "motion_type": "float",
                    "start_ori": "up",
                    "prop_rot_dir": "cw",
                    "start_loc": "south",
                    "end_loc": "west",
                    "turns": 1,
                    "end_ori": "up",
                    "prefloat_motion_type": None,
                    "prefloat_prop_rot_dir": None,
                },
                "red_attributes": {
                    "motion_type": "float",
                    "start_ori": "up",
                    "prop_rot_dir": "ccw",
                    "start_loc": "north",
                    "end_loc": "east",
                    "turns": 1,
                    "end_ori": "up",
                    "prefloat_motion_type": None,
                    "prefloat_prop_rot_dir": None,
                },
            },
            expected=Letter.B,
            description="Both motions are FLOAT, expected Letter B.",
        )
    ],
)
def test_letter_determiner(letter_determiner: LetterDeterminer, test_case):
    """
    Given a pictograph data instance,
    When the letter determiner is used,
    Then it should return the expected Letter.
    """
    result = letter_determiner.determine_letter(test_case.pictograph_data)

    assert result.letter == test_case.expected, (
        f"Expected {test_case.expected}, but got {result.letter}. "
        f"Test case: {test_case.description}"
    )
