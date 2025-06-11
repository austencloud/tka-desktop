"""
Factory for creating LearnTab instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.learn_tab import LearnTab

logger = logging.getLogger(__name__)


class LearnTabFactory(WidgetFactory):
    """Factory for creating LearnTab instances with dependency injection."""

    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "LearnTab":
        """
        Create a LearnTab instance with proper dependency injection.

        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies

        Returns:
            A new LearnTab instance
        """
        try:
            # Import here to avoid circular dependencies
            from main_window.main_widget.learn_tab.learn_tab import LearnTab

            # Get required services from app context
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager

            # Get required widgets from parent coordinator
            coordinator = parent  # parent is MainWidgetCoordinator

            # Create the learn tab with dependencies
            learn_tab = LearnTab(
                main_widget=coordinator,  # Pass coordinator as main_widget for compatibility
                settings_manager=settings_manager,
                json_manager=json_manager,
            )

            # Store references for backward compatibility
            learn_tab.app_context = app_context

            logger.info("Created LearnTab with dependency injection")
            return learn_tab

        except ImportError as e:
            logger.error(f"Failed to import LearnTab: {e}")
            # Create a placeholder widget if the real tab can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create LearnTab: {e}")
            raise
