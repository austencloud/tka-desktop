"""
VTG glyph renderer for pictograph components.

Handles rendering of VTG (Vertical/Timing/Grid) glyphs that show the
classification of pictographs (SS, SO, TS, TO, QS, QO).
"""

import os
from typing import Optional
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from domain.models.core_models import VTGMode
from presentation.components.pictograph.asset_utils import get_image_path


class VTGGlyphRenderer:
    """Handles VTG glyph rendering for pictographs."""

    def __init__(self, scene):
        self.scene = scene
        self.SCENE_SIZE = 950
        self.CENTER_X = 475
        self.CENTER_Y = 475

    def render_vtg_glyph(
        self, vtg_mode: Optional[VTGMode], letter_type: Optional[str] = None
    ) -> None:
        """
        Render the VTG glyph based on VTG mode.

        Args:
            vtg_mode: The VTG mode determining which glyph to show
            letter_type: The letter type (only Type1 letters show VTG glyphs)
        """
        # Only show VTG glyphs for Type1 letters
        if letter_type and letter_type != "Type1":
            return

        if not vtg_mode:
            return

        svg_path = get_image_path(f"vtg_glyphs/{vtg_mode.value}.svg")

        if not os.path.exists(svg_path):
            print(f"Warning: VTG glyph asset not found: {svg_path}")
            return

        # Create and configure the SVG item
        glyph_item = QGraphicsSvgItem()
        renderer = QSvgRenderer(svg_path)

        if renderer.isValid():
            glyph_item.setSharedRenderer(renderer)
            self._position_vtg_glyph(glyph_item)
            self.scene.addItem(glyph_item)
        else:
            print(f"Warning: Failed to load VTG glyph: {svg_path}")

    def _position_vtg_glyph(self, glyph_item: QGraphicsSvgItem) -> None:
        """
        Position the VTG glyph in the pictograph.

        Based on legacy positioning logic from vtg_glyph.py:
        - Positioned in the bottom-right area of the pictograph
        - 4% offset from edges
        """
        pictograph_width = self.SCENE_SIZE
        pictograph_height = self.SCENE_SIZE

        offset_percentage = 0.04
        offset_width = pictograph_width * offset_percentage
        offset_height = pictograph_height * offset_percentage

        width = glyph_item.boundingRect().width()
        height = glyph_item.boundingRect().height()

        # Position in bottom-right corner with offset
        x = pictograph_width - width - offset_width
        y = pictograph_height - height - offset_height

        glyph_item.setPos(x, y)
        glyph_item.setTransformOriginPoint(width / 2, height / 2)
