# dot_handler.py

from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING

from objects.glyphs.tka_glyph.turns_parser import parse_turns_tuple_string


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
            # Check if renderer exists and is valid before adding to group
            if dot.renderer is not None and dot.renderer.isValid():
                self.glyph.addToGroup(dot)
            else:
                print(
                    f"Warning: Dot renderer is None or invalid. Dot will not be displayed."
                )

    def hide_dots(self) -> None:
        """Hides both dot items."""
        # Check if dots exist before trying to hide them
        if hasattr(self.glyph, "same_dot") and self.glyph.same_dot is not None:
            self.glyph.same_dot.hide()
        if hasattr(self.glyph, "opp_dot") and self.glyph.opp_dot is not None:
            self.glyph.opp_dot.hide()

    def update_dots(self, turns_tuple: tuple) -> None:
        """
        Updates the dot positions based on the provided turns tuple.
        The first element of the parsed tuple determines which dot is visible.
        """
        try:
            # Check if the necessary attributes exist
            if not hasattr(self.glyph, "letter_item") or self.glyph.letter_item is None:
                print("Warning: Letter item is not available for positioning dots")
                return

            if not hasattr(self.glyph, "same_dot") or self.glyph.same_dot is None:
                print("Warning: Same dot is not available")
                return

            if not hasattr(self.glyph, "opp_dot") or self.glyph.opp_dot is None:
                print("Warning: Opposite dot is not available")
                return

            # Parse the direction from the turns tuple
            direction = parse_turns_tuple_string(turns_tuple)[0]
            padding = 10

            # Get the letter item's scene rectangle and center
            letter_scene_rect = self.glyph.letter_item.sceneBoundingRect()
            letter_scene_center = letter_scene_rect.center()

            # Create a dictionary mapping direction to (position, dot) pairs
            dot_positions = {
                SAME: (letter_scene_rect.top() - padding, self.glyph.same_dot),
                OPP: (letter_scene_rect.bottom() + padding, self.glyph.opp_dot),
            }

            # Update the position of each dot
            for position, dot in dot_positions.values():
                # Skip if the dot is not valid
                if dot is None or not hasattr(dot, "boundingRect"):
                    continue

                # Calculate the dot's position
                dot_height = dot.boundingRect().height()
                dot_center = QPointF(
                    letter_scene_center.x(),
                    position
                    + (
                        -dot_height / 2
                        if dot == self.glyph.same_dot
                        else dot_height / 2
                    ),
                )
                dot.setPos(dot_center - dot.boundingRect().center())

            # Set the visibility of each dot based on the direction
            if self.glyph.same_dot is not None:
                self.glyph.same_dot.setVisible(direction == SAME)
            if self.glyph.opp_dot is not None:
                self.glyph.opp_dot.setVisible(direction == OPP)

        except Exception as e:
            print(f"Error updating dots: {e}")
