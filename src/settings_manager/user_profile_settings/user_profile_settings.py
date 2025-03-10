# user_profile_settings.py
from typing import TYPE_CHECKING
from .user_manager.user_manager import UserManager
from PyQt6.QtCore import QSettings

if TYPE_CHECKING:
    from ..settings_manager import SettingsManager

class UserProfileSettings:
    DEFAULT_USER_SETTINGS = {
        "current_user": "",
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings: QSettings = settings_manager.settings
        self.user_manager = UserManager(self)


    def get_current_user(self) -> str:
        return self.settings.value(
            "user_profile/current_user", 
            self.DEFAULT_USER_SETTINGS["current_user"]
        )

    def set_current_user(self, user_name: str):
        self.settings.setValue("user_profile/current_user", user_name)

    def get_user_profiles(self) -> dict:
        profiles = {}
        self.settings.beginGroup("user_profiles")
        user_list = self.settings.childGroups()

        for user_name in user_list:
            self.settings.beginGroup(user_name)
            user_data = {
                "name": self.settings.value("name", user_name),
            }
            self.settings.endGroup()
            profiles[user_name] = user_data

        self.settings.endGroup()
        return profiles

    def set_user_profiles(self, user_profiles: dict):
        self.settings.beginGroup("user_profiles")
        self.settings.remove("")

        for user_name, profile_data in user_profiles.items():
            self.settings.beginGroup(user_name)
            self.settings.setValue("name", profile_data.get("name", user_name))
            self.settings.endGroup()

        self.settings.endGroup()
