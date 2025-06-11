"""
Factory for creating SequencePropertiesManager instances with proper dependency injection.
"""

from typing import TYPE_CHECKING
import logging

from core.application_context import ApplicationContext

if TYPE_CHECKING:
    from .sequence_properties_manager import SequencePropertiesManager

logger = logging.getLogger(__name__)


class SequencePropertiesManagerFactory:
    """Factory for creating SequencePropertiesManager instances with dependency injection."""

    @staticmethod
    def create(app_context: ApplicationContext) -> "SequencePropertiesManager":
        """
        Create a SequencePropertiesManager instance with proper dependency injection.

        Args:
            app_context: Application context with dependencies

        Returns:
            A new SequencePropertiesManager instance
        """
        try:
            from .sequence_properties_manager import SequencePropertiesManager

            # Create the manager with dependency injection
            manager = SequencePropertiesManager(app_context)

            logger.info("Created SequencePropertiesManager with dependency injection")
            return manager

        except Exception as e:
            logger.error(f"Failed to create SequencePropertiesManager: {e}")
            raise

    @staticmethod
    def create_legacy() -> "SequencePropertiesManager":
        """
        Create a SequencePropertiesManager instance using legacy compatibility.

        This method is for backward compatibility during the migration period.

        Returns:
            A new SequencePropertiesManager instance using legacy adapters
        """
        try:
            from .sequence_properties_manager import SequencePropertiesManager

            # Always create with None app_context to avoid timing issues with AppContextAdapter
            # The SequencePropertiesManager constructor will handle the AppContextAdapter check gracefully
            logger.info(
                "Creating SequencePropertiesManager with None app_context (legacy mode)"
            )
            manager = SequencePropertiesManager(None)
            logger.info("Created SequencePropertiesManager in legacy mode")
            return manager

        except Exception as e:
            logger.error(f"Failed to create SequencePropertiesManager (legacy): {e}")
            raise
