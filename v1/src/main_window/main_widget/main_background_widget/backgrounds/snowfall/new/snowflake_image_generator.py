import os
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPainterPath, QGuiApplication
from PyQt6.QtCore import Qt
import math
import random


class SnowflakeImageGenerator:
    """Generate pre-rendered snowflake images for use in the snowfall background."""

    @staticmethod
    def generate_images(count: int = 20) -> list[tuple[QPixmap, str]]:
        """
        Generate multiple snowflake images with variety.

        :param count: Number of snowflakes to generate
        :return: List of tuples containing QPixmap objects and their types
        """
        images = []

        for _ in range(count):
            size = random.randint(20, 50)  # Match size range from the original design
            snowflake_type = random.choice([1, 2, 3, 0])  # Include non-special snowflakes
            if snowflake_type == 0:
                images.append((SnowflakeImageGenerator.generate_circle_snowflake(size), "circle"))
            elif snowflake_type == 1:
                images.append((SnowflakeImageGenerator.generate_star_snowflake(size), "star"))
            elif snowflake_type == 2:
                images.append((SnowflakeImageGenerator.generate_spiky_snowflake(size), "spiky"))
            elif snowflake_type == 3:
                images.append((SnowflakeImageGenerator.generate_spiky_snowflake_variant(size), "spiky_variant"))

        return images

    @staticmethod
    def generate_circle_snowflake(size: int) -> QPixmap:
        """
        Generate a simple circle snowflake.

        :param size: Diameter of the snowflake
        :return: QPixmap of the snowflake
        """
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QColor(255, 255, 255))
        painter.setOpacity(random.uniform(0.6, 1.0))  # Match opacity logic
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, size, size)

        painter.end()
        return pixmap

    @staticmethod
    def generate_star_snowflake(size: int) -> QPixmap:
        """
        Generate a star-shaped snowflake.

        :param size: Diameter of the snowflake
        :return: QPixmap of the snowflake
        """
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        radius = size / 2
        angle_step = math.pi / 8
        path = QPainterPath()

        for i in range(16):
            angle = i * angle_step
            x = size / 2 + radius * math.cos(angle)
            y = size / 2 + radius * math.sin(angle)
            if i == 0:
                path.moveTo(size / 2, size / 2)
            path.lineTo(x, y)

        painter.setPen(QColor(255, 255, 255))
        painter.setOpacity(random.uniform(0.6, 1.0))  # Match opacity logic
        painter.drawPath(path)

        painter.end()
        return pixmap

    @staticmethod
    def generate_spiky_snowflake(size: int) -> QPixmap:
        """
        Generate a spiky snowflake.

        :param size: Diameter of the snowflake
        :return: QPixmap of the snowflake
        """
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        radius = size / 2
        small_radius = radius * 0.3
        angle_step = math.pi / 10
        path = QPainterPath()

        for i in range(20):
            angle = i * angle_step
            r = radius if i % 2 == 0 else small_radius
            x = size / 2 + r * math.cos(angle)
            y = size / 2 + r * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()

        painter.setPen(QColor(255, 255, 255))
        painter.setOpacity(random.uniform(0.6, 1.0))  # Match opacity logic
        painter.drawPath(path)

        painter.end()
        return pixmap

    @staticmethod
    def generate_spiky_snowflake_variant(size: int) -> QPixmap:
        """
        Generate a variant of the spiky snowflake.

        :param size: Diameter of the snowflake
        :return: QPixmap of the snowflake
        """
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        radius = size / 2
        small_radius = radius * 0.2
        angle_step = 2 * math.pi / 18
        path = QPainterPath()

        for i in range(18):
            angle = i * angle_step
            r = radius if i % 2 == 0 else small_radius
            x = size / 2 + r * math.cos(angle)
            y = size / 2 + r * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()

        painter.setPen(QColor(255, 255, 255))
        painter.setOpacity(random.uniform(0.6, 1.0))  # Match opacity logic
        painter.drawPath(path)

        painter.end()
        return pixmap


if __name__ == "__main__":
    import sys

    # Initialize QGuiApplication to allow pixmap generation
    app = QGuiApplication(sys.argv)

    # Create output directory
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    # Generate and save images
    images = SnowflakeImageGenerator.generate_images(count=50)
    for i, (image, snowflake_type) in enumerate(images):
        image.save(os.path.join(output_dir, f"snowflake_{snowflake_type}_{i + 1}.png"))

