from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon

if TYPE_CHECKING:
    from .user_profile_tab import UserProfileTab



class AddUserButton(QPushButton):
    """Button for adding a new user with plus icon."""

    def __init__(self, user_tab: "UserProfileTab", centered=False):
        super().__init__(user_tab)
        self.parent_tab = user_tab

        # Text and styling
        self.setText("Add User")
        self.setIcon(self._create_plus_icon())
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Size and alignment
        if centered:
            self.setFixedSize(150, 60)

        # Apply consistent styling
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        )

        # Connect click event
        self.clicked.connect(self._on_clicked)

    def _create_plus_icon(self):
        """Alternative to using a real icon - can be used if no icon resource available."""
        # You would typically use QIcon from a file: return QIcon("path/to/plus.svg")
        # But this is a fallback if needed
        return QIcon()

    def _on_clicked(self):
        """Show dialog to add a new user."""

        self.parent_tab.add_user()
