# user_profile_settings.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSettings

if TYPE_CHECKING:
    from ..legacy_settings_manager import LegacySettingsManager


class UserProfileSettings:
    """Simplified user profile settings for single-user management."""

    DEFAULT_USER_SETTINGS = {
        "current_user": "",
    }

    def __init__(self, settings_manager: "LegacySettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings: QSettings = settings_manager.settings

    def get_current_user(self) -> str:
        return self.settings.value(
            "user_profile/current_user", self.DEFAULT_USER_SETTINGS["current_user"]
        )

    def set_current_user(self, user_name: str):
        """Set the current user name."""
        self.settings.setValue("user_profile/current_user", user_name)
        self.settings.sync()  # Ensure immediate save

    def get_user_profiles(self) -> dict:
        """Get user profiles - simplified for single user."""
        current_user = self.get_current_user()
        if current_user:
            return {current_user: {"name": current_user}}
        return {}

    def set_user_profiles(self, user_profiles: dict):
        """Set user profiles - simplified for single user."""
        # For backward compatibility, just take the first user if any
        if user_profiles:
            first_user = next(iter(user_profiles.keys()))
            self.set_current_user(first_user)
