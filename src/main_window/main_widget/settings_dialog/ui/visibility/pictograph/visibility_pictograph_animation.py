from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from enums.glyph_enum import Glyph


class VisibilityPictographAnimation:
    def __init__(self, glyph: Glyph):
        self.glyph = glyph

        # Opacity animation
        self.opacity_animation = QPropertyAnimation(glyph, b"opacity")
        self.opacity_animation.setDuration(300)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def play_opacity_animation(self, target_opacity: float):
        """Animate the opacity of the glyph."""
        self.opacity_animation.stop()
        self.opacity_animation.setStartValue(self.glyph.opacity())
        self.opacity_animation.setEndValue(target_opacity)
        self.opacity_animation.start()
