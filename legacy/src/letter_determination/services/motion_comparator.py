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
        blue_attrs, red_attrs = pictograph_data[BLUE_ATTRS], pictograph_data[RED_ATTRS]
        blue_copy, red_copy = blue_attrs.copy(), red_attrs.copy()

        self._update_prefloat_attrs(blue_attrs, red_attrs, blue_copy, red_copy)
        self._update_prefloat_attrs(red_attrs, blue_attrs, red_copy, blue_copy)

        red_motion_type = self._get_motion_type(red_copy)
        blue_motion_type = self._get_motion_type(blue_copy)

        if (
            pictograph_data[START_POS] == example[START_POS]
            and pictograph_data[END_POS] == example[END_POS]
        ):
            if (
                example[BLUE_ATTRS][MOTION_TYPE] == blue_motion_type
                and example[RED_ATTRS][MOTION_TYPE] == red_motion_type
            ):
                return True

        return example[BLUE_ATTRS] == blue_copy and example[RED_ATTRS] == red_copy

    def _update_prefloat_attrs(self, attrs, other_attrs, copy, other_copy):
        if attrs[MOTION_TYPE] == FLOAT:
            copy[PREFLOAT_MOTION_TYPE] = other_attrs[MOTION_TYPE]
            copy[PREFLOAT_PROP_ROT_DIR] = other_attrs[PROP_ROT_DIR]

    def _get_motion_type(self, attrs):
        return (
            attrs[MOTION_TYPE]
            if attrs[MOTION_TYPE] != FLOAT
            else attrs[PREFLOAT_MOTION_TYPE]
        )

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
        self, motion_attrs: dict, example_attrs: dict, swap_prop_rot_dir: bool = False
    ) -> bool:
        expected_prop_rot_dir = self._get_expected_prop_rot_dir(
            example_attrs[PROP_ROT_DIR], swap_prop_rot_dir
        )
        return (
            motion_attrs[START_LOC] == example_attrs[START_LOC]
            and motion_attrs[END_LOC] == example_attrs[END_LOC]
            and self._is_motion_type_matching(motion_attrs, example_attrs)
            and motion_attrs[PROP_ROT_DIR] == expected_prop_rot_dir
        )

    def _get_expected_prop_rot_dir(self, prop_rot_dir, swap):
        return self._reverse_prop_rot_dir(prop_rot_dir) if swap else prop_rot_dir

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
        return COUNTER_CLOCKWISE if prop_rot_dir == CLOCKWISE else CLOCKWISE

    def _reverse_motion_type(self, motion_type: str) -> str:
        return ANTI if motion_type == PRO else PRO

    def compare_with_prefloat(
        self, target: dict, example: dict, swap_prop_rot_dir: bool = False
    ) -> float:
        float_attr, shift_attr = self._get_float_and_shift_attrs(target)
        example_float, example_shift = self._get_float_and_shift_attrs(example)

        float_expected_rot_dir = self._get_expected_prop_rot_dir(
            example_float[PROP_ROT_DIR], swap_prop_rot_dir
        )

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

    def _get_float_and_shift_attrs(self, data):
        if data[BLUE_ATTRS][MOTION_TYPE] == FLOAT:
            return data[BLUE_ATTRS], data[RED_ATTRS]
        return data[RED_ATTRS], data[BLUE_ATTRS]
