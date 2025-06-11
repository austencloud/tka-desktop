"""
Factory for creating SequenceWorkbench instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .sequence_workbench import SequenceWorkbench

logger = logging.getLogger(__name__)


class SequenceWorkbenchFactory(WidgetFactory):
    """Factory for creating SequenceWorkbench instances with dependency injection."""

    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "SequenceWorkbench":
        """
        Create a SequenceWorkbench instance with proper dependency injection.

        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies

        Returns:
            A new SequenceWorkbench instance
        """
        try:
            # Import here to avoid circular dependencies
            from .sequence_workbench import SequenceWorkbench

            # Get required services from app context
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager

            # Create the sequence workbench with dependencies
            sequence_workbench = SequenceWorkbench(parent)

            # Inject dependencies if the workbench supports it
            if hasattr(sequence_workbench, "set_dependencies"):
                sequence_workbench.set_dependencies(
                    settings_manager=settings_manager,
                    json_manager=json_manager,
                    app_context=app_context,
                )

            # Store references for backward compatibility
            sequence_workbench.settings_manager = settings_manager
            sequence_workbench.json_manager = json_manager
            sequence_workbench.app_context = app_context

            logger.info("Created SequenceWorkbench with dependency injection")
            return sequence_workbench

        except ImportError as e:
            logger.error(f"Failed to import SequenceWorkbench: {e}")
            # Create a placeholder widget if the real workbench can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create SequenceWorkbench: {e}")
            raise
