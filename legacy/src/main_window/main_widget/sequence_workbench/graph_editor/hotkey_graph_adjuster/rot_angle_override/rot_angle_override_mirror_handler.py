# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/arrow_rot_angle_override_manager.py
from typing import TYPE_CHECKING, Optional


from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideMirrorHandler:
    """Manages mirrored entry updates for rotation overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager

    def handle_addition(self, turn_data: dict[str, bool]) -> None:
        mirrored_entry_manager = self.manager.data_updater.mirrored_entry_manager
        mirrored_entry_manager.rot_angle_manager.update_rotation_angle_in_mirrored_entry(
            AppContext.get_selected_arrow(),
            turn_data,  # Now properly typed
        )

    def handle_removal(self, hybrid_key: str) -> None:
        mirrored_entry_handler = self.manager.data_updater.mirrored_entry_manager
        if mirrored_entry_handler:
            mirrored_entry_handler.rot_angle_manager.remove_rotation_angle_in_mirrored_entry(
                AppContext.get_selected_arrow(),
                hybrid_key,
            )

    def update_mirrored_entries(self, key: str, value: Optional[bool]) -> None:
        if value is not None:
            self.handle_addition({key: value})
        else:
            self.handle_removal(key)
