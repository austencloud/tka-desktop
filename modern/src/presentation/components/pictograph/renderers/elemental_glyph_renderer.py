"""
Elemental glyph renderer for pictograph components.

Handles rendering of elemental glyphs (fire, water, earth, air, sun, moon)
based on VTG mode classification.
"""

import os
from typing import Optional
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from domain.models.core_models import VTGMode, ElementalType
from presentation.components.pictograph.asset_utils import get_image_path


class ElementalGlyphRenderer:
    """Handles elemental glyph rendering for pictographs."""

    # Mapping from VTG modes to elemental types
    VTG_TO_ELEMENTAL = {
        VTGMode.SPLIT_SAME: ElementalType.WATER,
        VTGMode.SPLIT_OPP: ElementalType.FIRE,
        VTGMode.TOG_SAME: ElementalType.EARTH,
        VTGMode.TOG_OPP: ElementalType.AIR,
        VTGMode.QUARTER_SAME: ElementalType.SUN,
        VTGMode.QUARTER_OPP: ElementalType.MOON,
    }

    def __init__(self, scene):
        self.scene = scene
        self.SCENE_SIZE = 950
        self.CENTER_X = 475
        self.CENTER_Y = 475

    def render_elemental_glyph(
        self, vtg_mode: Optional[VTGMode], letter_type: Optional[str] = None
    ) -> None:
        """
        Render the elemental glyph based on VTG mode.

        Args:
            vtg_mode: The VTG mode determining which elemental glyph to show
            letter_type: The letter type (only Type1 letters show elemental glyphs)
        """
        # Only show elemental glyphs for Type1 letters
        if letter_type and letter_type != "Type1":
            return

        if not vtg_mode:
            return

        elemental_type = self.VTG_TO_ELEMENTAL.get(vtg_mode)
        if not elemental_type:
            return

        svg_path = get_image_path(f"elements/{elemental_type.value}.svg")

        if not os.path.exists(svg_path):
            print(f"Warning: Elemental glyph asset not found: {svg_path}")
            return

        # Create and configure the SVG item
        glyph_item = QGraphicsSvgItem()
        renderer = QSvgRenderer(svg_path)

        if renderer.isValid():
            glyph_item.setSharedRenderer(renderer)
            self._position_elemental_glyph(glyph_item)
            self.scene.addItem(glyph_item)
        else:
            print(f"Warning: Failed to load elemental glyph: {svg_path}")

    def _position_elemental_glyph(self, glyph_item: QGraphicsSvgItem) -> None:
        """
        Position the elemental glyph in the top-right corner of the pictograph.

        Based on legacy positioning logic from elemental_glyph.py:
        - 4% offset from edges
        - Positioned in top-right corner
        """
        pictograph_width = self.SCENE_SIZE
        pictograph_height = self.SCENE_SIZE

        offset_percentage = 0.04
        offset_width = pictograph_width * offset_percentage
        offset_height = pictograph_height * offset_percentage

        width = glyph_item.boundingRect().width()
        height = glyph_item.boundingRect().height()

        # Position in top-right corner with offset
        x = pictograph_width - width - offset_width
        y = offset_height

        glyph_item.setPos(x, y)
        glyph_item.setTransformOriginPoint(width / 2, height / 2)
