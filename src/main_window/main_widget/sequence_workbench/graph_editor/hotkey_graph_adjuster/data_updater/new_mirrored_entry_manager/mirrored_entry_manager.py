"""
Drop-in replacement for the old MirroredEntryManager class.
This class serves as a facade for the new architecture while maintaining the old interface.
"""
import logging
from typing import Optional

from settings_manager.global_settings.app_context import AppContext
from objects.arrow.arrow import Arrow

from .mirrored_entry_factory import MirroredEntryFactory
from .mirrored_entry_adapter import MirroredEntryAdapter

logger = logging.getLogger(__name__)

class MirroredEntryManager:
    """
    New implementation of MirroredEntryManager that uses the refactored architecture.
    Maintains the same public interface as the old class for backward compatibility.
    """
    
    def __init__(self, data_updater) -> None:
        """
        Initialize the mirrored entry manager with the given data updater.
        
        Args:
            data_updater: The data updater to use
        """
        self.data_updater = data_updater
        self.adapter = MirroredEntryAdapter(data_updater)
        
        # Create properties for backward compatibility
        self.turns_tuple_generator = self.adapter.factory.create_service(data_updater).turns_manager
        self.rot_angle_manager = self.adapter.rot_angle_manager()
        
        # This is just for backward compatibility, no real use
        self.data_prep = type('DataPrep', (), {
            'is_new_entry_needed': lambda arrow: False,
            'get_keys_for_mixed_start_ori': lambda grid_mode, letter, ori_key: (ori_key, {})
        })()
    
    def update_mirrored_entry_in_json(self) -> None:
        """
        Update the mirrored entry in JSON.
        This is the main entry point for the old interface.
        """
        self.adapter.update_mirrored_entry_in_json()
