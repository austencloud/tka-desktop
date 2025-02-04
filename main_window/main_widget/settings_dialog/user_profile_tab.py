from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from main_window.main_widget.settings_dialog.styles.card_frame import CardFrame


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class UserProfileTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self._setup_ui()

    def _setup_ui(self):
        card = CardFrame(self)
        layout = QVBoxLayout(card)

        self.header = QLabel("User:")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)

        user_manager = self.main_widget.settings_manager.users.user_manager
        users = user_manager.get_all_users()

        for user in users:
            button = QPushButton(user)
            button.setFont(self._get_default_font())
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("margin: 5px;")
            button.clicked.connect(lambda _, u=user: self._set_current_user(u))
            layout.addWidget(button)

        edit_users_button = QPushButton("Edit Users")
        edit_users_button.setFont(self._get_default_font())
        edit_users_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_users_button.clicked.connect(user_manager.open_edit_users_dialog)
        layout.addWidget(edit_users_button)

        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

    def _set_current_user(self, user_name: str):
        user_manager = self.main_widget.settings_manager.users.user_manager
        user_manager.set_current_user(user_name)
        self.main_widget.sequence_properties_manager.update_sequence_properties()

    def _get_title_font(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def _get_default_font(self):
        font = QFont()
        font_size = self.width() // 30
        font.setPointSize(font_size)
        return font

    def resizeEvent(self, event):
        font = QFont()
        font_size = self.settings_dialog.width() // 30
        font.setPointSize(font_size)
        font.setBold(True)
        self.header.setFont(font)
