
# From concatenated_letter_determiner.py


# From dual_float_letter_determiner.py
from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from .motion_comparator import MotionComparator
from .prefloat_attribute_updater import PrefloatAttributeUpdater

if TYPE_CHECKING:
    from .letter_determiner import LetterDeterminer
    from objects.motion.motion import Motion


class DualFloatLetterDeterminer:
    """Determines the letter for dual float motions."""

    def __init__(self, letter_engine: "LetterDeterminer"):
        self.main_widget = letter_engine.main_widget
        self.letters = letter_engine.letters
        self.prefloat_updater = PrefloatAttributeUpdater(self.main_widget)
        self.comparator = MotionComparator(self.main_widget)

    def determine_letter(self, motion: "Motion") -> Letter:
        """Determine the letter for dual float motions."""
        other_motion = motion.pictograph.managers.get.other_motion(motion)
        self.prefloat_updater.update_prefloat_attributes(motion, other_motion)
        return self._find_matching_letter(motion, other_motion)

    def _find_matching_letter(self, motion: "Motion", other_motion: "Motion") -> Letter:
        """Compare motion attributes to find the correct letter."""
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_to_example(
                    motion, other_motion, example
                ):
                    return letter
        return None


# From letter_determiner.py
from typing import TYPE_CHECKING, Optional
from enums.letter.letter import Letter
from data.constants import (
    BLUE,
    BLUE_ATTRS,
    RED,
    RED_ATTRS,
    MOTION_TYPE,
    FLOAT,
    PRO,
    ANTI,
)
from letter_determiner.non_hybrid_shift_letter_determiner import (
    NonHybridShiftLetterDeterminer,
)
from letter_determiner.motion_comparator import MotionComparator
from letter_determiner.prefloat_attribute_updater import PrefloatAttributeUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LetterDeterminer:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.letters = self.main_widget.pictograph_dataset
        self.comparator = MotionComparator(self.main_widget)
        self.prefloat_updater = PrefloatAttributeUpdater(self.main_widget)
        self.non_hybrid_letter_determiner = NonHybridShiftLetterDeterminer(
            self, self.comparator
        )

    def determine_letter(
        self, pictograph_data: dict, swap_prop_rot_dir: bool = False
    ) -> Optional[Letter]:
        blue_attrs = pictograph_data[BLUE_ATTRS]
        red_attrs = pictograph_data[RED_ATTRS]

        if self._is_dual_float_case(blue_attrs, red_attrs):
            letter = self._handle_dual_float_case(pictograph_data)
        else:
            letter = self._handle_hybrid_case(pictograph_data, swap_prop_rot_dir)

        # if letter == None:
        #     raise ValueError("Letter not found")

        return letter

    def _is_dual_float_case(self, blue: dict, red: dict) -> bool:
        return blue[MOTION_TYPE] == FLOAT and red[MOTION_TYPE] == FLOAT

    def _handle_dual_float_case(self, pictograph_data: dict) -> Optional[Letter]:
        self.prefloat_updater.update_prefloat_attributes(pictograph_data, BLUE, RED)
        blue_attrs = pictograph_data[BLUE_ATTRS]
        red_attrs = pictograph_data[RED_ATTRS]
        return self._find_matching_letter(blue_attrs, red_attrs)

    def _handle_hybrid_case(
        self, pictograph_data: dict, swap_prop_rot_dir: bool
    ) -> Optional[Letter]:
        blue_attrs = pictograph_data[BLUE_ATTRS]
        red_attrs = pictograph_data[RED_ATTRS]

        if (
            blue_attrs[MOTION_TYPE] in [PRO, ANTI] and red_attrs[MOTION_TYPE] == FLOAT
        ) or (
            red_attrs[MOTION_TYPE] in [PRO, ANTI] and blue_attrs[MOTION_TYPE] == FLOAT
        ):

            return self.non_hybrid_letter_determiner.determine_letter(pictograph_data)
        return self._find_matching_letter(blue_attrs, red_attrs)

    def _find_matching_letter(
        self, blue_attrs: dict, red_attrs: dict
    ) -> Optional[Letter]:
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_to_example(
                    blue_attrs, red_attrs, example
                ):
                    return letter
        return None


