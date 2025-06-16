"""
Settings service implementation that adapts UIStateManagementService.
"""

from typing import Any, Dict
from src.core.interfaces.settings_interfaces import ISettingsService
from src.core.interfaces.core_services import IUIStateManagementService


class SettingsServiceAdapter(ISettingsService):
    """Adapter that makes UIStateManagementService work as ISettingsService."""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.ui_state_service.get_setting(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self.ui_state_service.set_setting(key, value)

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        # Return a basic set of common settings
        return {
            "prop_type": self.get_setting("prop_type", "Staff"),
            "grid_mode": self.get_setting("grid_mode", "diamond"),
            "show_grid": self.get_setting("show_grid", True),
            "animation_speed": self.get_setting("animation_speed", 1.0),
            "auto_save": self.get_setting("auto_save", True),
            "theme": self.get_setting("theme", "dark"),
        }

    def save_settings(self) -> None:
        """Save settings."""
        # UIStateManagementService handles auto-saving
        pass
