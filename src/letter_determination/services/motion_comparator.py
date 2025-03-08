# services/motion_comparator.py
from typing import Dict, List, Tuple
import numpy as np

from ..models.motion import MotionType, RotationDirection
from ..models.pictograph import PictographData, MotionAttributes


class MotionComparator:
    def __init__(self, dataset: Dict[str, List[PictographData]]):
        self.dataset = dataset

    def compare(
        self, blue: MotionAttributes, red: MotionAttributes, example: PictographData
    ) -> bool:
        """Compare blue and red motion attributes with an example, considering prefloat properties."""
        blue_copy = blue.serialize()
        red_copy = red.serialize()

        # Ensure prefloat attributes are correctly applied
        if blue.is_float:
            blue_copy["prefloat_motion_type"] = red.motion_type.value
            blue_copy["prefloat_prop_rot_dir"] = red.prop_rot_dir.value

        if red.is_float:
            red_copy["prefloat_motion_type"] = blue.motion_type.value
            red_copy["prefloat_prop_rot_dir"] = blue.prop_rot_dir.value

        return example.blue_attributes == MotionAttributes(
            **blue_copy
        ) and example.red_attributes == MotionAttributes(**red_copy)

    def _is_prefloat_matching(
        self, motion_attrs: MotionAttributes, example_attrs: MotionAttributes
    ) -> bool:
        """Ensure prefloat attributes match correctly."""
        return (
            example_attrs.prefloat_motion_type is None
            or example_attrs.prefloat_motion_type == motion_attrs.prefloat_motion_type
        ) and (
            example_attrs.prefloat_prop_rot_dir is None
            or example_attrs.prefloat_prop_rot_dir == motion_attrs.prefloat_prop_rot_dir
        )

    def compare_motion_to_example(
        self,
        motion_attrs: MotionAttributes,
        example_attrs: MotionAttributes,
        swap_prop_rot_dir: bool = False,
    ) -> bool:
        """Compare a single motion's attributes to an example from the dataset."""

        # Apply swap if needed
        expected_rot_dir = example_attrs.prop_rot_dir
        if swap_prop_rot_dir:
            expected_rot_dir = self._reverse_rotation(expected_rot_dir)

        return (
            motion_attrs.start_loc == example_attrs.start_loc
            and motion_attrs.end_loc == example_attrs.end_loc
            and self._is_motion_type_matching(motion_attrs, example_attrs)
            and motion_attrs.prop_rot_dir == expected_rot_dir  # Swapped if necessary
        )

    def _is_motion_type_matching(
        self, motion_attrs: MotionAttributes, example_attrs: MotionAttributes
    ) -> bool:
        """Check if motion type matches example, considering prefloat attributes."""
        return (
            example_attrs.motion_type == motion_attrs.motion_type
            or example_attrs.motion_type == motion_attrs.prefloat_motion_type
        )

    def _is_prop_rot_dir_matching(
        self, motion_attrs: MotionAttributes, example_attrs: MotionAttributes
    ) -> bool:
        """Check if rotation direction matches, considering prefloat attributes."""
        return (
            example_attrs.prop_rot_dir == motion_attrs.prop_rot_dir
            or example_attrs.prop_rot_dir == motion_attrs.prefloat_prop_rot_dir
        )

    def _reverse_rotation(self, direction: RotationDirection) -> RotationDirection:
        if direction == RotationDirection.CLOCKWISE:
            return RotationDirection.COUNTER_CLOCKWISE
        return RotationDirection.CLOCKWISE

    def compare_with_prefloat(
        self,
        target: PictographData,
        example: PictographData,
        swap_prop_rot_dir: bool = False,
    ) -> float:
        """Special comparison accounting for prefloat attributes"""
        float_attr = (
            target.blue_attributes
            if target.blue_attributes.is_float
            else target.red_attributes
        )
        shift_attr = (
            target.red_attributes
            if target.blue_attributes.is_float
            else target.blue_attributes
        )

        example_float = (
            example.blue_attributes
            if example.blue_attributes.motion_type == MotionType.FLOAT
            else example.red_attributes
        )
        example_shift = (
            example.red_attributes
            if example.blue_attributes.motion_type == MotionType.FLOAT
            else example.blue_attributes
        )

        # Apply swapping logic to prefloat rotation direction
        float_expected_rot_dir = example_float.prop_rot_dir
        if swap_prop_rot_dir:
            float_expected_rot_dir = self._reverse_rotation(float_expected_rot_dir)

        float_match = (
            float_attr.start_loc == example_float.start_loc
            and float_attr.end_loc == example_float.end_loc
            and float_expected_rot_dir
            == self._reverse_rotation(float_attr.prefloat_prop_rot_dir)
            and example_float.motion_type == float_attr.prefloat_motion_type
        )

        shift_match = (
            shift_attr.start_loc == example_shift.start_loc
            and shift_attr.end_loc == example_shift.end_loc
            and shift_attr.prop_rot_dir == example_shift.prop_rot_dir
            and shift_attr.motion_type == example_shift.motion_type
        )

        return 1.0 if float_match and shift_match else 0.0
