import pytest
from enums.letter.letter import Letter
from letter_determination.core import LetterDeterminer
from letter_determination.models.pictograph import PictographData
from letter_determination.models.motion import (
    MotionAttributes,
    MotionType,
    RotationDirection,
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
            return MotionType.ANTI  # ✅ Return Enum, not string

        def get_json_prefloat_prop_rot_dir(self, index: int, color: str):
            return RotationDirection.COUNTER_CLOCKWISE  # ✅ Return Enum, not string

        def update_prefloat_motion_type(self, index: int, color: str, motion_type: MotionType):
            pass

        def update_prefloat_prop_rot_dir(self, index: int, color: str, direction: RotationDirection):
            pass

    class MockLoaderSaver:
        def get_json_prefloat_motion_type(self, index, color):
            return MotionType.ANTI  # ✅ Return Enum

        def get_json_prefloat_prop_rot_dir(self, index, color):
            return RotationDirection.COUNTER_CLOCKWISE  # ✅ Return Enum

    class MockUpdater:
        class MotionTypeUpdater:
            def update_json_prefloat_motion_type(self, index, color, motion_type):
                pass

        class PropRotDirUpdater:
            def update_prefloat_prop_rot_dir_in_json(self, index, color, direction):
                pass

        def __init__(self):
            self.motion_type_updater = self.MotionTypeUpdater()
            self.prop_rot_dir_updater = self.PropRotDirUpdater()

    return MockJsonHandler()


@pytest.fixture
def letter_determiner(mock_json_handler):
    dataset = {
        Letter.B: [
            PictographData(
                beat=1,
                letter="C",
                letter_type=LETTER_TYPE,
                duration=1,
                start_pos=ALPHA1,
                end_pos=ALPHA3,
                timing=SPLIT,
                direction=SAME,
                blue_attributes=MotionAttributes(
                    motion_type=MotionType.ANTI,
                    start_ori=IN,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=SOUTH,
                    end_loc=WEST,
                    turns=0,
                    end_ori=OUT,
                ),
                red_attributes=MotionAttributes(
                    motion_type=MotionType.FLOAT,
                    start_ori=IN,
                    prop_rot_dir=RotationDirection.NONE,
                    start_loc=NORTH,
                    end_loc=EAST,
                    turns="fl",
                    end_ori=CLOCK,
                ),
            )
        ],
        Letter.A: [
            PictographData(
                beat=1,
                letter="C",
                letter_type=LETTER_TYPE,
                duration=1,
                start_pos=ALPHA1,
                end_pos=ALPHA3,
                timing=SPLIT,
                direction=SAME,
                blue_attributes=MotionAttributes(
                    motion_type=MotionType.PRO,
                    start_ori=IN,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=SOUTH,
                    end_loc=WEST,
                    turns=0,
                    end_ori=IN,
                ),
                red_attributes=MotionAttributes(
                    motion_type=MotionType.FLOAT,
                    start_ori=IN,
                    prop_rot_dir=RotationDirection.NONE,
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
    pictograph = PictographData(
        beat=1,
        letter="C",
        letter_type=LETTER_TYPE,
        duration=1,
        start_pos=ALPHA1,
        end_pos=ALPHA3,
        timing=SPLIT,
        direction=SAME,
        blue_attributes=MotionAttributes(
            motion_type=MotionType.ANTI,
            start_ori=IN,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=SOUTH,
            end_loc=WEST,
            turns=0,
            end_ori=OUT,
        ),
        red_attributes=MotionAttributes(
            motion_type=MotionType.FLOAT,
            start_ori=IN,
            prop_rot_dir=RotationDirection.NONE,
            start_loc=NORTH,
            end_loc=EAST,
            turns="fl",
            end_ori=CLOCK,
            prefloat_motion_type=MotionType.ANTI,  # ✅ Ensure Prefloat Motion Type is included
            prefloat_prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,  # ✅ Ensure Prefloat Prop Rotation is included
        ),
    )
    result = letter_determiner.determine_letter(pictograph)
    assert result.letter == Letter.B, "Letter determination failed for case C -> B"


def test_letter_determiner_case_c_to_a(letter_determiner):
    pictograph = PictographData(
        beat=1,
        letter="C",
        letter_type=LETTER_TYPE,
        duration=1,
        start_pos=ALPHA1,
        end_pos=ALPHA3,
        timing=SPLIT,
        direction=SAME,
        blue_attributes=MotionAttributes(
            motion_type=MotionType.PRO,
            start_ori=IN,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=SOUTH,
            end_loc=WEST,
            turns=0,
            end_ori=IN,
        ),
        red_attributes=MotionAttributes(
            motion_type=MotionType.FLOAT,
            start_ori=IN,
            prop_rot_dir=RotationDirection.NONE,
            start_loc=NORTH,
            end_loc=EAST,
            turns="fl",
            end_ori=CLOCK,
            prefloat_motion_type=MotionType.ANTI,  # ✅ Ensure Prefloat Motion Type is included
            prefloat_prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,  # ✅ Ensure Prefloat Prop Rotation is included
        ),
    )
    result = letter_determiner.determine_letter(pictograph)
    assert result.letter == Letter.A, "Letter determination failed for case C -> A"
