from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .codex import Codex


class CodexToggleButton(QPushButton):
    """A button dedicated to toggling the Codex open/closed."""

    def __init__(self, codex: "Codex"):
        """Initializes the toggle button with a reference to the parent Codex."""
        super().__init__("Codex", codex)
        self.codex = codex
        self.main_widget = codex.main_widget
        self.codex_shown = True
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.toggle_codex)

    def toggle_codex(self) -> None:
        """Toggles the visibility of the codex with an animation."""
        self.codex_shown = not self.codex_shown
        self.codex.animation_manager.animate(self.codex_shown)

    def resizeEvent(self, event) -> None:
        """Adjusts the toggle button size based on the Codex's parent widget dimensions."""
        if self.main_widget is not None:
            button_height = self.main_widget.height() // 30
            button_width = self.main_widget.width() // 14
            self.setFixedHeight(button_height)
            self.setFixedWidth(button_width)

        font = self.font()
        font.setBold(True)
        font_size = self.main_widget.height() // 60
        font.setPointSize(font_size)
        self.setFont(font)
        super().resizeEvent(event)
