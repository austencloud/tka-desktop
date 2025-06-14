from PyQt6.QtGui import QPainter, QPixmap, QCursor
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from .ufo_manager import UFOManager


class UFODrawManager:
    def __init__(self, ufo_manager: "UFOManager"):
        self.ufo_manager = ufo_manager  # Access the UFOManager instance
        ufo_image_path = get_image_path("backgrounds/ufo.png")

        self.ufo_image = QPixmap(ufo_image_path)

    def draw_ufo(self, painter: QPainter, widget: QWidget, cursor_position: QPoint):
        """Draw the UFO image with scaling and movement, only if active."""
        ufo = self.ufo_manager.ufo  # Access the UFOManager's ufo dictionary

        if not ufo["active"]:
            return

        ufo_x = int(ufo["x"] * widget.width())
        ufo_y = int(ufo["y"] * widget.height())
        ufo_size = int(ufo["size"])

        # Scale the UFO image to the desired size with high quality
        scaled_ufo = self.ufo_image.scaled(
            ufo_size,
            ufo_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,  # High-quality scaling
        )

        # Check if the cursor is over the UFO and change the cursor
        cursor_x, cursor_y = cursor_position.x(), cursor_position.y()
        if (
            ufo_x - ufo_size // 2 <= cursor_x <= ufo_x + ufo_size // 2
            and ufo_y - ufo_size // 2 <= cursor_y <= ufo_y + ufo_size // 2
        ):
            widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            widget.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        # Draw the scaled UFO image at the calculated position
        painter.drawPixmap(
            ufo_x - scaled_ufo.width() // 2,
            ufo_y - scaled_ufo.height() // 2,
            scaled_ufo,
        )
