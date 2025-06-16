from typing import TYPE_CHECKING
from PyQt6.QtGui import (
    QPainter,
    QPen,
    QFont,
    QFontMetrics,
    QImage,
    QBrush,
)
from PyQt6.QtCore import QRect, Qt, QPoint

from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_creator.difficult_level_gradients import (
    DifficultyLevelGradients,
)


class ImageExportDifficultyLevelDrawer:
    def __init__(self):
        self.gradients = DifficultyLevelGradients()

    def draw_difficulty_level(
        self, image: QImage, difficulty_level: int, additional_height_top: int
    ):
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self._calculate_rect(additional_height_top)
        self._setup_painter(painter, rect, difficulty_level)

        self._draw_ellipse(painter, rect)
        self._draw_text(painter, rect, difficulty_level)

        painter.end()

    def _calculate_rect(self, additional_height_top: int) -> QRect:
        # Get the border width from the image creator
        border_width = 3  # Same as in ImageCreator._create_image

        shape_size = int(additional_height_top * 0.75)
        inset = additional_height_top // 8
        return QRect(inset + border_width, inset + border_width, shape_size, shape_size)

    def _setup_painter(self, painter: QPainter, rect: QRect, difficulty_level: int):
        pen = QPen(Qt.GlobalColor.black, max(1, rect.height() // 50))
        painter.setPen(pen)

        gradient = self.gradients.get_gradient(rect, difficulty_level)
        painter.setBrush(QBrush(gradient))

    def _draw_ellipse(self, painter: QPainter, rect: QRect):
        painter.drawEllipse(rect)

    def _draw_text(self, painter: QPainter, rect: QRect, difficulty_level: int):
        font = self._create_font(rect)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        text = str(difficulty_level)
        bounding_rect = self._calculate_text_rect(metrics, text, rect, difficulty_level)

        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(bounding_rect, Qt.AlignmentFlag.AlignLeft, text)

    def _create_font(self, rect: QRect) -> QFont:
        font_size = int(rect.height() // 1.75)
        return QFont("Georgia", font_size, QFont.Weight.Bold)

    def _calculate_text_rect(
        self, metrics: QFontMetrics, text: str, rect: QRect, difficulty_level: int
    ) -> QRect:
        bounding_rect = metrics.boundingRect(text)
        text_x = rect.center().x() - bounding_rect.width() // 2
        text_y = rect.center().y() - bounding_rect.height() // 2

        y_offset = -25 if difficulty_level == 3 else -15
        bounding_rect.moveTopLeft(QPoint(text_x, text_y + y_offset))

        return bounding_rect
