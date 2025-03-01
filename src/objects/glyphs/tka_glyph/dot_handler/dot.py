# dot.py

from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from utils.path_helpers import get_data_path, get_image_path

if TYPE_CHECKING:
    from objects.glyphs.tka_glyph.tka_glyph import DotHandler


_DOT_RENDERER_CACHE = {}


class Dot(QGraphicsSvgItem):
    def __init__(self, dot_handler: "DotHandler"):
        super().__init__()
        self.dot_handler = dot_handler

        dot_path = get_image_path("same_opp_dot.svg")
        self.renderer: QSvgRenderer = _DOT_RENDERER_CACHE.get(dot_path)

        if not self.renderer:
            new_renderer = QSvgRenderer(dot_path)
            if new_renderer.isValid():
                _DOT_RENDERER_CACHE[dot_path] = new_renderer
                self.renderer = new_renderer

        if self.renderer and self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
