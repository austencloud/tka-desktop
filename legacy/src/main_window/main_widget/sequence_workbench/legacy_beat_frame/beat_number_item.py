from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat


class BeatNumberItem(QGraphicsTextItem):
    def __init__(self, beat: "Beat", beat_number_text: str = ""):
        super().__init__(beat_number_text)
        self.beat = beat
        self.beat_number_int = beat_number_text
        self.setFont(QFont("Georgia", 70, QFont.Weight.DemiBold))
        self.setPos(
            QPointF(
                self.boundingRect().height() // 3,
                self.boundingRect().height() // 5,
            )
        )
        self.beat.addItem(self)

    def update_beat_number(self, beat_number_int: int = None) -> None:
        if self.beat.start_text_item:
            self.beat.start_text_item.setVisible(False)
        self.setVisible(True)
        if self.beat_number_int != 0:
            self.beat_number_int = beat_number_int
            self.setPlainText(str(beat_number_int))

    def get_beat_number_text(self) -> str:
        """
        Return the beat number or range of numbers if this beat spans multiple beats.
        """
        if self.beat.duration > 1:
            end_beat = int(self.beat_number_int) + self.beat.duration - 1
            return f"{self.beat_number_int},{end_beat}"
        else:
            return self.beat_number_int
