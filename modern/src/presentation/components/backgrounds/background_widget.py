from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer

from src.presentation.components.backgrounds.starfield_background import (
    StarfieldBackground,
)
from src.presentation.components.backgrounds.aurora_background import AuroraBackground
from src.presentation.components.backgrounds.aurora_borealis_background import (
    AuroraBorealisBackground,
)
from src.presentation.components.backgrounds.snowfall_background import (
    SnowfallBackground,
)
from src.presentation.components.backgrounds.bubbles_background import BubblesBackground
from src.presentation.components.backgrounds.base_background import BaseBackground


class MainBackgroundWidget(QWidget):
    def __init__(self, main_widget: QWidget, background_type: str = "Starfield"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.background_type = background_type
        self.background: Optional[BaseBackground] = None

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setGeometry(main_widget.rect())

        # Animation timer for calling animate_background()
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._animate_background)
        self.animation_timer.start(50)  # 20 FPS animation

        self._painting_active = False

        self.apply_background()

    def apply_background(self):
        # Disconnect old background if it exists
        if hasattr(self, "background") and self.background:
            try:
                self.background.update_required.disconnect(self.update)
            except (TypeError, RuntimeError, AttributeError):
                pass  # Signal wasn't connected or object already deleted

        # Create new background
        self.background = self._get_background(self.background_type)

        # Connect to update signal if background exists
        if self.background:
            self.background.update_required.connect(self.update)

        self.update()

    def _animate_background(self):
        """Called by animation timer to update background animation."""
        if self.background:
            self.background.animate_background()

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

    def paintEvent(self, event):
        """Paint the background directly without caching for animation support."""
        if self._painting_active:
            return
        self._painting_active = True

        try:
            painter = QPainter(self)
            if not painter.isActive():
                return

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Paint background directly for animation support
            if self.background:
                self.background.paint_background(self, painter)

        finally:
            self._painting_active = False

    def resizeEvent(self, event):
        """Handle widget resize."""
        super().resizeEvent(event)
        # No cached pixmap to clear since we paint directly

    def cleanup(self):
        """Clean up resources when widget is destroyed."""
        if hasattr(self, "animation_timer") and self.animation_timer:
            self.animation_timer.stop()
            self.animation_timer.deleteLater()
            self.animation_timer = None

        if hasattr(self, "background") and self.background:
            try:
                self.background.update_required.disconnect(self.update)
            except (TypeError, RuntimeError, AttributeError):
                pass  # Signal wasn't connected or object already deleted
            self.background = None

    def closeEvent(self, event):
        """Handle widget close event."""
        self.cleanup()
        super().closeEvent(event)

    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup()
