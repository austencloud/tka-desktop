"""
Factory for creating GenerateTab instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab

logger = logging.getLogger(__name__)


class GenerateTabFactory(WidgetFactory):
    """Factory for creating GenerateTab instances with dependency injection."""

    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "GenerateTab":
        """
        Create a GenerateTab instance with proper dependency injection.

        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies

        Returns:
            A new GenerateTab instance
        """
        try:
            # Import here to avoid circular dependencies
            from main_window.main_widget.generate_tab.generate_tab import GenerateTab

            # Get required services from app context
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager

            print(f"DEBUG: GenerateTabFactory - settings_manager: {settings_manager}")
            print(f"DEBUG: GenerateTabFactory - json_manager: {json_manager}")
            print(
                f"DEBUG: GenerateTabFactory - json_manager.loader_saver: {getattr(json_manager, 'loader_saver', 'MISSING')}"
            )

            # Get required widgets from parent coordinator
            coordinator = parent  # parent is MainWidgetCoordinator
            sequence_workbench = coordinator.widget_manager.get_widget(
                "sequence_workbench"
            )
            print(
                f"DEBUG: GenerateTabFactory - sequence_workbench: {sequence_workbench}"
            )

            # Services are now injected centrally in the coordinator
            print(
                f"DEBUG: GenerateTabFactory - coordinator.letter_determiner: {getattr(coordinator, 'letter_determiner', 'MISSING')}"
            )
            print(
                f"DEBUG: GenerateTabFactory - coordinator.json_manager: {getattr(coordinator, 'json_manager', 'MISSING')}"
            )

            # Create the generate tab with dependencies
            print(f"DEBUG: GenerateTabFactory - Creating GenerateTab...")
            generate_tab = GenerateTab(
                main_widget=coordinator,  # Pass coordinator as main_widget for compatibility
                settings_manager=settings_manager,
                json_manager=json_manager,
            )
            print(f"DEBUG: GenerateTabFactory - GenerateTab created successfully")

            # Store references for backward compatibility
            generate_tab.app_context = app_context
            generate_tab.sequence_workbench = sequence_workbench

            logger.info("Created GenerateTab with dependency injection")
            return generate_tab

        except ImportError as e:
            logger.error(f"Failed to import GenerateTab: {e}")
            # Create a placeholder widget if the real tab can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create GenerateTab: {e}")
            raise
