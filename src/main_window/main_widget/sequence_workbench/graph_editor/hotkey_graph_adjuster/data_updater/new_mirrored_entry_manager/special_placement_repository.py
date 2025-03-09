"""
Repository for accessing and updating special placement data.
"""
import logging
import os
from typing import Dict, Any, Optional

from enums.letter.letter import Letter
from settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_data_path

logger = logging.getLogger(__name__)

class SpecialPlacementRepository:
    """
    Repository for accessing and updating special placement data.
    Provides a clean interface for retrieving and saving special placement data.
    """
    
    def __init__(self, grid_mode: str):
        """
        Initialize the repository with the given grid mode.
        
        Args:
            grid_mode: The grid mode to use for special placements
        """
        self.grid_mode = grid_mode
    
    def get_letter_data(self, letter: Letter, ori_key: str) -> Dict[str, Any]:
        """
        Get the letter data for the given letter and orientation key.
        
        Args:
            letter: The letter to get data for
            ori_key: The orientation key to use
            
        Returns:
            The letter data dictionary
        """
        try:
            # Load the special placements data
            placements = AppContext.special_placement_loader().load_special_placements_fresh()
            
            # Extract the letter data
            grid_data = placements.get(self.grid_mode, {})
            ori_data = grid_data.get(ori_key, {})
            letter_data = ori_data.get(letter.value, {})
            
            return letter_data or {}
        except Exception as e:
            logger.error(f"Failed to get letter data: {str(e)}", exc_info=True)
            return {}
    
    def save_letter_data(self, letter: Letter, ori_key: str, letter_data: Dict[str, Any]) -> bool:
        """
        Save the letter data for the given letter and orientation key.
        
        Args:
            letter: The letter to save data for
            ori_key: The orientation key to use
            letter_data: The letter data to save
            
        Returns:
            True if the save was successful, False otherwise
        """
        try:
            # Get the file path
            file_path = self._get_file_path(letter, ori_key)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Load existing data
            placement_data = AppContext.special_placement_loader().load_json_data(file_path) or {}
            
            # Update with new data
            placement_data[letter.value] = letter_data
            
            # Save the updated data
            AppContext.special_placement_saver().save_json_data(placement_data, file_path)
            
            return True
        except Exception as e:
            logger.error(f"Failed to save letter data: {str(e)}", exc_info=True)
            return False
    
    def _get_file_path(self, letter: Letter, ori_key: str) -> str:
        """
        Get the file path for the given letter and orientation key.
        
        Args:
            letter: The letter to get the path for
            ori_key: The orientation key to use
            
        Returns:
            The file path for the letter data
        """
        return get_data_path(
            os.path.join(
                "arrow_placement",
                self.grid_mode,
                "special",
                ori_key,
                f"{letter.value}_placements.json",
            )
        )
    
    def clean_placement_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean the placement data by removing empty dictionaries and normalizing values.
        
        Args:
            data: The data to clean
            
        Returns:
            The cleaned data
        """
        if not isinstance(data, dict):
            return data
        
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                cleaned_value = self.clean_placement_data(value)
                if cleaned_value:  # Only add non-empty dictionaries
                    result[key] = cleaned_value
            elif isinstance(value, list):
                # Convert float indices to int if they're whole numbers
                result[key] = [int(item) if isinstance(item, float) and item.is_integer() else item for item in value]
            elif isinstance(value, float) and value.is_integer():
                # Convert float to int if it's a whole number
                result[key] = int(value)
            else:
                result[key] = value
        
        return result
