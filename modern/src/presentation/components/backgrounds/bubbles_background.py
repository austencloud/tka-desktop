import random

from PyQt6.QtGui import (
    QColor,
    QPainter,
    QLinearGradient,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF

from .base_background import BaseBackground
from .asset_utils import get_image_path


class BubblesBackground(BaseBackground):
    # Class variable to hold cached images
    _cached_fish_images = None

    def __init__(self, parent=None):
        super().__init__(parent)

        # Check if the fish images are already cached
        if BubblesBackground._cached_fish_images is None:
            # Define the backgrounds folder path
            backgrounds_folder = get_image_path("backgrounds/")

            # Load the fish images and store them in the class variable
            BubblesBackground._cached_fish_images = [
                QPixmap(backgrounds_folder + "Tropical-Fish-Sherbert.png"),
                QPixmap(backgrounds_folder + "Tropical-Fish-Coral.png"),
                QPixmap(backgrounds_folder + "Tropical-Fish-Seafoam.png"),
                QPixmap(backgrounds_folder + "orange_fish.png"),
                QPixmap(backgrounds_folder + "blue_orange_fish.png"),
                QPixmap(backgrounds_folder + "clown_fish.png"),
                QPixmap(backgrounds_folder + "yellow_fish.png"),
            ]

        # Use the cached images in this instance
        self.fish_images = BubblesBackground._cached_fish_images

        # Initialize bubbles and fish
        self._initialize_bubbles()
        self._initialize_fish()

    def _initialize_bubbles(self):
        # Create bubbles floating upward with additional reflection properties
        self.bubbles = [
            {
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "size": random.uniform(5, 15),
                "speed": random.uniform(0.0005, 0.002),
                "opacity": random.uniform(0.4, 0.8),
                "highlight_factor": random.uniform(0.7, 1.0),  # Highlight brightness
            }
            for _ in range(100)
        ]

    def _initialize_fish(self):
        # Initialize fish that occasionally swim across the screen
        self.fish = []
        self.fish_timer = 0  # Time between fish appearances
        self.spawn_fish_interval = random.randint(50, 100)  # More frequent fish spawn

    def animate_background(self):
        # Move the bubbles upwards
        for bubble in self.bubbles:
            bubble["y"] -= bubble["speed"]
            if bubble["y"] < 0:
                bubble["y"] = 1  # Reset bubble position to the bottom
                bubble["x"] = random.uniform(0, 1)
                bubble["size"] = random.uniform(5, 15)
                bubble["highlight_factor"] = random.uniform(0.7, 1.0)  # Reset highlight

        # Handle fish movement
        self.animate_fish()

        self.update_required.emit()

    def animate_fish(self):
        # Update existing fish positions
        for fish in self.fish:
            fish["x"] += fish["dx"] * fish["speed"]
            fish["y"] += fish["dy"] * fish["speed"]

        # Remove fish that have swum out of view
        self.fish = [
            fish
            for fish in self.fish
            if -0.2 <= fish["x"] <= 1.2 and -0.2 <= fish["y"] <= 1.2
        ]

        # Spawn a new fish if timer is up
        self.fish_timer += 1
        if self.fish_timer >= self.spawn_fish_interval:
            self.spawn_fish()
            self.fish_timer = 0  # Reset timer for next fish
            self.spawn_fish_interval = random.randint(100, 200)

    def spawn_fish(self):
        """Spawns a fish from a random side of the screen."""
        start_position_options = [
            (-0.1, random.uniform(0.2, 0.8)),  # Left side
            (1.1, random.uniform(0.2, 0.8)),  # Right side
        ]
        start_x, start_y = random.choice(start_position_options)

        # Bias towards horizontal movement by making dx larger and dy smaller
        dx = (
            random.uniform(0.3, 1) if start_x < 0 else random.uniform(-1, -0.3)
        )  # Horizontal bias
        dy = random.uniform(-0.1, 0.1)  # Smaller vertical movement

        normalization_factor = (dx**2 + dy**2) ** 0.5  # Normalize diagonal movement
        dx /= normalization_factor
        dy /= normalization_factor

        # Increase fish size and set random fish image
        self.fish.append(
            {
                "x": start_x,
                "y": start_y,
                "dx": dx,
                "dy": dy,
                "size": random.uniform(40, 80),  # Larger fish size
                "speed": random.uniform(0.003, 0.005),  # Fish speed
                "image": random.choice(self.fish_images),  # Use cached images
            }
        )

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create an underwater gradient (light blue at top, deep blue at bottom)
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor(100, 150, 255))  # Light blue
        gradient.setColorAt(1, QColor(0, 30, 90))  # Deep blue
        painter.fillRect(widget.rect(), gradient)

        # Draw bubbles
        for bubble in self.bubbles:
            x = int(bubble["x"] * widget.width())
            y = int(bubble["y"] * widget.height())
            size = int(bubble["size"])

            # Set bubble opacity and fill
            painter.setOpacity(bubble["opacity"])
            painter.setBrush(QColor(255, 255, 255, int(bubble["opacity"] * 255)))
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw the main bubble
            painter.drawEllipse(x, y, size, size)

            # Add a reflection highlight to the bubble for realism
            self.draw_bubble_reflection(
                painter,
                QPointF(x + size / 4, y + size / 4),
                size,
                bubble["highlight_factor"],
            )

        # Draw fish if any are swimming
        self.draw_fish(painter, widget)

        painter.setOpacity(1.0)  # Reset opacity after drawing

    def draw_bubble_reflection(
        self, painter: QPainter, center: QPointF, size: int, highlight_factor: float
    ):
        """Draws a reflection highlight on the top of the bubble to simulate lighting."""
        highlight_radius = size * 0.4 * highlight_factor
        gradient = QRadialGradient(center, highlight_radius)
        gradient.setColorAt(0, QColor(255, 255, 255, 180))  # Bright reflection
        gradient.setColorAt(1, QColor(255, 255, 255, 0))  # Soft fade out

        painter.setBrush(gradient)
        painter.drawEllipse(center, highlight_radius, highlight_radius)

    def draw_fish(self, painter: QPainter, widget: QWidget):
        """Draw fish swimming across the screen using the provided fish images."""
        for fish in self.fish:
            x = int(fish["x"] * widget.width())
            y = int(fish["y"] * widget.height())
            size = int(fish["size"])

            # Ensure full opacity for the fish
            painter.setOpacity(1.0)

            # Scale the fish image to its size using SmoothTransformation
            fish_image = fish["image"].scaled(
                size,
                size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Flip the fish image if it is moving left (dx < 0)
            if fish["dx"] < 0:
                transform = QTransform().scale(-1, 1)  # Mirror horizontally
                fish_image = fish_image.transformed(
                    transform, Qt.TransformationMode.SmoothTransformation
                )

            # Draw the fish at the correct position with no blending
            painter.drawPixmap(x, y, fish_image)
