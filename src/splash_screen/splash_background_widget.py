# background_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPaintEvent
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
import logging


class SplashBackgroundWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        self.setGeometry(main_widget.rect())
        self.setFixedSize(main_widget.size())
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._on_animation_tick)
        self.animation_timer.start(30)  # ~30 FPS, tweak as desired

    def _on_animation_tick(self):
        try:
            background_widget = self.main_widget.widget_manager.get_widget(
                "background_widget"
            )
            if background_widget and hasattr(self.main_widget, "background"):
                self.main_widget.background.animate_background()
        except AttributeError:
            # Fallback when background_widget not available
            pass
        self.update()

    def paintEvent(self, event):
        logging.debug("SplashBackgroundWidget.paintEvent called")
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.main_widget.background.paint_background(self, painter)
        painter.end()

    def resizeEvent(self, event):
        self.setGeometry(self.main_widget.rect())
        self.setFixedSize(self.main_widget.size())
