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

    ### --- USER PROFILE MANAGEMENT --- ###

    def get_current_user(self) -> str:
        return self.settings.value(
            "user_profile/current_user", 
            self.DEFAULT_USER_SETTINGS["current_user"]
        )

    def set_current_user(self, user_name: str):
        self.settings.setValue("user_profile/current_user", user_name)

    def get_user_profiles(self) -> dict:
        """Retrieve all user profiles as a dictionary."""
        profiles = {}

        # Begin reading the "user_profiles" group
        self.settings.beginGroup("user_profiles")
        user_list = self.settings.childGroups()  # Get all user profile names

        for user_name in user_list:
            self.settings.beginGroup(user_name)  # Open each user profile subgroup
            user_data = {
                "name": self.settings.value("name", user_name),  # Get the user's display name
                "notes": self.settings.value("notes", []),  # Retrieve stored notes (if any)
            }
            self.settings.endGroup()  # Close the subgroup
            profiles[user_name] = user_data  # Store in the dictionary

        self.settings.endGroup()  # Close the "user_profiles" group
        return profiles

    def set_user_profiles(self, user_profiles: dict):
        """Save user profiles into QSettings."""
        self.settings.beginGroup("user_profiles")
        self.settings.remove("")  # Clear previous entries before saving

        for user_name, profile_data in user_profiles.items():
            self.settings.beginGroup(user_name)  # Open subgroup for each user
            self.settings.setValue("name", profile_data.get("name", user_name))
            self.settings.setValue("notes", profile_data.get("notes", []))
            self.settings.endGroup()  # Close subgroup

        self.settings.endGroup()  # Close "user_profiles" group


    ### --- USER-SPECIFIC NOTES MANAGEMENT --- ###

    def get_user_notes(self, user_name: str) -> list:
        """Retrieve notes for a specific user."""
        user_profiles = self.get_user_profiles()
        return user_profiles.get(user_name, {}).get("notes", [])

    def set_user_notes(self, user_name: str, notes: list):
        """Save notes for a specific user."""
        self.settings.beginGroup("user_profiles")
        if user_name in self.settings.childGroups():
            self.settings.beginGroup(user_name)
            self.settings.setValue("notes", notes)  # Save notes as a list
            self.settings.endGroup()
        self.settings.endGroup()


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


    ### SETTERS ###


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
