from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from .sequence_viewer_nav_buttons_widget import SequenceViewerNavButtonsWidget


class SequenceViewerNavButton(StyledButton):
    def __init__(self, text: str, parent: "SequenceViewerNavButtonsWidget"):
        super().__init__(text)

        # Connect to parent's handler
        self.clicked.connect(parent.handle_button_click)

        # Set cursor style
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # # Custom styling for a modern and clean look
        # self.setStyleSheet(
        #     """
        #     QPushButton {
        #         background-color: #3c3f41;
        #         color: white;
        #         border: 2px solid #4b4e50;
        #         border-radius: 10px;
        #         padding: 10px 15px;
        #         font-weight: bold;
        #         font-family: 'Arial', sans-serif;
        #     }
        #     QPushButton:hover {
        #         background-color: #5c5f60;
        #         border: 2px solid white; /* White border effect on hover */
        #     }
        #     QPushButton:pressed {
        #         background-color: #2c2f31;
        #         border: 2px solid #1c1f20;
        #     }
        #     QPushButton:disabled {
        #         background-color: #7f7f7f;
        #         color: #c8c8c8;
        #         border: 2px solid #6f6f6f;
        #     }
        #     """
        # )
