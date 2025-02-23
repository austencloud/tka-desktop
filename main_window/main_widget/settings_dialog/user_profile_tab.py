from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from main_window.main_widget.settings_dialog.styles.card_frame import CardFrame

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class UserProfileTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self.user_manager = self.main_widget.settings_manager.users.user_manager
        self.user_buttons: dict[str, tuple[QWidget, QPushButton, QPushButton]] = {}
        self._setup_ui()

    def _setup_ui(self):
        """Creates the UI with user buttons and add/remove options."""
        card = CardFrame(self)
        layout = QVBoxLayout(card)

        # Header
        self.header = QLabel("User Profiles:")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setFont(self._get_title_font())
        layout.addWidget(self.header)

        # User buttons container
        self.user_buttons_layout = QVBoxLayout()
        layout.addLayout(self.user_buttons_layout)
        self._populate_user_buttons()

        # Input for new users
        self.new_user_field = QLineEdit(self)
        self.new_user_field.setPlaceholderText("Enter new user name")
        self.new_user_field.returnPressed.connect(self.add_user)  # Prevents dialog from closing

        # Add User button
        self.add_user_button = QPushButton("Add User", self)
        self.add_user_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_user_button.clicked.connect(self.add_user)

        # Input + Add button layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.new_user_field)
        input_layout.addWidget(self.add_user_button)
        layout.addLayout(input_layout)

        # Spacer for alignment
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Final Layout
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)

    def _populate_user_buttons(self):
        """Creates buttons for existing users."""
        users = self.user_manager.get_all_users()
        current_user = self.user_manager.get_current_user()
        for user in users:
            self._create_user_button(user, is_current=(user == current_user))

    def _create_user_button(self, user_name, is_current=False):
        """Creates a button for a user and adds it to the layout."""
        button = QPushButton(user_name, self)
        button.setFont(self._get_scaled_font())
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet(self._get_button_style(is_current))
        button.clicked.connect(lambda _, u=user_name: self._set_current_user(u))

        remove_button = QPushButton("❌", self)
        remove_button.setFixedSize(30, 30)
        remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_button.setStyleSheet("border: none; background: none; color: red; font-size: 16px;")
        remove_button.clicked.connect(lambda _, u=user_name: self.remove_user(u))

        user_layout = QHBoxLayout()
        user_layout.addWidget(button)
        user_layout.addWidget(remove_button)

        container = QWidget()
        container.setLayout(user_layout)
        self.user_buttons_layout.addWidget(container)

        self.user_buttons[user_name] = (container, button, remove_button)

    def _set_current_user(self, user_name):
        """Switches to the selected user and updates UI to reflect the change."""
        self.user_manager.set_current_user(user_name)
        self.main_widget.sequence_properties_manager.update_sequence_properties()
        self._update_user_button_styles()

    def add_user(self):
        """Adds a new user and creates a button for them."""
        new_user = self.new_user_field.text().strip()
        if new_user:
            if self.user_manager.add_new_user(new_user):
                self._create_user_button(new_user, is_current=True)
                self._update_user_button_styles()
                self.new_user_field.clear()
            else:
                self._show_warning(f"User '{new_user}' already exists.")
        else:
            self._show_warning("User name cannot be empty.")

    def remove_user(self, user_name):
        """Removes a user and deletes their button."""
        confirm = self._confirm_deletion(user_name)
        if confirm and self.user_manager.remove_user(user_name):
            container, button, remove_button = self.user_buttons.pop(user_name)
            container.deleteLater()
            self._update_user_button_styles()
        elif confirm:
            self._show_warning(f"Failed to remove user '{user_name}'.")

    def _update_user_button_styles(self):
        """Updates the styles of all user buttons to show the selected user."""
        current_user = self.user_manager.get_current_user()
        for user_name, (_, button, _) in self.user_buttons.items():
            button.setStyleSheet(self._get_button_style(user_name == current_user))

    def _confirm_deletion(self, user_name):
        """Asks for user confirmation before deletion."""
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete user '{user_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        return reply == QMessageBox.StandardButton.Yes

    def _show_warning(self, message):
        """Shows a warning message."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Warning", message)

    def _get_button_style(self, is_current=False):
        """Returns a styled button, with a different color for the active user."""
        return (
            "margin: 5px; padding: 8px; border-radius: 5px; background-color: #87CEFA; font-weight: bold;"
            if is_current else
            "margin: 5px; padding: 8px; border-radius: 5px; background-color: #f0f0f0;"
        )

    def _get_title_font(self):
        """Returns a styled font for the header."""
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def _get_scaled_font(self):
        """Returns a dynamically scaled font for user buttons."""
        font = QFont()
        font_size = max(10, self.settings_dialog.width() // 30)
        font.setPointSize(font_size)
        return font

    def resizeEvent(self, event):
        """Dynamically adjust font sizes when the window resizes."""
        self.header.setFont(self._get_title_font())
        for _, button, _ in self.user_buttons.values():
            button.setFont(self._get_scaled_font())