# From motion_comparator.py
from typing import TYPE_CHECKING
from data.constants import (
    BLUE,
    BLUE_ATTRS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    RED,
    RED_ATTRS,
    START_LOC,
    END_LOC,
    PROP_ROT_DIR,
    MOTION_TYPE,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MotionComparator:
    """Handles motion attribute comparisons for letter determination."""

    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def compare_motion_to_example(
        self, motion_attrs: dict, example_attrs: dict, color: str
    ) -> bool:
        """Compare a single motion's attributes to an example from the dataset."""
        return (
            motion_attrs[START_LOC] == example_attrs[START_LOC]
            and motion_attrs[END_LOC] == example_attrs[END_LOC]
            and self._is_prop_rot_dir_matching(motion_attrs, example_attrs, color)
            and self._is_motion_type_matching(motion_attrs, example_attrs)
        )

    def compare_dual_motion_to_example(
        self, blue_attrs: dict, red_attrs: dict, example: dict
    ) -> bool:
        """Compare two motions (dual motion case) to an example from the dataset."""
        return self.compare_motion_to_example(
            blue_attrs, example[BLUE_ATTRS], BLUE
        ) and self.compare_motion_to_example(red_attrs, example[RED_ATTRS], RED)

    def _is_prop_rot_dir_matching(
        self, motion_attrs: dict, example_attrs: dict, color: str
    ) -> bool:
        """Check if the motion's prop rotation direction matches the dataset example."""
        json_index = self._get_json_index_for_current_beat()
        stored_prop_rot_dir = (
            self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                json_index, color
            )
        )
        return (
            example_attrs[PROP_ROT_DIR] == stored_prop_rot_dir
            or example_attrs[PROP_ROT_DIR] == motion_attrs[PROP_ROT_DIR]
        )

    def _is_motion_type_matching(self, motion_attrs: dict, example_attrs: dict) -> bool:
        """Check if the motion type matches the dataset example."""
        return example_attrs[MOTION_TYPE] == motion_attrs[MOTION_TYPE] or example_attrs[
            MOTION_TYPE
        ] == motion_attrs.get(PREFLOAT_MOTION_TYPE)

    def _get_json_index_for_current_beat(self) -> int:
        """Retrieve the JSON index for the currently selected beat."""
        return (
            self.main_widget.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
            + 2
        )

    def _get_opposite_rotation_direction(self, rotation_direction: str) -> str:
        """Return the opposite prop rotation direction."""
        return COUNTER_CLOCKWISE if rotation_direction == CLOCKWISE else CLOCKWISE

    def compare_dual_motion_with_prefloat(
        self, float_attrs: dict, non_float_attrs: dict, example: dict
    ) -> bool:
        """Compare with pre-float attribute awareness."""
        is_matching_motion = (
            self._compare_float(float_attrs, non_float_attrs, example[BLUE_ATTRS])
            and self._compare_non_float(non_float_attrs, example[RED_ATTRS])
        ) or (
            self._compare_float(float_attrs, non_float_attrs, example[RED_ATTRS])
            and self._compare_non_float(non_float_attrs, example[BLUE_ATTRS])
        )
        if is_matching_motion:
            return is_matching_motion
        return False

    def _compare_float(
        self, float_attrs: dict, non_float_attrs: dict, example_attrs: dict
    ) -> bool:
        is_motion_matching = (
            float_attrs[START_LOC] == example_attrs[START_LOC]
            and float_attrs[END_LOC] == example_attrs[END_LOC]
            and (
                example_attrs[PROP_ROT_DIR]
                == self._get_opposite_rotation_direction(
                    float_attrs.get(PREFLOAT_PROP_ROT_DIR)
                )
                and (
                    example_attrs[MOTION_TYPE] == float_attrs.get(PREFLOAT_MOTION_TYPE)
                )
            )
        )

        return is_motion_matching

    def _compare_non_float(self, motion_attrs: dict, example_attrs: dict) -> bool:
        return (
            motion_attrs[START_LOC] == example_attrs[START_LOC]
            and motion_attrs[END_LOC] == example_attrs[END_LOC]
            and motion_attrs[PROP_ROT_DIR] == example_attrs[PROP_ROT_DIR]
            and motion_attrs[MOTION_TYPE] == example_attrs[MOTION_TYPE]
        )


