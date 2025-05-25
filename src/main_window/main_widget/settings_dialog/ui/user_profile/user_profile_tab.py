from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QSizePolicy,
    QPushButton,
    QMessageBox,
    QDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from main_window.main_widget.settings_dialog.card_frame import CardFrame
from main_window.main_widget.settings_dialog.ui.user_profile.add_user_dialog import (
    AddUserDialog,
)
from main_window.main_widget.settings_dialog.ui.user_profile.profile_picture_manager import (
    ProfilePictureManager,
)
from main_window.main_widget.settings_dialog.ui.user_profile.user_button import (
    UserButton,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class UserProfileTab(QWidget):
    """User Profile Tab with profile picture support."""

    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget

        # Get user_manager from dependency injection system
        try:
            settings_manager = self.main_widget.app_context.settings_manager
            self.user_manager = settings_manager.users.user_manager
        except AttributeError:
            # Fallback for cases where app_context is not available during initialization
            self.user_manager = None
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "settings_manager not available during UserProfileTab initialization"
            )

        self.user_buttons: dict[str, UserButton] = {}

        self._setup_ui()

    def _setup_ui(self):
        # Main layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)

        # Card with shadow/border
        self.card = CardFrame(self)
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        # Compact Header with management buttons
        header_layout = QHBoxLayout()

        # Smaller, more compact header
        self.header = QLabel("User Profiles")
        self.header.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        self.header.setFont(header_font)

        # Add user button - square with rounded edges
        self.add_button = self._create_square_button("+", "Add new user")
        self.add_button.clicked.connect(self._show_add_user_dialog)

        # Delete user button - square with rounded edges
        self.delete_button = self._create_square_button("🗑️", "Delete selected user")
        self.delete_button.clicked.connect(self._delete_selected_user)

        header_layout.addWidget(self.header, 1)
        header_layout.addWidget(self.add_button, 0)
        header_layout.addWidget(self.delete_button, 0)
        card_layout.addLayout(header_layout)

        # User Buttons Container
        self.users_container = QWidget()
        self.grid_layout = QGridLayout(self.users_container)
        self.grid_layout.setSpacing(15)
        card_layout.addWidget(self.users_container, 1)

        outer_layout.addWidget(self.card)

        # Populate initial users
        self.populate_users()

    def _create_square_button(self, text: str, tooltip: str) -> QPushButton:
        """Creates a square button with rounded edges."""
        button = QPushButton(text, self)
        button.setToolTip(tooltip)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Make the button square
        button_size = 40
        button.setFixedSize(button_size, button_size)

        # Set font
        font = button.font()
        font.setPointSize(16)
        button.setFont(font)

        # Style with rounded edges
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
            QPushButton:pressed {{
                background-color: #d0d0d0;
            }}
            """
        )

        return button

    def _show_add_user_dialog(self):
        """Shows a dialog to add a new user with profile picture."""
        dialog = AddUserDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_name, profile_pixmap = dialog.get_user_info()
            if user_name:
                self.add_user(user_name, profile_pixmap)
            else:
                self._show_warning("User name cannot be empty.")

    def _delete_selected_user(self):
        """Deletes the currently selected user after confirmation."""
        if not self.user_manager:
            self._show_warning("User manager not available.")
            return

        current_user = self.user_manager.get_current_user()

        if not current_user:
            self._show_warning("No user selected.")
            return

        if len(self.user_buttons) <= 1:
            self._show_warning("Cannot delete the last user.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete user '{current_user}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.remove_user(current_user)

    def populate_users(self):
        """Populates the user buttons in the grid layout."""
        if not self.user_manager:
            # Show message when user manager is not available
            empty_label = QLabel("User manager not available.")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(empty_label, 0, 0, 1, 3)
            return

        # Clear existing buttons
        for button in self.user_buttons.values():
            self.grid_layout.removeWidget(button)
            button.deleteLater()
        self.user_buttons.clear()

        # Remove any existing empty label
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.text().startswith(
                "No users created yet"
            ):
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()

        users = self.user_manager.get_all_users()
        current_user = self.user_manager.get_current_user()

        if not users:
            # Show message when no users exist
            empty_label = QLabel("No users created yet. Click '+' to add a new user.")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(empty_label, 0, 0, 1, 3)
            return

        # Add user buttons in a grid (3 columns)
        for i, user in enumerate(users):
            row, col = divmod(i, 3)
            button = UserButton(user, self, user == current_user)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.grid_layout.addWidget(button, row, col)
            self.user_buttons[user] = button

        # Update sizes
        self._update_button_sizes()

    def set_current_user(self, user_name: str):
        """Sets the current active user."""
        if not self.user_manager:
            return

        self.user_manager.set_current_user(user_name)
        for name, button in self.user_buttons.items():
            button.set_current(name == user_name)

    def add_user(self, user_name: str, profile_pixmap: Optional[QPixmap] = None):
        """Adds a new user with optional profile picture."""
        if not self.user_manager:
            self._show_warning("User manager not available.")
            return

        if not user_name:
            self._show_warning("User name cannot be empty.")
            return

        if user_name in self.user_buttons:
            self._show_warning(f"User '{user_name}' already exists.")
            return

        # Add user to the user manager
        if self.user_manager.add_new_user(user_name):
            # Save profile picture if provided
            if profile_pixmap and not profile_pixmap.isNull():
                ProfilePictureManager.save_profile_picture(user_name, profile_pixmap)

            # Set as current user if no user is currently selected
            if not self.user_manager.get_current_user():
                self.user_manager.set_current_user(user_name)

            self.populate_users()

    def remove_user(self, user_name: str):
        """Removes a user and updates the UI."""
        if not self.user_manager:
            self._show_warning("User manager not available.")
            return

        if len(self.user_buttons) <= 1:
            self._show_warning("Cannot delete the last user.")
            return

        if self.user_manager.remove_user(user_name):
            # Also remove the profile picture
            ProfilePictureManager.delete_profile_picture(user_name)
            self.populate_users()

    def _show_warning(self, message: str):
        """Shows a warning message dialog."""
        QMessageBox.warning(self, "Warning", message)

    def _update_button_sizes(self):
        """Updates the sizes of user buttons based on available space."""
        for button in self.user_buttons.values():
            button.update_size()

    def resizeEvent(self, event):
        """Handles resize events to update UI element sizes."""
        super().resizeEvent(event)
        self._update_button_sizes()

    def update_active_user_from_settings(self):
        """Updates the active user from settings."""
        if not self.user_manager:
            return

        current_user = self.user_manager.get_current_user()
        for name, button in self.user_buttons.items():
            button.set_current(name == current_user)
