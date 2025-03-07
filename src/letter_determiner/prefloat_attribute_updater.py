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