"""
Handles orientation-specific logic for mirrored entries.
"""
import logging
from typing import List, Dict, Any, Optional

from enums.letter.letter import Letter
from enums.letter.letter_condition import LetterCondition
from data.constants import BLUE, RED, IN, OUT, CLOCK, COUNTER
from objects.arrow.arrow import Arrow

from .turns_pattern_manager import TurnsPatternManager

logger = logging.getLogger(__name__)

class OrientationHandler:
    """
    Handles orientation-specific logic for mirrored entries.
    Determines how to process entries based on the type of orientation
    and provides appropriate attribute keys.
    """
    
    def __init__(self, arrow: Arrow, turns_manager: TurnsPatternManager):
        """
        Initialize the orientation handler with the specific arrow and turns manager.
        
        Args:
            arrow: The arrow to handle orientation logic for
            turns_manager: The turns pattern manager to use
        """
        self.arrow = arrow
        self.pictograph = arrow.pictograph
        self.motion = arrow.motion
        self.turns_manager = turns_manager
    
    def is_mixed_orientation(self) -> bool:
        """
        Check if the pictograph has mixed orientation.
        
        Returns:
            True if the pictograph has mixed orientation, False otherwise
        """
        return self.pictograph.managers.check.starts_from_mixed_orientation()
    
    def get_hybrid_letters(self) -> List[Letter]:
        """
        Get a list of letters that are considered 'hybrid' letters.
        
        Returns:
            A list of letters that are considered hybrid
        """
        return Letter.get_letters_by_condition(LetterCondition.HYBRID)
    
    def get_mixed_attribute_key(self) -> str:
        """
        Get the appropriate attribute key for a mixed orientation.
        
        Returns:
            The attribute key to use for mixed orientation
        """
        letter = self.pictograph.state.letter
        
        # Determine which layer this orientation is from
        layer = "1" if self.motion.state.start_ori in [IN, OUT] else "2"
        
        if letter.value in ["S", "T"]:
            # Special case for S and T letters
            attr = self.motion.state.lead_state
            return f"{attr}_from_layer{layer}"
        elif self.pictograph.managers.check.has_hybrid_motions():
            # If it has hybrid motions, use motion type
            attr = self.motion.state.motion_type
            return f"{attr}_from_layer{layer}"
        else:
            # Otherwise use the opposite color
            return BLUE if self.arrow.state.color == RED else RED
    
    def get_standard_attribute_key(self, other_arrow: Arrow) -> str:
        """
        Get the appropriate attribute key for a standard orientation.
        
        Args:
            other_arrow: The other arrow in the pictograph
            
        Returns:
            The attribute key to use for standard orientation
        """
        letter = self.pictograph.state.letter
        
        if letter.value in ["S", "T"]:
            return self.motion.state.lead_state
        elif self.pictograph.managers.check.has_hybrid_motions():
            return self.motion.state.motion_type
        else:
            return BLUE if self.arrow.state.color == RED else RED
    
    def should_create_standard_mirror(self, other_arrow: Arrow) -> bool:
        """
        Determine if a standard orientation mirror should be created.
        
        Args:
            other_arrow: The other arrow in the pictograph
            
        Returns:
            True if a standard mirror should be created, False otherwise
        """
        # Check if turns are different
        turns_different = self.motion.state.turns != other_arrow.motion.state.turns
        
        # Check if motion types are the same
        same_motion_type = self.motion.state.motion_type == other_arrow.motion.state.motion_type
        
        # If turns are different and motion types are the same, create a mirror
        if turns_different and same_motion_type:
            return True
        
        # If turns are different and motion types are different and no float, create a mirror
        if (turns_different 
                and not same_motion_type 
                and not self.pictograph.managers.check.has_one_float()):
            return True
        
        # If turns are different and motion types are different and has float, create a mirror
        if (turns_different 
                and not same_motion_type 
                and self.pictograph.managers.check.has_one_float()):
            return True
        
        # Otherwise, don't create a mirror
        return False
    
    def determine_layer(self) -> str:
        """
        Determine which orientation layer the current arrow belongs to.
        
        Returns:
            The layer identifier ('1' or '2')
        """
        return "1" if self.motion.state.start_ori in [IN, OUT] else "2"
