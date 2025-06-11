"""
Modern slider with custom styling.
"""

from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt


class ModernSlider(QSlider):
    """A modern slider with custom styling."""

    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setObjectName("modernSlider")
        self.setStyleSheet(
            """


            QSlider::groove:horizontal {
                height: 8px;
                background: palette(mid);
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #3498db;
                border: none;
                width: 18px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 9px;
            }

            QSlider::handle:horizontal:hover {
                background: #2980b9;
            }

            QSlider::sub-page:horizontal {
                background: #3498db;
                border-radius: 4px;
            }
        """
        )
