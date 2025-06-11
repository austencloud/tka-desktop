from typing import Callable, Optional
from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtCore import (
    Qt,
    QEasingCurve,
    QPropertyAnimation,
    QParallelAnimationGroup,
    pyqtProperty,
    QSize,
)
from PyQt6.QtGui import QIcon, QColor, QPainter, QMouseEvent


class SequenceWorkbenchButton(QPushButton):
    """
    A custom animated button for the SequenceWorkbench, inheriting from QPushButton.
    - Hover fade (background color).
    - Press shrink/expand.
    - Icon size scales to 85% of button size.
    """

    def __init__(
        self,
        icon_path: str,
        callback: Callable[[], None],
        tooltip: str = "",
        parent: Optional["QPushButton"] = None,
    ):
        super().__init__(QIcon(icon_path), "", parent)

        # Store callback so we can call it on click
        self._callback = callback
        self._tooltip_text = tooltip

        # States
        self._scale = 1.0
        self._bg_color = QColor("white")  # current color
        self._base_color = QColor("white")  # color if not hovered
        self._hover_color = QColor("#F0F0F0")
        self._pressed_scale = 0.9
        self._pressed = False
        self._icon_percentage = 0.75

        # Animations
        self.anim_group = QParallelAnimationGroup(self)

        # 1) Scale animation
        self.scale_anim = QPropertyAnimation(self, b"clickScale")
        self.scale_anim.setDuration(120)
        self.scale_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim_group.addAnimation(self.scale_anim)

        # 2) Color animation
        self.color_anim = QPropertyAnimation(self, b"backgroundColor")
        self.color_anim.setDuration(200)
        self.color_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim_group.addAnimation(self.color_anim)

        # Initialize
        self.setMouseTracking(True)
        self.setToolTip(tooltip)
        self._update_stylesheet()

        # Connect click signal
        self.clicked.connect(self._on_clicked)

    # -------------------------------------------------
    # Event overrides
    # -------------------------------------------------
    def enterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        self._animate_hover(entering=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        self._animate_hover(entering=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self._animate_press()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._pressed and event.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
            self._animate_release()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        """
        Ensure icon size is updated whenever the button is resized.
        """
        super().resizeEvent(event)
        icon_size = int(min(self.width(), self.height()) * self._icon_percentage)
        self.setIconSize(QSize(icon_size, icon_size))
        self._update_stylesheet()  # Update radius if resized

    def paintEvent(self, event):
        """
        We override paintEvent to apply the scale transform around the center
        before letting QPushButton do its painting.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self._scale, self._scale)
        painter.translate(-self.width() / 2, -self.height() / 2)

        super().paintEvent(event)  # Draw the "normal" QPushButton stuff

    # -------------------------------------------------
    # Custom "click" callback
    # -------------------------------------------------
    def _on_clicked(self):
        """
        Calls the callback we passed in, if any.
        """
        if self._callback:
            self._callback()

    # -------------------------------------------------
    # Animated properties
    # -------------------------------------------------
    @pyqtProperty(float)
    def clickScale(self) -> float:
        return self._scale

    @clickScale.setter
    def clickScale(self, value: float):
        self._scale = value
        self.update()

    @pyqtProperty(QColor)
    def backgroundColor(self) -> QColor:
        return self._bg_color

    @backgroundColor.setter
    def backgroundColor(self, color: QColor):
        self._bg_color = color
        self._update_stylesheet()

    # -------------------------------------------------
    # Animation methods
    # -------------------------------------------------
    def _animate_hover(self, entering: bool):
        self.color_anim.stop()
        self.color_anim.setStartValue(self._bg_color)
        end_color = self._hover_color if entering else self._base_color
        self.color_anim.setEndValue(end_color)
        self.anim_group.start()

    def _animate_press(self):
        self.scale_anim.stop()
        self.scale_anim.setStartValue(self._scale)
        self.scale_anim.setEndValue(self._pressed_scale)
        self.anim_group.start()

    def _animate_release(self):
        self.scale_anim.stop()
        self.scale_anim.setStartValue(self._scale)
        self.scale_anim.setEndValue(1.0)
        self.anim_group.start()

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------
    def _update_stylesheet(self):
        """
        Apply background color + rounding.
        If you want a border, add "border: 1px solid #555;" here.
        """
        radius = min(self.width(), self.height()) // 2
        self.setStyleSheet(
            f"""
            QPushButton {{
                border-radius: {radius}px;
                background-color: {self._bg_color.name()};
            }}
        """
        )
