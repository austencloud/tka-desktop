"""
Thumbnail Size Calculator - Handles size calculations for different view modes.

Extracted from ThumbnailImageLabel to follow Single Responsibility Principle.
"""

import logging
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSize

if TYPE_CHECKING:
    from ..thumbnail_box import ThumbnailBox


class ThumbnailSizeCalculator:
    """
    Calculates thumbnail sizes for different view modes and contexts.
    
    Responsibilities:
    - Calculate target sizes based on view mode
    - Handle sequence viewer vs browse mode sizing
    - Manage aspect ratio considerations
    - Provide consistent sizing logic
    """
    
    # Size constants for different modes
    BROWSE_MODE_SIZE = QSize(200, 200)
    SEQUENCE_VIEWER_SIZE = QSize(150, 150)
    MINIMUM_SIZE = QSize(50, 50)
    MAXIMUM_SIZE = QSize(400, 400)
    
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        self.thumbnail_box = thumbnail_box
        self.logger = logging.getLogger(__name__)
    
    def calculate_target_size(self, is_sequence_viewer: bool) -> QSize:
        """
        Calculate the target size for thumbnail processing.
        
        Args:
            is_sequence_viewer: Whether in sequence viewer mode
            
        Returns:
            Target QSize for thumbnail processing
        """
        try:
            if is_sequence_viewer:
                return self._calculate_sequence_viewer_size()
            else:
                return self._calculate_browse_mode_size()
                
        except Exception as e:
            self.logger.warning(f"Error calculating target size: {e}")
            return self.BROWSE_MODE_SIZE
    
    def _calculate_sequence_viewer_size(self) -> QSize:
        """
        Calculate size for sequence viewer mode.
        
        Returns:
            QSize optimized for sequence viewer
        """
        # In sequence viewer, use smaller thumbnails for better overview
        base_size = self.SEQUENCE_VIEWER_SIZE
        
        # Could be adjusted based on available space or user preferences
        return self._clamp_size(base_size)
    
    def _calculate_browse_mode_size(self) -> QSize:
        """
        Calculate size for browse mode.
        
        Returns:
            QSize optimized for browse mode
        """
        # In browse mode, use larger thumbnails for better detail
        base_size = self.BROWSE_MODE_SIZE
        
        # Could be adjusted based on grid layout or zoom level
        return self._clamp_size(base_size)
    
    def calculate_display_size(self, target_size: QSize, available_size: QSize) -> QSize:
        """
        Calculate the actual display size within available space.
        
        Args:
            target_size: Desired target size
            available_size: Available space for display
            
        Returns:
            Actual display size that fits within available space
        """
        try:
            # Ensure thumbnail fits within available space
            scale_w = available_size.width() / target_size.width()
            scale_h = available_size.height() / target_size.height()
            scale = min(scale_w, scale_h, 1.0)  # Don't scale up
            
            display_size = QSize(
                int(target_size.width() * scale),
                int(target_size.height() * scale)
            )
            
            return self._clamp_size(display_size)
            
        except Exception as e:
            self.logger.warning(f"Error calculating display size: {e}")
            return target_size
    
    def calculate_aspect_ratio_size(self, original_size: QSize, target_size: QSize) -> QSize:
        """
        Calculate size maintaining aspect ratio within target bounds.
        
        Args:
            original_size: Original image size
            target_size: Target bounds
            
        Returns:
            Size that maintains aspect ratio within target bounds
        """
        try:
            if original_size.width() == 0 or original_size.height() == 0:
                return target_size
            
            aspect_ratio = original_size.width() / original_size.height()
            target_aspect = target_size.width() / target_size.height()
            
            if aspect_ratio > target_aspect:
                # Image is wider - fit to width
                new_width = target_size.width()
                new_height = int(target_size.width() / aspect_ratio)
            else:
                # Image is taller - fit to height
                new_height = target_size.height()
                new_width = int(target_size.height() * aspect_ratio)
            
            return self._clamp_size(QSize(new_width, new_height))
            
        except Exception as e:
            self.logger.warning(f"Error calculating aspect ratio size: {e}")
            return target_size
    
    def get_grid_cell_size(self, container_width: int, columns: int, spacing: int = 10) -> QSize:
        """
        Calculate cell size for grid layout.
        
        Args:
            container_width: Width of the container
            columns: Number of columns in grid
            spacing: Spacing between items
            
        Returns:
            Size for each grid cell
        """
        try:
            if columns <= 0:
                columns = 1
            
            # Calculate available width per column
            total_spacing = spacing * (columns - 1)
            available_width = container_width - total_spacing
            cell_width = max(available_width // columns, self.MINIMUM_SIZE.width())
            
            # Use square cells for thumbnails
            cell_height = cell_width
            
            return self._clamp_size(QSize(cell_width, cell_height))
            
        except Exception as e:
            self.logger.warning(f"Error calculating grid cell size: {e}")
            return self.BROWSE_MODE_SIZE
    
    def _clamp_size(self, size: QSize) -> QSize:
        """
        Clamp size to minimum and maximum bounds.
        
        Args:
            size: Size to clamp
            
        Returns:
            Clamped size within bounds
        """
        width = max(self.MINIMUM_SIZE.width(), 
                   min(size.width(), self.MAXIMUM_SIZE.width()))
        height = max(self.MINIMUM_SIZE.height(), 
                    min(size.height(), self.MAXIMUM_SIZE.height()))
        
        return QSize(width, height)
    
    def get_size_for_zoom_level(self, base_size: QSize, zoom_factor: float) -> QSize:
        """
        Calculate size for a given zoom level.
        
        Args:
            base_size: Base size before zoom
            zoom_factor: Zoom factor (1.0 = no zoom)
            
        Returns:
            Zoomed size
        """
        try:
            zoom_factor = max(0.1, min(zoom_factor, 5.0))  # Clamp zoom factor
            
            zoomed_size = QSize(
                int(base_size.width() * zoom_factor),
                int(base_size.height() * zoom_factor)
            )
            
            return self._clamp_size(zoomed_size)
            
        except Exception as e:
            self.logger.warning(f"Error calculating zoom size: {e}")
            return base_size
