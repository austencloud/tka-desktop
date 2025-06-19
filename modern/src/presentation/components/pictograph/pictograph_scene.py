"""
Simplified pictograph scene using modular renderers.

This scene coordinates multiple specialized renderers to create the complete pictograph.
"""

from typing import Optional
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QBrush, QColor

from domain.models.core_models import BeatData, LetterType
from domain.models.letter_type_classifier import LetterTypeClassifier

from presentation.components.pictograph.renderers.grid_renderer import GridRenderer
from presentation.components.pictograph.renderers.prop_renderer import PropRenderer
from presentation.components.pictograph.renderers.arrow_renderer import ArrowRenderer
from presentation.components.pictograph.renderers.letter_renderer import LetterRenderer
from presentation.components.pictograph.renderers.elemental_glyph_renderer import (
    ElementalGlyphRenderer,
)
from presentation.components.pictograph.renderers.vtg_glyph_renderer import (
    VTGGlyphRenderer,
)
from presentation.components.pictograph.renderers.tka_glyph_renderer import (
    TKAGlyphRenderer,
)
from presentation.components.pictograph.renderers.position_glyph_renderer import (
    PositionGlyphRenderer,
)


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
        self.letter_renderer = LetterRenderer(self)  # Initialize glyph renderers
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
            self.prop_renderer.apply_beta_positioning(
                self.beat_data
            )  # Render arrows for blue and red motions
        # Create full pictograph data for Type 3 detection
        full_pictograph_data = None
        if self.beat_data.blue_motion and self.beat_data.red_motion:
            from domain.models.pictograph_models import PictographData, ArrowData

            blue_arrow = ArrowData(motion_data=self.beat_data.blue_motion, color="blue")
            red_arrow = ArrowData(motion_data=self.beat_data.red_motion, color="red")

            # CRITICAL FIX: Include letter information for special placement service
            full_pictograph_data = PictographData(
                arrows={"blue": blue_arrow, "red": red_arrow},
                letter=self.beat_data.letter,  # This enables special placement and logging
            )

        if self.beat_data.blue_motion:
            # Create single-arrow pictograph data if full data doesn't exist
            single_blue_data = full_pictograph_data
            if not full_pictograph_data:
                from domain.models.pictograph_models import PictographData, ArrowData

                blue_arrow = ArrowData(
                    motion_data=self.beat_data.blue_motion, color="blue"
                )
                single_blue_data = PictographData(
                    arrows={"blue": blue_arrow}, letter=self.beat_data.letter
                )

            self.arrow_renderer.render_arrow(
                "blue", self.beat_data.blue_motion, single_blue_data
            )
        if self.beat_data.red_motion:
            # Create single-arrow pictograph data if full data doesn't exist
            single_red_data = full_pictograph_data
            if not full_pictograph_data:
                from domain.models.pictograph_models import PictographData, ArrowData

                red_arrow = ArrowData(
                    motion_data=self.beat_data.red_motion, color="red"
                )
                single_red_data = PictographData(
                    arrows={"red": red_arrow}, letter=self.beat_data.letter
                )

            self.arrow_renderer.render_arrow(
                "red", self.beat_data.red_motion, single_red_data
            )

        # Render glyphs if glyph data is available
        # Note: Letters are rendered via TKA glyph, not simple letter renderer
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
                )  # Render TKA glyph
            if glyph_data.show_tka and self.beat_data.letter:
                # Determine the correct letter type from the actual letter
                letter_type_str = LetterTypeClassifier.get_letter_type(
                    self.beat_data.letter
                )
                letter_type = LetterType(letter_type_str)

                self.tka_glyph_renderer.render_tka_glyph(
                    self.beat_data.letter,
                    letter_type,
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
