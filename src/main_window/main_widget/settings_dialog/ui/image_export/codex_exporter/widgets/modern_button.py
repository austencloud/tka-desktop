"""
Modern button with custom styling.
"""
from PyQt6.QtWidgets import QPushButton


class ModernButton(QPushButton):
    """A modern button with custom styling."""

    def __init__(self, text, parent=None, primary=True):
        super().__init__(text, parent)
        self.primary = primary
        self.setObjectName("modernButton")
        self._update_style()

    def _update_style(self):
        if self.primary:
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #2980b9;
                    cursor: pointer;
                }

                QPushButton:pressed {
                    background-color: #1f6aa5;
                }
            """
            )
        else:
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: palette(button);
                    color: palette(buttontext);
                    border: 1px solid palette(mid);
                    border-radius: 5px;
                    padding: 10px 20px;
                }

                QPushButton:hover {
                    background-color: palette(light);
                    cursor: pointer;
                    border: 1px solid palette(highlight);
                }

                QPushButton:pressed {
                    background-color: palette(midlight);
                }
            """
            )
