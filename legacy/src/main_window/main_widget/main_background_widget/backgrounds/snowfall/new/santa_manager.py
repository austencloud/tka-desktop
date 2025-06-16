import random
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from data.constants import DIRECTION


class SantaManager:
    _cached_santa_image = None

    def __init__(self):
        # Load the Santa image if not already cached
        if SantaManager._cached_santa_image is None:
            santa_image_path = get_image_path("backgrounds/santa.png")
            SantaManager._cached_santa_image = QPixmap(santa_image_path)

        self.santa_image: QPixmap = SantaManager._cached_santa_image

        # Set initial parameters for Santa
        self.santa = {
            "x": -0.2,
            "y": random.uniform(0.1, 0.3),
            "speed": random.uniform(0.003, 0.005),
            "active": False,
            DIRECTION: 1,  # 1 for left to right, -1 for right to left
            "opacity": 0.8,
        }

        self.santa_timer = 0  # Timer to control when Santa appears
        self.santa_interval = random.randint(500, 1000)  # Frames between appearances

    def animate_santa(self):
        if self.santa["active"]:

            # Move Santa across the screen
            self.santa["x"] += self.santa["speed"] * self.santa[DIRECTION]

            # Check if Santa has moved off-screen
            if (self.santa[DIRECTION] == 1 and self.santa["x"] > 1.2) or (
                self.santa[DIRECTION] == -1 and self.santa["x"] < -0.2
            ):
                self.santa["active"] = False
                self.santa_timer = 0
        else:
            # Increment timer and check if it's time to show Santa
            self.santa_timer += 1
            if self.santa_timer >= self.santa_interval:
                self.santa["active"] = True
                self.santa[DIRECTION] = random.choice([-1, 1])

                self.santa["x"] = -0.2 if self.santa[DIRECTION] == 1 else 1.2
                self.santa["y"] = random.uniform(0.1, 0.3)
                self.santa["speed"] = random.uniform(0.003, 0.005)
                self.santa_interval = random.randint(500, 1000)

    def draw_santa(self, painter: QPainter, widget: QWidget):

        # Define minimum and maximum Santa widths in pixels
        MIN_SANTA_WIDTH = 50
        MAX_SANTA_WIDTH = 100

        # Determine desired Santa width based on widget size
        desired_width_percentage = 0.5
        desired_width = widget.width() * desired_width_percentage

        # Clamp the desired width between min and max
        santa_width = int(max(MIN_SANTA_WIDTH, min(desired_width, MAX_SANTA_WIDTH)))

        # Calculate the scaling factor
        scaling_factor = santa_width / self.santa_image.width()
        santa_height = int(self.santa_image.height() * scaling_factor)

        x = int(self.santa["x"] * widget.width())
        y = int(self.santa["y"] * widget.height())
        santa_image = self.santa_image.scaled(
            santa_width,
            santa_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        if self.santa[DIRECTION] == -1:
            transform = QTransform().scale(-1, 1)
            santa_image = santa_image.transformed(
                transform, Qt.TransformationMode.SmoothTransformation
            )
            x -= santa_width  # Adjust position since image is mirrored

        painter.setOpacity(self.santa["opacity"])
        painter.drawPixmap(x, y, santa_image)
        painter.setOpacity(1.0)
