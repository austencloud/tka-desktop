from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt


class StyledCheckBox(QCheckBox):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_stylesheet(self, color: str) -> None:
        self.setStyleSheet(
            f"""
            QCheckBox {{
            color: {color}; /* The text color, if desired */
            spacing: 8px; /* space between checkbox and text */
            }}

            /* Set a fixed size for the indicator */
            QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            }}

            /* Style the unchecked indicator to have a clear border and background */
            QCheckBox::indicator:unchecked {{
            border: 2px solid #ccc;
            border-radius: 3px;
            background: #fff; /* a white background for clarity */
            }}

            /* Optional: For a more noticeable hover effect (if desired) */
            QCheckBox::indicator:hover {{
            border: 2px solid #68d4ff;
            }}
            """
        )
