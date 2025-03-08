import pytest
from enums.letter.letter import Letter
from letter_determination.core import LetterDeterminer
from letter_determination.services.attribute_manager import AttributeManager
from letter_determination.services.motion_comparator import MotionComparator
from letter_determination.services.json_handler import LetterDeterminationJsonHandler
from data.constants import (
    ANTI,
    BEAT,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DIRECTION,
    DURATION,
    EAST,
    END_POS,
    FLOAT,
    LETTER,
    NO_ROT,
    NORTH,
    PRO,
    SOUTH,
    ALPHA1,
    ALPHA3,
    SPLIT,
    LETTER_TYPE,
    START_POS,
    TIMING,
    WEST,
    SAME,
    BLUE_ATTRS,
    RED_ATTRS,
    START_LOC,
    END_LOC,
    MOTION_TYPE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PROP_ROT_DIR,
)


@pytest.fixture
def mock_json_handler():
    class MockJsonHandler(LetterDeterminationJsonHandler):
        def __init__(self):
            self.loader_saver = MockLoaderSaver()
            self.updater = MockUpdater()

        def get_json_prefloat_motion_type(self, index: int, color: str):
            return ANTI

        def get_json_prefloat_prop_rot_dir(self, index: int, color: str):
            return COUNTER_CLOCKWISE

        def update_prefloat_motion_type(self, index: int, color: str, motion_type: str):
            pass

        def update_prefloat_prop_rot_dir(self, index: int, color: str, direction: str):
            pass

    class MockLoaderSaver:
        def get_json_prefloat_motion_type(self, index, color):
            return ANTI

        def get_json_prefloat_prop_rot_dir(self, index, color):
            return COUNTER_CLOCKWISE

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
            {
                BEAT: 1,
                LETTER: "B",
                LETTER_TYPE: LETTER_TYPE,
                DURATION: 1,
                START_POS: ALPHA1,
                END_POS: ALPHA3,
                TIMING: SPLIT,
                DIRECTION: SAME,
                BLUE_ATTRS: {
                    MOTION_TYPE: ANTI,
                    START_LOC: SOUTH,
                    END_LOC: WEST,
                    PROP_ROT_DIR: COUNTER_CLOCKWISE,
                },
                RED_ATTRS: {
                    MOTION_TYPE: FLOAT,
                    START_LOC: NORTH,
                    END_LOC: EAST,
                    PROP_ROT_DIR: NO_ROT,
                    PREFLOAT_MOTION_TYPE: ANTI,
                    PREFLOAT_PROP_ROT_DIR: COUNTER_CLOCKWISE,
                },
            }
        ],
        Letter.A: [
            {
                BEAT: 1,
                LETTER: "A",
                LETTER_TYPE: LETTER_TYPE,
                DURATION: 1,
                START_POS: ALPHA1,
                END_POS: ALPHA3,
                TIMING: SPLIT,
                DIRECTION: SAME,
                BLUE_ATTRS: {
                    MOTION_TYPE: PRO,
                    START_LOC: SOUTH,
                    END_LOC: WEST,
                    PROP_ROT_DIR: CLOCKWISE,
                },
                RED_ATTRS: {
                    MOTION_TYPE: FLOAT,
                    START_LOC: NORTH,
                    END_LOC: EAST,
                    PROP_ROT_DIR: NO_ROT,
                    PREFLOAT_MOTION_TYPE: PRO,
                    PREFLOAT_PROP_ROT_DIR: CLOCKWISE,
                },
            }
        ],
    }
    return LetterDeterminer(dataset, mock_json_handler)


def test_letter_determiner_case_c_to_b(letter_determiner: LetterDeterminer):
    pictograph = {
        BEAT: 1,
        LETTER: "C",
        LETTER_TYPE: LETTER_TYPE,
        DURATION: 1,
        START_POS: ALPHA1,
        END_POS: ALPHA3,
        TIMING: SPLIT,
        DIRECTION: SAME,
        BLUE_ATTRS: {
            MOTION_TYPE: ANTI,
            START_LOC: SOUTH,
            END_LOC: WEST,
            PROP_ROT_DIR: COUNTER_CLOCKWISE,
        },
        RED_ATTRS: {
            MOTION_TYPE: FLOAT,
            START_LOC: NORTH,
            END_LOC: EAST,
            PROP_ROT_DIR: NO_ROT,
            PREFLOAT_MOTION_TYPE: ANTI,
            PREFLOAT_PROP_ROT_DIR: COUNTER_CLOCKWISE,
        },
    }
    result = letter_determiner.determine_letter(pictograph)
    assert result == Letter.B, f"Expected 'B', got {result}"


def test_letter_determiner_case_c_to_a(letter_determiner: LetterDeterminer):
    pictograph = {
        BEAT: 1,
        LETTER: "C",
        LETTER_TYPE: LETTER_TYPE,
        DURATION: 1,
        START_POS: ALPHA1,
        END_POS: ALPHA3,
        TIMING: SPLIT,
        DIRECTION: SAME,
        BLUE_ATTRS: {
            MOTION_TYPE: PRO,
            START_LOC: SOUTH,
            END_LOC: WEST,
            PROP_ROT_DIR: CLOCKWISE,
        },
        RED_ATTRS: {
            MOTION_TYPE: FLOAT,
            START_LOC: NORTH,
            END_LOC: EAST,
            PROP_ROT_DIR: NO_ROT,
            PREFLOAT_MOTION_TYPE: ANTI,
            PREFLOAT_PROP_ROT_DIR: COUNTER_CLOCKWISE,
        },
    }
    letter = letter_determiner.determine_letter(pictograph)
    assert letter == Letter.A, f"Expected 'A', got {letter}"


def test_attribute_manager_sync_attributes(mock_json_handler):
    attribute_manager = AttributeManager(mock_json_handler)

    pictograph_data = {
        BEAT: 1,
        BLUE_ATTRS: {
            MOTION_TYPE: FLOAT,
            START_LOC: NORTH,
            END_LOC: EAST,
            PROP_ROT_DIR: NO_ROT,
        },
        RED_ATTRS: {
            MOTION_TYPE: PRO,
            START_LOC: SOUTH,
            END_LOC: WEST,
            PROP_ROT_DIR: CLOCKWISE,
        },
    }

    attribute_manager.sync_attributes(pictograph_data)

    assert (
        pictograph_data[BLUE_ATTRS][PREFLOAT_MOTION_TYPE] == PRO
    ), "Prefloat motion type not correctly updated"
    assert (
        pictograph_data[BLUE_ATTRS][PREFLOAT_PROP_ROT_DIR] == CLOCKWISE
    ), "Prefloat prop rotation not correctly updated"


def test_motion_comparator(mock_json_handler):
    comparator = MotionComparator({})

    motion_1 = {
        START_LOC: NORTH,
        END_LOC: EAST,
        MOTION_TYPE: FLOAT,
        PROP_ROT_DIR: NO_ROT,
        PREFLOAT_MOTION_TYPE: ANTI,
        PREFLOAT_PROP_ROT_DIR: COUNTER_CLOCKWISE,
    }

    motion_2 = {
        START_LOC: NORTH,
        END_LOC: EAST,
        MOTION_TYPE: FLOAT,
        PROP_ROT_DIR: NO_ROT,
        PREFLOAT_MOTION_TYPE: ANTI,
        PREFLOAT_PROP_ROT_DIR: COUNTER_CLOCKWISE,
    }

    assert comparator.compare_motion_to_example(motion_1, motion_2) is True, "Motion comparison failed"
