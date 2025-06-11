"""
Factory for creating Codex instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .codex import Codex

logger = logging.getLogger(__name__)


class CodexFactory(WidgetFactory):
    """Factory for creating Codex instances with dependency injection."""

    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "Codex":
        """
        Create a Codex instance with proper dependency injection.

        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies

        Returns:
            A new Codex instance
        """
        try:
            # Import here to avoid circular dependencies
            from .codex import Codex

            # Get required services from app context
            settings_manager = app_context.settings_manager

            # Create the codex with dependencies
            codex = Codex(parent)

            # Inject dependencies if the codex supports it
            if hasattr(codex, "set_dependencies"):
                codex.set_dependencies(
                    settings_manager=settings_manager, app_context=app_context
                )

            # Store references for backward compatibility
            codex.settings_manager = settings_manager
            codex.app_context = app_context

            logger.info("Created Codex with dependency injection")
            return codex

        except ImportError as e:
            logger.error(f"Failed to import Codex: {e}")
            # Create a placeholder widget if the real codex can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create Codex: {e}")
            raise
