import random
from PyQt6.QtGui import QPainter, QPixmap, QCursor
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from utils.path_helpers import get_image_path


class UFOManager:
    def __init__(self):
        # Load the UFO image
        ufo_image_path = get_image_path("backgrounds/ufo.png")
        self.ufo_image = QPixmap(ufo_image_path)

        # UFO parameters
        self.ufo = {
            "x": random.uniform(0.1, 0.9),  # Random starting position
            "y": random.uniform(0.1, 0.9),
            "size": 50,
            "speed": random.uniform(0.005, 0.01),  # Adjust speed for wandering
            "dx": random.uniform(-0.5, 0.5),
            "dy": random.uniform(-0.5, 0.5),
            "paused": False,
            "pause_duration": random.randint(100, 300),  # Random pause time
        }

        # UFO state management
        self.pause_timer = random.randint(50, 150)  # Timer before next pause
        self.pause_duration = random.randint(50, 150)  # How long UFO stays paused

    def move_ufo(self):
        """Move the UFO and handle pausing and resuming."""
        ufo = self.ufo

        if ufo["paused"]:
            # Decrease the pause duration
            ufo["pause_duration"] -= 1
            if ufo["pause_duration"] <= 0:
                # Resume movement after pausing
                ufo["paused"] = False
                ufo["dx"] = random.uniform(-0.5, 0.5)
                ufo["dy"] = random.uniform(-0.5, 0.5)
                ufo["speed"] = random.uniform(0.005, 0.01)
                self.pause_timer = random.randint(
                    100, 200
                )  # Set time before next pause

        else:
            # Move the UFO
            ufo["x"] += ufo["dx"] * ufo["speed"]
            ufo["y"] += ufo["dy"] * ufo["speed"]

            # Handle UFO reaching the screen edges (bounce off the edges)
            if ufo["x"] < 0 or ufo["x"] > 1:
                ufo["dx"] *= -1  # Reverse direction horizontally
            if ufo["y"] < 0 or ufo["y"] > 1:
                ufo["dy"] *= -1  # Reverse direction vertically

            # Randomly pause the UFO after some time
            self.pause_timer -= 1
            if self.pause_timer <= 0:
                ufo["paused"] = True
                ufo["pause_duration"] = random.randint(100, 300)  # Set pause duration

    def draw_ufo(self, painter: QPainter, widget: QWidget, cursor_position: QPoint):
        """Draw the UFO image with scaling and movement."""
        ufo = self.ufo

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

    def animate_ufo(self):
        """Manage UFO movement and pausing behavior."""
        self.move_ufo()
