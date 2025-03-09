"""
Processes rotation angle overrides for mirrored entries.
"""
import logging
from typing import Dict, Any, Optional

from data.constants import DASH, STATIC
from objects.arrow.arrow import Arrow
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
    ArrowRotAngleOverrideKeyGenerator,
)

logger = logging.getLogger(__name__)

class RotationAngleProcessor:
    """
    Processes rotation angle overrides for mirrored entries.
    Handles the detection, application, and removal of rotation angle overrides.
    """
    
    def __init__(self):
        """
        Initialize the rotation angle processor.
        """
        self.key_generator = ArrowRotAngleOverrideKeyGenerator()
    
    def process_rotation_override(
        self, 
        arrow: Arrow, 
        original_data: Dict[str, Any],
        mirrored_data: Dict[str, Any],
        mirrored_turns_tuple: str
    ) -> None:
        """
        Process rotation angle overrides for the given arrow and data.
        
        Args:
            arrow: The arrow to process rotation angle overrides for
            original_data: The original turn data
            mirrored_data: The mirrored data to update
            mirrored_turns_tuple: The mirrored turns tuple to use
        """
        try:
            # Check if we should handle rotation angles
            if not self._should_handle_rotation_angle(arrow):
                return
            
            # Look for rotation angle override in the original data
            rot_angle_override = self._find_rotation_angle_override(original_data)
            if rot_angle_override is None:
                return
            
            # Generate the rotation angle override key
            rot_angle_key = self.key_generator.generate_rotation_angle_override_key(arrow)
            
            # Ensure the mirrored turns tuple exists in the mirrored data
            if mirrored_turns_tuple not in mirrored_data:
                mirrored_data[mirrored_turns_tuple] = {}
            
            # Add the rotation angle override to the mirrored data
            mirrored_data[mirrored_turns_tuple][rot_angle_key] = rot_angle_override
            
        except Exception as e:
            logger.error(f"Failed to process rotation angle override: {str(e)}", exc_info=True)
    
    def remove_rotation_angle_override(
        self,
        arrow: Arrow,
        mirrored_data: Dict[str, Any],
        mirrored_turns_tuple: str,
        hybrid_key: str
    ) -> None:
        """
        Remove a rotation angle override from the mirrored data.
        
        Args:
            arrow: The arrow to remove the override for
            mirrored_data: The mirrored data to update
            mirrored_turns_tuple: The mirrored turns tuple to use
            hybrid_key: The hybrid key to remove
        """
        try:
            # Check if the mirrored turns tuple exists in the mirrored data
            if mirrored_turns_tuple in mirrored_data:
                # Check if the hybrid key exists in the mirrored turns tuple
                if hybrid_key in mirrored_data[mirrored_turns_tuple]:
                    # Remove the rotation angle override
                    del mirrored_data[mirrored_turns_tuple][hybrid_key]
                    
                    # If the mirrored turns tuple is now empty, remove it
                    if not mirrored_data[mirrored_turns_tuple]:
                        del mirrored_data[mirrored_turns_tuple]
        except Exception as e:
            logger.error(f"Failed to remove rotation angle override: {str(e)}", exc_info=True)
    
    def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
        """
        Check if we should handle rotation angles for the given arrow.
        
        Args:
            arrow: The arrow to check
            
        Returns:
            True if we should handle rotation angles, False otherwise
        """
        return arrow.motion.state.motion_type in [STATIC, DASH]
    
    def _find_rotation_angle_override(self, data: Dict[str, Any]) -> Optional[Any]:
        """
        Find a rotation angle override in the given data.
        
        Args:
            data: The data to search
            
        Returns:
            The rotation angle override value if found, None otherwise
        """
        for key, value in data.items():
            if "rot_angle_override" in key:
                return value
        return None
