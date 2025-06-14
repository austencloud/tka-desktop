"""
Factory for creating FontColorUpdater instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .font_color_updater import FontColorUpdater

logger = logging.getLogger(__name__)


class FontColorUpdaterFactory(WidgetFactory):
    """Factory for creating FontColorUpdater instances with dependency injection."""
    
    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "FontColorUpdater":
        """
        Create a FontColorUpdater instance with proper dependency injection.
        
        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies
            
        Returns:
            A new FontColorUpdater instance
        """
        try:
            # Import here to avoid circular dependencies
            from .font_color_updater import FontColorUpdater
            
            # Get required services from app context
            settings_manager = app_context.settings_manager
            
            # Create the font color updater with dependencies
            font_color_updater = FontColorUpdater(parent)
            
            # Inject dependencies if the updater supports it
            if hasattr(font_color_updater, 'set_dependencies'):
                font_color_updater.set_dependencies(
                    settings_manager=settings_manager,
                    app_context=app_context
                )
            
            # Store references for backward compatibility
            font_color_updater.settings_manager = settings_manager
            font_color_updater.app_context = app_context
            
            logger.info("Created FontColorUpdater with dependency injection")
            return font_color_updater
            
        except ImportError as e:
            logger.error(f"Failed to import FontColorUpdater: {e}")
            # Create a placeholder widget if the real updater can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create FontColorUpdater: {e}")
            raise
