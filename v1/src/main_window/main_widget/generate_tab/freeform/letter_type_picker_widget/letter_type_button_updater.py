from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor

if TYPE_CHECKING:
    from .letter_type_button import LetterTypeButton


class LetterTypeButtonUpdater:
    def __init__(self, button_widget: "LetterTypeButton"):
        self.button_widget = button_widget

    def update_colors(self):
        if self.button_widget.is_selected:
            self.button_widget._baseColor = QColor("white")
            self.button_widget.label.setStyleSheet("color: black;")
        else:
            base_dim = self._dim_color("#ffffff")
            self.button_widget._baseColor = QColor(base_dim)
            self.button_widget.label.setStyleSheet("color: gray;")

        p = self.button_widget.primary_color
        s = self.button_widget.secondary_color
        if not self.button_widget.is_selected:
            p = self._dim_color(p)
            s = self._dim_color(s)
        self.button_widget.overlay.update_border_colors(p, s)

        if not self.button_widget._hovered:
            self.button_widget.animator.backgroundColor = self.button_widget._baseColor
        self.update_stylesheet()

    def update_stylesheet(self):
        self.button_widget.setStyleSheet(
            f"""
            background-color: {self.button_widget.animator.backgroundColor.name()};
            border-radius: 50%;
        """
        )

    def _dim_color(self, hex_color: str) -> str:
        c = QColor(hex_color)
        gray_val = (c.red() + c.green() + c.blue()) // 3
        return QColor(gray_val, gray_val, gray_val).name()
