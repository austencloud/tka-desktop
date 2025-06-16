"""
Utility functions for working with mirrored entries.
"""
import logging
from typing import Dict, Any, Tuple

from enums.letter.letter import Letter
from data.constants import BLUE, RED, IN, OUT, CLOCK, COUNTER
from objects.arrow.arrow import Arrow
from src.legacy_settings_manager.global_settings.app_context import AppContext

logger = logging.getLogger(__name__)

class MirroredEntryUtils:
    """
    Utility functions for working with mirrored entries.
    Provides helper methods for common operations.
    """
    
    @staticmethod
    def is_new_entry_needed(arrow: Arrow) -> bool:
        """
        Determine if a new mirrored entry is needed for the given arrow.
        
        Args:
            arrow: The arrow to check
            
        Returns:
            True if a new mirrored entry is needed, False otherwise
        """
        try:
            AppContext.special_placement_loader().reload()
            
            # Get the orientation key
            data_updater = arrow.pictograph.managers.arrow_placement_manager.data_updater
            ori_key = data_updater.ori_key_generator.generate_ori_key_from_motion(arrow.motion)
            
            # Check if the letter exists in the special placements
            letter = arrow.pictograph.state.letter
            return letter not in AppContext.special_placement_loader().load_or_return_special_placements().get(ori_key, {})
        except Exception as e:
            logger.error(f"Failed to check if new entry is needed: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def determine_opposite_color(color: str) -> str:
        """
        Determine the opposite color for the given color.
        
        Args:
            color: The color to get the opposite of
            
        Returns:
            The opposite color
        """
        return RED if color == BLUE else BLUE
    
    @staticmethod
    def get_orientation_layer(orientation: str) -> str:
        """
        Get the layer for the given orientation.
        
        Args:
            orientation: The orientation to get the layer for
            
        Returns:
            The layer ('1' or '2')
        """
        return "1" if orientation in [IN, OUT] else "2"
    
    @staticmethod
    def get_other_layer3_ori_key(ori_key: str) -> str:
        """
        Get the other layer 3 orientation key for the given orientation key.
        
        Args:
            ori_key: The orientation key to get the other key for
            
        Returns:
            The other layer 3 orientation key
        """
        if ori_key == "from_layer3_blue1_red2":
            return "from_layer3_blue2_red1"
        elif ori_key == "from_layer3_blue2_red1":
            return "from_layer3_blue1_red2"
        return ori_key
    
    @staticmethod
    def is_mixed_orientation(arrow: Arrow) -> bool:
        """
        Check if the arrow's pictograph has mixed orientation.
        
        Args:
            arrow: The arrow to check
            
        Returns:
            True if the pictograph has mixed orientation, False otherwise
        """
        other_motion = arrow.pictograph.managers.get.other_motion(arrow.motion)
        blue_in_layer1 = arrow.state.color == BLUE and arrow.motion.state.start_ori in [IN, OUT]
        red_in_layer2 = arrow.state.color == RED and other_motion.state.start_ori in [CLOCK, COUNTER]
        blue_in_layer2 = arrow.state.color == BLUE and arrow.motion.state.start_ori in [CLOCK, COUNTER]
        red_in_layer1 = arrow.state.color == RED and other_motion.state.start_ori in [IN, OUT]
        
        return (blue_in_layer1 and red_in_layer2) or (blue_in_layer2 and red_in_layer1)
    
    @staticmethod
    def get_keys_for_mixed_start_ori(grid_mode: str, letter: Letter, ori_key: str) -> Tuple[str, Dict[str, Any]]:
        """
        Get the keys and data for mixed start orientation.
        
        Args:
            grid_mode: The grid mode to use
            letter: The letter to get data for
            ori_key: The orientation key to use
            
        Returns:
            A tuple of (other_ori_key, other_letter_data)
        """
        other_ori_key = MirroredEntryUtils.get_other_layer3_ori_key(ori_key)
        other_letter_data = MirroredEntryUtils._get_letter_data(grid_mode, other_ori_key, letter)
        return other_ori_key, other_letter_data
    
    @staticmethod
    def _get_letter_data(grid_mode: str, ori_key: str, letter: Letter) -> Dict[str, Any]:
        """
        Get the letter data for the given grid mode, orientation key, and letter.
        
        Args:
            grid_mode: The grid mode to use
            ori_key: The orientation key to use
            letter: The letter to get data for
            
        Returns:
            The letter data
        """
        return (
            AppContext.special_placement_loader()
            .load_or_return_special_placements()
            .get(grid_mode, {})
            .get(ori_key, {})
            .get(letter.value, {})
        )
