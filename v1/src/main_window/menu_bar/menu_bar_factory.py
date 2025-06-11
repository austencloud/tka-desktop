"""
Factory for creating MenuBar instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .menu_bar import MenuBarWidget

logger = logging.getLogger(__name__)


class MenuBarFactory(WidgetFactory):
    """Factory for creating MenuBarWidget instances with dependency injection."""

    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "MenuBarWidget":
        """
        Create a MenuBarWidget instance with proper dependency injection.

        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies

        Returns:
            A new MenuBarWidget instance
        """
        try:
            # Import here to avoid circular dependencies
            from .menu_bar import MenuBarWidget

            # Get required services from app context
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager

            # Create the menu bar with dependencies
            menu_bar = MenuBarWidget(parent)

            # Inject dependencies if the menu bar supports it
            if hasattr(menu_bar, "set_dependencies"):
                menu_bar.set_dependencies(
                    settings_manager=settings_manager,
                    json_manager=json_manager,
                    app_context=app_context,
                )

            # Store references for backward compatibility
            menu_bar.settings_manager = settings_manager
            menu_bar.json_manager = json_manager
            menu_bar.app_context = app_context

            logger.info("Created MenuBarWidget with dependency injection")
            return menu_bar

        except ImportError as e:
            logger.error(f"Failed to import MenuBarWidget: {e}")
            # Create a placeholder widget if the real menu bar can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create MenuBarWidget: {e}")
            raise
