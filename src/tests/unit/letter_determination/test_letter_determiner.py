import pytest
from enums.letter.letter import Letter
from letter_determination.core import LetterDeterminer
from letter_determination.models.pictograph import dict
from letter_determination.models.motion import (
    dict,
    str,
    str,
)
from letter_determination.services.json_handler import LetterDeterminationJsonHandler
from data.constants import (
    CLOCK,
    EAST,
    NORTH,
    SOUTH,
    ALPHA1,
    ALPHA3,
    SPLIT,
    IN,
    OUT,
    LETTER_TYPE,
    WEST,
    SAME,
)


@pytest.fixture
def mock_json_handler():
    class MockJsonHandler(LetterDeterminationJsonHandler):
        def __init__(self):
            self.loader_saver = MockLoaderSaver()
            self.updater = MockUpdater()

        def get_json_prefloat_motion_type(self, index: int, color: str):
            return str.ANTI  # ✅ Return Enum, not string

        def get_json_prefloat_prop_rot_dir(self, index: int, color: str):
            return str.COUNTER_CLOCKWISE  # ✅ Return Enum, not string

        def update_prefloat_motion_type(self, index: int, color: str, motion_type: str):
            pass

        def update_prefloat_prop_rot_dir(self, index: int, color: str, direction: str):
            pass

    class MockLoaderSaver:
        def get_json_prefloat_motion_type(self, index, color):
            return str.ANTI  # ✅ Return Enum

        def get_json_prefloat_prop_rot_dir(self, index, color):
            return str.COUNTER_CLOCKWISE  # ✅ Return Enum

    class MockUpdater:
        class strUpdater:
            def update_json_prefloat_motion_type(self, index, color, motion_type):
                pass

        class PropRotDirUpdater:
            def update_prefloat_prop_rot_dir_in_json(self, index, color, direction):
                pass

        def __init__(self):
            self.motion_type_updater = self.strUpdater()
            self.prop_rot_dir_updater = self.PropRotDirUpdater()

    return MockJsonHandler()


@pytest.fixture
def letter_determiner(mock_json_handler):
    dataset = {
        Letter.B: [
            dict(
                beat=1,
                letter="C",
                letter_type=LETTER_TYPE,
                duration=1,
                start_pos=ALPHA1,
                end_pos=ALPHA3,
                timing=SPLIT,
                direction=SAME,
                blue_attributes=dict(
                    motion_type=str.ANTI,
                    start_ori=IN,
                    prop_rot_dir=str.COUNTER_CLOCKWISE,
                    start_loc=SOUTH,
                    end_loc=WEST,
                    turns=0,
                    end_ori=OUT,
                ),
                red_attributes=dict(
                    motion_type=FLOAT,
                    start_ori=IN,
                    prop_rot_dir=str.NONE,
                    start_loc=NORTH,
                    end_loc=EAST,
                    turns="fl",
                    end_ori=CLOCK,
                ),
            )
        ],
        Letter.A: [
            dict(
                beat=1,
                letter="C",
                letter_type=LETTER_TYPE,
                duration=1,
                start_pos=ALPHA1,
                end_pos=ALPHA3,
                timing=SPLIT,
                direction=SAME,
                blue_attributes=dict(
                    motion_type=str.PRO,
                    start_ori=IN,
                    prop_rot_dir=str.CLOCKWISE,
                    start_loc=SOUTH,
                    end_loc=WEST,
                    turns=0,
                    end_ori=IN,
                ),
                red_attributes=dict(
                    motion_type=FLOAT,
                    start_ori=IN,
                    prop_rot_dir=str.NONE,
                    start_loc=NORTH,
                    end_loc=EAST,
                    turns="fl",
                    end_ori=CLOCK,
                ),
            )
        ],
    }
    return LetterDeterminer(dataset, mock_json_handler)


def test_letter_determiner_case_c_to_b(letter_determiner):
    pictograph = dict(
        beat=1,
        letter="C",
        letter_type=LETTER_TYPE,
        duration=1,
        start_pos=ALPHA1,
        end_pos=ALPHA3,
        timing=SPLIT,
        direction=SAME,
        blue_attributes=dict(
            motion_type=str.ANTI,
            start_ori=IN,
            prop_rot_dir=str.COUNTER_CLOCKWISE,
            start_loc=SOUTH,
            end_loc=WEST,
            turns=0,
            end_ori=OUT,
        ),
        red_attributes=dict(
            motion_type=FLOAT,
            start_ori=IN,
            prop_rot_dir=str.NONE,
            start_loc=NORTH,
            end_loc=EAST,
            turns="fl",
            end_ori=CLOCK,
            prefloat_motion_type=str.ANTI,  # ✅ Ensure Prefloat Motion Type is included
            prefloat_prop_rot_dir=str.COUNTER_CLOCKWISE,  # ✅ Ensure Prefloat Prop Rotation is included
        ),
    )
    result = letter_determiner.determine_letter(pictograph)
    assert result.letter == Letter.B, "Letter determination failed for case C -> B"


def test_letter_determiner_case_c_to_a(letter_determiner):
    pictograph = dict(
        beat=1,
        letter="C",
        letter_type=LETTER_TYPE,
        duration=1,
        start_pos=ALPHA1,
        end_pos=ALPHA3,
        timing=SPLIT,
        direction=SAME,
        blue_attributes=dict(
            motion_type=str.PRO,
            start_ori=IN,
            prop_rot_dir=str.CLOCKWISE,
            start_loc=SOUTH,
            end_loc=WEST,
            turns=0,
            end_ori=IN,
        ),
        red_attributes=dict(
            motion_type=FLOAT,
            start_ori=IN,
            prop_rot_dir=str.NONE,
            start_loc=NORTH,
            end_loc=EAST,
            turns="fl",
            end_ori=CLOCK,
            prefloat_motion_type=str.ANTI,  # ✅ Ensure Prefloat Motion Type is included
            prefloat_prop_rot_dir=str.COUNTER_CLOCKWISE,  # ✅ Ensure Prefloat Prop Rotation is included
        ),
    )
    result = letter_determiner.determine_letter(pictograph)
    assert result.letter == Letter.A, "Letter determination failed for case C -> A"
