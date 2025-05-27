"""
Dialog configuration manager for the modern settings dialog.

Handles dialog setup, positioning, and window properties.
"""

from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QApplication
import logging

if TYPE_CHECKING:
    from src.core.application_context import ApplicationContext
    from main_window.main_widget.main_widget import MainWidget

logger = logging.getLogger(__name__)


class DialogConfigurationManager:
    """
    Manages dialog configuration and positioning.
    
    Responsibilities:
    - Setup dialog properties (frameless, modal, etc.)
    - Handle dialog positioning and centering
    - Manage window flags and attributes
    """

    def __init__(self, dialog: QDialog, main_widget: "MainWidget", app_context: "ApplicationContext" = None):
        self.dialog = dialog
        self.main_widget = main_widget
        self.app_context = app_context

    def setup_dialog(self):
        """Setup modern frameless dialog properties."""
        self.dialog.setWindowTitle("Settings")
        self.dialog.setModal(True)

        # Remove window frame for modern modal appearance
        self.dialog.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        # Set transparent background for glassmorphism effect
        self.dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set a larger size for better content accommodation
        self.dialog.setFixedSize(1400, 900)

        # Center the dialog properly
        self.center_dialog()

        logger.debug("Modern frameless dialog setup complete")

    def center_dialog(self):
        """Center the dialog on the screen or parent window."""
        try:
            # Get the main window to center on
            main_window = self._get_main_window()

            if main_window and main_window.isVisible():
                self._center_on_main_window(main_window)
                return

            # Fallback: center on primary screen
            self._center_on_primary_screen()

        except Exception as e:
            logger.error(f"Error centering dialog: {e}")
            # Ultimate fallback
            self.dialog.move(200, 200)

    def _get_main_window(self) -> Optional[object]:
        """Get the main window from the main_widget."""
        if not self.main_widget:
            return None

        # Try different ways to get the main window
        if hasattr(self.main_widget, "window"):
            return self.main_widget.window()
        elif hasattr(self.main_widget, "parent") and self.main_widget.parent():
            main_window = self.main_widget.parent()
            while main_window and main_window.parent():
                main_window = main_window.parent()
            return main_window

        return None

    def _center_on_main_window(self, main_window):
        """Center the dialog on the main window."""
        main_geometry = main_window.geometry()
        dialog_width = self.dialog.width()
        dialog_height = self.dialog.height()

        # Calculate center position relative to main window
        x = main_geometry.x() + (main_geometry.width() - dialog_width) // 2
        y = main_geometry.y() + (main_geometry.height() - dialog_height) // 2

        # Get the screen that contains the main window
        screen = main_window.screen() if hasattr(main_window, "screen") else None
        if not screen:
            screen = QApplication.screenAt(main_window.pos())

        if screen:
            screen_geometry = screen.availableGeometry()
            # Ensure dialog stays within the screen bounds
            x = max(
                screen_geometry.x(),
                min(
                    x,
                    screen_geometry.x() + screen_geometry.width() - dialog_width,
                ),
            )
            y = max(
                screen_geometry.y(),
                min(
                    y,
                    screen_geometry.y() + screen_geometry.height() - dialog_height,
                ),
            )

        self.dialog.move(x, y)
        logger.debug(f"Centered dialog on main window at ({x}, {y})")

    def _center_on_primary_screen(self):
        """Center the dialog on the primary screen."""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            dialog_width = self.dialog.width()
            dialog_height = self.dialog.height()

            x = screen_geometry.x() + (screen_geometry.width() - dialog_width) // 2
            y = screen_geometry.y() + (screen_geometry.height() - dialog_height) // 2

            self.dialog.move(x, y)
            logger.debug(f"Centered dialog on primary screen at ({x}, {y})")
        else:
            # Ultimate fallback
            self.dialog.move(200, 200)
            logger.debug("Used fallback position (200, 200)")
