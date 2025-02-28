from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtCore import Qt

from main_window.main_widget.settings_dialog.card_frame import CardFrame

from .user_profile_tab_controller import UserProfileTabController
from .user_profile_ui_manager import UserProfileUIManager
from .user_profile_ui_factory import UserProfileUIFactory

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class UserProfileTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self.user_manager = self.main_widget.settings_manager.users.user_manager

        self.ui_manager = UserProfileUIManager(self)
        self.tab_controller = UserProfileTabController(self)

        self._setup_ui()

    def _setup_ui(self):
        card = CardFrame(self)

        layout = QVBoxLayout(card)
        self.header = UserProfileUIFactory.create_header(self)
        layout.addWidget(self.header)

        layout.addLayout(self.tab_controller.user_buttons_layout)

        # Add User Input
        self.new_user_field, self.add_user_button, input_layout = (
            UserProfileUIFactory.create_user_input(self)
        )
        layout.addLayout(input_layout)

        # --- Notes Section ---
        self.notes_label = QLabel("Notes:")
        self.notes_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.notes_dropdown = QComboBox(self)
        self.notes_dropdown.setPlaceholderText("Select a note")

        self.note_input = QLineEdit(self)
        self.note_input.setPlaceholderText("Enter new note")

        self.add_note_button = QPushButton("Add Note")
        self.add_note_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_note_button.clicked.connect(self.tab_controller.add_note)

        self.remove_note_button = QPushButton("Remove Note")
        self.remove_note_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_note_button.clicked.connect(self.tab_controller.remove_note)

        notes_layout = QVBoxLayout()
        notes_layout.addWidget(self.notes_label)

        dropdown_layout = QHBoxLayout()
        dropdown_layout.addWidget(self.notes_dropdown)
        dropdown_layout.addWidget(self.remove_note_button)

        notes_layout.addLayout(dropdown_layout)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.note_input)
        input_layout.addWidget(self.add_note_button)

        notes_layout.addLayout(input_layout)
        layout.addLayout(notes_layout)

        layout.addSpacerItem(UserProfileUIFactory.create_spacer())

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)

        self.tab_controller.populate_user_buttons()
        self.tab_controller.populate_notes()

    def resizeEvent(self, event):
        self.ui_manager.handle_resize_event()
