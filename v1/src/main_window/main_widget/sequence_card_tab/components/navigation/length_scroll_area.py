# src/main_window/main_widget/sequence_card_tab/components/navigation/sidebar.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict

from main_window.main_widget.sequence_card_tab.components.navigation.length_option_frame import (
    LengthOptionFrame,
)


class LengthScrollArea(QScrollArea):
    length_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.length_frames: Dict[int, LengthOptionFrame] = {}
        self.setup_ui()

    def setup_ui(self):
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setObjectName("lengthScrollArea")

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(6, 6, 6, 6)
        self.content_layout.setSpacing(8)

        self.create_length_options()
        self.content_layout.addStretch()
        self.setWidget(content_widget)

    def create_length_options(self):
        self.add_length_option(0, "Show All")

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("separator")
        self.content_layout.addWidget(separator)

        lengths = [2, 3, 4, 5, 6, 8, 10, 12, 16]
        for length in lengths:
            self.add_length_option(length)

    def add_length_option(self, length: int, custom_text: str = None):
        frame = LengthOptionFrame(length, custom_text)
        frame.length_clicked.connect(self.length_selected.emit)
        self.length_frames[length] = frame
        self.content_layout.addWidget(frame)

    def update_selection(self, selected_length: int):
        for length, frame in self.length_frames.items():
            frame.set_selected(length == selected_length)
