from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal


class SidebarButton(QPushButton):
    """A specialized QPushButton for sidebar elements, handling its own styling."""

    clicked_signal = pyqtSignal(str)  # Custom signal to pass section data

    def __init__(self, label: str, is_selected: bool = False):
        super().__init__(label)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.is_selected = is_selected

        self.update_styles()
        self.clicked.connect(self.emit_clicked_signal)

    def update_styles(self):
        """Apply the appropriate styles based on the selection state."""
        background_color = "lightgray" if self.is_selected else "transparent"
        font_color = "black" if self.is_selected else "white"

        self.setStyleSheet(
            f"""
            QPushButton {{
                background: {background_color};
                border-radius: 5px;
                color: {font_color};
                padding: 5px;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background: #f0f0f0;
                color: black;
            }}
            """
        )

    def set_selected(self, selected: bool):
        """Update the button selection state and restyle it."""
        self.is_selected = selected
        self.update_styles()

    def emit_clicked_signal(self):
        """Emit a signal when clicked, passing the button label."""
        self.clicked_signal.emit(self.text())
