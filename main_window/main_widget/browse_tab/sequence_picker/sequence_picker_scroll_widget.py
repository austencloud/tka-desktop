from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout

from ..thumbnail_box.thumbnail_box import ThumbnailBox

if TYPE_CHECKING:
    from .sequence_picker import SequencePicker
    from ..browse_tab_section_header import BrowseTabSectionHeader


class SequencePickerScrollWidget(QWidget):
    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.thumbnail_boxes: dict[str, ThumbnailBox] = {}
        self.section_headers: dict[int, "BrowseTabSectionHeader"] = {}

        self.setStyleSheet("background: transparent;")
        self._setup_scroll_area()
        self._setup_layout()

    def _setup_layout(self):
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def _setup_scroll_area(self):
        self.scroll_content = QWidget()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidget(self.scroll_content)

    def clear_layout(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

