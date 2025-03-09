"""
Adapter for integrating the new mirrored entry system with existing code.
"""
import logging
from typing import Optional

from objects.arrow.arrow import Arrow
from settings_manager.global_settings.app_context import AppContext

from .mirrored_entry_factory import MirroredEntryFactory
from .mirrored_entry_utils import MirroredEntryUtils

logger = logging.getLogger(__name__)

class MirroredEntryAdapter:
    """
    Adapter for integrating the new mirrored entry system with existing code.
    Provides compatibility methods that match the old interface.
    """
    
    def __init__(self, data_updater):
        """
        Initialize the adapter with the given data updater.
        
        Args:
            data_updater: The data updater to use
        """
        self.data_updater = data_updater
        self.utils = MirroredEntryUtils()
        
        # Store the factory as a class attribute for easy access
        self.factory = MirroredEntryFactory
    
    def update_mirrored_entry_in_json(self) -> None:
        """
        Update the mirrored entry in JSON.
        This is the main entry point for the old interface.
        """
        selected_arrow = AppContext.get_selected_arrow()
        if not selected_arrow:
            logger.warning("No arrow selected, cannot update mirrored entry")
            return
        
        try:
            if MirroredEntryUtils.is_new_entry_needed(selected_arrow):
                self._create_new_entry(selected_arrow)
            else:
                self._update_existing_entry(selected_arrow)
                
            AppContext.special_placement_loader().reload()
        except Exception as e:
            logger.error(f"Failed to update mirrored entry in JSON: {str(e)}", exc_info=True)
    
    def _create_new_entry(self, arrow: Arrow) -> None:
        """
        Create a new mirrored entry for the given arrow.
        
        Args:
            arrow: The arrow to create a mirrored entry for
        """
        service = self.factory.create_service(self.data_updater)
        service.update_mirrored_entry(arrow)
    
    def _update_existing_entry(self, arrow: Arrow) -> None:
        """
        Update an existing mirrored entry for the given arrow.
        
        Args:
            arrow: The arrow to update the mirrored entry for
        """
        service = self.factory.create_service(self.data_updater)
        service.update_mirrored_entry(arrow)
    
    def rot_angle_manager(self):
        """
        Get a rotation angle processor for compatibility with old code.
        
        Returns:
            A dummy interface that matches the old rotation angle manager
        """
        class RotationAngleManagerAdapter:
            def update_rotation_angle_in_mirrored_entry(self, arrow, updated_turn_data):
                service = MirroredEntryFactory.create_service(self.data_updater)
                service.update_mirrored_entry(arrow)
            
            def remove_rotation_angle_in_mirrored_entry(self, arrow, hybrid_key):
                service = MirroredEntryFactory.create_service(self.data_updater)
                service.update_mirrored_entry(arrow)
        
        return RotationAngleManagerAdapter()
