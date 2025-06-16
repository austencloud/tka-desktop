# tka_glyph.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItemGroup

from src.legacy_settings_manager.global_settings.app_context import AppContext

from .dot_handler.dot import Dot
from .dot_handler.dot_handler import DotHandler
from .turns_number_group.turns_number import TurnsNumber
from .tka_letter import TKALetter
from .dash import Dash
from .turns_number_group.turns_column import TurnsColumn

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class TKA_Glyph(QGraphicsItemGroup):
    name = "TKA"

    letter_item: TKALetter
    dash: Dash
    top_number: TurnsNumber
    bottom_number: TurnsNumber
    same_dot: Dot
    opp_dot: Dot

    def __init__(self, pictograph: "LegacyPictograph") -> None:
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
        self.turns_column = TurnsColumn(self)

    def update_tka_glyph(self, visible=True) -> None:
        self.letter = self.pictograph.state.letter
        if not self.letter or self.pictograph.state.hide_tka_glyph:
            self.setVisible(False)
            return
        self.setVisible(
            AppContext.settings_manager().visibility.get_glyph_visibility("TKA")
            if visible
            else False
        )

        self.letter_item.set_letter()
        turns_tuple = self.pictograph.managers.get.turns_tuple()
        self.dot_handler.update_dots(turns_tuple)
        self.dash.update_dash()
        self.turns_column.update_turns_column(turns_tuple)

    def get_all_items(self):
        return [
            self.letter_item,
            self.dash,
            self.same_dot,
            self.opp_dot,
            self.top_number,
            self.bottom_number,
        ]
