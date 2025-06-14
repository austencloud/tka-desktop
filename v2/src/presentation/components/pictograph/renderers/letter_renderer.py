"""
Letter renderer for pictograph components.

Handles rendering of letter text elements with V1-style positioning and styling.
"""

from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont, QColor


class LetterRenderer:
    """Handles letter rendering for pictographs with V1-style positioning."""

    def __init__(self, scene):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.RADIUS = 300

    def render_letter(self, letter: str) -> None:
        """Render the letter with V1-style positioning and styling."""
        if not letter:
            return

        # Create letter text item with V1-style font and positioning
        letter_item = QGraphicsTextItem(letter)

        # Use V1-style font: larger, bold, and properly positioned
        font = QFont("Arial", 48, QFont.Weight.Bold)  # Increased size for visibility
        letter_item.setFont(font)

        # Set V1-style color (black text)
        letter_item.setDefaultTextColor(QColor(0, 0, 0))

        # V1-style positioning: center the letter below the grid
        # Calculate text bounds for proper centering
        text_rect = letter_item.boundingRect()

        # Position letter below the grid, centered horizontally
        x_pos = self.CENTER_X - (text_rect.width() / 2)
        y_pos = self.CENTER_Y + self.RADIUS + 30  # Below the grid with padding

        letter_item.setPos(x_pos, y_pos)

        # Add to scene
        self.scene.addItem(letter_item)

        print(f"📝 Letter '{letter}' rendered at ({x_pos:.1f}, {y_pos:.1f})")
