from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat


class BeatStartTextItem(QGraphicsTextItem):
    def __init__(self, beat: "Beat"):
        super().__init__("Start")
        self.beat = beat
        self.beat.addItem(self)

    def add_start_text(self):
        if self.beat.beat_number_item:
            self.beat.beat_number_item.setVisible(False)
        self.setVisible(True)
        self.setFont(QFont("Georgia", 60, QFont.Weight.DemiBold))
        text_padding = self.beat.height() // 28
        self.setPos(QPointF(text_padding, text_padding))
