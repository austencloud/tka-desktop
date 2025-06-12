"""
Simplified pictograph scene using modular renderers.

This scene coordinates multiple specialized renderers to create the complete pictograph.
"""

from typing import Optional
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QBrush, QColor

from ...domain.models.core_models import BeatData
from .grid_renderer import GridRenderer
from .prop_renderer import PropRenderer
from .arrow_renderer import ArrowRenderer
from .letter_renderer import LetterRenderer


class PictographScene(QGraphicsScene):
    """Graphics scene for rendering pictographs using modular renderers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.beat_data: Optional[BeatData] = None

        self.SCENE_SIZE = 950
        self.CENTER_X = 475
        self.CENTER_Y = 475

        self.setSceneRect(0, 0, self.SCENE_SIZE, self.SCENE_SIZE)
        self.setBackgroundBrush(QBrush(QColor(255, 255, 255)))

        # Initialize renderers
        self.grid_renderer = GridRenderer(self)
        self.prop_renderer = PropRenderer(self)
        self.arrow_renderer = ArrowRenderer(self)
        self.letter_renderer = LetterRenderer(self)

    def update_beat(self, beat_data: BeatData) -> None:
        """Update the scene with new beat data."""
        self.beat_data = beat_data
        self.clear()
        self._render_pictograph()

    def _render_pictograph(self) -> None:
        """Render the pictograph elements using specialized renderers."""
        if not self.beat_data:
            return

        # Render grid
        self.grid_renderer.render_grid()

        # Render props for blue and red motions
        if self.beat_data.blue_motion:
            self.prop_renderer.render_prop("blue", self.beat_data.blue_motion)
        if self.beat_data.red_motion:
            self.prop_renderer.render_prop("red", self.beat_data.red_motion)

        # Render arrows for blue and red motions
        if self.beat_data.blue_motion:
            self.arrow_renderer.render_arrow("blue", self.beat_data.blue_motion)
        if self.beat_data.red_motion:
            self.arrow_renderer.render_arrow("red", self.beat_data.red_motion)

        # Render letter
        if self.beat_data.letter:
            self.letter_renderer.render_letter(self.beat_data.letter)
