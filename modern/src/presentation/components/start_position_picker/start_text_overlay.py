"""
Start Text Overlay Component for Modern Pictographs

This component replicates legacy's BeatStartTextItem functionality by adding
"START" text directly to the pictograph scene, matching legacy's exact styling
and positioning.
"""

from typing import Optional
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsScene
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QPointF


class StartTextOverlay(QGraphicsTextItem):
    def __init__(self, parent_scene: Optional[QGraphicsScene] = None):
        super().__init__("START")
        self.parent_scene = parent_scene
        self._is_valid = True

        # Match legacy's font styling exactly
        self.setFont(QFont("Georgia", 60, QFont.Weight.DemiBold))

        # Initially hidden
        self.setVisible(False)

        # Add to scene if provided
        if parent_scene:
            parent_scene.addItem(self)

    def show_start_text(self):
        """Show the START text with legacy-style positioning"""
        if not self._is_valid or not self.parent_scene:
            return

        try:
            # Calculate padding like legacy: scene.height() // 28
            scene_height = self.parent_scene.height()
            text_padding = scene_height // 28

            # Position text with padding from top-left like legacy
            self.setPos(QPointF(text_padding, text_padding))

            # Make visible
            self.setVisible(True)
        except (RuntimeError, AttributeError):
            # Object may have been deleted
            self._is_valid = False

    def hide_start_text(self):
        """Hide the START text"""
        if not self._is_valid:
            return

        try:
            self.setVisible(False)
        except (RuntimeError, AttributeError):
            self._is_valid = False

    def update_for_scene_size(self, scene_size: float):
        """Update positioning when scene size changes"""
        if not self._is_valid:
            return

        try:
            # Check validity before accessing isVisible()
            if self._is_valid:
                # Don't call isVisible() as it might crash, just update position
                text_padding = scene_size // 28
                self.setPos(QPointF(text_padding, text_padding))
        except (RuntimeError, AttributeError):
            self._is_valid = False

    def is_valid(self) -> bool:
        """Check if the overlay is still valid (not deleted)"""
        if not self._is_valid:
            return False

        # Additional check: try to access a Qt property to verify object is still alive
        try:
            # This will raise RuntimeError if the C++ object has been deleted
            _ = self.isVisible()
            return True
        except (RuntimeError, AttributeError):
            # Object has been deleted, mark as invalid
            self._is_valid = False
            return False

    def cleanup(self):
        """Cleanup the overlay safely"""
        # Mark as invalid immediately to prevent further access
        self._is_valid = False


def add_start_text_to_pictograph(pictograph_component) -> Optional[StartTextOverlay]:
    """
    Add START text overlay to a pictograph component.

    Args:
        pictograph_component: SimplePictographComponent instance

    Returns:
        StartTextOverlay instance if successful, None otherwise
    """
    if not hasattr(pictograph_component, "scene") or not pictograph_component.scene:
        return None

    # Create and add the start text overlay
    start_text = StartTextOverlay(pictograph_component.scene)
    start_text.show_start_text()

    return start_text


def remove_start_text_from_pictograph(
    pictograph_component, start_text_overlay: StartTextOverlay
):
    """
    Remove START text overlay from a pictograph component.

    Args:
        pictograph_component: SimplePictographComponent instance
        start_text_overlay: StartTextOverlay instance to remove
    """
    if start_text_overlay:
        # Use the overlay's cleanup method instead of direct scene access
        start_text_overlay.cleanup()

        # Try to remove from scene safely
        try:
            if pictograph_component and pictograph_component.scene:
                pictograph_component.scene.removeItem(start_text_overlay)
        except (RuntimeError, AttributeError):
            # Object may already be deleted - this is expected
            pass
