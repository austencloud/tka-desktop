from PyQt6.QtWidgets import QToolButton, QLabel
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QFont


class CustomTooltipButton(QToolButton):
    """
    A QToolButton subclass that uses a custom tooltip (a QLabel) rather than
    the standard Qt tooltip system. This ensures consistent styling,
    position, and behavior across platforms.
    """

    def __init__(self, text: str, tooltip_text: str, parent=None):
        super().__init__(parent)
        self.setText(text)
        self._tooltip_text = tooltip_text

        # Create a QLabel for the tooltip. Make it a child of this button
        # so it will appear "on top" when shown.
        self._tooltip_label = QLabel(self)
        self._tooltip_label.setText(self._tooltip_text)

        # Style the label to appear like a tooltip: bold white text on a black background.
        self._tooltip_label.setStyleSheet(
            """
            background-color: black;
            color: white;
            font-weight: bold;
            border: 1px solid white;
            border-radius: 4px;
            padding: 5px;
        """
        )
        font = QFont()
        font.setBold(True)
        self._tooltip_label.setFont(font)

        # Start hidden until we hover
        self._tooltip_label.hide()

    def enterEvent(self, event):
        """
        When the mouse enters the button, position and show the tooltip.
        """
        self._position_tooltip()
        self._tooltip_label.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        When the mouse leaves the button, hide the tooltip.
        """
        self._tooltip_label.hide()
        super().leaveEvent(event)

    def _position_tooltip(self):
        """
        Determine where the tooltip label should appear.
        For example, 5px below the button, horizontally centered.
        """
        # Horizontal center: (width_of_button - width_of_tooltip) / 2
        tooltip_width = self._tooltip_label.width()
        button_width = self.width()
        x = (button_width - tooltip_width) // 2

        # 5 px below the bottom edge
        y = self.height() + 5

        self._tooltip_label.move(QPoint(x, y))
