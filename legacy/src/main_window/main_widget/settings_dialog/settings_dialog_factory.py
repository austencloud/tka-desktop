"""
Factory for creating ModernSettingsDialog instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .legacy_settings_dialog import LegacySettingsDialog

logger = logging.getLogger(__name__)


class SettingsDialogFactory(WidgetFactory):
    """Factory for creating ModernSettingsDialog instances with dependency injection."""

    @staticmethod
    def create(
        parent: QWidget, app_context: ApplicationContext
    ) -> "LegacySettingsDialog":
        """
        Create a ModernSettingsDialog instance with proper dependency injection.

        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies

        Returns:
            A new ModernSettingsDialog instance
        """
        try:
            from .legacy_settings_dialog import LegacySettingsDialog

            # ModernSettingsDialog expects main_widget parameter and app_context
            # The parent should be the MainWidgetCoordinator which has main_widget
            main_widget = getattr(parent, "main_widget", parent)
            settings_dialog = LegacySettingsDialog(main_widget, app_context)
            logger.info("✅ Created ModernSettingsDialog with dependency injection")
            return settings_dialog

        except ImportError as e:
            logger.error(f"Failed to import ModernSettingsDialog: {e}")
            # Create a placeholder widget if no dialog can be imported
            placeholder = QWidget(parent)
            placeholder.setWindowTitle("Settings (Unavailable)")
            return placeholder
        except Exception as e:
            logger.error(f"Failed to create ModernSettingsDialog: {e}")
            raise
