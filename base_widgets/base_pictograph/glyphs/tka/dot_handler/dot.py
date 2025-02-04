from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from ..dot_handler import DotHandler


class Dot(QGraphicsSvgItem):
    def __init__(self, dot_handler: "DotHandler"):
        super().__init__()
        self.dot_handler = dot_handler
        dot_path = get_images_and_data_path("images/same_opp_dot.svg")

        self.renderer: QSvgRenderer = QSvgRenderer(dot_path)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
        else:
            print(f"Warning: Renderer for {dot_path} is not valid.")
