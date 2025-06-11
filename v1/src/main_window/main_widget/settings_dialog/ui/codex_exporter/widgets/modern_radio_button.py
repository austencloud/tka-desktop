"""
Modern radio button with custom styling.
"""

from PyQt6.QtWidgets import QRadioButton


class ModernRadioButton(QRadioButton):
    """A modern radio button with custom styling."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("modernRadioButton")
        self.setStyleSheet(
            """
            QRadioButton {
                spacing: 8px;
                font-size: 14px;
                color: palette(windowtext);
                background-color: transparent;
            }

            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #3498db;
            }

            QRadioButton::indicator:checked {
                background-color: #3498db;
                border: 2px solid #3498db;
            }

            QRadioButton::indicator:unchecked {
                background-color: palette(light);
                border: 2px solid palette(mid);
            }

            QRadioButton::indicator:hover {
                border: 2px solid palette(highlight);
            }
        """
        )
