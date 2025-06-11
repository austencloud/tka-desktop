from typing import TYPE_CHECKING
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QObject, QAbstractAnimation
import logging

if TYPE_CHECKING:
    from .codex import Codex

logger = logging.getLogger(__name__)


class CodexAnimationManager(QObject):
    """Manages animations for the CodexWidget, including opening and closing."""

    ANIMATION_DURATION = 350  # milliseconds

    def __init__(self, codex: "Codex"):
        super().__init__(codex)
        self.codex = codex

        self.animation = QPropertyAnimation(self.codex, b"maximumWidth")
        self.animation.setDuration(self.ANIMATION_DURATION)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.target_width = 0

    def animate(self, show: bool):
        """Toggle the visibility of the codex with animations for both showing and hiding."""
        logger.debug(f"Toggling codex visibility to {'show' if show else 'hide'}.")

        if self.animation.state() == QAbstractAnimation.State.Running:
            self.animation.stop()

        learn_tab = self.codex.main_widget.learn_tab
        learn_tab_width = learn_tab.width()
        current_width = self.codex.width()

        if show:
            self.target_width = int(learn_tab_width * 0.5)
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(self.target_width)

        else:
            self.target_width = 0
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(self.target_width)

        self.animation.start()
