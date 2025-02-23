import pytest

from objects.motion.motion_state import MotionState



def test_motion_state_updates_with_partial_data():
    state = MotionState(
        color="blue",
        motion_type="pro",
        turns=0,
        start_loc="n",
        end_loc=None
    )

    new_data = {
        "color": "red",
        "turns": 1.5,
        "end_loc": "s",
    }

    state.update_motion_state(new_data)

    assert state.color == "red"
    assert state.turns == 1.5
    assert state.end_loc == "s"
    assert state.motion_type == "pro"
    assert state.start_loc == "n"

def test_motion_state_handles_prefloat_logic():
    state = MotionState(motion_type="pro")

    new_data = {
        "prefloat_motion_type": "anti",
        "prefloat_prop_rot_dir": "something",
    }

    state.update_motion_state(new_data)

    assert state.prefloat_motion_type == "anti"
    assert state.prefloat_prop_rot_dir == "something"

def test_motion_state_doesnt_set_prefloat_for_non_shift():
    state = MotionState(motion_type="dash")

    new_data = {
        "prefloat_motion_type": "something_else",
        "prefloat_prop_rot_dir": "some_dir",
    }

    state.update_motion_state(new_data)
    assert state.prefloat_motion_type == None
    assert state.prefloat_prop_rot_dir == None
