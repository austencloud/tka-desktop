from typing import TYPE_CHECKING
from data.constants import COUNTER_CLOCKWISE, CLOCKWISE

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from main_window.main_widget.main_widget import MainWidget


class PrefloatAttributeUpdater:
    """Handles updating pre-float attributes in the JSON."""

    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def update_prefloat_attributes(
        self, motion: "Motion", other_motion: "Motion"
    ) -> None:
        """Update pre-float motion attributes in JSON."""
        json_index = self._get_json_index_for_current_beat()

        self.main_widget.json_manager.updater.motion_type_updater.update_json_prefloat_motion_type(
            json_index, motion.state.color, other_motion.state.prefloat_motion_type
        )

        motion.state.prefloat_prop_rot_dir = self._get_prefloat_prop_rot_dir(
            json_index, motion
        )
        self.main_widget.json_manager.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            json_index, motion.state.color, motion.state.prefloat_prop_rot_dir
        )

    def _get_json_index_for_current_beat(self) -> int:
        """Retrieve the JSON index for the currently selected beat."""
        return (
            self.main_widget.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
            + 2
        )

    def _get_prefloat_prop_rot_dir(self, json_index: int, motion: "Motion") -> str:
        """Retrieve the pre-float prop rotation direction from JSON."""
        return (
            self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                json_index, motion.state.color
            )
        )

    def get_opposite_rotation_direction(self, rotation_direction: str) -> str:
        """Return the opposite rotation direction."""
        return COUNTER_CLOCKWISE if rotation_direction == CLOCKWISE else CLOCKWISE