# From non_hybrid_shift_letter_determiner.py
from math import pi
from tkinter import NO
from typing import TYPE_CHECKING, Optional
from enums.letter.letter import Letter

from data.constants import (
    ANTI,
    BLUE,
    BLUE_ATTRS,
    COLOR,
    COUNTER_CLOCKWISE,
    CLOCKWISE,
    DIRECTION,
    FLOAT,
    LETTER,
    NO_ROT,
    OPP,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
    MOTION_TYPE,
)
from letter_determiner.dual_float_letter_determiner import MotionComparator
from letter_determiner.prefloat_attribute_updater import PrefloatAttributeUpdater

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from .letter_determiner import LetterDeterminer


class NonHybridShiftLetterDeterminer:
    """
    This is for when there is one float and one shift,
    ensuring that hybrid letters (like C, F, I, or L) are not used
    when there is one float and one Pro/Anti.
    """

    def __init__(
        self, letter_determiner: "LetterDeterminer", comparator: MotionComparator
    ):
        self.main_widget = letter_determiner.main_widget
        self.letters = letter_determiner.letters
        self.comparator = comparator
        self.prefloat_updater = PrefloatAttributeUpdater(self.main_widget)

    def determine_letter(self, pictograph_data: dict) -> Optional[Letter]:
        """Determine the letter while handling pre-float attributes."""
        blue_attrs, red_attrs = pictograph_data[BLUE_ATTRS], pictograph_data[RED_ATTRS]
        print(pictograph_data[LETTER])
        if blue_attrs[MOTION_TYPE] == FLOAT and red_attrs[MOTION_TYPE] in [PRO, ANTI]:
            self._update_prefloat_attributes(
                pictograph_data, blue_attrs, red_attrs, BLUE
            )
            return self._find_matching_letter(blue_attrs, red_attrs)
        elif red_attrs[MOTION_TYPE] == FLOAT and blue_attrs[MOTION_TYPE] in [PRO, ANTI]:
            self._update_prefloat_attributes(
                pictograph_data, red_attrs, blue_attrs, RED
            )
            return self._find_matching_letter(red_attrs, blue_attrs)
        return None

    def _update_prefloat_attributes(
        self,
        pictograph_data: dict,
        float_attrs: dict,
        non_float_attrs: dict,
        float_color: str,
    ) -> None:
        """Update pre-float attributes in both pictograph data and JSON."""
        non_float_color = RED if float_color == BLUE else BLUE
        json_index = self._get_json_index_for_current_beat()

        float_attrs[PREFLOAT_MOTION_TYPE] = non_float_attrs[MOTION_TYPE]
        self.prefloat_updater.update_json_prefloat_motion_type(
            json_index, float_color, non_float_attrs[MOTION_TYPE]
        )

        if PROP_ROT_DIR in float_attrs or non_float_attrs[MOTION_TYPE] in [PRO, ANTI]:
            prop_rot_dir = self._get_prop_rot_dir(
                float_attrs, non_float_attrs, non_float_color, pictograph_data
            )


            float_attrs[PREFLOAT_PROP_ROT_DIR] = prop_rot_dir
            self.prefloat_updater.update_prefloat_prop_rot_dir_in_json(
                json_index, float_color, prop_rot_dir
            )

    def _find_matching_letter(
        self, float_attrs: dict, shift_attrs: dict
    ) -> Optional[Letter]:
        """Find a matching letter with pre-float aware comparison."""
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_with_prefloat(
                    float_attrs, shift_attrs, example
                ):
                    return letter
        return None

    def _get_json_index_for_current_beat(self) -> int:
        """Calculate the JSON index for the currently selected beat."""
        return (
            self.main_widget.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
            + 2
        )

    def _get_opposite_rotation_direction(self, rotation_direction: str) -> str:
        """Return the opposite prop rotation direction."""
        # return COUNTER_CLOCKWISE if rotation_direction == CLOCKWISE else CLOCKWISE
        if rotation_direction == CLOCKWISE:
            return COUNTER_CLOCKWISE
        elif rotation_direction == COUNTER_CLOCKWISE:
            return CLOCKWISE
        else:
            raise ValueError(f"Invalid rotation direction: {rotation_direction}")

    def _get_prop_rot_dir(
        self,
        float_attrs: dict,
        non_float_attrs: dict,
        non_float_color: str,
        pictograph_data,
    ) -> str:
        """Retrieve the prop rotation direction from JSON."""
        prop_rot_dir = float_attrs[PROP_ROT_DIR]

        if prop_rot_dir == NO_ROT:
            prefloat_prop_rot_dir = float_attrs.get(PREFLOAT_PROP_ROT_DIR)
            if prefloat_prop_rot_dir:
                prop_rot_dir = self._get_opposite_rotation_direction(prefloat_prop_rot_dir)
            else:
                raise ValueError(
                    f"Prop Rot Dir not found in {non_float_color} attributes"
                )

        elif pictograph_data.get(DIRECTION) == OPP:
            prop_rot_dir = self._get_opposite_rotation_direction(prop_rot_dir)

        elif non_float_attrs[MOTION_TYPE] in [PRO, ANTI]:
            prop_rot_dir = non_float_attrs.get(PROP_ROT_DIR)
            if not prop_rot_dir:
                raise ValueError(
                    f"Prop Rot Dir not found in {non_float_color} attributes"
                )
            if pictograph_data.get(DIRECTION) == OPP:
                prop_rot_dir = self._get_opposite_rotation_direction(prop_rot_dir)
        return prop_rot_dir


