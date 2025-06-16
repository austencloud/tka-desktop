"""
Modern Settings Dialog - Refactored with coordinator pattern.

This is now a lightweight wrapper around the SettingsDialogCoordinator
that maintains backward compatibility while using the new architecture.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QEvent, pyqtSignal
import logging

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from src.core.application_context import ApplicationContext

logger = logging.getLogger(__name__)


class LegacySettingsDialog(QDialog):
    """
    Modern settings dialog - now a lightweight wrapper around SettingsDialogCoordinator.

    This maintains backward compatibility while using the new refactored architecture.
    """

    # Signals
    settings_applied = pyqtSignal(bool)  # success
    dialog_closed = pyqtSignal()

    def __init__(
        self, main_widget: "MainWidget", app_context: "ApplicationContext" = None
    ):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.app_context = app_context

        # Initialize the coordinator that handles all the complexity
        from .core.settings_dialog_coordinator import SettingsDialogCoordinator

        self.coordinator = SettingsDialogCoordinator(self, main_widget, app_context)

        # Initialize the dialog through the coordinator
        self.coordinator.initialize_dialog()

        # Connect coordinator signals to our signals for backward compatibility
        self.coordinator.settings_applied.connect(self.settings_applied.emit)
        self.coordinator.dialog_closed.connect(self.dialog_closed.emit)

        logger.info("Modern Settings Dialog initialized with coordinator pattern")

    # Backward compatibility methods - delegate to coordinator
    def showEvent(self, event: QEvent):
        """Handle dialog show event."""
        super().showEvent(event)
        self.coordinator.show_dialog()

    def mousePressEvent(self, event):
        """Handle mouse press for dragging frameless dialog."""
        self.coordinator.handle_mouse_press(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging frameless dialog."""
        self.coordinator.handle_mouse_move(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop dragging."""
        self.coordinator.handle_mouse_release(event)

    def closeEvent(self, event):
        """Handle dialog close event."""
        self.coordinator.handle_close_event(event)
        super().closeEvent(event)

    # Backward compatibility properties
    @property
    def tabs(self):
        """Get tabs dictionary for backward compatibility."""
        return self.coordinator.tabs if hasattr(self.coordinator, "tabs") else {}

    def get_tab(self, tab_name: str):
        """Get a specific tab widget."""
        return self.coordinator.get_tab(tab_name)

    def refresh_all_tabs(self):
        """Refresh all tab contents."""
        self.coordinator.refresh_all_tabs()
