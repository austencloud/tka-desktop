from PyQt6.QtWidgets import QGraphicsItemGroup
from typing import TYPE_CHECKING
from .turns_tuple_interpretor import TurnsTupleInterpreter
from .turns_number import TurnsNumber
from utils.path_helpers import get_image_path
from ..turns_parser import parse_turns_tuple_string

if TYPE_CHECKING:
    from ..tka_glyph import TKA_Glyph


class TurnsColumn(QGraphicsItemGroup):
    def __init__(self, glyph: "TKA_Glyph") -> None:
        super().__init__()
        self.glyph = glyph

        # Get the path to the numbers directory
        self.svg_path_prefix = get_image_path("numbers/")

        # Try to get the blank.svg path, with fallback options
        try:
            import os

            # First try the standard path
            self.blank_svg_path = get_image_path("blank.svg")

            # Check if the file exists
            if not os.path.exists(self.blank_svg_path):
                # Try alternate locations
                possible_paths = [
                    os.path.join(os.path.dirname(self.svg_path_prefix), "blank.svg"),
                    os.path.abspath(
                        os.path.join(os.getcwd(), "src", "images", "blank.svg")
                    ),
                    os.path.abspath(os.path.join(os.getcwd(), "images", "blank.svg")),
                ]

                for path in possible_paths:
                    if os.path.exists(path):
                        self.blank_svg_path = path
                        break
                else:
                    # If still not found, use a path that will trigger the fallback in TurnsNumber
                    self.blank_svg_path = (
                        "blank.svg"  # This will trigger the fallback mechanism
                    )
        except Exception:
            self.blank_svg_path = (
                "blank.svg"  # This will trigger the fallback mechanism
            )

        self.glyph.top_number = TurnsNumber(self)
        self.glyph.bottom_number = TurnsNumber(self)
        self.glyph.addToGroup(self)

        self.interpreter = TurnsTupleInterpreter(glyph)

    def set_number(self, numeric_value: str, is_top: bool, color: str = None) -> None:
        new_item = self.glyph.top_number if is_top else self.glyph.bottom_number

        if color:
            new_item.set_color(color)

        new_item.load_number_svg(numeric_value)

        old_item = self.glyph.top_number if is_top else self.glyph.bottom_number
        if old_item:
            self.removeFromGroup(old_item)

        self.addToGroup(new_item)
        if is_top:
            self.glyph.top_number = new_item
        else:
            self.glyph.bottom_number = new_item

    def position_turns(self) -> None:
        reference_rect = (
            self.glyph.dash.sceneBoundingRect()
            if self.glyph.dash.isVisible()
            else self.glyph.letter_item.sceneBoundingRect()
        )
        letter_scene_rect = self.glyph.letter_item.sceneBoundingRect()
        base_pos_x = reference_rect.right() + 15
        high_pos_y = letter_scene_rect.top() - 5
        low_pos_y = (
            letter_scene_rect.bottom()
            - (
                self.glyph.bottom_number.boundingRect().height()
                if self.glyph.bottom_number
                else 0
            )
            + 5
        )
        if self.glyph.top_number:
            self.glyph.top_number.setPos(base_pos_x, high_pos_y)
        if self.glyph.bottom_number:
            adjusted_low_pos_y = low_pos_y if self.glyph.top_number else high_pos_y + 20
            self.glyph.bottom_number.setPos(base_pos_x, adjusted_low_pos_y)

    def update_turns_column(self, turns_tuple: str) -> None:
        _, raw_top_val, raw_bottom_val = parse_turns_tuple_string(turns_tuple)
        top_val_str = str(raw_top_val)
        bottom_val_str = str(raw_bottom_val)

        top_key = f"top_{top_val_str}"
        bottom_key = f"bottom_{bottom_val_str}"

        color_map = self.interpreter.interpret_turns_tuple(top_key, bottom_key)

        self.glyph.top_number.setVisible(
            bool(float(top_val_str) if not top_val_str == "fl" else True)
        )
        self.glyph.bottom_number.setVisible(
            bool(float(bottom_val_str if not bottom_val_str == "fl" else True))
        )

        self.set_number(top_val_str, True, color_map.get(top_key))
        self.set_number(bottom_val_str, False, color_map.get(bottom_key))

        self.position_turns()
