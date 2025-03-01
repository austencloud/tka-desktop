from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QPushButton,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QColor


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer_action_button_panel import (
        SequenceViewerActionButtonPanel,
    )


from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, Qt
from PyQt6.QtGui import QIcon, QColor


class SequenceViewerActionButton(QPushButton):
    def __init__(
        self, icon_path: str, tooltip: str, panel: "SequenceViewerActionButtonPanel"
    ):
        super().__init__(QIcon(icon_path), "", panel)
        self.panel = panel
        self.setToolTip(tooltip)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._color = QColor("white")
        self.default_color = QColor("white")
        self.hover_color = QColor("#e0e0e0")

        self.animation = QPropertyAnimation(self, b"color", self)
        self.animation.setDuration(100)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self._update_stylesheet(self._color)

    def setColor(self, color: QColor):
        self._color = color
        self._update_stylesheet(color)

    @pyqtProperty(QColor)
    def color(self) -> QColor:
        return self._color

    @color.setter
    def color(self, new_color: QColor):
        self._color = new_color
        self._update_stylesheet(new_color)

    def enterEvent(self, event):
        self.animation.setStartValue(self.color)
        self.animation.setEndValue(self.hover_color)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setStartValue(self.color)
        self.animation.setEndValue(self.default_color)
        self.animation.start()

    def _update_stylesheet(self, color: QColor):
        radius = self.width() // 2
        self.setStyleSheet(
            f"QPushButton {{ "
            f"  border-radius: {radius}px; "
            f"  background-color: {color.name()}; "
            f"}}"
        )
