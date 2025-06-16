"""
Widget manager responsible for managing non-tab widgets.

This component follows SRP by focusing solely on widget lifecycle management.
"""

from typing import TYPE_CHECKING, Dict, Optional, Any
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject, pyqtSignal
import logging

from core.application_context import ApplicationContext

if TYPE_CHECKING:
    from .main_widget_coordinator import MainWidgetCoordinator

logger = logging.getLogger(__name__)


class WidgetManager(QObject):
    """
    Manages non-tab widgets with clear separation of concerns.

    Responsibilities:
    - Create and manage widget instances
    - Handle widget lifecycle
    - Provide widget access interface
    - Manage widget dependencies
    """

    widget_ready = pyqtSignal(str)  # widget_name
    widget_error = pyqtSignal(str, str)  # widget_name, error_message

    def __init__(
        self, coordinator: "MainWidgetCoordinator", app_context: ApplicationContext
    ):
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.app_context = app_context
        self._widgets: Dict[str, QWidget] = {}
        self._widget_factories = {}

        # Register widget factories
        self._register_widget_factories()

    def _register_widget_factories(self) -> None:
        """Register factories for creating different widget types."""
        try:
            from main_window.main_widget.sequence_workbench.sequence_workbench_factory import (
                SequenceWorkbenchFactory,
            )
            from main_window.main_widget.settings_dialog.settings_dialog_factory import (
                SettingsDialogFactory,
            )
            from main_window.main_widget.full_screen_image_overlay_factory import (
                FullScreenImageOverlayFactory,
            )
            from main_window.main_widget.codex.codex_factory import CodexFactory
            from main_window.main_widget.fade_manager.fade_manager_factory import (
                FadeManagerFactory,
            )
            from main_window.main_widget.font_color_updater.font_color_updater_factory import (
                FontColorUpdaterFactory,
            )
            from main_window.main_widget.pictograph_collector_factory import (
                PictographCollectorFactory,
            )
            from main_window.main_widget.main_background_widget.main_background_widget_factory import (
                MainBackgroundWidgetFactory,
            )
            from main_window.menu_bar.menu_bar_factory import MenuBarFactory

            self._widget_factories = {
                "sequence_workbench": SequenceWorkbenchFactory,
                "settings_dialog": SettingsDialogFactory,
                "full_screen_overlay": FullScreenImageOverlayFactory,
                "codex": CodexFactory,
                "fade_manager": FadeManagerFactory,
                "font_color_updater": FontColorUpdaterFactory,
                "pictograph_collector": PictographCollectorFactory,
                "background_widget": MainBackgroundWidgetFactory,
                "menu_bar": MenuBarFactory,
            }

        except ImportError as e:
            logger.error(f"Failed to import widget factory: {e}")

    def initialize_widgets(self) -> None:
        """Initialize core widgets that are needed immediately."""
        # Create essential widgets first
        essential_widgets = [
            "sequence_workbench",
            "settings_dialog",
            "background_widget",  # Re-enabled with fixed positioning
            "menu_bar",
            "fade_manager",
            "font_color_updater",
            "pictograph_collector",
        ]

        for widget_name in essential_widgets:
            self._create_widget(widget_name)

        logger.info("Initialized essential widgets")

    def _create_widget(self, widget_name: str) -> Optional[QWidget]:
        """
        Create a widget instance if it doesn't exist.

        Args:
            widget_name: Name of the widget to create

        Returns:
            The widget instance or None if creation failed
        """
        if widget_name in self._widgets:
            return self._widgets[widget_name]

        if widget_name not in self._widget_factories:
            logger.error(f"No factory registered for widget: {widget_name}")
            self.widget_error.emit(widget_name, "No factory registered")
            return None

        try:
            factory = self._widget_factories[widget_name]

            # Create widget with dependency injection
            widget = factory.create(
                parent=self.coordinator, app_context=self.app_context
            )

            self._widgets[widget_name] = widget

            # Perform any post-creation setup
            self._setup_widget(widget_name, widget)

            self.widget_ready.emit(widget_name)
            logger.info(f"Created widget: {widget_name}")

            return widget

        except Exception as e:
            error_msg = f"Failed to create widget {widget_name}: {e}"
            logger.error(error_msg)
            self.widget_error.emit(widget_name, str(e))
            return None

    def _setup_widget(self, widget_name: str, widget: QWidget) -> None:
        """Perform post-creation setup for specific widgets."""
        if widget_name == "background_widget":
            # DON'T add background widget to the layout - it should be a child widget with manual positioning
            # The background widget sets its own geometry and should not be layout-managed
            # Just ensure it's sent to the back of the stacking order
            widget.lower()  # Send background widget to the back of the stacking order

        elif widget_name == "sequence_workbench":
            # Set up sequence workbench in app context if needed
            # This replaces the old AppContext.set_sequence_beat_frame call
            if hasattr(widget, "beat_frame"):
                # Store reference for components that need it
                self._sequence_beat_frame = widget.beat_frame

                # Register the sequence beat frame in AppContext for legacy compatibility
                try:
                    from src.legacy_settings_manager.global_settings.app_context import (
                        AppContext,
                    )

                    AppContext.set_sequence_beat_frame(widget.beat_frame)
                    logger.info("Sequence beat frame registered in AppContext")
                except Exception as e:
                    logger.warning(
                        f"Failed to register sequence beat frame in AppContext: {e}"
                    )

    def get_widget(self, widget_name: str) -> Optional[QWidget]:
        """
        Get a widget by name, creating it if necessary.

        Args:
            widget_name: Name of the widget

        Returns:
            The widget instance or None if creation failed
        """
        if widget_name not in self._widgets:
            return self._create_widget(widget_name)

        return self._widgets[widget_name]

    def is_widget_created(self, widget_name: str) -> bool:
        """Check if a widget has been created."""
        return widget_name in self._widgets

    def update_for_tab(self, tab_name: str) -> None:
        """Update widget visibility/state based on current tab."""
        # Update widgets that need to respond to tab changes
        fade_manager = self._widgets.get("fade_manager")
        if fade_manager and hasattr(fade_manager, "update_for_tab"):
            fade_manager.update_for_tab(tab_name)

        font_color_updater = self._widgets.get("font_color_updater")
        if font_color_updater and hasattr(font_color_updater, "update_for_tab"):
            font_color_updater.update_for_tab(tab_name)

    def get_sequence_beat_frame(self):
        """Get the sequence beat frame from the sequence workbench."""
        sequence_workbench = self._widgets.get("sequence_workbench")
        if sequence_workbench and hasattr(sequence_workbench, "beat_frame"):
            return sequence_workbench.beat_frame
        return None

    def cleanup(self) -> None:
        """Cleanup widget resources."""
        for widget_name, widget in self._widgets.items():
            if hasattr(widget, "cleanup"):
                try:
                    widget.cleanup()
                except Exception as e:
                    logger.error(f"Error cleaning up widget {widget_name}: {e}")

        self._widgets.clear()
        logger.info("Widget manager cleaned up")


class WidgetFactory:
    """Base class for widget factories."""

    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> QWidget:
        """
        Create a widget instance.

        Args:
            parent: Parent widget
            app_context: Application context with dependencies

        Returns:
            The created widget
        """
        raise NotImplementedError("Subclasses must implement create method")
