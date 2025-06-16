from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QPixmap,
    QImage,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat


class BeatGrabber:
    def __init__(self, beat: "Beat"):
        self.beat = beat

    def grab(self) -> QPixmap:
        original_size = self.beat.sceneRect().size().toSize()
        target_width = original_size.width()
        target_height = original_size.height()
        image = QImage(target_width, target_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.beat:
            painter.setPen(QColor(0, 0, 0))
            painter.setBrush(QColor(0, 255, 255))
            painter.drawRect(0, 0, target_width - 1, target_height - 1)
        else:
            self.beat.render(painter)
        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(0, 0, target_width - 1, target_height - 1)
        painter.end()
        return QPixmap.fromImage(image)
