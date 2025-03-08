import numpy as np
from data.constants import (
    ANTI,
    BLUE_ATTRS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    END_LOC,
    END_POS,
    FLOAT,
    MOTION_TYPE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
    PROP_ROT_DIR,
    RED_ATTRS,
    START_LOC,
    START_POS,
)

class MotionComparator:
    def __init__(self, dataset: dict[str, list[dict]]):
        self.dataset = dataset

    def compare(self, pictograph_data: dict, example: dict) -> bool:
        blue_attrs: dict = pictograph_data[BLUE_ATTRS]
        red_attrs: dict = pictograph_data[RED_ATTRS]

        blue_copy = blue_attrs.copy()
        red_copy = red_attrs.copy()

        if blue_attrs[MOTION_TYPE] == FLOAT:
            blue_copy[PREFLOAT_MOTION_TYPE] = red_attrs[MOTION_TYPE]
            blue_copy[PREFLOAT_PROP_ROT_DIR] = red_attrs[PROP_ROT_DIR]

        if red_attrs[MOTION_TYPE] == FLOAT:
            red_copy[PREFLOAT_MOTION_TYPE] = blue_attrs[MOTION_TYPE]
            red_copy[PREFLOAT_PROP_ROT_DIR] = blue_attrs[PROP_ROT_DIR]

        red_motion_type = (
            red_copy[MOTION_TYPE]
            if red_copy[MOTION_TYPE] != FLOAT
            else red_copy[PREFLOAT_MOTION_TYPE]
        )
        blue_motion_type = (
            blue_copy[MOTION_TYPE]
            if blue_copy[MOTION_TYPE] != FLOAT
            else blue_copy[PREFLOAT_MOTION_TYPE]
        )

        if pictograph_data[START_POS] == example[START_POS]:
            if pictograph_data[END_POS] == example[END_POS]:
                if example[BLUE_ATTRS][MOTION_TYPE] == blue_motion_type:
                    if example[RED_ATTRS][MOTION_TYPE] == red_motion_type:
                        return True

        return example[BLUE_ATTRS] == blue_copy and example[RED_ATTRS] == red_copy

    def _is_prefloat_matching(self, motion_attrs: dict, example_attrs: dict) -> bool:
        return (
            example_attrs[PREFLOAT_MOTION_TYPE] is None
            or example_attrs[PREFLOAT_MOTION_TYPE] == motion_attrs[PREFLOAT_MOTION_TYPE]
        ) and (
            example_attrs[PREFLOAT_PROP_ROT_DIR] is None
            or example_attrs[PREFLOAT_PROP_ROT_DIR]
            == motion_attrs[PREFLOAT_PROP_ROT_DIR]
        )

    def compare_motion_to_example(
        self,
        motion_attrs: dict,
        example_attrs: dict,
        swap_prop_rot_dir: bool = False,
    ) -> bool:
        expected_prop_rot_dir = example_attrs[PROP_ROT_DIR]
        if swap_prop_rot_dir:
            expected_prop_rot_dir = self._reverse_prop_rot_dir(expected_prop_rot_dir)

        return (
            motion_attrs[START_LOC] == example_attrs[START_LOC]
            and motion_attrs[END_LOC] == example_attrs[END_LOC]
            and self._is_motion_type_matching(motion_attrs, example_attrs)
            and motion_attrs[PROP_ROT_DIR] == expected_prop_rot_dir
        )

    def _is_motion_type_matching(self, motion_attrs: dict, example_attrs: dict) -> bool:
        return (
            example_attrs[MOTION_TYPE] == motion_attrs[MOTION_TYPE]
            or example_attrs[MOTION_TYPE] == motion_attrs[PREFLOAT_MOTION_TYPE]
        )

    def _is_prop_rot_dir_matching(
        self, motion_attrs: dict, example_attrs: dict
    ) -> bool:
        return (
            example_attrs[PROP_ROT_DIR] == motion_attrs[PROP_ROT_DIR]
            or example_attrs[PROP_ROT_DIR] == motion_attrs[PREFLOAT_PROP_ROT_DIR]
        )

    def _reverse_prop_rot_dir(self, prop_rot_dir: str) -> str:
        if prop_rot_dir == CLOCKWISE:
            return COUNTER_CLOCKWISE
        return CLOCKWISE

    def _reverse_motion_type(self, motion_type: str) -> str:
        if motion_type == PRO:
            return ANTI
        return PRO

    def compare_with_prefloat(
        self,
        target: dict,
        example: dict,
        swap_prop_rot_dir: bool = False,
    ) -> float:
        float_attr = (
            target[BLUE_ATTRS]
            if target[BLUE_ATTRS][MOTION_TYPE] == FLOAT
            else target[RED_ATTRS]
        )
        shift_attr = (
            target[RED_ATTRS]
            if target[BLUE_ATTRS][MOTION_TYPE] == FLOAT
            else target[BLUE_ATTRS]
        )

        example_float = (
            example[BLUE_ATTRS]
            if example[BLUE_ATTRS][MOTION_TYPE] == FLOAT
            else example[RED_ATTRS]
        )
        example_shift = (
            example[RED_ATTRS]
            if example[BLUE_ATTRS][MOTION_TYPE] == FLOAT
            else example[BLUE_ATTRS]
        )

        float_expected_rot_dir = example_float[PROP_ROT_DIR]
        if swap_prop_rot_dir:
            float_expected_rot_dir = self._reverse_prop_rot_dir(float_expected_rot_dir)

        float_match = (
            float_attr[START_LOC] == example_float[START_LOC]
            and float_attr[END_LOC] == example_float[END_LOC]
            and float_expected_rot_dir
            == self._reverse_prop_rot_dir(float_attr[PREFLOAT_PROP_ROT_DIR])
            and example_float[MOTION_TYPE] == float_attr[PREFLOAT_MOTION_TYPE]
        )

        shift_match = (
            shift_attr[START_LOC] == example_shift[START_LOC]
            and shift_attr[END_LOC] == example_shift[END_LOC]
            and shift_attr[PROP_ROT_DIR] == example_shift[PROP_ROT_DIR]
            and shift_attr[MOTION_TYPE] == example_shift[MOTION_TYPE]
        )

        return 1.0 if float_match and shift_match else 0.0
