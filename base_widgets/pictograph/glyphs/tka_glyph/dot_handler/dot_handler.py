# dot_handler.py

from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING

from base_widgets.pictograph.glyphs.tka_glyph.turns_parser import (
    parse_turns_tuple_string,
)
from .dot import Dot
from data.constants import OPP, SAME

if TYPE_CHECKING:
    from ..tka_glyph import TKA_Glyph


class DotHandler:
    def __init__(self, glyph: "TKA_Glyph") -> None:
        self.glyph = glyph
        # Create our Dot instances; they use the cached renderer from Dot
        self.glyph.same_dot = Dot(self)
        self.glyph.opp_dot = Dot(self)
        self.add_dots()
        self.hide_dots()

    def add_dots(self) -> None:
        """Adds the dot items to the glyph’s QGraphicsItemGroup."""
        for dot in [self.glyph.same_dot, self.glyph.opp_dot]:
            if dot.renderer.isValid():
                self.glyph.addToGroup(dot)

    def hide_dots(self) -> None:
        """Hides both dot items."""
        self.glyph.same_dot.hide()
        self.glyph.opp_dot.hide()

    def update_dots(self, turns_tuple: tuple) -> None:
        """
        Updates the dot positions based on the provided turns tuple.
        The first element of the parsed tuple determines which dot is visible.
        """
        direction = parse_turns_tuple_string(turns_tuple)[0]
        padding = 10
        letter_scene_rect = self.glyph.letter_item.sceneBoundingRect()
        letter_scene_center = letter_scene_rect.center()

        # Define the ideal positions for SAME and OPP dots
        dot_positions = {
            SAME: (letter_scene_rect.top() - padding, self.glyph.same_dot),
            OPP: (letter_scene_rect.bottom() + padding, self.glyph.opp_dot),
        }

        # Update each dot's position
        for position, dot in dot_positions.values():
            dot_height = dot.boundingRect().height()
            # Center the dot vertically at the specified position
            dot_center = QPointF(
                letter_scene_center.x(),
                position
                + (-dot_height / 2 if dot == self.glyph.same_dot else dot_height / 2),
            )
            # Offset by the dot’s own boundingRect center
            dot.setPos(dot_center - dot.boundingRect().center())

        # Set visibility based on the direction (SAME or OPP)
        self.glyph.same_dot.setVisible(direction == SAME)
        self.glyph.opp_dot.setVisible(direction == OPP)
