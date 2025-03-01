from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QPixmap, QImage, QPainter, QFont, QPen, QFontMetrics, QIcon
from PyQt6.QtCore import Qt, QRect, QPoint, QSize
from main_window.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager.image_creator.difficult_level_gradients import (
    DifficultyLevelGradients,
)
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )
class DifficultyLevelIcon:
    @staticmethod
    def get_pixmap(difficulty_level: int, size: int) -> QPixmap:
        """Returns a QPixmap of the difficulty level icon for display."""
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        DifficultyLevelIcon._draw_difficulty_level(image, difficulty_level, size)
        return QPixmap.fromImage(image)

    @staticmethod
    def _draw_difficulty_level(image: QImage, difficulty_level: int, size: int):
        """Draws the difficulty level icon into an image."""
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRect(size // 8, size // 8, int(size * 0.75), int(size * 0.75))

        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(
            DifficultyLevelGradients().get_gradient(rect, difficulty_level)
        )
        painter.drawEllipse(rect)

        DifficultyLevelIcon._draw_text(painter, rect, difficulty_level)
        painter.end()

    @staticmethod
    def _draw_text(painter: QPainter, rect: QRect, difficulty_level: int):
        font_size = int(rect.height() // 1.75)
        font = QFont("Georgia", font_size, QFont.Weight.Bold)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        text = str(difficulty_level)
        bounding_rect = metrics.boundingRect(text)

        # Expand bounding rect slightly for better centering
        bounding_rect.setWidth(bounding_rect.width() + 8)
        bounding_rect.setHeight(bounding_rect.height() + 5)

        text_x = rect.center().x() - bounding_rect.width() // 2
        text_y = rect.center().y() - bounding_rect.height() // 2

        # Subtle position tweaks per level
        text_y -= 5 if difficulty_level != 3 else 10
        bounding_rect.moveTopLeft(QPoint(text_x, text_y))

        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(bounding_rect, Qt.AlignmentFlag.AlignCenter, text)
