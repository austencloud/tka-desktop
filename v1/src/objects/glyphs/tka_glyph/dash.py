# dash.py

from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from utils.path_helpers import get_data_path, get_image_path

if TYPE_CHECKING:
    from .tka_glyph import TKA_Glyph

_DASH_RENDERER_CACHE = {}


class Dash(QGraphicsSvgItem):
    def __init__(self, glyph: "TKA_Glyph") -> None:
        super().__init__()
        self.glyph = glyph
        self.glyph.addToGroup(self)

    def add_dash(self) -> None:
        dash_path = get_image_path("dash.svg")
        renderer = _DASH_RENDERER_CACHE.get(dash_path)

        if not renderer:
            new_renderer = QSvgRenderer(dash_path)
            if new_renderer.isValid():
                _DASH_RENDERER_CACHE[dash_path] = new_renderer
                renderer = new_renderer

        if renderer and renderer.isValid():
            self.setSharedRenderer(renderer)
            self.setVisible(True)

    def position_dash(self) -> None:
        if not self.isVisible():
            return

        padding = 5
        letter_scene_rect = self.glyph.letter_item.sceneBoundingRect()
        dash_x = letter_scene_rect.right() + padding
        dash_y = letter_scene_rect.center().y() - self.boundingRect().height() / 2
        self.setPos(dash_x, dash_y)

    def update_dash(self) -> None:

        if "-" in self.glyph.pictograph.state.letter.value:
            self.add_dash()
            self.position_dash()
        else:
            self.setVisible(False)
