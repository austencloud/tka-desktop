# cue_frame.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from .cue_box.cue_box import CueBox

if TYPE_CHECKING:
    from ..cue_scroll import CueScroll


class CueFrame(QWidget):
    def __init__(self, cue_scroll: "CueScroll"):
        super().__init__(cue_scroll)
        self.act_sheet = cue_scroll.act_sheet
        self.cue_scroll = cue_scroll

        self.cue_boxes: dict[int, CueBox] = {}  # Store CueBox instances

        self.setup_layout()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.init_cue_boxes(self.cue_scroll.act_sheet.DEFAULT_ROWS)

    def setup_layout(self):
        """Initializes main layout settings for the cue frame."""
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def init_cue_boxes(self, num_rows: int):
        """Creates and stores CueBox for each row."""
        for row in range(num_rows):
            cue_box = CueBox(self, f"{row * 10 // 60}:{row * 10 % 60:02d}", "")
            self.cue_boxes[row] = cue_box

            self.layout.addWidget(cue_box)
            cue_box.timestamp.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

