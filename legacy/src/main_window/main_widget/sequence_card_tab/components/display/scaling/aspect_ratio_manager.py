"""
Aspect Ratio Manager - Handles aspect ratio calculations and management.

Extracted from the monolithic ImageProcessor class to follow SRP.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pages.printable_factory import PrintablePageFactory


class AspectRatioManager:
    """
    Handles aspect ratio calculations and management.
    
    Responsibilities:
    - Aspect ratio calculations
    - Page factory aspect ratio updates
    - Ratio validation and constraints
    """
    
    def __init__(self, page_factory: "PrintablePageFactory"):
        self.page_factory = page_factory
        self.logger = logging.getLogger(__name__)
        
    def calculate_aspect_ratio(self, width: int, height: int) -> float:
        """
        Calculate aspect ratio from dimensions.
        
        Args:
            width: Image width
            height: Image height
            
        Returns:
            Aspect ratio (width/height), or 1.0 if invalid
        """
        if height <= 0:
            self.logger.warning(f"Invalid height for aspect ratio: {height}")
            return 1.0
            
        return width / height
        
    def update_page_aspect_ratio(self, width: int, height: int, page_index: int = -1) -> None:
        """
        Update page factory aspect ratio if this is the first image.
        
        Args:
            width: Image width
            height: Image height
            page_index: Page index (-1 for first image)
        """
        # Only update for the first image in a batch
        if page_index == -1 and width > 0 and height > 0:
            aspect_ratio = self.calculate_aspect_ratio(width, height)
            try:
                self.page_factory.update_card_aspect_ratio(aspect_ratio)
                self.logger.debug(f"Updated page aspect ratio to {aspect_ratio:.3f}")
            except Exception as e:
                self.logger.warning(f"Failed to update page aspect ratio: {e}")
                
    def validate_aspect_ratio(self, aspect_ratio: float) -> bool:
        """
        Validate aspect ratio is reasonable.
        
        Args:
            aspect_ratio: Aspect ratio to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Reasonable aspect ratio bounds (very wide or very tall images)
        min_ratio = 0.1  # Very tall
        max_ratio = 10.0  # Very wide
        
        if aspect_ratio < min_ratio or aspect_ratio > max_ratio:
            self.logger.warning(f"Unusual aspect ratio: {aspect_ratio:.3f}")
            return False
            
        return True
        
    def constrain_aspect_ratio(self, aspect_ratio: float) -> float:
        """
        Constrain aspect ratio to reasonable bounds.
        
        Args:
            aspect_ratio: Original aspect ratio
            
        Returns:
            Constrained aspect ratio
        """
        min_ratio = 0.1
        max_ratio = 10.0
        
        if aspect_ratio < min_ratio:
            self.logger.info(f"Constraining aspect ratio from {aspect_ratio:.3f} to {min_ratio}")
            return min_ratio
        elif aspect_ratio > max_ratio:
            self.logger.info(f"Constraining aspect ratio from {aspect_ratio:.3f} to {max_ratio}")
            return max_ratio
        else:
            return aspect_ratio
