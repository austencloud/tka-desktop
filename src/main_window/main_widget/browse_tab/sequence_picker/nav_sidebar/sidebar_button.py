from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal


class SidebarButton(QPushButton):
    """A specialized QPushButton for sidebar elements, handling its own styling."""

    clicked_signal = pyqtSignal(str)  # Custom signal to pass section data

    def __init__(self, section_key: str):
        super().__init__(section_key)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.is_selected = False
        self.update_styles()
        self.clicked.connect(self.emit_clicked_signal)
        self.section_key = section_key
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

    def set_button_enabled(self, enabled: bool):
        """Enables/disables the button and updates its style/cursor."""
        background_color = "lightgray" if self.is_selected else "transparent"
        font_color = "black" if self.is_selected else "white"
        self.setEnabled(enabled)
        if enabled:
            # Normal look
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
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
                    background: #555;
                }}
                """
            )
        else:
            # Disabled look
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))  # or ForbiddenCursor
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: gray;
                    color: #888;
                    border: 1px solid #333;
                    font-weight: normal;
                }
            """
            )
