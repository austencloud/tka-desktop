from PyQt6.QtGui import QPixmap, QImage, QPainter, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRect, QPoint
from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_creator.difficult_level_gradients import (
    DifficultyLevelGradients,
)


class DifficultyLevelIcon:
    @staticmethod
    def get_pixmap(difficulty_level: int, size: int) -> QPixmap:
        """Returns a QPixmap of the difficulty level icon for display."""
        image = DifficultyLevelIcon._create_base_image(size)
        DifficultyLevelIcon._draw_difficulty_level(image, difficulty_level, size)
        return QPixmap.fromImage(image)

    @staticmethod
    def _create_base_image(size: int) -> QImage:
        """Creates a base transparent image."""
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        return image

    @staticmethod
    def _draw_difficulty_level(image: QImage, difficulty_level: int, size: int):
        """Draws the difficulty level icon into an image."""
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = DifficultyLevelIcon._calculate_rect(size)
        DifficultyLevelIcon._draw_ellipse(painter, rect, difficulty_level)
        DifficultyLevelIcon._draw_text(painter, rect, difficulty_level)

        painter.end()

    @staticmethod
    def _calculate_rect(size: int) -> QRect:
        """Calculates the rectangle for drawing the ellipse."""
        return QRect(size // 8, size // 8, int(size * 0.75), int(size * 0.75))

    @staticmethod
    def _draw_ellipse(painter: QPainter, rect: QRect, difficulty_level: int):
        """Draws the ellipse with gradient based on difficulty level."""
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(
            DifficultyLevelGradients().get_gradient(rect, difficulty_level)
        )
        painter.drawEllipse(rect)

    @staticmethod
    def _draw_text(painter: QPainter, rect: QRect, difficulty_level: int):
        """Draws the difficulty level text inside the ellipse."""
        font = DifficultyLevelIcon._create_font(rect)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        text = str(difficulty_level)
        bounding_rect = DifficultyLevelIcon._calculate_bounding_rect(metrics, text)

        text_x, text_y = DifficultyLevelIcon._calculate_text_position(
            rect, bounding_rect, difficulty_level
        )
        bounding_rect.moveTopLeft(QPoint(text_x, text_y))

        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(bounding_rect, Qt.AlignmentFlag.AlignCenter, text)

    @staticmethod
    def _create_font(rect: QRect) -> QFont:
        """Creates the font for the difficulty level text."""
        font_size = int(rect.height() // 1.75)
        return QFont("Georgia", font_size, QFont.Weight.Bold)

    @staticmethod
    def _calculate_bounding_rect(metrics: QFontMetrics, text: str) -> QRect:
        """Calculates the bounding rectangle for the text."""
        bounding_rect = metrics.boundingRect(text)
        bounding_rect.setWidth(bounding_rect.width() + 8)
        bounding_rect.setHeight(bounding_rect.height() + 5)
        return bounding_rect

    @staticmethod
    def _calculate_text_position(
        rect: QRect, bounding_rect: QRect, difficulty_level: int
    ) -> tuple[int, int]:
        """Calculates the position for the text."""
        bounding_width = bounding_rect.width()
        text_x = rect.center().x() - bounding_width // 2
        bounding_height = bounding_rect.height()
        text_y = rect.center().y() - bounding_height // 2

        # Subtle position tweaks per level
        if difficulty_level == 1:
            text_x += bounding_width // 10
            text_y -= bounding_height // 10
        elif difficulty_level == 2:
            text_x += 0
            text_y -= bounding_height // 12
        elif difficulty_level == 3:
            text_x += 0
            text_y -= bounding_height // 8
        return text_x, text_y
