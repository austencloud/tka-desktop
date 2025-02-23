# user_profile_settings.py
from typing import TYPE_CHECKING
from .notes_manager.notes_manager import NotesManager
from .user_manager.user_manager import UserManager
from PyQt6.QtCore import QSettings

if TYPE_CHECKING:
    from ..settings_manager import SettingsManager

class UserProfileSettings:
    """
    - Store 'current_user', 'current_note', 'saved_notes' under the [user_profile] group.
    - Store each user's profile data under [user_profiles/<username>].
      e.g. [user_profiles/Austen Cloud]
           name=Austen Cloud
           email=austen@example.com
           ...
    """

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

    ### CURRENT USER ###

    def get_current_user(self) -> str:
        return self.settings.value(
            "user_profile/current_user", 
            self.DEFAULT_USER_SETTINGS["current_user"]
        )

    def set_current_user(self, user_name: str):
        self.settings.setValue("user_profile/current_user", user_name)

    ### CURRENT NOTE ###

    def get_current_note(self) -> str:
        return self.settings.value(
            "user_profile/current_note",
            self.DEFAULT_USER_SETTINGS["current_note"]
        )

    def set_current_note(self, note: str):
        self.settings.setValue("user_profile/current_note", note)

    ### SAVED NOTES ###

    def get_saved_notes(self) -> list:
        """
        Retrieve notes from subkeys in [user_profile/saved_notes]:
          0=Created using The Kinetic Alphabet
          1="Turn left on first half, turn right on second half"
        """
        notes = []
        self.settings.beginGroup("user_profile/saved_notes")
        all_keys = self.settings.childKeys()    # e.g. ["0", "1", "2"...]
        sorted_keys = sorted(all_keys, key=lambda x: int(x) if x.isdigit() else x)
        for key in sorted_keys:
            val = self.settings.value(key, "")
            notes.append(val)
        self.settings.endGroup()

        if not notes:
            return self.DEFAULT_USER_SETTINGS["saved_notes"]
        return notes

    def set_saved_notes(self, notes: list):
        # Clear existing subkeys
        self.settings.beginGroup("user_profile/saved_notes")
        self.settings.remove("")
        self.settings.endGroup()

        # Write each note as user_profile/saved_notes/0=theFirstNote
        self.settings.beginGroup("user_profile/saved_notes")
        for i, note in enumerate(notes):
            self.settings.setValue(str(i), note)
        self.settings.endGroup()

    ### USER PROFILES ###

    def get_user_profiles(self) -> dict:
        """
        Reads each user’s profile data from top-level group [user_profiles/<username>].
        e.g. [user_profiles/Austen Cloud]
             name=Austen Cloud
             email=austen@example.com
        Returns: { "Austen Cloud": {"name": "Austen Cloud", "email": "austen@example.com", ...},
                   "Doc Womp":     {"name": "Doc Womp", ...} }
        """
        profiles = {}
        self.settings.beginGroup("user_profiles")
        user_list = self.settings.childGroups()   # e.g. ["Austen Cloud", "Doc Womp", ...]
        for user_name in user_list:
            self.settings.beginGroup(user_name)
            # gather each key
            keys = self.settings.childKeys()   # e.g. ["name", "favorite_prop"...]
            sub_dict = {}
            for k in keys:
                sub_dict[k] = self.settings.value(k)
            self.settings.endGroup()  # done with user
            profiles[user_name] = sub_dict
        self.settings.endGroup()  # done with user_profiles
        return profiles

    def set_user_profiles(self, user_profiles: dict):
        """
        Store each user's data in a top-level group [user_profiles/<username>].
        That yields final INI sections:
          [user_profiles/Austen Cloud]
          name=Austen Cloud
          ...
        """
        # Remove old user_profiles subtree
        self.settings.beginGroup("user_profiles")
        self.settings.remove("")
        self.settings.endGroup()

        # Now re-add each user
        for user_name, profile_data in user_profiles.items():
            self.settings.beginGroup(f"user_profiles/{user_name}")
            for key, val in profile_data.items():
                self.settings.setValue(key, val)
            self.settings.endGroup()
