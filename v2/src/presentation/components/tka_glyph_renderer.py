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

from src.domain.models.core_models import LetterType
from src.presentation.components.asset_utils import get_image_path


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
        print(
            f"🔤 TKA GLYPH RENDERER: Called with letter='{letter}', letter_type={letter_type}, has_dash={has_dash}"
        )

        if not letter or not letter_type:
            print(f"🔤 TKA GLYPH RENDERER: Skipping - missing letter or letter_type")
            return

        # Create a group to hold all TKA components
        tka_group = QGraphicsItemGroup()
        print(f"🔤 TKA GLYPH: Created group")

        # Render the letter
        print(f"🔤 TKA GLYPH: Rendering letter '{letter}' with type {letter_type}")
        letter_item = self._render_letter(letter, letter_type)
        if letter_item:
            print(f"🔤 TKA GLYPH: Letter item created successfully")
            tka_group.addToGroup(letter_item)
        else:
            print(f"🔤 TKA GLYPH: ❌ Failed to create letter item")

        # Render the dash if needed
        if has_dash and "-" in letter and letter_item:
            print(f"🔤 TKA GLYPH: Rendering dash")
            dash_item = self._render_dash()
            if dash_item:
                tka_group.addToGroup(dash_item)
                self._position_dash(dash_item, letter_item)

        # Position the entire TKA group
        print(f"🔤 TKA GLYPH: Positioning TKA group")
        self._position_tka_glyph(tka_group)
        print(f"🔤 TKA GLYPH: Adding to scene")
        self.scene.addItem(tka_group)
        print(f"🔤 TKA GLYPH: ✅ Successfully added TKA glyph to scene")

    def _render_letter(
        self, letter: str, letter_type: LetterType
    ) -> Optional[QGraphicsSvgItem]:
        """Render the letter SVG."""
        print(f"🔤 _render_letter: letter='{letter}', letter_type={letter_type}")

        # Determine the SVG path based on letter type
        svg_path = get_image_path(f"letters_trimmed/{letter_type.value}/{letter}.svg")
        print(f"🔤 _render_letter: svg_path='{svg_path}'")

        if not os.path.exists(svg_path):
            print(f"🔤 _render_letter: ❌ Letter glyph asset not found: {svg_path}")
            return None

        print(f"🔤 _render_letter: ✅ SVG file exists, creating QGraphicsSvgItem")
        letter_item = QGraphicsSvgItem()
        renderer = QSvgRenderer(svg_path)
        print(f"🔤 _render_letter: Created QSvgRenderer, isValid={renderer.isValid()}")

        if renderer.isValid():
            letter_item.setSharedRenderer(renderer)
            print(f"🔤 _render_letter: ✅ Successfully created letter item")
            return letter_item
        else:
            print(f"🔤 _render_letter: ❌ Failed to load letter glyph: {svg_path}")
            return None

    def _render_dash(self) -> Optional[QGraphicsSvgItem]:
        """Render the dash SVG."""
        svg_path = get_image_path("dash.svg")

        if not os.path.exists(svg_path):
            print(f"Warning: Dash glyph asset not found: {svg_path}")
            return None

        dash_item = QGraphicsSvgItem()
        renderer = QSvgRenderer(svg_path)

        if renderer.isValid():
            dash_item.setSharedRenderer(renderer)
            return dash_item
        else:
            print(f"Warning: Failed to load dash glyph: {svg_path}")
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

        Based on v1 positioning logic from tka_letter.py:
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
