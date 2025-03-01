from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QFrame
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.act_sheet.act_splitter.act_beat_scroll.act_beat_frame.act_beat_frame import (
    ActBeatFrame,
)

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.act_sheet.act_sheet import ActSheet


class ActBeatScroll(QScrollArea):
    def __init__(self, act_sheet: "ActSheet"):
        super().__init__(act_sheet)
        self.act_sheet = act_sheet
        self.setWidgetResizable(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setViewportMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setAcceptDrops(False)  # ActBeatScroll will pass drag events to children

        self.act_beat_frame = ActBeatFrame(self)
        self.setWidget(self.act_beat_frame)
        self.setStyleSheet("background: transparent; padding: 0px; margin: 0px;")
