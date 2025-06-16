from PyQt6.QtGui import QPixmap, QImage, QPainter, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRect, QPoint
from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_creator.difficult_level_gradients import (
    DifficultyLevelGradients,
)

class LevelSelectorDifficultyDrawer:
    def __init__(self):
        self.gradients = DifficultyLevelGradients()

    def get_difficulty_level_pixmap(self, difficulty_level: int, size: int) -> QPixmap:
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        self._draw_difficulty_level(image, difficulty_level, size)
        return QPixmap.fromImage(image)

    def _draw_difficulty_level(self, image: QImage, difficulty_level: int, size: int):
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self._calculate_rect(size)
        self._draw_ellipse(painter, rect, difficulty_level)
        self._draw_text(painter, rect, difficulty_level)

        painter.end()

    def _calculate_rect(self, size: int) -> QRect:
        return QRect(size // 8, size // 8, int(size * 0.75), int(size * 0.75))

    def _draw_ellipse(self, painter: QPainter, rect: QRect, difficulty_level: int):
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(self.gradients.get_gradient(rect, difficulty_level))
        painter.drawEllipse(rect)

    def _draw_text(self, painter: QPainter, rect: QRect, difficulty_level: int):
        font_size = int(rect.height() // 1.75)
        font = QFont("Georgia", font_size, QFont.Weight.Bold)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        text = str(difficulty_level)
        bounding_rect = metrics.boundingRect(text)
        extra_width = rect.width() // 2

        bounding_rect.setWidth(bounding_rect.width() + int(extra_width))
        text_x = rect.center().x() - bounding_rect.width() // 2
        text_y = rect.center().y() - bounding_rect.height() // 2

        text_y -= self._adjust_text_y(difficulty_level)

        bounding_rect.moveTopLeft(QPoint(text_x + int(extra_width // 2), text_y))

        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(bounding_rect, Qt.AlignmentFlag.AlignLeft, text)

    def _adjust_text_y(self, difficulty_level: int) -> int:
        adjustments = {1: 5, 2: 5, 3: 8, 4: 6, 5: 7}
        return adjustments.get(difficulty_level, 0)
