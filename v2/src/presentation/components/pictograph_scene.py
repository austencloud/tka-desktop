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
from .elemental_glyph_renderer import ElementalGlyphRenderer
from .vtg_glyph_renderer import VTGGlyphRenderer
from .tka_glyph_renderer import TKAGlyphRenderer
from .position_glyph_renderer import PositionGlyphRenderer


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

        # Initialize glyph renderers
        self.elemental_glyph_renderer = ElementalGlyphRenderer(self)
        self.vtg_glyph_renderer = VTGGlyphRenderer(self)
        self.tka_glyph_renderer = TKAGlyphRenderer(self)
        self.position_glyph_renderer = PositionGlyphRenderer(self)

    def update_beat(self, beat_data: BeatData) -> None:
        """Update the scene with new beat data."""
        self.beat_data = beat_data
        self.clear()
        # Clear prop renderer cache for new beat
        self.prop_renderer.clear_rendered_props()
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

        # Apply beta prop positioning after both props are rendered
        if self.beat_data.blue_motion and self.beat_data.red_motion:
            self.prop_renderer.apply_beta_positioning(self.beat_data)

        # Render arrows for blue and red motions
        if self.beat_data.blue_motion:
            self.arrow_renderer.render_arrow("blue", self.beat_data.blue_motion)
        if self.beat_data.red_motion:
            self.arrow_renderer.render_arrow("red", self.beat_data.red_motion)

        # Render letter
        if self.beat_data.letter:
            self.letter_renderer.render_letter(self.beat_data.letter)

        # Render glyphs if glyph data is available
        if self.beat_data.glyph_data:
            glyph_data = self.beat_data.glyph_data

            # Render elemental glyph
            if glyph_data.show_elemental and glyph_data.vtg_mode:
                self.elemental_glyph_renderer.render_elemental_glyph(
                    glyph_data.vtg_mode,
                    glyph_data.letter_type.value if glyph_data.letter_type else None,
                )

            # Render VTG glyph
            if glyph_data.show_vtg and glyph_data.vtg_mode:
                self.vtg_glyph_renderer.render_vtg_glyph(
                    glyph_data.vtg_mode,
                    glyph_data.letter_type.value if glyph_data.letter_type else None,
                )

            # Render TKA glyph
            if glyph_data.show_tka and self.beat_data.letter and glyph_data.letter_type:
                self.tka_glyph_renderer.render_tka_glyph(
                    self.beat_data.letter,
                    glyph_data.letter_type,
                    glyph_data.has_dash,
                    glyph_data.turns_data,
                )

            # Render position glyph
            if (
                glyph_data.show_positions
                and glyph_data.start_position
                and glyph_data.end_position
            ):
                self.position_glyph_renderer.render_position_glyph(
                    glyph_data.start_position,
                    glyph_data.end_position,
                    self.beat_data.letter,
                )
