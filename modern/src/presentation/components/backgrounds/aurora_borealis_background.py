import math
import random

from PyQt6.QtGui import QLinearGradient, QColor, QPainter
from PyQt6.QtWidgets import QWidget

from .base_background import BaseBackground


class AuroraBorealisBackground(BaseBackground):
    """
    Aurora Borealis background with animated light waves.

    This background creates a mesmerizing aurora effect using mathematical
    wave functions to simulate the natural movement of northern lights.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize light waves with random phases for natural variation
        self.light_waves = [random.random() * 2 * math.pi for _ in range(10)]

        # Color palette for aurora borealis effect
        self.aurora_colors = [
            (0, 25, 50, 100),  # Deep blue
            (0, 50, 100, 50),  # Medium blue
            (0, 100, 150, 25),  # Light blue
            (50, 150, 100, 40),  # Blue-green
            (100, 200, 150, 30),  # Green
            (150, 255, 200, 20),  # Light green
        ]

    def animate_background(self):
        """Update light wave positions for smooth animation."""
        # Advance each wave at slightly different speeds for natural variation
        for i in range(len(self.light_waves)):
            wave_speed = 0.008 + (i * 0.002)  # Varying speeds
            self.light_waves[i] += wave_speed

            # Keep waves within reasonable bounds to prevent overflow
            if self.light_waves[i] > 4 * math.pi:
                self.light_waves[i] -= 4 * math.pi

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        """Paint the aurora borealis effect."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create base gradient from dark to lighter
        base_gradient = QLinearGradient(0, 0, widget.width(), widget.height())
        base_gradient.setColorAt(0, QColor(5, 10, 25))  # Very dark blue
        base_gradient.setColorAt(0.5, QColor(10, 20, 40))  # Dark blue
        base_gradient.setColorAt(1, QColor(15, 30, 60))  # Medium dark blue
        painter.fillRect(widget.rect(), base_gradient)

        # Create multiple aurora layers with different wave patterns
        self._paint_aurora_layer(painter, widget, 0, 3)  # Background layer
        self._paint_aurora_layer(painter, widget, 3, 6)  # Middle layer
        self._paint_aurora_layer(painter, widget, 6, 10)  # Foreground layer

    def _paint_aurora_layer(
        self, painter: QPainter, widget: QWidget, wave_start: int, wave_end: int
    ):
        """Paint a single aurora layer using specified wave range."""
        gradient = QLinearGradient(0, 0, widget.width(), widget.height())

        # Calculate wave positions and create gradient stops
        wave_positions = []
        for i in range(wave_start, min(wave_end, len(self.light_waves))):
            wave = self.light_waves[i]
            # Use sine wave to create smooth position transitions
            pos = (math.sin(wave) + 1) / 2  # Normalize to 0-1 range
            wave_positions.append((pos, i))

        # Sort positions to ensure proper gradient ordering
        wave_positions.sort(key=lambda x: x[0])

        # Create gradient with aurora colors
        for pos, wave_index in wave_positions:
            color_index = wave_index % len(self.aurora_colors)
            color_rgba = self.aurora_colors[color_index]
            color = QColor(*color_rgba)

            # Add some dynamic intensity variation
            intensity_factor = (math.sin(self.light_waves[wave_index] * 1.5) + 1) / 2
            color.setAlpha(int(color_rgba[3] * intensity_factor))

            gradient.setColorAt(pos, color)

        # Fill with the aurora gradient
        painter.fillRect(widget.rect(), gradient)
