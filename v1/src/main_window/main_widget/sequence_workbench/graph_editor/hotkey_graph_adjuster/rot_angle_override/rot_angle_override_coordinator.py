# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideCoordinator:
    """Handles high-level coordination of rotation angle overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager

    def execute_override_flow(self) -> None:
        if not self._should_execute_override():
            return

        override_data = self.manager.data_handler.prepare_override_data()
        self.manager.data_handler.apply_rotation_override(override_data)
        self.manager.view_updater.refresh_affected_views()

    def _should_execute_override(self) -> bool:
        return self.manager.validator.is_valid_override_condition()
