from typing import List, Optional
from src.core.interfaces.tab_settings_interfaces import IUserProfileService
from src.core.interfaces.core_services import IUIStateManagementService


class UserProfileService(IUserProfileService):
    """Service for managing user profiles and settings"""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service

    def get_current_user(self) -> str:
        """Get the current active user"""
        return self.ui_state_service.get_setting("current_user", "Default User")

    def set_current_user(self, username: str) -> None:
        """Set the current active user"""
        self.ui_state_service.set_setting("current_user", username)

    def get_all_users(self) -> List[str]:
        """Get all available user profiles"""
        users = self.ui_state_service.get_setting("user_profiles", ["Default User"])
        return users if isinstance(users, list) else ["Default User"]

    def add_user(self, username: str) -> bool:
        """Add a new user profile"""
        if not username or not username.strip():
            return False

        users = self.get_all_users()
        if username in users:
            return False

        users.append(username)
        self.ui_state_service.set_setting("user_profiles", users)
        return True

    def remove_user(self, username: str) -> bool:
        """Remove a user profile"""
        users = self.get_all_users()
        if username not in users or len(users) <= 1:  # Keep at least one user
            return False

        users.remove(username)
        self.ui_state_service.set_setting("user_profiles", users)

        # If we removed the current user, switch to the first available
        if self.get_current_user() == username:
            self.set_current_user(users[0])

        return True

    def get_user_setting(self, username: str, setting_key: str, default=None):
        """Get a setting for a specific user"""
        user_settings = self.ui_state_service.get_setting(f"user_{username}", {})
        return user_settings.get(setting_key, default)

    def set_user_setting(self, username: str, setting_key: str, value) -> None:
        """Set a setting for a specific user"""
        user_settings = self.ui_state_service.get_setting(f"user_{username}", {})
        user_settings[setting_key] = value
        self.ui_state_service.set_setting(f"user_{username}", user_settings)
