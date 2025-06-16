"""
Factory for creating PictographCollector instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .pictograph_collector import PictographCollector

logger = logging.getLogger(__name__)


class PictographCollectorFactory(WidgetFactory):
    """Factory for creating PictographCollector instances with dependency injection."""
    
    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "PictographCollector":
        """
        Create a PictographCollector instance with proper dependency injection.
        
        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies
            
        Returns:
            A new PictographCollector instance
        """
        try:
            # Import here to avoid circular dependencies
            from .pictograph_collector import PictographCollector
            
            # Get required services from app context
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager
            
            # Create the pictograph collector with dependencies
            pictograph_collector = PictographCollector(parent)
            
            # Inject dependencies if the collector supports it
            if hasattr(pictograph_collector, 'set_dependencies'):
                pictograph_collector.set_dependencies(
                    settings_manager=settings_manager,
                    json_manager=json_manager,
                    app_context=app_context
                )
            
            # Store references for backward compatibility
            pictograph_collector.settings_manager = settings_manager
            pictograph_collector.json_manager = json_manager
            pictograph_collector.app_context = app_context
            
            logger.info("Created PictographCollector with dependency injection")
            return pictograph_collector
            
        except ImportError as e:
            logger.error(f"Failed to import PictographCollector: {e}")
            # Create a placeholder widget if the real collector can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create PictographCollector: {e}")
            raise
