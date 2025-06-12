"""
Start Text Overlay Component for V2 Pictographs

This component replicates v1's BeatStartTextItem functionality by adding
"START" text directly to the pictograph scene, matching v1's exact styling
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

        # Match v1's font styling exactly
        self.setFont(QFont("Georgia", 60, QFont.Weight.DemiBold))

        # Initially hidden
        self.setVisible(False)

        # Add to scene if provided
        if parent_scene:
            parent_scene.addItem(self)

    def show_start_text(self):
        """Show the START text with v1-style positioning"""
        if not self.parent_scene:
            return

        # Calculate padding like v1: scene.height() // 28
        scene_height = self.parent_scene.height()
        text_padding = scene_height // 28

        # Position text with padding from top-left like v1
        self.setPos(QPointF(text_padding, text_padding))

        # Make visible
        self.setVisible(True)

    def hide_start_text(self):
        """Hide the START text"""
        self.setVisible(False)

    def update_for_scene_size(self, scene_size: float):
        """Update positioning when scene size changes"""
        if self.isVisible():
            text_padding = scene_size // 28
            self.setPos(QPointF(text_padding, text_padding))


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
    if start_text_overlay and pictograph_component.scene:
        pictograph_component.scene.removeItem(start_text_overlay)
