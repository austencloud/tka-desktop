from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QFont

from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.start_pos_beat import (
    StartPositionBeat,
)
from utils.ui_utils import ensure_positive_size

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )


class StartPositionBeatView(LegacyBeatView):
    def __init__(self, beat_frame: "LegacyBeatFrame") -> None:
        self.beat_frame = beat_frame
        super().__init__(beat_frame)
        self.is_start_pos = True
        self._setup_blank_beat()

    def _setup_blank_beat(self):
        self.blank_beat = StartPositionBeat(self.beat_frame)
        self.set_start_pos(self.blank_beat)
        self.blank_beat.elements.grid.hide()

    def set_start_pos(self, start_pos: "StartPositionBeat") -> None:
        self.start_pos = self.beat = self.pictograph = start_pos
        self.is_filled = True
        self.start_pos.view = self
        self.setScene(self.start_pos)
        view_width = self.height()
        self.view_scale = view_width / self.start_pos.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        self.start_pos.start_text_item.add_start_text()

    def _add_start_text(self):
        self.start_text_item = QGraphicsTextItem("Start")
        self.start_text_item.setFont(QFont("Georgia", 80, QFont.Weight.DemiBold))
        text_padding = self.scene().height() // 28
        self.start_text_item.setPos(QPointF(text_padding, text_padding))
        self.scene().addItem(self.start_text_item)
        self.start_text_item.setVisible(self.is_start_pos)
