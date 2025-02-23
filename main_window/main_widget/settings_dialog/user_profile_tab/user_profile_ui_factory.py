from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.user_profile_tab.user_profile_tab import (
        UserProfileTab,
    )


class UserProfileUIFactory:
    """Factory class for creating UI components of the UserProfileTab."""

    @staticmethod
    def create_header(parent_tab: "UserProfileTab") -> QLabel:
        """Creates and returns the header label."""
        header = QLabel("User Profiles:")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(parent_tab.ui_manager.get_title_font())
        return header

    @staticmethod
    def create_user_input(
        parent_tab: "UserProfileTab",
    ) -> tuple[QLineEdit, QPushButton, QHBoxLayout]:
        """Creates the user input field and add button."""
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter new user name")
        input_field.returnPressed.connect(parent_tab.tab_controller.add_user)

        add_button = QPushButton("Add User")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button.clicked.connect(parent_tab.tab_controller.add_user)

        input_layout = QHBoxLayout()
        input_layout.addWidget(input_field)
        input_layout.addWidget(add_button)

        return input_field, add_button, input_layout

    @staticmethod
    def create_spacer() -> QSpacerItem:
        """Creates a spacer item for layout alignment."""
        return QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
