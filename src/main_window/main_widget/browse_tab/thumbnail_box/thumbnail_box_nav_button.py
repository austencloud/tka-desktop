from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .thumbnail_box_nav_buttons_widget import ThumbnailBoxNavButtonsWidget


class ThumbnailBoxNavButton(QPushButton):
    def __init__(self, text: str, parent: "ThumbnailBoxNavButtonsWidget"):
        super().__init__(text, parent)

        # Connect to parent's handler
        self.clicked.connect(parent.handle_button_click)

        # Set cursor style
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Custom styling with white border hover effect and a compact size
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #3c3f41;
                color: white;
                border: 2px solid #4b4e50;
                border-radius: 6px; 
                padding: 6px 10px; 
                font-weight: bold;
                font-family: 'Arial', sans-serif;
            }
            QPushButton:hover {
                background-color: #5c5f60;
                border: 2px solid white; /* White border effect on hover */
            }
            QPushButton:pressed {
                background-color: #2c2f31;
                border: 2px solid #1c1f20;
            }
            QPushButton:disabled {
                background-color: #7f7f7f;
                color: #c8c8c8;
                border: 2px solid #6f6f6f;
            }
            """
        )
