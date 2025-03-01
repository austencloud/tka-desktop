from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QSize, Qt

from utils.path_helpers import get_data_path, get_image_path


if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class SettingsButton(QPushButton):
    def __init__(self, menu_bar: "MenuBarWidget") -> None:
        super().__init__(
            QIcon(get_image_path("icons\\sequence_workbench_icons\\settings.png")),
            None,
            menu_bar,
        )
        self.main_widget = menu_bar.main_widget
        self.clicked.connect(self.show_settings_dialog)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def show_settings_dialog(self):
        dialog = self.main_widget.settings_dialog
        dialog.show()

    def resizeEvent(self, event):
        size = int(self.main_widget.width() // 24)
        self.setFixedSize(QSize(size, size))
        icon_size = int(size * 0.75)
        self.setIconSize(QSize(icon_size, icon_size))
        super().resizeEvent(event)
