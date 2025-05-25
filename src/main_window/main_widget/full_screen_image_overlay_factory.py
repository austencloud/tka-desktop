"""
Factory for creating FullScreenImageOverlay instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .full_screen_image_overlay import FullScreenImageOverlay

logger = logging.getLogger(__name__)


class FullScreenImageOverlayFactory(WidgetFactory):
    """Factory for creating FullScreenImageOverlay instances with dependency injection."""
    
    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "FullScreenImageOverlay":
        """
        Create a FullScreenImageOverlay instance with proper dependency injection.
        
        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies
            
        Returns:
            A new FullScreenImageOverlay instance
        """
        try:
            # Import here to avoid circular dependencies
            from .full_screen_image_overlay import FullScreenImageOverlay
            
            # Create the overlay with dependencies
            overlay = FullScreenImageOverlay(parent)
            
            # Store references for backward compatibility
            overlay.app_context = app_context
            
            logger.info("Created FullScreenImageOverlay with dependency injection")
            return overlay
            
        except ImportError as e:
            logger.error(f"Failed to import FullScreenImageOverlay: {e}")
            # Create a placeholder widget if the real overlay can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create FullScreenImageOverlay: {e}")
            raise
