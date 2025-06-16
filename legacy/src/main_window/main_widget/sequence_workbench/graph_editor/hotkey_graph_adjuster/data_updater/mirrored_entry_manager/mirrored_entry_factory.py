"""
Factory for creating and configuring mirrored entry components.
"""
import logging

from objects.arrow.arrow import Arrow
from src.legacy_settings_manager.global_settings.app_context import AppContext

from .mirrored_entry_service import MirroredEntryService

logger = logging.getLogger(__name__)

class MirroredEntryFactory:
    """
    Factory for creating and configuring mirrored entry components.
    Provides a simple way to get a fully configured mirrored entry service.
    """
    
    @staticmethod
    def create_service(data_updater) -> MirroredEntryService:
        """
        Create a fully configured mirrored entry service.
        
        Args:
            data_updater: The data updater to use
            
        Returns:
            A configured mirrored entry service
        """
        try:
            # Create and return the service
            return MirroredEntryService(data_updater)
        except Exception as e:
            logger.error(f"Failed to create mirrored entry service: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def update_mirrored_entry(arrow: Arrow) -> bool:
        """
        Update the mirrored entry for the given arrow.
        This is a convenience method that creates a service and updates the entry.
        
        Args:
            arrow: The arrow to update the mirrored entry for
            
        Returns:
            True if the update was successful, False otherwise
        """
        try:
            data_updater = arrow.pictograph.managers.arrow_placement_manager.data_updater
            service = MirroredEntryFactory.create_service(data_updater)
            service.update_mirrored_entry(arrow)
            AppContext.special_placement_loader().reload()
            return True
        except Exception as e:
            logger.error(f"Failed to update mirrored entry: {str(e)}", exc_info=True)
            return False