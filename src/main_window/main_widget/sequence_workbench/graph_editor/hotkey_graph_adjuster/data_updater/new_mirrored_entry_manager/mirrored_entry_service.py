"""
Provides core functionality for managing mirrored entries in special placements.
This is the main entry point for all mirrored entry operations.
"""
import logging
from typing import Optional, Dict, Any, List

from enums.letter.letter import Letter
from objects.arrow.arrow import Arrow
from settings_manager.global_settings.app_context import AppContext

from .orientation_handler import OrientationHandler
from .turns_pattern_manager import TurnsPatternManager
from .special_placement_repository import SpecialPlacementRepository
from .rotation_angle_processor import RotationAngleProcessor

logger = logging.getLogger(__name__)

class MirroredEntryService:
    """
    Service for managing mirrored entries in special placements.
    Coordinates all mirrored entry operations using specialized helper classes.
    """
    
    def __init__(self, data_updater):
        """
        Initialize the MirroredEntryService with required dependencies.
        
        Args:
            data_updater: The data updater that can update special placement data
        """
        self.data_updater = data_updater
        self.turns_manager = TurnsPatternManager()
        self.repository = SpecialPlacementRepository(data_updater.getter.grid_mode())
        self.rotation_processor = RotationAngleProcessor()
        
        # Don't create orientation handler yet as it needs arrow data
        self.orientation_handler = None
    
    def update_mirrored_entry(self, arrow: Arrow) -> None:
        """
        Updates the mirrored entry for the given arrow.
        This is the main entry point for mirrored entry updates.
        
        Args:
            arrow: The arrow to update mirrored entries for
        """
        logger.debug(f"Updating mirrored entry for arrow: {arrow.state.color}")
        
        try:
            # Initialize orientation handler with current arrow
            self.orientation_handler = OrientationHandler(arrow, self.turns_manager)
            
            # Get the base data for the entry
            letter = arrow.pictograph.state.letter
            ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(arrow.motion)
            
            # Load current data
            letter_data = self._load_letter_data(letter, ori_key)
            
            # Process the entry based on orientation
            if self.orientation_handler.is_mixed_orientation():
                self._process_mixed_orientation_entry(arrow, letter, ori_key, letter_data)
            else:
                self._process_standard_orientation_entry(arrow, letter, ori_key, letter_data)
            
            # Save the updated data
            AppContext.special_placement_loader().reload()
            
        except Exception as e:
            logger.error(f"Failed to update mirrored entry: {str(e)}", exc_info=True)
            raise
    
    def _load_letter_data(self, letter: Letter, ori_key: str) -> Dict[str, Any]:
        """
        Loads the letter data for the given orientation key.
        
        Args:
            letter: The letter to load data for
            ori_key: The orientation key to use
            
        Returns:
            The letter data dictionary
        """
        return self.repository.get_letter_data(letter, ori_key)
    
    def _process_mixed_orientation_entry(
        self, arrow: Arrow, letter: Letter, ori_key: str, letter_data: Dict[str, Any]
    ) -> None:
        """
        Process a mixed orientation entry.
        
        Args:
            arrow: The arrow to process
            letter: The letter of the pictograph
            ori_key: The orientation key
            letter_data: The current letter data
        """
        turns_tuple = self.turns_manager.generate_turns_tuple(arrow.pictograph)
        mirrored_tuple = self.turns_manager.generate_mirrored_tuple(arrow)
        
        # Get the mirror orientation key and data
        mirror_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        mirror_letter_data = self.repository.get_letter_data(letter, mirror_ori_key)
        
        # Get the key to use for the mirror
        attribute_key = self.orientation_handler.get_mixed_attribute_key()
        source_data = letter_data.get(turns_tuple, {}).get(attribute_key, {})
        
        # Ensure the mirrored dictionary structure exists
        if mirrored_tuple not in mirror_letter_data:
            mirror_letter_data[mirrored_tuple] = {}
        
        # Update the mirrored entry
        mirror_letter_data[mirrored_tuple][attribute_key] = source_data
        
        # Process any rotation angle overrides
        self.rotation_processor.process_rotation_override(
            arrow, letter_data.get(turns_tuple, {}), mirror_letter_data, mirrored_tuple
        )
        
        # Save the updated mirror data
        self.data_updater.update_specific_entry_in_json(letter, mirror_letter_data, mirror_ori_key)
    
    def _process_standard_orientation_entry(
        self, arrow: Arrow, letter: Letter, ori_key: str, letter_data: Dict[str, Any]
    ) -> None:
        """
        Process a standard orientation entry.
        
        Args:
            arrow: The arrow to process
            letter: The letter of the pictograph
            ori_key: The orientation key
            letter_data: The current letter data
        """
        # Skip special cases that don't need mirroring
        if letter.value in ["S", "T", "β"] or letter in self.orientation_handler.get_hybrid_letters():
            return
        
        turns_tuple = self.turns_manager.generate_turns_tuple(arrow.pictograph)
        mirrored_tuple = self.turns_manager.generate_mirrored_tuple(arrow)
        
        # Determine whether to mirror based on turns values
        other_arrow = arrow.pictograph.managers.get.other_arrow(arrow)
        should_mirror = self.orientation_handler.should_create_standard_mirror(other_arrow)
        
        if not should_mirror:
            return
        
        # Get the attribute key and source data
        attribute_key = self.orientation_handler.get_standard_attribute_key(other_arrow)
        source_data = letter_data.get(turns_tuple, {}).get(arrow.state.color, {})
        
        # Ensure the mirrored dictionary structure exists
        if mirrored_tuple not in letter_data:
            letter_data[mirrored_tuple] = {}
        
        # Update the mirrored entry
        letter_data[mirrored_tuple][attribute_key] = source_data
        
        # Save the updated data
        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)
