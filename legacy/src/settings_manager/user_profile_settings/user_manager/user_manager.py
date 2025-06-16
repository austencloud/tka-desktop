from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QObject
from .edit_user_profiles_dialog import EditUserProfilesDialog

if TYPE_CHECKING:
    from ..user_profile_settings import UserProfileSettings


class UserManager(QObject):
    def __init__(self, user_profile_settings: "UserProfileSettings"):
        super().__init__()
        self.user_profile_settings = user_profile_settings
        self.previous_user = ""
        self.user_combo_box = None
        self.is_in_image_export = False

    def populate_user_profiles_combo_box(self, user_combo_box: QComboBox):
        self.is_in_image_export = True
        user_profiles = self.user_profile_settings.get_user_profiles()
        current_user = self.user_profile_settings.get_current_user()
        self.user_combo_box = user_combo_box
        self.user_combo_box.clear()
        for user_name in user_profiles.keys():
            self.user_combo_box.addItem(user_name)
        self.user_combo_box.addItem("Edit Users")
        if current_user in user_profiles:
            index = self.user_combo_box.findText(current_user)
            if index != -1:
                self.user_combo_box.setCurrentIndex(index)
        self.user_combo_box.currentIndexChanged.connect(
            self._update_current_user_in_combo_box
        )

    def _update_current_user_in_combo_box(self):
        selected_user = self.user_combo_box.currentText()
        if selected_user == "Edit Users":
            self.open_edit_users_dialog()
        else:
            self.user_profile_settings.set_current_user(selected_user)

    def open_edit_users_dialog(self):
        dialog = EditUserProfilesDialog(self)
        if dialog.exec():
            if self.is_in_image_export:
                self.populate_user_profiles_combo_box(self.user_combo_box)

    def get_all_users(self):
        return list(self.user_profile_settings.get_user_profiles().keys())

    def add_new_user(self, user_name):
        user_profiles = self.user_profile_settings.get_user_profiles()
        if user_name in user_profiles:
            return False
        user_profiles[user_name] = {"name": user_name}
        self.user_profile_settings.set_user_profiles(user_profiles)
        self.user_profile_settings.set_current_user(user_name)
        return True

    def remove_user(self, user_name):
        user_profiles = self.user_profile_settings.get_user_profiles()
        if user_name in user_profiles:
            del user_profiles[user_name]
            self.user_profile_settings.set_user_profiles(user_profiles)
            return True
        return False

    def save_users(self):
        # User data is directly saved with set_user_profiles method, no additional save needed
        pass

    def get_current_user(self):
        return self.user_profile_settings.get_current_user()

    def set_current_user(self, user_name):
        self.user_profile_settings.set_current_user(user_name)

    ### --- User-Specific Notes Management --- ###

    def get_user_notes(self, user_name):
        """Get all notes for a specific user."""
        user_profiles = self.user_profile_settings.get_user_profiles()
        return user_profiles.get(user_name, {}).get("notes", [])

    def add_user_note(self, user_name, note):
        """Add a note to a specific user's profile."""
        user_profiles = self.user_profile_settings.get_user_profiles()
        if user_name in user_profiles:
            if note in user_profiles[user_name].get("notes", []):
                return False  # Prevent duplicate notes
            user_profiles[user_name]["notes"].append(note)
            self.user_profile_settings.set_user_profiles(user_profiles)
            return True
        return False

    def remove_user_note(self, user_name, note):
        """Remove a note from a specific user's profile."""
        user_profiles = self.user_profile_settings.get_user_profiles()
        if user_name in user_profiles and note in user_profiles[user_name].get(
            "notes", []
        ):
            user_profiles[user_name]["notes"].remove(note)
            self.user_profile_settings.set_user_profiles(user_profiles)
            return True
        return False
