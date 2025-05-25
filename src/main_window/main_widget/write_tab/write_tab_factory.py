"""
Factory for creating WriteTab instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .write_tab import WriteTab

logger = logging.getLogger(__name__)


class WriteTabFactory(WidgetFactory):
    """Factory for creating WriteTab instances with dependency injection."""
    
    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "WriteTab":
        """
        Create a WriteTab instance with proper dependency injection.
        
        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies
            
        Returns:
            A new WriteTab instance
        """
        try:
            # Import here to avoid circular dependencies
            from .write_tab import WriteTab
            
            # Get required services from app context
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager
            
            # Get required widgets from parent coordinator
            coordinator = parent  # parent is MainWidgetCoordinator
            
            # Create the write tab with dependencies
            write_tab = WriteTab(
                main_widget=coordinator,  # Pass coordinator as main_widget for compatibility
                settings_manager=settings_manager,
                json_manager=json_manager,
            )
            
            # Store references for backward compatibility
            write_tab.app_context = app_context
            
            logger.info("Created WriteTab with dependency injection")
            return write_tab
            
        except ImportError as e:
            logger.error(f"Failed to import WriteTab: {e}")
            # Create a placeholder widget if the real tab can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create WriteTab: {e}")
            raise
