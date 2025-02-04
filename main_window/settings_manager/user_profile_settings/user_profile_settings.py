from typing import TYPE_CHECKING
from .notes_manager.notes_manager import NotesManager
from .user_manager.user_manager import UserManager

if TYPE_CHECKING:
    from ..settings_manager import SettingsManager


class UserProfileSettings:
    DEFAULT_USER_SETTINGS = {
        "current_user": "",
        "user_profiles": {},
        "current_note": "Created using The Kinetic Alphabet",
        "saved_notes": ["Created using The Kinetic Alphabet"],
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance
        self.user_manager = UserManager(self)
        self.notes_manager = NotesManager(self)

    def get_current_user(self):
        return self.settings.value(
            "user_profile/current_user", self.DEFAULT_USER_SETTINGS["current_user"]
        )

    def set_current_user(self, user_name: str):
        self.settings.setValue("user_profile/current_user", user_name)

    def get_user_profiles(self):
        return self.settings.value(
            "user_profile/user_profiles", self.DEFAULT_USER_SETTINGS["user_profiles"]
        )

    def set_user_profiles(self, user_profiles: dict):
        self.settings.setValue("user_profile/user_profiles", user_profiles)

    def get_current_note(self):
        return self.settings.value(
            "user_profile/current_note", self.DEFAULT_USER_SETTINGS["current_note"]
        )

    def set_current_note(self, note: str):
        self.settings.setValue("user_profile/current_note", note)

    def get_saved_notes(self):
        return self.settings.value(
            "user_profile/saved_notes", self.DEFAULT_USER_SETTINGS["saved_notes"]
        )

    def set_saved_notes(self, notes: list):
        self.settings.setValue("user_profile/saved_notes", notes)
