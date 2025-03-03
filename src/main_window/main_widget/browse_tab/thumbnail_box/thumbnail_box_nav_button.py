from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

from styles.base_styled_button import BaseStyledButton

if TYPE_CHECKING:
    from .thumbnail_box_nav_buttons_widget import ThumbnailBoxNavButtonsWidget


class ThumbnailBoxNavButton(BaseStyledButton):
    def __init__(self, text: str, parent: "ThumbnailBoxNavButtonsWidget"):
        super().__init__(text)

        # Connect to parent's handler
        self.clicked.connect(parent.handle_button_click)

        # Set cursor style
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def resizeEvent(self, event) -> None:
        """Handle resizing to adjust border radius dynamically."""
        super().resizeEvent(event)
        current_style = self.styleSheet()
        new_style = f"{current_style} QPushButton {{ padding: 0; }}"
        self.setStyleSheet(new_style)
