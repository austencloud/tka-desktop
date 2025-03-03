import pytest
from data.constants import EAST, NORTH, WEST
from objects.motion.handpath_calculator import HandpathCalculator


@pytest.fixture
def calculator() -> HandpathCalculator:
    """Fixture to initialize HandpathCalculator before tests."""
    return HandpathCalculator()


@pytest.mark.parametrize(
    "start_loc, end_loc", HandpathCalculator().hand_rot_dir_map.keys()
)
def test_handpath_calculator(calculator: HandpathCalculator, start_loc, end_loc):
    """Ensures that valid pairs return correct hand rotation paths."""
    expected_handpath = calculator.hand_rot_dir_map[(start_loc, end_loc)]
    result = calculator.get_hand_rot_dir(start_loc, end_loc)
    assert (
        result == expected_handpath
    ), f"Expected {expected_handpath}, but got {result}."


@pytest.mark.parametrize(
    "start_loc, end_loc",
    [
        ("INVALID", EAST),
        (NORTH, "INVALID"),
        (None, WEST),
        (EAST, None),
    ],
)
def test_handpath_calculator_invalid(
    calculator: HandpathCalculator, start_loc, end_loc
):
    """Ensures that invalid inputs return the default 'NO HAND ROTATION FOUND'."""
    result = calculator.get_hand_rot_dir(start_loc, end_loc)
    assert result == "NO HAND ROTATION FOUND", f"Expected failure but got {result}."
