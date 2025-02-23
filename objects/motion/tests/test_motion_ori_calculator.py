import pytest

from data.constants import (
    ANTI,
    CLOCK,
    CLOCKWISE,
    COUNTER,
    COUNTER_CLOCKWISE,
    FLOAT,
    IN,
    NORTH,
    OUT,
    WEST,
)
from objects.motion.motion import Motion
from objects.motion.motion_ori_calculator import MotionOriCalculator


@pytest.mark.parametrize(
    "start_ori, prop_rot_dir, turns, expected_end_ori",
    [
        (IN, CLOCKWISE, 0.5, CLOCK),
        (IN, COUNTER_CLOCKWISE, 0.5, COUNTER),
        (OUT, CLOCKWISE, 0.5, COUNTER),
        (OUT, COUNTER_CLOCKWISE, 0.5, CLOCK),
        (IN, CLOCKWISE, 1.5, COUNTER),
        (IN, COUNTER_CLOCKWISE, 1.5, CLOCK),
        (OUT, CLOCKWISE, 1.5, CLOCK),
        (OUT, COUNTER_CLOCKWISE, 1.5, COUNTER),
    ],
)
def test_anti_half_turn_parametrized(start_ori, prop_rot_dir, turns, expected_end_ori):
    motion = Motion(pictograph=None, motion_data={})
    motion.state.motion_type = ANTI
    motion.state.start_ori = start_ori
    motion.state.prop_rot_dir = prop_rot_dir
    motion.state.turns = turns

    ori_calc = MotionOriCalculator(motion)

    end_ori = ori_calc.get_end_ori()

    assert end_ori == expected_end_ori, (
        f"For anti half-turn (start_ori={start_ori}, rot_dir={prop_rot_dir}, "
        f"turns={turns}), expected {expected_end_ori} but got {end_ori}"
    )



@pytest.mark.parametrize(
    "start_loc, end_loc, start_ori, expected_end_ori",
    [
        (NORTH, WEST, IN, COUNTER),
        (NORTH, WEST, OUT, CLOCK),
        (WEST, NORTH, IN, CLOCK),
        (WEST, NORTH, OUT, COUNTER),
    ],
)
def test_float_scenario_parametrized(start_loc, end_loc, start_ori, expected_end_ori):
    motion = Motion(pictograph=None, motion_data={})
    motion.state.motion_type = FLOAT
    motion.state.start_loc = start_loc
    motion.state.end_loc = end_loc
    motion.state.start_ori = start_ori

    ori_calc = MotionOriCalculator(motion)
    end_ori = ori_calc.get_end_ori()

    assert (
        end_ori == expected_end_ori
    ), f"For float from {start_ori}, expected {expected_end_ori} but got {end_ori}"
