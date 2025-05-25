from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QSize, Qt

from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class SettingsButton(QPushButton):
    """A modern, responsive, and round settings button with hover effects."""

    def __init__(self, menu_bar: "MenuBarWidget") -> None:
        super().__init__(menu_bar)
        self.main_widget = menu_bar.main_widget

        # Load icon and set defaults
        self.setIcon(
            QIcon(get_image_path("icons/sequence_workbench_icons/settings.png"))
        )
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self._update_style()
        self.clicked.connect(self.show_settings_dialog)

    def show_settings_dialog(self):
        """Opens the settings dialog."""
        try:
            dialog = self.main_widget.widget_manager.get_widget("settings_dialog")
            if dialog:
                dialog.show()
        except AttributeError:
            # Fallback when settings_dialog not available
            import logging

            logger = logging.getLogger(__name__)
            logger.warning("settings_dialog not available")

    def enterEvent(self, event):
        """Change style on hover."""
        self.setStyleSheet(self._get_hover_style())

    def leaveEvent(self, event):
        """Revert style when hover ends."""
        self._update_style()

    def resizeEvent(self, event):
        """Dynamically resizes the button and icon."""
        size = max(32, self.main_widget.width() // 24)
        self.setFixedSize(QSize(size, size))

        icon_size = int(size * 0.75)
        self.setIconSize(QSize(icon_size, icon_size))

        self._update_style()
        super().resizeEvent(event)

    def _update_style(self):
        """Applies default styling."""
        radius = self.width() // 2
        self.setStyleSheet(self._get_style(radius))

    def _get_style(self, radius):
        """Returns the default button style."""
        return f"""
            QPushButton {{
                background-color: #D3D3D3;  /* Light gray background */
                border: 2px solid #AAAAAA;
                border-radius: {radius}px;
                padding: 5px;
            }}
            QPushButton:pressed {{
                background-color: #B0B0B0;  /* Slightly darker gray when pressed */
                border: 2px solid #DDDDDD;
            }}
        """

    def _get_hover_style(self):
        """Returns the hover style."""
        radius = self.width() // 2
        return f"""
            QPushButton {{
                background-color: #C0C0C0;  /* Another shade of gray for hover */
                border: 2px solid #FFFFFF;
                border-radius: {radius}px;
            }}
        """
