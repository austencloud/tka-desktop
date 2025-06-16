# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING
from data.constants import STATIC, DASH

from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideValidator:
    """Validates conditions for rotation overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager

    def is_valid_override_condition(self) -> bool:
        selected_arrow = AppContext.get_selected_arrow()
        return (
            selected_arrow is not None
            and selected_arrow.motion.state.motion_type in [STATIC, DASH]
        )
