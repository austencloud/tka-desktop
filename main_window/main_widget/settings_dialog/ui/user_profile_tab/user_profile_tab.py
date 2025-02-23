from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from .user_profile_tab_controller import UserProfileTabController
from .user_profile_ui_factory import UserProfileUIFactory
from .user_profile_ui_manager import UserProfileUIManager


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
        from main_window.main_widget.settings_dialog.styles.card_frame import CardFrame

        card = CardFrame(self)
        layout = QVBoxLayout(card)

        self.header = UserProfileUIFactory.create_header(self)
        layout.addWidget(self.header)

        layout.addLayout(self.tab_controller.user_buttons_layout)
        self.tab_controller.populate_user_buttons()

        self.new_user_field, self.add_user_button, input_layout = (
            UserProfileUIFactory.create_user_input(self)
        )
        layout.addLayout(input_layout)

        layout.addSpacerItem(UserProfileUIFactory.create_spacer())

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)

    def resizeEvent(self, event):
        self.ui_manager.handle_resize_event()

