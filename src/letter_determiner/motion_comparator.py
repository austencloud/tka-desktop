from typing import TYPE_CHECKING
from data.constants import START_LOC, END_LOC, PROP_ROT_DIR, MOTION_TYPE

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from main_window.main_widget.main_widget import MainWidget


class MotionComparator:
    """Handles motion attribute comparisons for letter determination."""

    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def compare_motion_to_example(self, motion: "Motion", example: dict) -> bool:
        """Compare a single motion's attributes to an example from the dataset."""
        return (
            example[f"{motion.state.color}_attributes"][START_LOC]
            == motion.state.start_loc
            and example[f"{motion.state.color}_attributes"][END_LOC]
            == motion.state.end_loc
            and self._is_prop_rot_dir_matching(motion, example)
            and self._is_motion_type_matching(motion, example)
        )

    def compare_dual_motion_to_example(
        self, motion: "Motion", other_motion: "Motion", example: dict
    ) -> bool:
        """Compare two motions (dual motion case) to an example from the dataset."""
        return self.compare_motion_to_example(
            motion, example
        ) and self.compare_motion_to_example(other_motion, example)

    def _is_prop_rot_dir_matching(self, motion: "Motion", example: dict) -> bool:
        """Check if the motion's prop rotation direction matches the dataset example."""
        json_index = self._get_json_index_for_current_beat()
        stored_prop_rot_dir = (
            self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                json_index, motion.state.color
            )
        )
        return (
            example[f"{motion.state.color}_attributes"][PROP_ROT_DIR]
            == stored_prop_rot_dir
            or example[f"{motion.state.color}_attributes"][PROP_ROT_DIR]
            == motion.state.prop_rot_dir
        )

    def _is_motion_type_matching(self, motion: "Motion", example: dict) -> bool:
        """Check if the motion type matches the dataset example."""
        return (
            example[f"{motion.state.color}_attributes"][MOTION_TYPE]
            == motion.state.motion_type
            or example[f"{motion.state.color}_attributes"][MOTION_TYPE]
            == motion.state.prefloat_motion_type
        )

    def _get_json_index_for_current_beat(self) -> int:
        """Retrieve the JSON index for the currently selected beat."""
        return (
            self.main_widget.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
            + 2
        )
