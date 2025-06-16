"""
Settings dialog coordinator - orchestrates all dialog components.

This replaces the monolithic ModernSettingsDialog with a coordinator pattern
that manages smaller, focused components.
"""

from typing import TYPE_CHECKING, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal, QEvent, Qt
from PyQt6.QtWidgets import QDialog
import logging

if TYPE_CHECKING:
    from src.core.application_context import ApplicationContext
    from main_window.main_widget.main_widget import MainWidget

logger = logging.getLogger(__name__)


class SettingsDialogCoordinator(QObject):
    """
    Coordinates all settings dialog components following SRP.

    Responsibilities:
    - Orchestrate component initialization
    - Coordinate component interactions
    - Handle dialog lifecycle events
    - Maintain component references
    """

    # Signals
    settings_applied = pyqtSignal(bool)  # success
    dialog_closed = pyqtSignal()

    def __init__(
        self,
        dialog: QDialog,
        main_widget: "MainWidget",
        app_context: "ApplicationContext" = None,
    ):
        super().__init__(dialog)
        self.dialog = dialog
        self.main_widget = main_widget
        self.app_context = app_context

        # Component managers
        self.config_manager = None
        self.layout_manager = None
        self.styling_manager = None
        self.tab_manager = None
        self.event_coordinator = None

        # Component references
        self.components: Dict[str, Any] = {}
        self.tabs: Dict[str, Any] = {}

        # Drag functionality for frameless window
        self.drag_position = None

        # Initialize services
        self._initialize_services()

    def _initialize_services(self):
        """Initialize core services and managers."""
        try:
            # Get settings manager from dependency injection
            if self.app_context:
                self.settings_manager = self.app_context.settings_manager
            else:
                # Fallback to legacy AppContext
                from src.legacy_settings_manager.global_settings.app_context import AppContext

                self.settings_manager = AppContext.settings_manager()

            # Initialize state manager
            from ..core.settings_state_manager import SettingsStateManager

            self.state_manager = SettingsStateManager(self.settings_manager)

            logger.debug("Core services initialized")

        except Exception as e:
            logger.error(f"Error initializing services: {e}")
            raise

    def initialize_dialog(self):
        """Initialize the complete dialog with all components."""
        try:
            logger.info("Initializing settings dialog coordinator...")

            # Initialize component managers
            self._initialize_managers()

            # Setup dialog configuration
            self.config_manager.setup_dialog()

            # Setup layout and get component references
            self.components = self.layout_manager.setup_layout()

            # Create and setup tabs
            self.tabs = self.tab_manager.create_tabs(
                self.components["sidebar"], self.components["content_area"]
            )

            # Setup event handling
            self.event_coordinator.setup_connections(self.components, self.tabs)

            # Apply styling
            self.styling_manager.apply_styling(self.components, self.tabs)

            # Connect coordinator signals
            self._connect_coordinator_signals()

            logger.info("Settings dialog coordinator initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing dialog coordinator: {e}")
            raise

    def _initialize_managers(self):
        """Initialize all component managers."""
        from .dialog_configuration_manager import DialogConfigurationManager
        from .dialog_layout_manager import DialogLayoutManager
        from .dialog_styling_manager import DialogStylingManager
        from ..tabs.settings_tab_manager import SettingsTabManager
        from ..events.settings_event_coordinator import SettingsEventCoordinator

        self.config_manager = DialogConfigurationManager(
            self.dialog, self.main_widget, self.app_context
        )
        self.layout_manager = DialogLayoutManager(self.dialog, self.app_context)
        self.styling_manager = DialogStylingManager(self.dialog, self.app_context)
        self.tab_manager = SettingsTabManager(
            self.settings_manager, self.state_manager, self.app_context, self.dialog
        )
        self.event_coordinator = SettingsEventCoordinator(
            self.settings_manager,
            self.state_manager,
            self.tab_manager,
            self.app_context,
            self,
        )

    def _connect_coordinator_signals(self):
        """Connect coordinator-level signals."""
        # Forward event coordinator signals
        self.event_coordinator.settings_applied.connect(self.settings_applied.emit)
        self.event_coordinator.dialog_closed.connect(self._handle_dialog_close)

    def _handle_dialog_close(self):
        """Handle dialog close request."""
        self.dialog_closed.emit()
        self.dialog.reject()

    def show_dialog(self):
        """Show the dialog and handle show event."""
        try:
            # Center the dialog when shown
            self.config_manager.center_dialog()

            # Restore last selected tab
            self._restore_last_selected_tab()

            # Update specific tabs
            tab_order = self.tab_manager.get_tab_order()
            last_tab = self._get_last_selected_tab()
            self.event_coordinator.update_tab_on_show(last_tab or tab_order[0])

        except Exception as e:
            logger.error(f"Error in show dialog: {e}")

    def _restore_last_selected_tab(self):
        """Restore the last selected tab."""
        try:
            last_tab = self._get_last_selected_tab()
            if last_tab:
                tab_order = self.tab_manager.get_tab_order()
                if last_tab in tab_order:
                    tab_index = tab_order.index(last_tab)
                    self.components["sidebar"].setCurrentRow(tab_index)
                    self.components["content_area"].setCurrentIndex(tab_index)
        except Exception as e:
            logger.error(f"Error restoring last selected tab: {e}")

    def _get_last_selected_tab(self) -> str:
        """Get the last selected tab from settings."""
        try:
            if self.settings_manager and hasattr(
                self.settings_manager, "global_settings"
            ):
                return (
                    self.settings_manager.global_settings.get_current_settings_dialog_tab()
                )
        except Exception as e:
            logger.error(f"Error getting last selected tab: {e}")
        return None

    def handle_mouse_press(self, event):
        """Handle mouse press for dragging frameless dialog."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Store the position where the mouse was pressed
            self.drag_position = (
                event.globalPosition().toPoint() - self.dialog.frameGeometry().topLeft()
            )
            event.accept()
        else:
            QDialog.mousePressEvent(self.dialog, event)

    def handle_mouse_move(self, event):
        """Handle mouse move for dragging frameless dialog."""
        if (
            event.buttons() == Qt.MouseButton.LeftButton
            and self.drag_position is not None
        ):
            # Move the dialog to the new position
            self.dialog.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
        else:
            QDialog.mouseMoveEvent(self.dialog, event)

    def handle_mouse_release(self, event):
        """Handle mouse release to stop dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()
        else:
            QDialog.mouseReleaseEvent(self.dialog, event)

    def handle_close_event(self, event):
        """Handle dialog close event."""
        try:
            # Check for unsaved changes
            if self.state_manager.is_modified():
                # Changes will be handled by cancel/ok buttons
                pass

            self.dialog_closed.emit()

        except Exception as e:
            logger.error(f"Error in close event: {e}")

    def get_tab(self, tab_name: str):
        """Get a specific tab widget."""
        return self.tab_manager.get_tab(tab_name)

    def refresh_all_tabs(self):
        """Refresh all tab contents."""
        self.tab_manager.refresh_all_tabs()
