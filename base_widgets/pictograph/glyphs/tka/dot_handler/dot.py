# dot.py

from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from base_widgets.pictograph.glyphs.tka.dot_handler.dot_handler import DotHandler

_DOT_RENDERER_CACHE = {}


class Dot(QGraphicsSvgItem):
    def __init__(self, dot_handler: "DotHandler"):
        super().__init__()
        self.dot_handler = dot_handler

        dot_path = get_images_and_data_path("images/same_opp_dot.svg")
        self.renderer: QSvgRenderer = _DOT_RENDERER_CACHE.get(dot_path)

        if not self.renderer:
            new_renderer = QSvgRenderer(dot_path)
            if new_renderer.isValid():
                _DOT_RENDERER_CACHE[dot_path] = new_renderer
                self.renderer = new_renderer

        if self.renderer and self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
