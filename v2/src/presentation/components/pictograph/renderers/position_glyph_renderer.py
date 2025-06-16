"""
Start-to-end position glyph renderer for pictograph components.

Handles rendering of position glyphs that show the start and end positions
with an arrow between them (e.g., α → β).
"""

import os
from typing import Optional
from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from presentation.components.pictograph.asset_utils import get_image_path


class PositionGlyphRenderer:
    """Handles start-to-end position glyph rendering for pictographs."""

    # Mapping from position names to SVG files
    POSITION_SVGS = {
        "alpha": "α.svg",
        "beta": "β.svg",
        "gamma": "Γ.svg",
    }

    def __init__(self, scene):
        self.scene = scene
        self.SCENE_SIZE = 950
        self.CENTER_X = 475
        self.CENTER_Y = 475

    def render_position_glyph(
        self,
        start_position: Optional[str] = None,
        end_position: Optional[str] = None,
        letter: Optional[str] = None,
    ) -> None:
        """
        Render the start-to-end position glyph.

        Args:
            start_position: The starting position (e.g., "alpha")
            end_position: The ending position (e.g., "beta")
            letter: The letter (skip rendering for α, β, Γ letters)
        """
        # Don't show position glyph for alpha, beta, gamma letters
        if letter and letter in ["α", "β", "Γ"]:
            return

        if not start_position or not end_position:
            return

        # Extract alphabetic parts from positions
        start_pos = "".join(filter(str.isalpha, start_position))
        end_pos = "".join(filter(str.isalpha, end_position))

        # Create a group to hold all position components
        position_group = QGraphicsItemGroup()

        # Render start position
        start_item = self._render_position_symbol(start_pos)
        if start_item:
            position_group.addToGroup(start_item)

        # Render arrow
        arrow_item = self._render_arrow()
        if arrow_item:
            position_group.addToGroup(arrow_item)

        # Render end position
        end_item = self._render_position_symbol(end_pos)
        if end_item:
            position_group.addToGroup(end_item)

        # Position all elements within the group
        if start_item and arrow_item and end_item:
            self._position_elements(start_item, arrow_item, end_item)

        # Position the entire group in the pictograph
        self._position_position_glyph(position_group)
        self.scene.addItem(position_group)

    def _render_position_symbol(self, position: str) -> Optional[QGraphicsSvgItem]:
        """Render a position symbol (α, β, Γ)."""
        svg_filename = self.POSITION_SVGS.get(position.lower())
        if not svg_filename:
            print(f"Warning: Unknown position symbol: {position}")
            return None

        svg_path = get_image_path(f"letters_trimmed/Type6/{svg_filename}")

        if not os.path.exists(svg_path):
            print(f"Warning: Position symbol asset not found: {svg_path}")
            return None

        symbol_item = QGraphicsSvgItem()
        renderer = QSvgRenderer(svg_path)

        if renderer.isValid():
            symbol_item.setSharedRenderer(renderer)
            # Apply scaling to match legacy behavior
            scale_factor = 0.75
            symbol_item.setScale(scale_factor)
            return symbol_item
        else:
            print(f"Warning: Failed to load position symbol: {svg_path}")
            return None

    def _render_arrow(self) -> Optional[QGraphicsSvgItem]:
        """Render the arrow between positions."""
        svg_path = get_image_path("arrow.svg")

        if not os.path.exists(svg_path):
            print(f"Warning: Arrow asset not found: {svg_path}")
            return None

        arrow_item = QGraphicsSvgItem()
        renderer = QSvgRenderer(svg_path)

        if renderer.isValid():
            arrow_item.setSharedRenderer(renderer)
            # Apply scaling to match legacy behavior
            scale_factor = 0.75
            arrow_item.setScale(scale_factor)
            return arrow_item
        else:
            print(f"Warning: Failed to load arrow: {svg_path}")
            return None

    def _position_elements(
        self,
        start_item: QGraphicsSvgItem,
        arrow_item: QGraphicsSvgItem,
        end_item: QGraphicsSvgItem,
    ) -> None:
        """Position the start symbol, arrow, and end symbol horizontally."""
        spacing = 25  # Spacing between elements
        scale_factor = 0.75

        # Position start symbol at origin
        start_item.setPos(0, 0)

        # Position arrow after start symbol with proper spacing (matching legacy logic)
        arrow_x = (
            start_item.boundingRect().width() * scale_factor + spacing * scale_factor
        )
        # Center arrow vertically relative to start symbol (matching legacy logic)
        arrow_y = (
            start_item.boundingRect().height() * scale_factor // 2
            - arrow_item.boundingRect().height() * scale_factor
        )
        arrow_item.setPos(arrow_x, arrow_y)

        # Position end symbol after arrow with proper spacing
        end_x = (
            start_item.boundingRect().width() * scale_factor
            + arrow_item.boundingRect().width() * scale_factor
            + spacing
        )
        end_item.setPos(end_x, 0)

    def _position_position_glyph(self, position_group: QGraphicsItemGroup) -> None:
        """
        Position the position glyph in the pictograph.

        Uses legacy's precise positioning logic from start_to_end_pos_glyph.py:
        - Calculate total width manually to match legacy behavior
        - Center horizontally at top of pictograph
        """
        if not position_group.childItems():
            return

        # Get individual items from the group
        items = position_group.childItems()
        if len(items) < 3:
            return

        # Calculate total width using legacy's method for precise alignment
        scale_factor = 0.75
        spacing = 25

        # Find start, arrow, and end items (they should be in order)
        start_item = items[0]
        arrow_item = items[1]
        end_item = items[2]

        # Calculate total width exactly like legacy
        total_width = (
            start_item.boundingRect().width() * scale_factor
            + arrow_item.boundingRect().width() * scale_factor
            + end_item.boundingRect().width() * scale_factor
            + spacing
        )

        # Center horizontally using legacy's calculation (integer division for exact match)
        x_position = self.SCENE_SIZE // 2 - total_width // 2
        y_position = 50  # 50px from top

        position_group.setPos(x_position, y_position)
