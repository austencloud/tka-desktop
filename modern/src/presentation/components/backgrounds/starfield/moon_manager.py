from PyQt6.QtGui import QPainter, QPixmap, QColor, QRadialGradient
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from ..asset_utils import get_image_path


class MoonManager:
    """
    Manages moon rendering in the starfield background.
    
    Displays a realistic moon with proper scaling and positioning.
    Falls back to a procedural moon if image is not available.
    """
    
    def __init__(self):
        # Try to load moon image
        moon_image_path = get_image_path("backgrounds/moon.png")
        self.moon_image = QPixmap(moon_image_path)
        
        # Check if image loaded successfully
        self.use_image = not self.moon_image.isNull()
        
        if not self.use_image:
            print("Moon image not found, using procedural moon")

    def draw_moon(self, painter: QPainter, widget: QWidget):
        """Draw the moon in the upper right corner of the sky."""
        # Calculate moon size and position
        moon_size = int(min(widget.width(), widget.height()) * 0.12)
        x = int(widget.width() * 0.85)  # Upper right
        y = int(widget.height() * 0.05)
        
        if self.use_image and not self.moon_image.isNull():
            # Draw moon from image
            moon_scaled = self.moon_image.scaled(
                moon_size,
                moon_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(x, y, moon_scaled)
        else:
            # Draw procedural moon
            self._draw_procedural_moon(painter, x, y, moon_size)
    
    def _draw_procedural_moon(self, painter: QPainter, x: int, y: int, size: int):
        """Draw a procedural moon with gradient and craters."""
        # Create radial gradient for moon
        gradient = QRadialGradient(x + size//2, y + size//2, size//2)
        gradient.setColorAt(0, QColor(240, 240, 220))  # Bright center
        gradient.setColorAt(0.7, QColor(200, 200, 180))  # Mid tone
        gradient.setColorAt(1, QColor(160, 160, 140))  # Dark edge
        
        # Draw main moon body
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(x, y, size, size)
        
        # Add some simple crater effects
        crater_color = QColor(180, 180, 160, 100)  # Semi-transparent darker color
        painter.setBrush(crater_color)
        
        # Draw a few craters
        crater_size = size // 8
        painter.drawEllipse(x + size//3, y + size//4, crater_size, crater_size)
        painter.drawEllipse(x + size//2, y + size//2, crater_size//2, crater_size//2)
        painter.drawEllipse(x + size*2//3, y + size//3, crater_size*3//4, crater_size*3//4)
