from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from typing import TYPE_CHECKING, Union

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from base_widgets.base_pictograph.glyphs.tka.turns_number_group.turns_number_group import TurnsNumberGroup


class TurnsNumber(QGraphicsSvgItem):
    def __init__(self, turns_column: "TurnsNumberGroup"):
        super().__init__()
        self.turns_column = turns_column
        self.svg_path_prefix = turns_column.svg_path_prefix
        self.blank_svg_path = turns_column.blank_svg_path
        self.number_svg_cache = {}

    def load_number_svg(self, number: Union[int, float, str]) -> None:
        if number == "fl":
            svg_path = get_images_and_data_path("images/numbers/float.svg")
        else:
            svg_path = (
                self.blank_svg_path
                if number == 0
                else f"{self.svg_path_prefix}{number}.svg"
            )

        if svg_path not in self.number_svg_cache:
            renderer = QSvgRenderer(svg_path)
            if renderer.isValid():
                self.number_svg_cache[svg_path] = renderer
            else:
                return None
        else:
            renderer = self.number_svg_cache[svg_path]

        self.setSharedRenderer(renderer)
        return self
