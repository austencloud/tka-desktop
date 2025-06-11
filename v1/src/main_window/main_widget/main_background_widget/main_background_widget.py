from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
from interfaces.settings_manager_interface import ISettingsManager
from .backgrounds.aurora.aurora_background import AuroraBackground
from .backgrounds.aurora_borealis_background import AuroraBorealisBackground
from .backgrounds.base_background import BaseBackground
from .backgrounds.bubbles_background import BubblesBackground
from .backgrounds.snowfall.snowfall_background import SnowfallBackground
from .backgrounds.starfield.starfield_background import StarfieldBackground

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget

from contextlib import contextmanager
from PyQt6.QtGui import QPainter


@contextmanager
def use_painter(paint_device):
    painter = QPainter()
    if painter.begin(paint_device):
        try:
            yield painter
        finally:
            painter.end()
    else:
        yield None


class MainBackgroundWidget(QWidget):
    background: Optional[BaseBackground] = None

    def __init__(self, main_widget: "MainWidget", settings_manager: ISettingsManager):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.settings_manager = settings_manager
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setGeometry(main_widget.rect())
        self.setFixedSize(main_widget.size())
        self.apply_background()

        self._cached_background_pixmap: Optional[QPixmap] = None

    def paintEvent(self, event):
        if getattr(self, "_painting_active", False):  # Prevent recursion
            print("[WARN] paintEvent re-entered while still active!")
            return
        self._painting_active = True  # Mark painting as active

        try:
            painter = QPainter(self)
            if not painter.isActive():
                return

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            painter.save()
            try:
                if self._cached_background_pixmap is None:
                    self._cached_background_pixmap = QPixmap(self.size())
                    self._cached_background_pixmap.fill(Qt.GlobalColor.transparent)

                    cache_painter = QPainter(self._cached_background_pixmap)
                    if cache_painter.isActive() and self.main_widget.background:
                        cache_painter.save()
                        try:
                            self.main_widget.background.paint_background(
                                self, cache_painter
                            )
                        finally:
                            cache_painter.restore()
                    cache_painter.end()

                painter.drawPixmap(0, 0, self._cached_background_pixmap)
            finally:
                painter.restore()  # Always restore before leaving
        finally:
            self._painting_active = False  # Unlock painting

    def _setup_background(self):
        bg_type = self.settings_manager.get_global_settings().get_background_type()
        self.background = self._get_background(bg_type)
        self.main_widget.background = self.background

    def apply_background(self):
        self._setup_background()

        self._cached_background_pixmap = None

    def _get_background(self, bg_type: str) -> Optional[BaseBackground]:
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
        self._cached_background_pixmap = None
        self.background = None
        self.is_animating = False
