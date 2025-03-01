from data.constants import PREFLOAT_MOTION_TYPE, PREFLOAT_PROP_ROT_DIR
from objects.motion.motion_state import MotionState


def test_motion_state_updates_with_partial_data():
    state = MotionState(
        color=BLUE, motion_type=PRO, turns=0, start_loc="n", end_loc=None
    )

    new_data = {
        "color": RED,
        TURNS: 1.5,
        END_LOC: "s",
    }

    state.update_motion_state(new_data)

    assert state.color == RED
    assert state.turns == 1.5
    assert state.end_loc == "s"
    assert state.motion_type == PRO
    assert state.start_loc == "n"


def test_motion_state_handles_prefloat_logic():
    state = MotionState(motion_type=PRO)

    new_data = {
        PREFLOAT_MOTION_TYPE: ANTI,
        PREFLOAT_PROP_ROT_DIR: "cw",
    }

    state.update_motion_state(new_data)

    assert state.prefloat_motion_type == ANTI
    assert state.prefloat_prop_rot_dir == "cw"


def test_motion_state_doesnt_set_prefloat_for_non_shift():
    state = MotionState(motion_type=DASH)

    new_data = {
        PREFLOAT_MOTION_TYPE: "something_else",
        PREFLOAT_PROP_ROT_DIR: "some_dir",
    }

    state.update_motion_state(new_data)
    assert state.prefloat_motion_type == None
    assert state.prefloat_prop_rot_dir == None
