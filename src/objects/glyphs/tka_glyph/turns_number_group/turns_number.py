from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtGui import QPainter, QPen, QColor
from typing import TYPE_CHECKING, Union
from utils.path_helpers import get_data_path, get_image_path

if TYPE_CHECKING:
    from objects.glyphs.tka_glyph.turns_number_group.turns_column import (
        TurnsColumn,
    )


class TurnsNumber(QGraphicsSvgItem):
    def __init__(self, turns_column: "TurnsColumn"):
        super().__init__()
        self.turns_column = turns_column
        self.svg_path_prefix = turns_column.svg_path_prefix
        self.blank_svg_path = turns_column.blank_svg_path
        self.number_svg_cache = {}

        self.current_color: Union[str, None] = None
        self.last_number: Union[str, None] = None

    def set_color(self, color: str):
        self.current_color = color

        if self.last_number is not None:
            self.load_number_svg(self.last_number)

    def paint(self, painter: QPainter, option, widget=None):
        if self.current_color:
            painter.setPen(QPen(QColor(self.current_color), 0))
            painter.setBrush(QColor(self.current_color))
        super().paint(painter, option, widget)

    def load_number_svg(self, number: Union[int, float, str]) -> None:
        self.last_number = number

        if number == "fl":
            svg_path = get_image_path("numbers/float.svg")
        else:
            try:
                float_value = float(number)
                if float_value == 0:
                    svg_path = self.blank_svg_path
                else:
                    svg_path = f"{self.svg_path_prefix}{number}.svg"
            except ValueError:
                svg_path = self.blank_svg_path

        with open(svg_path, "r", encoding="utf-8") as f:
            svg_data = f.read()

        if self.current_color:
            svg_data = self.turns_column.glyph.pictograph.managers.svg_manager.color_manager.apply_color_transformations(
                svg_data, self.current_color
            )

        renderer = QSvgRenderer(bytearray(svg_data, encoding="utf-8"))
        if renderer.isValid():
            self.setSharedRenderer(renderer)
