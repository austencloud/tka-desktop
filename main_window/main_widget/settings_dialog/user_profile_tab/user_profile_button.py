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

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class UserProfileButton(QWidget):
    """A widget containing a user button and a remove button."""

    def __init__(self, user_name: str, parent: QWidget, is_current: bool = False):
        super().__init__(parent)
        self.user_name = user_name
        self.button = QPushButton(user_name, self)
        self.remove_button = QPushButton("❌", self)
        self._setup_ui(is_current)

    def _setup_ui(self, is_current: bool):
        """Sets up the UI for the user profile button."""
        self.button.setFont(self._get_scaled_font())
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setStyleSheet(self._get_button_style(is_current))

        self.remove_button.setFixedSize(30, 30)
        self.remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_button.setStyleSheet(
            "border: none; background: none; color: red; font-size: 16px;"
        )

        user_layout = QHBoxLayout()
        user_layout.addWidget(self.button)
        user_layout.addWidget(self.remove_button)

        self.setLayout(user_layout)

    def _get_button_style(self, is_current: bool = False) -> str:
        """Returns a styled button, with a different color for the active user."""
        return (
            "margin: 5px; padding: 8px; border-radius: 5px; background-color: #87CEFA; font-weight: bold;"
            if is_current
            else "margin: 5px; padding: 8px; border-radius: 5px; background-color: #f0f0f0;"
        )

    def _get_scaled_font(self) -> QFont:
        """Returns a dynamically scaled font for user buttons."""
        font = QFont()
        font_size = 10  # Default size
        if self.parentWidget():
            font_size = max(10, self.parentWidget().width() // 30)
        font.setPointSize(font_size)
        return font

    def set_button_style(self, is_current: bool):
        """Updates the button style based on whether the user is current."""
        self.button.setStyleSheet(self._get_button_style(is_current))
