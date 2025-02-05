from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItemGroup

from .dot_handler.dot import Dot
from .dot_handler.dot_handler import DotHandler

from .turns_number_group.turns_number import TurnsNumber
from .tka_letter import TKALetter
from .dash import Dash
from .turns_number_group.turns_number_group import TurnsNumberGroup


if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph import Pictograph


class TKA_Glyph(QGraphicsItemGroup):
    name = "TKA"

    letter_item: TKALetter
    dash: Dash
    top_number: TurnsNumber
    bottom_number: TurnsNumber
    same_dot: Dot
    opp_dot: Dot

    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.letter = None
        self.init_handlers()

    def boundingRect(self):
        return self.childrenBoundingRect()

    def init_handlers(self) -> None:
        self.letter_item = TKALetter(self)
        self.dash = Dash(self)
        self.dot_handler = DotHandler(self)
        self.turns_column = TurnsNumberGroup(self)

    def update_tka_glyph(self, visibility=True) -> None:
        self.letter = self.pictograph.letter
        self.letter_item.set_letter()
        if not self.letter:
            return

        turns_tuple = self.pictograph.get.turns_tuple()
        self.dot_handler.update_dots(turns_tuple)
        self.dash.update_dash()

        self.turns_column.update_turns(turns_tuple)

        self.setVisible(
            self.pictograph.main_widget.settings_manager.visibility.get_glyph_visibility(
                "TKA"
            )
            if visibility
            else False
        )

    def get_all_items(self):
        return [
            self.letter_item,
            self.dash,
            self.same_dot,
            self.opp_dot,
            self.top_number,
            self.bottom_number,
        ]
