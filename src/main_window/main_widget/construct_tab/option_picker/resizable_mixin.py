from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFontMetrics
from typing import Callable, Union
from PyQt6.QtWidgets import QLabel


class ResizableMixin:
    def __init__(self, size_provider: Callable[[], QSize], *args, **kwargs):
        self._size_provider = size_provider
        super().__init__(*args, **kwargs)

    def update_size_and_style(
        self: Union[QLabel, "ResizableMixin"],
        base_font_family: str = "Monotype Corsiva",
        scale_factor: float = 0.03,
        padding: int = 20,
    ) -> int:
        size = self._size_provider()
        font_size = int(scale_factor * size.height())
        font = self.font()
        font.setPointSize(font_size)
        font.setFamily(base_font_family)
        self.setFont(font)
        fm = QFontMetrics(font)
        text = self.text() if hasattr(self, "text") else ""
        w = fm.horizontalAdvance(text) + padding
        h = fm.height() + padding
        self.setFixedSize(w, h)
        return h
