from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory
from main_window.main_widget.main_background_widget.main_background_widget import (
    MainBackgroundWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget

logger = logging.getLogger(__name__)


class MainBackgroundWidgetFactory(WidgetFactory):
    """Factory for creating MainBackgroundWidget instances with proper dependency injection."""

    @staticmethod
    def create(
        parent: QWidget, app_context: ApplicationContext
    ) -> MainBackgroundWidget:
        """
        Create a MainBackgroundWidget instance with proper dependency injection.

        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies

        Returns:
            A new MainBackgroundWidget instance
        """
        try:
            # Get required services from app context
            settings_manager = app_context.settings_manager

            # Create the background widget with dependencies
            background_widget = MainBackgroundWidget(
                main_widget=parent,  # parent is the MainWidgetCoordinator
                settings_manager=settings_manager,
            )

            logger.info("Created MainBackgroundWidget with dependency injection")
            return background_widget

        except Exception as e:
            logger.error(f"Failed to create MainBackgroundWidget: {e}")
            raise
