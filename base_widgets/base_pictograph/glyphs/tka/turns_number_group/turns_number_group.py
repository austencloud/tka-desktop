from PyQt6.QtWidgets import QGraphicsItemGroup
from typing import TYPE_CHECKING, Union

from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from .turns_number import TurnsNumber
from utilities.path_helpers import get_images_and_data_path
from ..turns_parser import parse_turns_tuple_string

if TYPE_CHECKING:
    from ..tka_glyph import TKA_Glyph


class TurnsNumberGroup(QGraphicsItemGroup):
    def __init__(self, glyph: "TKA_Glyph") -> None:
        super().__init__()
        self.glyph = glyph
        self.svg_path_prefix = get_images_and_data_path("images/numbers/")
        self.blank_svg_path = get_images_and_data_path("images/blank.svg")
        self.glyph.top_number = TurnsNumber(self)
        self.glyph.bottom_number = TurnsNumber(self)
        self.glyph.addToGroup(self)

    def set_number(self, number: Union[int, float, str], is_top: bool) -> None:
        new_item = self.glyph.top_number if is_top else self.glyph.bottom_number
        new_item.load_number_svg(number)
        old_item = self.glyph.top_number if is_top else self.glyph.bottom_number

        if old_item:
            self.removeFromGroup(old_item)

        if new_item:
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

    def update_turns(self, turns_tuple: str) -> None:
        _, top_turn, bottom_turn = parse_turns_tuple_string(turns_tuple)

        self.glyph.top_number.setVisible(bool(top_turn))
        self.glyph.bottom_number.setVisible(bool(bottom_turn))
        for turn, is_top in [(top_turn, True), (bottom_turn, False)]:
            self.set_number(turn, is_top)

        self.position_turns()