# From prefloat_attribute_updater.py
from typing import TYPE_CHECKING
from data.constants import (
    COUNTER_CLOCKWISE,
    CLOCKWISE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class PrefloatAttributeUpdater:
    """Handles updating pre-float attributes in the JSON."""

    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def update_prefloat_attributes(
        self, pictograph_data: dict, color: str, other_color: str
    ) -> None:
        """Update pre-float motion attributes in JSON."""
        json_index = self._get_json_index_for_current_beat()

        self.main_widget.json_manager.updater.motion_type_updater.update_json_prefloat_motion_type(
            json_index,
            color,
            pictograph_data[other_color + "_attributes"].get(PREFLOAT_MOTION_TYPE),
        )

        prefloat_prop_rot_dir = self._get_prefloat_prop_rot_dir(json_index, color)
        pictograph_data[color + "_attributes"][
            PREFLOAT_PROP_ROT_DIR
        ] = prefloat_prop_rot_dir
        self.main_widget.json_manager.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            json_index, color, prefloat_prop_rot_dir
        )

    def _get_json_index_for_current_beat(self) -> int:
        """Retrieve the JSON index for the currently selected beat."""
        return (
            self.main_widget.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
            + 2
        )

    def _get_prefloat_prop_rot_dir(self, json_index: int, color: str) -> str:
        """Retrieve the pre-float prop rotation direction from JSON."""
        return (
            self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                json_index, color
            )
        )

    def get_opposite_rotation_direction(self, rotation_direction: str) -> str:
        """Return the opposite rotation direction."""
        return COUNTER_CLOCKWISE if rotation_direction == CLOCKWISE else CLOCKWISE

    def update_prefloat_prop_rot_dir_in_json(
        self, json_index: int, color: str, prop_rot_dir: str
    ) -> None:
        """Update JSON with pre-float prop rotation direction."""
        self.main_widget.json_manager.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            json_index, color, prop_rot_dir
        )

    def update_json_prefloat_motion_type(
        self, json_index: int, color: str, motion_type: str
    ) -> None:
        """Update JSON with pre-float motion type."""
        self.main_widget.json_manager.updater.motion_type_updater.update_json_prefloat_motion_type(
            json_index, color, motion_type
        )

