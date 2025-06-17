"""
TKA glyph renderer for pictograph components.

Handles rendering of TKA (The Kinetic Alphabet) glyphs that show the
letter, dash, dots, and turn numbers for pictographs.
"""

import os
from typing import Optional
from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from domain.models.core_models import LetterType
from presentation.components.pictograph.asset_utils import get_image_path


class TKAGlyphRenderer:
    """Handles TKA glyph rendering for pictographs."""

    def __init__(self, scene):
        self.scene = scene
        self.SCENE_SIZE = 950
        self.CENTER_X = 475
        self.CENTER_Y = 475

    def render_tka_glyph(
        self,
        letter: Optional[str] = None,
        letter_type: Optional[LetterType] = None,
        has_dash: bool = False,
        turns_data: Optional[str] = None,
    ) -> None:
        """
        Render the TKA glyph with letter, dash, and turns information.

        Args:
            letter: The letter to display
            letter_type: The type of letter determining the SVG path
            has_dash: Whether to show a dash after the letter
            turns_data: Turn information for dots and numbers
        """
        if not letter or not letter_type:
            return

        # Create a group to hold all TKA components
        tka_group = QGraphicsItemGroup()

        # Render the letter
        letter_item = self._render_letter(letter, letter_type)
        if letter_item:
            tka_group.addToGroup(letter_item)

        # Render the dash if needed
        # Don't add separate dash for Type3 and Type5 letters as they already include dash in SVG
        # Also don't add dash for Type6 letters (α, β, Γ) as they never have dashes
        if (
            has_dash
            and "-" in letter
            and letter_item
            and letter_type
            not in [LetterType.TYPE3, LetterType.TYPE5, LetterType.TYPE6]
        ):
            dash_item = self._render_dash()
            if dash_item:
                tka_group.addToGroup(dash_item)
                self._position_dash(dash_item, letter_item)

        # Position the entire TKA group
        self._position_tka_glyph(tka_group)
        self.scene.addItem(tka_group)

    def _render_letter(
        self, letter: str, letter_type: LetterType
    ) -> Optional[QGraphicsSvgItem]:
        """Render the letter SVG."""

        # Determine the SVG path based on letter type
        svg_path = get_image_path(f"letters_trimmed/{letter_type.value}/{letter}.svg")

        if not os.path.exists(svg_path):
            return None

        renderer = QSvgRenderer(svg_path)

        if renderer.isValid():
            letter_item = QGraphicsSvgItem()
            letter_item.setSharedRenderer(renderer)
            return letter_item
        return None

    def _render_dash(self) -> Optional[QGraphicsSvgItem]:
        """Render the dash SVG."""
        svg_path = get_image_path("dash.svg")

        if not os.path.exists(svg_path):
            return None

        dash_item = QGraphicsSvgItem()
        renderer = QSvgRenderer(svg_path)

        if renderer.isValid():
            dash_item.setSharedRenderer(renderer)
            return dash_item
        else:
            return None

    def _position_dash(
        self, dash_item: QGraphicsSvgItem, letter_item: QGraphicsSvgItem
    ) -> None:
        """Position the dash relative to the letter."""
        if not letter_item:
            return

        padding = 5
        letter_rect = letter_item.boundingRect()
        dash_x = letter_rect.right() + padding
        dash_y = letter_rect.center().y() - dash_item.boundingRect().height() / 2
        dash_item.setPos(dash_x, dash_y)

    def _position_tka_glyph(self, tka_group: QGraphicsItemGroup) -> None:
        """
        Position the TKA glyph in the bottom-left area of the pictograph.

        Based on legacy positioning logic from tka_letter.py:
        - Positioned in bottom-left area
        - Specific offset from bottom edge
        """
        if not tka_group.childItems():
            return

        # Get the first child (letter) for positioning reference
        letter_item = tka_group.childItems()[0]
        letter_height = letter_item.boundingRect().height()

        x = int(letter_height / 1.5)
        y = int(self.SCENE_SIZE - (letter_height * 1.7))

        tka_group.setPos(x, y)
