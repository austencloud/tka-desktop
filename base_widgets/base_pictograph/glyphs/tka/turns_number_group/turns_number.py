from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtGui import QPainter, QPen, QColor
from typing import TYPE_CHECKING, Union
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from base_widgets.base_pictograph.glyphs.tka.turns_number_group.turns_number_group import TurnsNumberGroup


class TurnsNumber(QGraphicsSvgItem):
    """
    Represents a single turn number (top or bottom) in the TKA glyph.
    Loads an SVG based on numeric value, can apply a color transform,
    and re-loads the SVG whenever the color changes.
    """

    def __init__(self, turns_column: "TurnsNumberGroup"):
        super().__init__()
        self.turns_column = turns_column
        self.svg_path_prefix = turns_column.svg_path_prefix
        self.blank_svg_path = turns_column.blank_svg_path
        self.number_svg_cache = {}

        self.current_color: Union[str, None] = None
        self.last_number: Union[str, None] = None  # The last loaded numeric value

    def set_color(self, color: str):
        """
        Store the chosen color (e.g. '#ED1C24' for red, '#2E3192' for blue).
        If we have already loaded a number, re-load it to apply color transformations immediately.
        """
        self.current_color = color

        # If we have a last_number, re-load it so color changes appear right away
        if self.last_number is not None:
            self.load_number_svg(self.last_number)

    def paint(self, painter: QPainter, option, widget=None):
        """
        Override paint to apply 'self.current_color' in the pen/brush if needed.
        This is only used if you rely on the fill color in the SVG being #010101, etc.
        If you do color transformations on the raw SVG text, you often won't need it.
        """
        if self.current_color:
            painter.setPen(QPen(QColor(self.current_color), 0))
            painter.setBrush(QColor(self.current_color))
        super().paint(painter, option, widget)

    def load_number_svg(self, number: Union[int, float, str]) -> None:
        """
        Load and parse the SVG from disk, optionally applying color transformations
        if self.current_color is set.
        """
        self.last_number = number  # Keep track of what we just loaded

        # 1) Decide which file to load
        if number == "fl":
            svg_path = get_images_and_data_path("images/numbers/float.svg")
        else:
            try:
                float_value = float(number)
                # If numeric is 0 => load blank
                if float_value == 0:
                    svg_path = self.blank_svg_path
                else:
                    svg_path = f"{self.svg_path_prefix}{number}.svg"
            except ValueError:
                # If the conversion fails, fallback to blank or a default
                svg_path = self.blank_svg_path

        # 2) Read raw text
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_data = f.read()

        # 3) If we have a color, transform it (regex replace #010101 => self.current_color, etc.)
        if self.current_color:
            svg_data = self.turns_column.glyph.pictograph.svg_manager.color_manager.apply_color_transformations(
                svg_data, self.current_color
            )

        # 4) Create a QSvgRenderer from the (possibly color-transformed) text
        renderer = QSvgRenderer(bytearray(svg_data, encoding="utf-8"))
        if renderer.isValid():
            self.setSharedRenderer(renderer)
