from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout
from main_window.main_widget.settings_dialog.user_profile_tab.user_profile_button import (
    UserProfileButton,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.user_profile_tab.user_profile_tab import (
        UserProfileTab,
    )


class UserProfileTabController:
    """Manages user profile buttons (creation, updates, and removal)."""

    def __init__(self, user_profile_tab: "UserProfileTab"):
        self.tab = user_profile_tab
        self.user_manager = self.tab.user_manager
        self.user_buttons: dict[str, UserProfileButton] = {}
        self.user_buttons_layout = QVBoxLayout()

    def populate_user_buttons(self):
        """Creates buttons for existing users and ensures the current user is highlighted."""
        users = self.user_manager.get_all_users()
        current_user = self.user_manager.get_current_user()

        print(f"[DEBUG] Populating user buttons... Current user: {current_user}")

        # Clear existing buttons (prevents duplicates)
        for user_button in self.user_buttons.values():
            user_button.deleteLater()
        self.user_buttons.clear()

        for user in users:
            is_current = (user == current_user)
            print(f"[DEBUG] Creating button for user: {user} (is_current={is_current})")
            self.create_user_button(user, is_current=is_current)

        # 🔥 Ensure we apply styles after all buttons are created
        self.tab.ui_manager.update_user_button_styles()
        self.tab.update()


    def create_user_button(self, user_name, is_current=False):
        """Creates a button for a user and adds it to the layout."""
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
        """Switches to the selected user and updates UI."""
        self.user_manager.set_current_user(user_name)
        self.tab.main_widget.sequence_properties_manager.update_sequence_properties()
        self.tab.ui_manager.update_user_button_styles()

    def add_user(self):
        """Adds a new user and creates a button for them."""
        new_user = self.tab.new_user_field.text().strip()
        if new_user:
            if self.user_manager.add_new_user(new_user):
                self.create_user_button(new_user, is_current=True)
                self.tab.ui_manager.update_user_button_styles()
                self.tab.new_user_field.clear()
            else:
                self.tab.ui_manager.show_warning(f"User '{new_user}' already exists.")
        else:
            self.tab.ui_manager.show_warning("User name cannot be empty.")

    def remove_user(self, user_name):
        """Removes a user and deletes their button."""
        confirm = self.tab.ui_manager.confirm_deletion(user_name)
        if confirm and self.user_manager.remove_user(user_name):
            user_button = self.user_buttons.pop(user_name)
            user_button.deleteLater()
            self.tab.ui_manager.update_user_button_styles()
        elif confirm:
            self.tab.ui_manager.show_warning(f"Failed to remove user '{user_name}'.")
