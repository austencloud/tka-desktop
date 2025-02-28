from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt, pyqtSignal

if TYPE_CHECKING:
    from .layout_selector import LayoutSelector


class LayoutDropdown(QComboBox):
    current_layout_changed = pyqtSignal(str)

    def __init__(self, layout_selector: "LayoutSelector"):
        super().__init__(layout_selector)
        self.layout_selector = layout_selector
        self.setCursor(Qt.CursorShape.PointingHandCursor)


    def _populate_dropdown(self):
        valid_layout_strs = [f"{rows} x {cols}" for rows, cols in self.layout_selector.valid_layouts]
        self.addItems(valid_layout_strs)
        self.currentTextChanged.connect(self._on_current_text_changed)

    def _on_current_text_changed(self, layout: str):
        # Only emit through one channel
        self.current_layout_changed.emit(layout)
        # Remove the direct emit to controls_widget