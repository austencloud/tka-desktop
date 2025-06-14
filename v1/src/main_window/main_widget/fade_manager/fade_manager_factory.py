"""
Factory for creating FadeManager instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .fade_manager import FadeManager

logger = logging.getLogger(__name__)


class FadeManagerFactory(WidgetFactory):
    """Factory for creating FadeManager instances with dependency injection."""
    
    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "FadeManager":
        """
        Create a FadeManager instance with proper dependency injection.
        
        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies
            
        Returns:
            A new FadeManager instance
        """
        try:
            # Import here to avoid circular dependencies
            from .fade_manager import FadeManager
            
            # Get required services from app context
            settings_manager = app_context.settings_manager
            
            # Create the fade manager with dependencies
            fade_manager = FadeManager(parent)
            
            # Inject dependencies if the manager supports it
            if hasattr(fade_manager, 'set_dependencies'):
                fade_manager.set_dependencies(
                    settings_manager=settings_manager,
                    app_context=app_context
                )
            
            # Store references for backward compatibility
            fade_manager.settings_manager = settings_manager
            fade_manager.app_context = app_context
            
            logger.info("Created FadeManager with dependency injection")
            return fade_manager
            
        except ImportError as e:
            logger.error(f"Failed to import FadeManager: {e}")
            # Create a placeholder widget if the real manager can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create FadeManager: {e}")
            raise
