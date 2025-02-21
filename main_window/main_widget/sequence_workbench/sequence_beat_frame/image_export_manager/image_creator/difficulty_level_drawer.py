from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QPen, QFont, QFontMetrics, QImage
from PyQt6.QtCore import QRect, Qt

if TYPE_CHECKING:
    from ..image_creator.image_creator import ImageCreator


class DifficultyLevelDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator

    def draw_difficulty_level(
        self, image: QImage, difficulty_level: int, additional_height_top: int
    ):
        """Draw the difficulty level on the top left corner of the image."""
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        font_size = int(additional_height_top // 4)

        # Define the size and position for the difficulty level circle
        circle_size = int(additional_height_top // 2)
        inset_left = additional_height_top // 8
        inset_top = additional_height_top // 4
        rect = QRect(inset_left, inset_top, circle_size, circle_size)

        # Draw the circle
        pen = QPen(Qt.GlobalColor.black, additional_height_top // 50)
        painter.setPen(pen)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawEllipse(rect)

        # Set the font and get the metrics
        font = QFont("Georgia", font_size)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.black)
        metrics = QFontMetrics(font)

        # Calculate the bounding rectangle for the text
        text = str(difficulty_level)
        bounding_rect = metrics.boundingRect(rect, Qt.AlignmentFlag.AlignCenter, text)

        # Adjust the bounding rectangle to center the text within the circle
        bounding_rect.moveCenter(rect.center())

        # Draw the difficulty level number
        painter.drawText(bounding_rect, Qt.AlignmentFlag.AlignCenter, text)

        painter.end()
