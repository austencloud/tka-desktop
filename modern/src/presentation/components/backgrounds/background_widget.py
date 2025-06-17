from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt

from src.presentation.components.backgrounds.starfield_background import (
    StarfieldBackground,
)
from src.presentation.components.backgrounds.aurora_background import AuroraBackground
from src.presentation.components.backgrounds.snowfall_background import (
    SnowfallBackground,
)
from src.presentation.components.backgrounds.bubbles_background import BubblesBackground


class BaseBackground:
    def __init__(self, widget: QWidget):
        self.widget = widget

    def paint_background(self, widget: QWidget, painter: QPainter):
        pass

    def animate_background(self):
        pass

    def stop_animation(self):
        pass


class MainBackgroundWidget(QWidget):
    def __init__(self, main_widget: QWidget, background_type: str = "Starfield"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.background_type = background_type
        self.background: Optional[BaseBackground] = None

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setGeometry(main_widget.rect())

        self._cached_background_pixmap: Optional[QPixmap] = None
        self._painting_active = False

        self.apply_background()

    def apply_background(self):
        self.background = self._get_background(self.background_type)
        self._cached_background_pixmap = None
        self.update()

    def _get_background(self, bg_type: str) -> Optional[BaseBackground]:
        background_map = {
            "Starfield": StarfieldBackground,
            "Aurora": AuroraBackground,
            "Snowfall": SnowfallBackground,
            "Bubbles": BubblesBackground,
        }
        manager_class = background_map.get(bg_type)
        return manager_class(self.main_widget) if manager_class else None

    def paintEvent(self, event):
        if self._painting_active:
            return
        self._painting_active = True

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
                    if cache_painter.isActive() and self.background:
                        cache_painter.save()
                        try:
                            self.background.paint_background(self, cache_painter)
                        finally:
                            cache_painter.restore()
                    cache_painter.end()

                painter.drawPixmap(0, 0, self._cached_background_pixmap)
            finally:
                painter.restore()
        finally:
            self._painting_active = False

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._cached_background_pixmap = None
