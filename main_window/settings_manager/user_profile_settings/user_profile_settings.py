# user_profile_settings.py
from typing import TYPE_CHECKING
from .notes_manager.notes_manager import NotesManager
from .user_manager.user_manager import UserManager
from PyQt6.QtCore import QSettings

if TYPE_CHECKING:
    from ..settings_manager import SettingsManager

class UserProfileSettings:
    DEFAULT_USER_SETTINGS = {
        "current_user": "",
        "current_note": "Created using The Kinetic Alphabet",
        "saved_notes": ["Created using The Kinetic Alphabet"],
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings: QSettings = settings_manager.settings
        self.user_manager = UserManager(self)
        self.notes_manager = NotesManager(self)

    ### GETTERS ###

    def get_current_user(self) -> str:
        return self.settings.value(
            "user_profile/current_user", 
            self.DEFAULT_USER_SETTINGS["current_user"]
        )

    def get_current_note(self) -> str:
        return self.settings.value(
            "user_profile/current_note",
            self.DEFAULT_USER_SETTINGS["current_note"]
        )

    def get_saved_notes(self) -> list:
        notes = []
        self.settings.beginGroup("user_profile/saved_notes")
        all_keys = self.settings.childKeys()
        sorted_keys = sorted(all_keys, key=lambda x: int(x) if x.isdigit() else x)
        for key in sorted_keys:
            val = self.settings.value(key, "")
            notes.append(val)
        self.settings.endGroup()

        if not notes:
            return self.DEFAULT_USER_SETTINGS["saved_notes"]
        return notes

    def get_user_profiles(self) -> dict:
        profiles = {}
        self.settings.beginGroup("user_profiles")
        user_list = self.settings.childGroups()
        for user_name in user_list:
            self.settings.beginGroup(user_name)
            keys = self.settings.childKeys()
            sub_dict = {}
            for k in keys:
                sub_dict[k] = self.settings.value(k)
            self.settings.endGroup()
            profiles[user_name] = sub_dict
        self.settings.endGroup()
        return profiles

    ### SETTERS ###

    def set_current_user(self, user_name: str):
        self.settings.setValue("user_profile/current_user", user_name)

    def set_current_note(self, note: str):
        self.settings.setValue("user_profile/current_note", note)

    def set_saved_notes(self, notes: list):
        self.settings.beginGroup("user_profile/saved_notes")
        self.settings.remove("")
        self.settings.endGroup()

        self.settings.beginGroup("user_profile/saved_notes")
        for i, note in enumerate(notes):
            self.settings.setValue(str(i), note)
        self.settings.endGroup()

    def set_user_profiles(self, user_profiles: dict):
        self.settings.beginGroup("user_profiles")
        self.settings.remove("")
        self.settings.endGroup()

        for user_name, profile_data in user_profiles.items():
            self.settings.beginGroup(f"user_profiles/{user_name}")
            for key, val in profile_data.items():
                self.settings.setValue(key, val)
            self.settings.endGroup()
