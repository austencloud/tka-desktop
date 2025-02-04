from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import QPropertyAnimation, QRect, Qt, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter


class PyToggle(QCheckBox):
    def __init__(
        self,
        width=60,
        bg_color="#00BCff",  # Default background color
        active_color="#00BCff",  # Background color when checked (if changing)
        circle_color="#DDD",
        animation_curve=QEasingCurve.Type.OutBounce,
        change_bg_on_state=False,  # New parameter to control background color change
    ):
        super().__init__()
        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Colors
        self._bg_color = QColor(bg_color)
        self._active_color = QColor(active_color)
        self._circle_color = QColor(circle_color)

        self._change_bg_on_state = change_bg_on_state  # Store the new parameter

        # Animation properties
        self._circle_position = 3  # Initial circle position
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(300)

        # Connect to state change
        self.stateChanged.connect(self.start_transition)

    def start_transition(self, state):
        """Start the animation when toggle is clicked."""
        self.animation.stop()  # Stop any ongoing animation
        if state:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)
        self.animation.start()
        self.update()  # Ensure the widget is redrawn when the state changes

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    # SET A NEW HIT AREA
    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def paintEvent(self, e):
        """Custom paint for drawing the toggle switch."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Determine background color based on toggle state and parameter
        rect = QRect(0, 0, self.width(), self.height())
        if self._change_bg_on_state and self.isChecked():
            painter.setBrush(self._active_color)
        else:
            painter.setBrush(self._bg_color)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self.height() / 2, self.height() / 2)

        # Draw the circle using the animated position
        painter.setBrush(self._circle_color)
        painter.drawEllipse(int(self._circle_position), 3, 22, 22)
        painter.end()
