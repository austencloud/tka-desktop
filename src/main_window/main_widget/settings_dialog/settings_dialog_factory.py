"""
Factory for creating SettingsDialog instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .settings_dialog import SettingsDialog

logger = logging.getLogger(__name__)


class SettingsDialogFactory(WidgetFactory):
    """Factory for creating SettingsDialog instances with dependency injection."""
    
    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "SettingsDialog":
        """
        Create a SettingsDialog instance with proper dependency injection.
        
        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies
            
        Returns:
            A new SettingsDialog instance
        """
        try:
            # Import here to avoid circular dependencies
            from .settings_dialog import SettingsDialog
            
            # Get required services from app context
            settings_manager = app_context.settings_manager
            
            # Create the settings dialog with dependencies
            settings_dialog = SettingsDialog(parent)
            
            # Inject dependencies if the dialog supports it
            if hasattr(settings_dialog, 'set_dependencies'):
                settings_dialog.set_dependencies(
                    settings_manager=settings_manager,
                    app_context=app_context
                )
            
            # Store references for backward compatibility
            settings_dialog.settings_manager = settings_manager
            settings_dialog.app_context = app_context
            
            logger.info("Created SettingsDialog with dependency injection")
            return settings_dialog
            
        except ImportError as e:
            logger.error(f"Failed to import SettingsDialog: {e}")
            # Create a placeholder widget if the real dialog can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create SettingsDialog: {e}")
            raise
