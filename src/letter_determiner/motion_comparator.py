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
