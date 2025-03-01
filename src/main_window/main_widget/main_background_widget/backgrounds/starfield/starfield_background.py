# StarfieldBackgroundManager: Combines all managers and handles rendering
from ..base_background import BaseBackground
from .comet_manager import CometManager
from .moon_manager import MoonManager
from .star_manager import StarManager
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget
from .ufo_manager.ufo_manager import UFOManager


class StarfieldBackground(BaseBackground):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.star_manager = StarManager()
        self.comet_manager = CometManager()
        self.moon_manager = MoonManager()
        self.ufo_manager = UFOManager()

    def animate_background(self):
        # Animate stars and comets
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
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Paint black background
        painter.fillRect(widget.rect(), QColor(0, 0, 0))

        cursor_position = widget.mapFromGlobal(widget.cursor().pos())

        # Paint stars, comet, and moon
        self.star_manager.draw_stars(painter, widget)
        self.comet_manager.draw_comet(painter, widget)
        self.moon_manager.draw_moon(painter, widget)
        self.ufo_manager.draw_ufo(painter, widget, cursor_position)
