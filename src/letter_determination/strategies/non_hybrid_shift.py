# strategies/non_hybrid_shift.py
from data.constants import OPP
from ..models.motion import MotionAttributes, RotationDirection
from ..core import BaseDeterminationStrategy, DeterminationResult
from ..models.pictograph import PictographData


class NonHybridShiftStrategy(BaseDeterminationStrategy):
    def execute(
        self, pictograph: PictographData, swap_prop_rot_dir: bool = False
    ) -> DeterminationResult:
        """Enhanced version with proper OPP direction handling"""
        self.attribute_manager.sync_attributes(pictograph)
        float_attr, shift_attr, float_color = self._identify_components(pictograph)

        if not float_attr or not shift_attr:
            return DeterminationResult(None, {})

        # Handle direction-based inversion BEFORE setting prefloat attributes
        self._update_prefloat_attributes(
            pictograph, float_attr, shift_attr, float_color
        )

        # Modified comparison logic that accounts for OPP direction
        return self._find_matching_letter(pictograph, float_attr, shift_attr)

    def _update_prefloat_attributes(
        self,
        data: PictographData,
        float_attr: MotionAttributes,
        shift_attr: MotionAttributes,
        color: str,
    ):
        """Updated to use direction-aware rotation calculation"""
        json_index = self.attribute_manager._get_json_index(data)

        # Set prefloat motion type
        float_attr.prefloat_motion_type = shift_attr.motion_type
        self.attribute_manager.json_handler.update_prefloat_motion_type(
            json_index, color, shift_attr.motion_type
        )

        # Get direction-adjusted rotation
        base_rotation = self._get_base_rotation(float_attr, shift_attr)
        final_rotation = self._apply_direction_inversion(data.direction, base_rotation)

        # Set prefloat rotation
        float_attr.prefloat_prop_rot_dir = final_rotation
        self.attribute_manager.json_handler.update_prefloat_prop_rot_dir(
            json_index, color, final_rotation
        )

    def _get_base_rotation(
        self, float_attr: MotionAttributes, shift_attr: MotionAttributes
    ) -> RotationDirection:
        """Resolve rotation source based on motion state"""
        if float_attr.prop_rot_dir == RotationDirection.NONE:
            return shift_attr.prop_rot_dir
        return float_attr.prop_rot_dir

    def _apply_direction_inversion(
        self, direction: str, rotation: RotationDirection
    ) -> RotationDirection:
        """Handle OPP direction inversion"""
        if direction == OPP:
            return (
                RotationDirection.COUNTER_CLOCKWISE
                if rotation == RotationDirection.CLOCKWISE
                else RotationDirection.CLOCKWISE
            )
        return rotation

    def _find_matching_letter(
        self,
        pictograph: PictographData,
        float_attr: MotionAttributes,
        shift_attr: MotionAttributes,
    ) -> DeterminationResult:
        """Match using prefloat-aware comparison"""
        for letter, examples in self.comparator.dataset.items():
            for example in examples:
                if self._matches_example(pictograph, float_attr, shift_attr, example):
                    return DeterminationResult(letter, example.serialized_attributes())
        return DeterminationResult(None, {})

    def _matches_example(
        self,
        pictograph: PictographData,
        float_attr: MotionAttributes,
        shift_attr: MotionAttributes,
        example: PictographData,
    ) -> bool:
        """Direction-aware comparison logic"""
        # Get example components
        example_float = next(
            (
                attr
                for attr in [example.blue_attributes, example.red_attributes]
                if attr.is_float
            ),
            None,
        )
        example_shift = next(
            (
                attr
                for attr in [example.blue_attributes, example.red_attributes]
                if not attr.is_float
            ),
            None,
        )

        # Verify float match with prefloat attributes
        float_match = (
            example_float.start_loc == float_attr.start_loc
            and example_float.end_loc == float_attr.end_loc
            and example_float.prop_rot_dir == float_attr.prefloat_prop_rot_dir
            and example_float.motion_type == float_attr.prefloat_motion_type
        )

        # Verify shift match with direction adjustment
        shift_match = (
            example_shift.start_loc == shift_attr.start_loc
            and example_shift.end_loc == shift_attr.end_loc
            and example_shift.prop_rot_dir
            == self._apply_direction_inversion(
                pictograph.direction, shift_attr.prop_rot_dir
            )
            and example_shift.motion_type == shift_attr.motion_type
        )

        return float_match and shift_match
