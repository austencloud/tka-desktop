# strategies/non_hybrid_shift.py
from typing import Optional
from data.constants import (
    ANTI,
    BLUE,
    BLUE_ATTRS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DIRECTION,
    END_LOC,
    FLOAT,
    MOTION_TYPE,
    NO_ROT,
    OPP,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
    START_LOC,
)
from letter_determination.determination_result import DeterminationResult
from letter_determination.strategies.base_strategy import LetterDeterminationStrategy


class NonHybridShiftStrategy(LetterDeterminationStrategy):
    def execute(
        self, pictograph: dict, swap_prop_rot_dir: bool = False
    ) -> DeterminationResult:
        """Enhanced version with proper OPP direction handling"""
        self.attribute_manager.sync_attributes(pictograph)
        float_attr, non_float_attrs, float_color = self._identify_components(pictograph)

        if not float_attr or not non_float_attrs:
            return None

        # Handle direction-based inversion BEFORE setting prefloat attributes
        self._update_prefloat_attributes(
            pictograph, float_attr, non_float_attrs, float_color
        )

        # Modified comparison logic that accounts for OPP direction
        return self._find_matching_letter(pictograph, float_attr, non_float_attrs)

    def _identify_components(self, data: dict) -> tuple[dict, dict, str]:
        """Identify float and shift attributes"""
        float_attrs = next(
            (
                attr
                for attr in [data[BLUE_ATTRS], data[RED_ATTRS]]
                if attr[MOTION_TYPE] == FLOAT
            ),
            None,
        )
        non_float_attrs = next(
            (
                attr
                for attr in [data[BLUE_ATTRS], data[RED_ATTRS]]
                if attr[MOTION_TYPE] != FLOAT
            ),
            None,
        )
        if float_attrs == data[BLUE_ATTRS]:
            return float_attrs, non_float_attrs, BLUE
        return float_attrs, non_float_attrs, RED

    def _update_prefloat_attributes(
        self,
        pictograph_data: dict,
        float_attr: dict,
        non_float_attrs: dict,
        color: str,
    ):
        """Updated to use direction-aware rotation calculation"""
        json_index = self.attribute_manager._get_json_index(pictograph_data)

        # Set prefloat motion type
        float_attr[PREFLOAT_MOTION_TYPE] = non_float_attrs[MOTION_TYPE]
        self.attribute_manager.json_handler.update_prefloat_motion_type(
            json_index, color, non_float_attrs[MOTION_TYPE]
        )

        # Get direction-adjusted rotation
        base_rotation = self._get_base_rotation(float_attr, non_float_attrs)
        final_rotation = self._apply_direction_inversion(
            pictograph_data[DIRECTION], base_rotation
        )

        # Set prefloat rotation
        float_attr[PREFLOAT_PROP_ROT_DIR] = final_rotation
        self.attribute_manager.json_handler.update_prefloat_prop_rot_dir(
            json_index, color, final_rotation
        )

    def _get_base_rotation(self, float_attrs: dict, non_float_attrs: dict) -> str:
        """Resolve rotation source based on motion state"""
        if float_attrs[PROP_ROT_DIR] == NO_ROT:
            return non_float_attrs[PROP_ROT_DIR]
        return float_attrs[PROP_ROT_DIR]

    def _apply_direction_inversion(self, direction: str, prop_rot_dir: str) -> str:
        """Handle OPP direction inversion"""
        if direction == OPP:
            return COUNTER_CLOCKWISE if prop_rot_dir == CLOCKWISE else CLOCKWISE
        return prop_rot_dir

    def _find_matching_letter(
        self,
        pictograph: dict,
        float_attr: dict,
        non_float_attrs: dict,
    ) -> Optional[str]:
        """Match using prefloat-aware comparison"""
        for letter, examples in self.comparator.dataset.items():
            for example in examples:
                if self._matches_example(
                    pictograph, float_attr, non_float_attrs, example
                ):
                    return letter
        return None

    def _matches_example(
        self,
        pictograph: dict,
        float_attrs: dict,
        non_float_attrs: dict,
        example: dict,
    ) -> bool:
        """Corrected comparison logic that avoids searching for FLOAT in examples"""

        # Get example components (neither will be FLOAT)
        example_blue = example[BLUE_ATTRS]
        example_red = example[RED_ATTRS]

        # Identify the shift motion in the example (since it has no floats)
        reference_for_non_float = (
            example_blue if example_red[MOTION_TYPE] == FLOAT else example_red
        )
        reference_for_float = (
            example_blue if reference_for_non_float == example_red else example_red
        )

        # Ensure we are comparing the float motion against the example’s shift motion
        float_match = (
            float_attrs[START_LOC] == reference_for_float[START_LOC]
            and float_attrs[END_LOC] == reference_for_float[END_LOC]
            and float_attrs[PREFLOAT_PROP_ROT_DIR] == reference_for_float[PROP_ROT_DIR]
            and float_attrs[PREFLOAT_MOTION_TYPE] == reference_for_float[MOTION_TYPE]
        )

        # Verify shift motion with potential OPP direction inversion
        non_float_match = (
            non_float_attrs[START_LOC] == reference_for_non_float[START_LOC]
            and non_float_attrs[END_LOC] == reference_for_non_float[END_LOC]
            and non_float_attrs[PROP_ROT_DIR]
            == self._apply_direction_inversion(
                pictograph[DIRECTION], reference_for_non_float[PROP_ROT_DIR]
            )
            and non_float_attrs[MOTION_TYPE] == reference_for_non_float[MOTION_TYPE]
        )

        return float_match and non_float_match

    def applies_to(self, pictograph: dict) -> bool:
        """This strategy applies when one motion is FLOAT and the other is PRO/ANTI."""
        return (
            pictograph[BLUE_ATTRS][MOTION_TYPE] == FLOAT
            and pictograph[RED_ATTRS][MOTION_TYPE] in [PRO, ANTI]
        ) or (
            pictograph[RED_ATTRS][MOTION_TYPE] == FLOAT
            and pictograph[BLUE_ATTRS][MOTION_TYPE] in [PRO, ANTI]
        )
