"""
Modern button for selecting pictograph letters.
"""
from PyQt6.QtWidgets import QPushButton


class LetterButton(QPushButton):
    """A modern button for selecting pictograph letters."""

    def __init__(self, letter, parent=None):
        super().__init__(letter, parent)
        self.letter = letter
        self.setCheckable(True)
        self.setChecked(True)
        self.setFixedSize(40, 40)
        self.setObjectName(f"letterButton_{letter}")

        # Determine if this is a hybrid letter
        hybrid_letters = ["C", "F", "I", "L", "O", "R", "S", "T", "U", "V"]
        self.is_hybrid = letter in hybrid_letters

        # Apply stylesheet based on hybrid status
        self._update_style()

    def _update_style(self):
        base_style = """
            QPushButton {
                border-radius: 20px;
                font-weight: bold;
                font-size: 16px;
                color: palette(text);
                background-color: palette(button);
                border: 1px solid palette(mid);
                cursor: pointer;
            }
            QPushButton:checked {
                color: white;
            }
            QPushButton:hover:!checked {
                background-color: palette(light);
                border: 1px solid palette(highlight);
            }
            QPushButton:hover {
                cursor: pointer;
            }
        """

        if self.is_hybrid:
            # Hybrid letters use a gradient background when checked
            self.setStyleSheet(
                base_style
                + """
                QPushButton:checked {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #3498db, stop:1 #e74c3c);
                }
            """
            )
        else:
            # Non-hybrid letters use a solid blue background when checked
            self.setStyleSheet(
                base_style
                + """
                QPushButton:checked {
                    background-color: #3498db;
                }
            """
            )
