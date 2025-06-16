"""
Thumbnail Event Handler - Manages user interactions and selection states.

Extracted from ThumbnailImageLabel to follow Single Responsibility Principle.
"""

import logging
from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

from data.constants import GOLD, BLUE

if TYPE_CHECKING:
    from ..thumbnail_box import ThumbnailBox


class ThumbnailEventHandler:
    """
    Handles user interactions and visual states for thumbnails.
    
    Responsibilities:
    - Mouse event handling (press, enter, leave)
    - Selection state management
    - Border color management
    - Cursor state management
    """
    
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        self.thumbnail_box = thumbnail_box
        self.logger = logging.getLogger(__name__)
        
        # State tracking
        self._is_selected = False
        self._is_hovered = False
        self._border_color: Optional[str] = None
    
    def handle_mouse_press(self, event) -> None:
        """
        Handle mouse press events for thumbnail selection.
        
        Args:
            event: QMouseEvent from the thumbnail label
        """
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                # Get the thumbnail label that was clicked
                thumbnail_label = event.source() if hasattr(event, 'source') else None
                
                if thumbnail_label and hasattr(thumbnail_label, 'index'):
                    index = thumbnail_label.index
                    self.logger.debug(f"Thumbnail clicked: index {index}")
                    
                    # Delegate to thumbnail box for selection handling
                    if hasattr(self.thumbnail_box, 'handle_thumbnail_selection'):
                        self.thumbnail_box.handle_thumbnail_selection(index)
                    
                    # Update selection state
                    self.set_selection_state(True)
                    
        except Exception as e:
            self.logger.warning(f"Error handling mouse press: {e}")
    
    def handle_enter_event(self, event) -> None:
        """
        Handle mouse enter events for hover effects.
        
        Args:
            event: QEnterEvent from the thumbnail label
        """
        try:
            self._is_hovered = True
            
            # Set hover cursor
            if hasattr(event, 'source') and event.source():
                event.source().setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            
            # Update border color for hover effect
            if not self._is_selected:
                self._border_color = BLUE
                self._update_visual_state()
                
        except Exception as e:
            self.logger.debug(f"Error handling enter event: {e}")
    
    def handle_leave_event(self, event) -> None:
        """
        Handle mouse leave events to remove hover effects.
        
        Args:
            event: QEvent from the thumbnail label
        """
        try:
            self._is_hovered = False
            
            # Reset cursor
            if hasattr(event, 'source') and event.source():
                event.source().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            
            # Update border color (remove hover if not selected)
            if not self._is_selected:
                self._border_color = None
                self._update_visual_state()
                
        except Exception as e:
            self.logger.debug(f"Error handling leave event: {e}")
    
    def set_selection_state(self, selected: bool) -> None:
        """
        Set the selection state of the thumbnail.
        
        Args:
            selected: Whether the thumbnail is selected
        """
        self._is_selected = selected
        
        if selected:
            self._border_color = GOLD
        else:
            # If not selected but hovered, show hover color
            self._border_color = BLUE if self._is_hovered else None
        
        self._update_visual_state()
        self.logger.debug(f"Selection state changed: selected={selected}")
    
    def get_border_color(self) -> Optional[str]:
        """
        Get the current border color based on state.
        
        Returns:
            Border color string or None
        """
        return self._border_color
    
    def is_selected(self) -> bool:
        """
        Check if thumbnail is currently selected.
        
        Returns:
            True if selected, False otherwise
        """
        return self._is_selected
    
    def is_hovered(self) -> bool:
        """
        Check if thumbnail is currently hovered.
        
        Returns:
            True if hovered, False otherwise
        """
        return self._is_hovered
    
    def _update_visual_state(self) -> None:
        """Update the visual state of the thumbnail based on current state."""
        try:
            # This would trigger a repaint of the thumbnail with new border color
            # The actual implementation would depend on how the thumbnail label
            # handles visual updates
            self.logger.debug(f"Visual state updated: border_color={self._border_color}")
            
        except Exception as e:
            self.logger.debug(f"Error updating visual state: {e}")
    
    def reset_state(self) -> None:
        """Reset all interaction states."""
        self._is_selected = False
        self._is_hovered = False
        self._border_color = None
        self._update_visual_state()
        self.logger.debug("Event handler state reset")
