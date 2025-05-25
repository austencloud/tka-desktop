"""
Factory for creating ConstructTab instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
import logging

from core.application_context import ApplicationContext
from main_window.main_widget.core.widget_manager import WidgetFactory

if TYPE_CHECKING:
    from .construct_tab import ConstructTab

logger = logging.getLogger(__name__)


class ConstructTabFactory(WidgetFactory):
    """Factory for creating ConstructTab instances with dependency injection."""

    @staticmethod
    def create(parent: QWidget, app_context: ApplicationContext) -> "ConstructTab":
        """
        Create a ConstructTab instance with proper dependency injection.

        Args:
            parent: Parent widget (MainWidgetCoordinator)
            app_context: Application context with dependencies

        Returns:
            A new ConstructTab instance
        """
        try:
            # Import here to avoid circular dependencies
            from .construct_tab import ConstructTab

            # Get required services from app context
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager

            # Get required widgets from parent coordinator
            coordinator = parent  # parent is MainWidgetCoordinator
            sequence_workbench = coordinator.widget_manager.get_widget(
                "sequence_workbench"
            )
            fade_manager = coordinator.widget_manager.get_widget("fade_manager")

            # Get pictograph dataset from the dependency injection system
            try:
                # Try to get PictographDataLoader from dependency injection
                from main_window.main_widget.pictograph_data_loader import (
                    PictographDataLoader,
                )

                pictograph_data_loader = app_context.get_service(PictographDataLoader)
                pictograph_dataset = pictograph_data_loader.get_pictograph_dataset()
            except (AttributeError, KeyError):
                # Fallback: check if coordinator has pictograph_dataset
                pictograph_dataset = getattr(coordinator, "pictograph_dataset", {})
                if not pictograph_dataset:
                    # Last resort: create a PictographDataLoader directly
                    logger.warning("Creating PictographDataLoader directly as fallback")
                    pictograph_data_loader = PictographDataLoader(coordinator)
                    pictograph_dataset = pictograph_data_loader.get_pictograph_dataset()

            # Create the construct tab with dependencies
            construct_tab = ConstructTab(
                beat_frame=(
                    sequence_workbench.beat_frame if sequence_workbench else None
                ),
                pictograph_dataset=pictograph_dataset,
                size_provider=lambda: coordinator.size(),
                fade_to_stack_index=lambda index: (
                    fade_manager.stack_fader.fade_stack(coordinator.right_stack, index)
                    if fade_manager
                    else None
                ),
                fade_manager=fade_manager,
                settings_manager=settings_manager,
                json_manager=json_manager,
            )

            # Store app context for future use
            construct_tab.app_context = app_context

            logger.info("Created ConstructTab with dependency injection")
            return construct_tab

        except ImportError as e:
            logger.error(f"Failed to import ConstructTab: {e}")
            # Create a placeholder widget if the real tab can't be imported
            return QWidget(parent)
        except Exception as e:
            logger.error(f"Failed to create ConstructTab: {e}")
            raise
