# background_widget.py
from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from .backgrounds.aurora.aurora_background import AuroraBackground
from .backgrounds.aurora_borealis_background import AuroraBorealisBackground
from .backgrounds.base_background import BaseBackground
from .backgrounds.bubbles_background import BubblesBackground
from .backgrounds.snowfall.snowfall_background import SnowfallBackground
from .backgrounds.starfield.starfield_background import StarfieldBackground

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MainBackgroundWidget(QWidget):
    background: Optional[BaseBackground] = None

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        self.setGeometry(main_widget.rect())
        self.setFixedSize(main_widget.size())
        self.apply_background()

    def _on_animation_tick(self):
        if self.main_widget.background_widget:
            self.main_widget.background.animate_background()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.main_widget.background.paint_background(self, painter)
        painter.end()

    def _setup_background(self):
        """Initializes the background based on the current background type."""
        bg_type = (
            self.main_widget.settings_manager.global_settings.get_background_type()
        )
        self.background = self._get_background(bg_type)
        self.main_widget.background = self.background

    def apply_background(self):
        """Applies or reapplies the background."""

        self._setup_background()
        self.main_widget.font_color_updater.update_main_widget_font_colors(
            self.main_widget.settings_manager.global_settings.get_background_type()
        )

    def _get_background(self, bg_type: str) -> Optional[BaseBackground]:
        """Returns an instance of the appropriate Background based on bg_type."""
        background_map = {
            "Starfield": StarfieldBackground,
            "Aurora": AuroraBackground,
            "AuroraBorealis": AuroraBorealisBackground,
            "Snowfall": SnowfallBackground,
            "Bubbles": BubblesBackground,
        }
        manager_class = background_map.get(bg_type)
        return manager_class(self.main_widget) if manager_class else None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_background()

    def resize_background(self):
        self.setGeometry(self.main_widget.rect())
        self.setFixedSize(self.main_widget.size())
        self.background: Optional[BaseBackground] = None
        self.is_animating = False
