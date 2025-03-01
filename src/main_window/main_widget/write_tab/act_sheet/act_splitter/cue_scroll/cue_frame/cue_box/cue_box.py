# cue_box.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

from .cue_label.cue_label import CueLabel
from .timestamp.timestamp import Timestamp


if TYPE_CHECKING:
    from ..cue_frame import CueFrame


# cue_box.py
class CueBox(QWidget):
    def __init__(
        self, cue_frame: "CueFrame", timestamp_text: str, cue_label_text: str = ""
    ):
        super().__init__(cue_frame)
        self.cue_frame = cue_frame

        self.timestamp = Timestamp(self, timestamp_text)
        self.cue_label = CueLabel(self, cue_label_text)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.timestamp, 1)
        self.layout.addWidget(self.cue_label, 6)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._apply_styles()

    def _apply_styles(self):
        self.setObjectName("cue_box")
        self.setStyleSheet("#cue_box {border-top: 1px solid black;}")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        beat_frame = (
            self.cue_frame.cue_scroll.act_sheet.act_container.beat_scroll.act_beat_frame
        )
        scrollbar_width = (
            beat_frame.act_sheet.act_container.beat_scroll.verticalScrollBar().width()
        )
        width_without_scrollbar = beat_frame.width() - scrollbar_width
        self.beat_size = int(
            width_without_scrollbar // beat_frame.act_sheet.DEFAULT_COLUMNS
        )
        self.steps_label_height = int(self.beat_size * (2 / 3))

        height = self.beat_size + self.steps_label_height
        self.setFixedHeight(height)