# From test_letter_determiner.py
# import pytest
# from dataclasses import dataclass
# from data.constants import (
#     ANTI,
#     BLUE_ATTRS,
#     CLOCKWISE,
#     COUNTER_CLOCKWISE,
#     EAST,
#     END_LOC,
#     FLOAT,
#     MOTION_TYPE,
#     NO_ROT,
#     NORTH,
#     NORTHEAST,
#     NORTHWEST,
#     PREFLOAT_MOTION_TYPE,
#     PREFLOAT_PROP_ROT_DIR,
#     PRO,
#     PROP_ROT_DIR,
#     RED_ATTRS,
#     SOUTH,
#     START_LOC,
#     WEST,
# )
# from enums.letter.letter import Letter
# from letter_determiner.letter_determiner import LetterDeterminer
# from main_window.main_widget.pictograph_data_loader import PictographDataLoader


# class MockBeatFrame:
#     def __init__(self):
#         self.get = MockBeatFrameGetter()


# class MockBeatFrameGetter:
#     def index_of_currently_selected_beat(self) -> int:
#         return 0


# class MockSequenceWorkbench:
#     def __init__(self):
#         self.beat_frame = MockBeatFrame()


# class MockMainWidget:
#     def __init__(self):
#         self.pictograph_dataset = None
#         self.json_manager = MockJsonManager()
#         self.sequence_workbench = MockSequenceWorkbench()


# class MockJsonManager:
#     def __init__(self):
#         self.loader_saver = MockLoaderSaver()
#         self.updater = MockUpdater()


# class MockLoaderSaver:
#     def get_json_prefloat_prop_rot_dir(self, json_index: int, color: str) -> str:
#         return CLOCKWISE


# class MockUpdater:
#     def update_json_prefloat_motion_type(
#         self, json_index: int, color: str, motion_type: str
#     ) -> None:
#         pass

#     def update_prefloat_prop_rot_dir_in_json(
#         self, json_index: int, color: str, prop_rot_dir: str
#     ) -> None:
#         pass


# @pytest.fixture
# def mock_main_widget():
#     widget = MockMainWidget()
#     loader = PictographDataLoader(widget)
#     widget.pictograph_dataset = loader.load_pictograph_dataset()
#     return widget


# @pytest.fixture
# def letter_determiner(mock_main_widget):
#     return LetterDeterminer(mock_main_widget)


# @pytest.fixture
# def pictograph_dataset(mock_main_widget):
#     return mock_main_widget.pictograph_dataset


# def test_specific_pictograph(letter_determiner, pictograph_dataset):
#     pictograph = pictograph_dataset[Letter.A][0]
#     expected_letter = Letter.A
#     determined_letter = letter_determiner.determine_letter(pictograph)
#     assert (
#         determined_letter == expected_letter
#     ), f"Expected {expected_letter}, got {determined_letter} for pictograph: {pictograph}"


# @dataclass
# class MotionCase:
#     input_data: dict
#     expected_letter: Letter
#     description: str


# TEST_CASES = [
#     MotionCase(
#         input_data={
#             BLUE_ATTRS: {
#                 MOTION_TYPE: ANTI,
#                 START_LOC: SOUTH,
#                 END_LOC: WEST,
#                 PROP_ROT_DIR: COUNTER_CLOCKWISE,
#             },
#             RED_ATTRS: {
#                 MOTION_TYPE: FLOAT,
#                 START_LOC: NORTH,
#                 END_LOC: EAST,
#                 PROP_ROT_DIR: NO_ROT,
#                 PREFLOAT_MOTION_TYPE: PRO,
#                 PREFLOAT_PROP_ROT_DIR: CLOCKWISE,
#             },
#         },
#         expected_letter=Letter.B,
#         description="Pro motion with mirrored float pre-float",
#     )
# ]


# From __init__.py


