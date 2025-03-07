from typing import TYPE_CHECKING
from data.constants import (
    BLUE,
    BLUE_ATTRS,
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

    def compare_motion_attributes_for_type1(
        self, motion_attrs: dict, other_motion_attrs: dict, example: dict
    ) -> bool:
        """Compare motion attributes for type1 cases."""
        return (
            self._is_motion_type_matching(
                motion_attrs, example[f"{motion_attrs['color']}_attributes"]
            )
            and example[f"{motion_attrs['color']}_attributes"][START_LOC]
            == motion_attrs[START_LOC]
            and example[f"{motion_attrs['color']}_attributes"][END_LOC]
            == motion_attrs[END_LOC]
            and self._is_prop_rot_dir_matching(
                motion_attrs,
                example[f"{motion_attrs['color']}_attributes"],
                motion_attrs["color"],
            )
            and self._is_motion_type_matching(
                other_motion_attrs, example[f"{other_motion_attrs['color']}_attributes"]
            )
            and example[f"{other_motion_attrs['color']}_attributes"][START_LOC]
            == other_motion_attrs[START_LOC]
            and example[f"{other_motion_attrs['color']}_attributes"][END_LOC]
            == other_motion_attrs[END_LOC]
            and self._is_prop_rot_dir_matching(
                other_motion_attrs,
                example[f"{other_motion_attrs['color']}_attributes"],
                other_motion_attrs["color"],
            )
        )

    def compare_motion_attributes_for_type1_hybrids_with_one_float(
        self, float_motion_attrs: dict, example: dict
    ) -> bool:
        """Compare motion attributes for type1 hybrids with one float."""
        non_float_motion_attrs = self._get_other_motion_attrs(float_motion_attrs)
        return (
            self._is_motion_type_matching(
                float_motion_attrs, example[f"{float_motion_attrs['color']}_attributes"]
            )
            and example[f"{float_motion_attrs['color']}_attributes"][START_LOC]
            == float_motion_attrs[START_LOC]
            and example[f"{float_motion_attrs['color']}_attributes"][END_LOC]
            == float_motion_attrs[END_LOC]
            and example[f"{float_motion_attrs['color']}_attributes"][PROP_ROT_DIR]
            == self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                self._get_json_index_for_current_beat(), float_motion_attrs["color"]
            )
            and self._is_motion_type_matching(
                non_float_motion_attrs,
                example[f"{non_float_motion_attrs['color']}_attributes"],
            )
            and example[f"{non_float_motion_attrs['color']}_attributes"][START_LOC]
            == non_float_motion_attrs[START_LOC]
            and example[f"{non_float_motion_attrs['color']}_attributes"][END_LOC]
            == non_float_motion_attrs[END_LOC]
            and example[f"{non_float_motion_attrs['color']}_attributes"][PROP_ROT_DIR]
            == non_float_motion_attrs[PROP_ROT_DIR]
        )

    def compare_motion_attributes_for_type1_nonhybrids_with_one_float(
        self, float_motion_attrs: dict, example: dict
    ) -> bool:
        """Compare motion attributes for type1 non-hybrids with one float."""
        non_float_motion_attrs = self._get_other_motion_attrs(float_motion_attrs)
        return (
            self._is_motion_type_matching(
                float_motion_attrs, example[f"{float_motion_attrs['color']}_attributes"]
            )
            and example[f"{float_motion_attrs['color']}_attributes"][START_LOC]
            == float_motion_attrs[START_LOC]
            and example[f"{float_motion_attrs['color']}_attributes"][END_LOC]
            == float_motion_attrs[END_LOC]
            and example[f"{float_motion_attrs['color']}_attributes"][PROP_ROT_DIR]
            == self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                self._get_json_index_for_current_beat(), float_motion_attrs["color"]
            )
            and self._is_motion_type_matching(
                non_float_motion_attrs,
                example[f"{non_float_motion_attrs['color']}_attributes"],
            )
            and example[f"{non_float_motion_attrs['color']}_attributes"][START_LOC]
            == non_float_motion_attrs[START_LOC]
            and example[f"{non_float_motion_attrs['color']}_attributes"][END_LOC]
            == non_float_motion_attrs[END_LOC]
            and example[f"{non_float_motion_attrs['color']}_attributes"][PROP_ROT_DIR]
            == non_float_motion_attrs[PROP_ROT_DIR]
        )

    def compare_motion_attributes_for_type2_3(
        self, shift_motion_attrs: dict, example: dict
    ) -> bool:
        """Compare motion attributes for type2 and type3 cases."""
        non_shift_motion_attrs = self._get_other_motion_attrs(shift_motion_attrs)
        return (
            self._is_motion_type_matching(
                shift_motion_attrs, example[f"{shift_motion_attrs['color']}_attributes"]
            )
            and example[f"{shift_motion_attrs['color']}_attributes"][START_LOC]
            == shift_motion_attrs[START_LOC]
            and example[f"{shift_motion_attrs['color']}_attributes"][END_LOC]
            == shift_motion_attrs[END_LOC]
            and self._is_prop_rot_dir_matching(
                shift_motion_attrs,
                example[f"{shift_motion_attrs['color']}_attributes"],
                shift_motion_attrs["color"],
            )
            and example[f"{non_shift_motion_attrs['color']}_attributes"][MOTION_TYPE]
            == non_shift_motion_attrs[MOTION_TYPE]
            and example[f"{non_shift_motion_attrs['color']}_attributes"][START_LOC]
            == non_shift_motion_attrs[START_LOC]
            and example[f"{non_shift_motion_attrs['color']}_attributes"][END_LOC]
            == non_shift_motion_attrs[END_LOC]
        )

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

    def _get_other_motion_attrs(self, motion_attrs: dict) -> dict:
        """Retrieve the attributes of the other motion in the pictograph."""
        # Assuming the pictograph data structure is such that the other motion's attributes can be retrieved
        # based on the current motion's color.
        other_color = RED if motion_attrs["color"] == BLUE else BLUE
        return self.main_widget.pictograph_data[other_color + "_attributes"]

    def compare_dual_motion_with_prefloat(
        self, float_attrs: dict, shift_attrs: dict, example: dict
    ) -> bool:
        """Compare with pre-float attribute awareness."""
        return (
            self._compare_motion_with_prefloat(float_attrs, example[BLUE_ATTRS])
            and self._compare_base_motion(shift_attrs, example[RED_ATTRS])
        ) or (
            self._compare_motion_with_prefloat(float_attrs, example[RED_ATTRS])
            and self._compare_base_motion(shift_attrs, example[BLUE_ATTRS])
        )

    def _compare_motion_with_prefloat(
        self, motion_attrs: dict, example_attrs: dict
    ) -> bool:
        return (
            motion_attrs[START_LOC] == example_attrs[START_LOC]
            and motion_attrs[END_LOC] == example_attrs[END_LOC]
            and (
                example_attrs[PROP_ROT_DIR] == motion_attrs.get(PREFLOAT_PROP_ROT_DIR)
                and (
                    example_attrs[MOTION_TYPE] == motion_attrs.get(PREFLOAT_MOTION_TYPE)
                )
            )
        )

    def _compare_base_motion(self, motion_attrs: dict, example_attrs: dict) -> bool:
        return (
            motion_attrs[START_LOC] == example_attrs[START_LOC]
            and motion_attrs[END_LOC] == example_attrs[END_LOC]
            and motion_attrs[PROP_ROT_DIR] == example_attrs[PROP_ROT_DIR]
            and motion_attrs[MOTION_TYPE] == example_attrs[MOTION_TYPE]
        )
