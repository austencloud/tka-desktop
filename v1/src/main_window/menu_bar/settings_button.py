from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QSize, Qt

from styles.styled_button import StyledButton, ButtonContext
from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class SettingsButton(StyledButton):
    """A modern, responsive, and round settings button with hover effects."""

    def __init__(self, menu_bar: "MenuBarWidget") -> None:
        super().__init__(
            "",
            icon_path=get_image_path("icons/sequence_workbench_icons/settings.png"),
            context=ButtonContext.SETTINGS,
        )
        self.main_widget = menu_bar.main_widget

        # Load icon and set defaults
        self.setIcon(
            QIcon(get_image_path("icons/sequence_workbench_icons/settings.png"))
        )
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

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

    def resizeEvent(self, event):
        """Dynamically resizes the button and icon."""
        size = max(32, self.main_widget.width() // 24)
        self.setFixedSize(QSize(size, size))

        icon_size = int(size * 0.75)
        self.setIconSize(QSize(icon_size, icon_size))

        # Update appearance to recalculate circular border radius
        self.update_appearance()
        super().resizeEvent(event)
