from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout
from .user_profile_button import UserProfileButton

if TYPE_CHECKING:
    from .user_profile_tab import UserProfileTab


class UserProfileTabController:
    def __init__(self, user_profile_tab: "UserProfileTab"):
        self.tab = user_profile_tab
        self.user_manager = self.tab.user_manager
        self.user_buttons: dict[str, UserProfileButton] = {}
        self.user_buttons_layout = QVBoxLayout()

    def populate_user_buttons(self):
        users = self.user_manager.get_all_users()
        current_user = self.user_manager.get_current_user()

        for user_button in self.user_buttons.values():
            user_button.deleteLater()
        self.user_buttons.clear()

        for user in users:
            is_current = user == current_user
            self.create_user_button(user, is_current)

        self.populate_notes()

    def create_user_button(self, user_name, is_current=False):
        """Create a button for each user."""
        user_button = UserProfileButton(user_name, self.tab, is_current)
        user_button.button.clicked.connect(
            lambda _, u=user_name: self.set_current_user(u)
        )
        user_button.remove_button.clicked.connect(
            lambda _, u=user_name: self.remove_user(u)
        )

        self.user_buttons_layout.addWidget(user_button)
        self.user_buttons[user_name] = user_button

    def set_current_user(self, user_name):
        """Switch to the selected user and refresh notes."""
        self.user_manager.set_current_user(user_name)
        self.tab.ui_manager.update_active_user_from_settings()
        self.populate_notes()

    def populate_notes(self):
        """Populate the notes dropdown with notes from the selected user."""
        self.tab.notes_dropdown.clear()
        current_user = self.user_manager.get_current_user()
        notes = self.user_manager.get_user_notes(current_user)

        if notes:
            self.tab.notes_dropdown.addItems(notes)

    def add_note(self):
        """Add a new note for the selected user."""
        new_note = self.tab.note_input.text().strip()
        if new_note:
            current_user = self.user_manager.get_current_user()
            if self.user_manager.add_user_note(current_user, new_note):
                self.tab.notes_dropdown.addItem(new_note)
                self.tab.note_input.clear()
            else:
                self.tab.ui_manager.show_warning(f"Note '{new_note}' already exists.")

    def remove_note(self):
        """Remove the selected note from the user."""
        selected_note = self.tab.notes_dropdown.currentText()
        if selected_note:
            current_user = self.user_manager.get_current_user()
            if self.user_manager.remove_user_note(current_user, selected_note):
                self.tab.notes_dropdown.removeItem(
                    self.tab.notes_dropdown.currentIndex()
                )

    def remove_user(self, user_name):
        """Remove the selected user and refresh the user buttons."""
        if self.user_manager.remove_user(user_name):
            self.populate_user_buttons()
            self.tab.ui_manager.update_active_user_from_settings()

    def add_user(self):
        """Handles adding a new user from the input field."""
        new_user_name = self.tab.new_user_field.text().strip()
        if not new_user_name:
            self.tab.ui_manager.show_warning("User name cannot be empty.")
            return

        if self.user_manager.add_new_user(new_user_name):
            self.populate_user_buttons()  # Refresh the list of users
            self.tab.new_user_field.clear()
        else:
            self.tab.ui_manager.show_warning(f"User '{new_user_name}' already exists.")
