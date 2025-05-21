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

    def _get_default_svg(self) -> str:
        """Return a simple default SVG as fallback."""
        return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="80" height="80" fill="none" stroke="black" stroke-width="2"/>
  <text x="50" y="60" font-family="Arial" font-size="40" text-anchor="middle" fill="black">?</text>
</svg>"""

    def load_number_svg(self, number: Union[int, float, str]) -> None:
        self.last_number = number

        try:
            # Determine the SVG path based on the number
            if number == "fl":
                svg_path = get_image_path("numbers/float.svg")
            else:
                try:
                    float_value = float(number)
                    if float_value in [0.0, 1.0, 2.0, 3.0]:
                        number = int(float_value)
                    if number == 0:
                        svg_path = self.blank_svg_path
                    else:
                        svg_path = f"{self.svg_path_prefix}{number}.svg"
                except ValueError:
                    svg_path = self.blank_svg_path

            # Try to load the SVG file
            try:
                import os

                if not os.path.exists(svg_path):
                    # Try with src/images/ prefix
                    alt_path = os.path.join(
                        os.path.abspath(os.path.join(os.getcwd(), "src", "images")),
                        os.path.basename(svg_path),
                    )
                    if os.path.exists(alt_path):
                        svg_path = alt_path
                    else:
                        # If still not found, use default SVG
                        svg_data = self._get_default_svg()
                        # Skip the file reading step
                        raise FileNotFoundError("Using default SVG")

                # Read the SVG file if it exists
                with open(svg_path, "r", encoding="utf-8") as f:
                    svg_data = f.read()

            except FileNotFoundError as e:
                if str(e) != "Using default SVG":
                    svg_data = self._get_default_svg()

            # Apply color transformation if needed
            if self.current_color:
                svg_data = self.turns_column.glyph.pictograph.managers.svg_manager.color_manager.apply_color_transformations(
                    svg_data, self.current_color
                )

            # Create and set the renderer
            renderer = QSvgRenderer(bytearray(svg_data, encoding="utf-8"))
            if renderer.isValid():
                self.setSharedRenderer(renderer)
            else:
                # Use default SVG as fallback for invalid SVG
                default_svg_data = self._get_default_svg()
                default_renderer = QSvgRenderer(
                    bytearray(default_svg_data, encoding="utf-8")
                )
                self.setSharedRenderer(default_renderer)

        except Exception:
            # Use default SVG as fallback for any unexpected errors
            default_svg_data = self._get_default_svg()
            default_renderer = QSvgRenderer(
                bytearray(default_svg_data, encoding="utf-8")
            )
            self.setSharedRenderer(default_renderer)
