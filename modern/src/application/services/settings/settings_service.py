from typing import Any, Dict
from src.core.interfaces.settings_interfaces import ISettingsService
from src.core.interfaces.core_services import IUIStateManagementService


class SettingsService(ISettingsService):
    """Main settings service that coordinates all settings operations"""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.ui_state_service.get_setting(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value"""
        self.ui_state_service.set_setting(key, value)

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings"""
        return self.ui_state_service.get_all_settings()

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        # Keep essential settings but clear others
        essential_keys = ["current_user", "user_profiles"]
        current_settings = self.get_all_settings()
        essential_settings = {
            key: current_settings.get(key)
            for key in essential_keys
            if key in current_settings
        }

        # Clear all settings
        self.ui_state_service.clear_settings()

        # Restore essential settings
        for key, value in essential_settings.items():
            if value is not None:
                self.set_setting(key, value)

    def save_settings(self) -> bool:
        """Save settings to persistent storage"""
        try:
            self.ui_state_service.save_state()
            return True
        except Exception:
            return False

    def load_settings(self) -> bool:
        """Load settings from persistent storage"""
        try:
            self.ui_state_service.load_state()
            return True
        except Exception:
            return False
