from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal, QEvent


class SidebarButton(QPushButton):
    """A specialized QPushButton for sidebar elements, handling its own styling."""

    clicked_signal = pyqtSignal(str)  # Custom signal to pass section data

    def __init__(self, section_key: str):
        super().__init__(section_key)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.is_selected = False
        self.section_key = section_key
        self.border_radius = 5  # Default border radius
        self.update_button_styles()
        self.clicked.connect(self.emit_clicked_signal)

    def update_button_styles(self) -> None:
        """Apply the appropriate styles based on the selection state and enabled state."""
        background_color = (
            "rgba(211, 211, 211, 0.5)" if self.is_selected else "rgba(0, 0, 0, 0.1)"
        )
        font_color = "black" if self.is_selected else "white"
        border_color = "black" if self.isEnabled() else "#333"
        hover_background = "#555" if self.isEnabled() else "rgba(240, 240, 240, 0.5)"
        hover_font_color = "black" if self.isEnabled() else "#888"

        self.setStyleSheet(
            f"""
            QPushButton {{
                background: {background_color};
                border-radius: {self.border_radius}px;
                color: {font_color};
                padding: 5px;
                font-weight: bold;
                text-align: center;
                border: 1px solid {border_color};
            }}
            QPushButton:hover {{
                background: {hover_background};
                color: {hover_font_color};
                border: 1px solid white;
            }}
            """
        )

    def set_selected(self, selected: bool) -> None:
        """Update the button selection state and restyle it."""
        self.is_selected = selected
        self.update_button_styles()

    def emit_clicked_signal(self) -> None:
        """Emit a signal when clicked, passing the button label."""
        self.clicked_signal.emit(self.text())

    def set_button_enabled(self, enabled: bool) -> None:
        """Enables/disables the button and updates its style/cursor."""
        self.setEnabled(enabled)
        self.setCursor(
            QCursor(
                Qt.CursorShape.PointingHandCursor
                if enabled
                else Qt.CursorShape.ForbiddenCursor
            )
        )
        self.update_button_styles()

    def resizeEvent(self, event: QEvent) -> None:
        """Handle the resize event to update the border radius."""
        self.border_radius = min(self.height(), self.width()) // 2
        self.update_button_styles()
        super().resizeEvent(event)
