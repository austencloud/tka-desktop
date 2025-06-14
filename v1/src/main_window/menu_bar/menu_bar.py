from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from main_window.menu_bar.navigation_widget.menu_bar_nav_widget import MenuBarNavWidget
from main_window.menu_bar.settings_button import SettingsButton
from .social_media_widget import SocialMediaWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MenuBarWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_widget.splash_screen.updater.update_progress("MenuBarWidget")

        self.social_media_widget = SocialMediaWidget(self)
        self.navigation_widget = MenuBarNavWidget(self)
        self.settings_button = SettingsButton(self)

    def resizeEvent(self, event):
        self.social_media_widget.resize_social_media_buttons()
