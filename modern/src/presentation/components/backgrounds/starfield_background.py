from .base_background import BaseBackground
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget

# A+ Enhancement: Import Qt resource pooling
from core.qt_integration import qt_resources, pooled_pen, pooled_brush

from .starfield.star_manager import StarManager
from .starfield.comet_manager import CometManager
from .starfield.moon_manager import MoonManager
from .starfield.ufo_manager import UFOManager


class StarfieldBackground(BaseBackground):
    """
    Enhanced starfield background with stars, comets, moon, and UFOs.

    This is the full-featured starfield that matches the legacy implementation
    with all the sophisticated space scene elements.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize all starfield components
        self.star_manager = StarManager()
        self.comet_manager = CometManager()
        self.moon_manager = MoonManager()
        self.ufo_manager = UFOManager()

    def animate_background(self):
        """Animate all starfield components."""
        # Animate stars and UFO
        self.star_manager.animate_stars()
        self.ufo_manager.animate_ufo()

        # Handle comet activation and movement
        if self.comet_manager.comet_active:
            self.comet_manager.move_comet()
        else:
            self.comet_manager.comet_timer -= 1
            if self.comet_manager.comet_timer <= 0:
                self.comet_manager.activate_comet()

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        """Paint the complete starfield scene."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Paint deep space background
        painter.fillRect(widget.rect(), QColor(5, 5, 15))  # Very dark blue-black

        # Get cursor position for UFO interaction
        cursor_position = widget.mapFromGlobal(widget.cursor().pos())

        # Paint all starfield elements in proper order (back to front)
        self.star_manager.draw_stars(painter, widget)
        self.comet_manager.draw_comet(painter, widget)
        self.moon_manager.draw_moon(painter, widget)
        self.ufo_manager.draw_ufo(painter, widget, cursor_position)
