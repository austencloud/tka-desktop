"""
Letter renderer for pictograph components.

Handles rendering of letter text elements.
"""

from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont


class LetterRenderer:
    """Handles letter rendering for pictographs."""

    def __init__(self, scene):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.RADIUS = 300

    def render_letter(self, letter: str) -> None:
        """Render the letter if present."""
        if not letter:
            return

        letter_item = QGraphicsTextItem(letter)
        font = QFont("Arial", 24, QFont.Weight.Bold)
        letter_item.setFont(font)

        letter_item.setPos(self.CENTER_X - 10, self.CENTER_Y + self.RADIUS + 20)
        self.scene.addItem(letter_item)
