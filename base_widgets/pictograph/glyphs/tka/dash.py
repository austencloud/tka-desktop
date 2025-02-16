from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from .tka_glyph import TKA_Glyph


class Dash(QGraphicsSvgItem):
    def __init__(self, glyph: "TKA_Glyph") -> None:
        super().__init__()
        self.glyph = glyph
        self.glyph.addToGroup(self)

    def add_dash(self) -> None:
        dash_path = get_images_and_data_path("images/dash.svg")
        renderer = QSvgRenderer(dash_path)
        if renderer.isValid():
            self.setSharedRenderer(renderer)
        self.setVisible(True)

    def position_dash(self) -> None:
        padding = 5
        if self:
            letter_scene_rect = self.glyph.letter_item.sceneBoundingRect()
            dash_x = letter_scene_rect.right() + padding
            dash_y = letter_scene_rect.center().y() - self.boundingRect().height() / 2
            self.setPos(dash_x, dash_y)

    def update_dash(self) -> None:
        if "-" in self.glyph.pictograph.letter.value:
            self.add_dash()
            self.position_dash()
        else:
            self.setVisible(False)
