from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .letter_types import LetterType


class OptionPickerSectionButton(QPushButton):
    def __init__(self, letter_type: str, parent=None):
        super().__init__(parent)
        self.letter_type = letter_type
        self.is_expanded = True
        self._setup_styling()
        self._update_text()

    def _setup_styling(self):
        self.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 220),
                    stop:1 rgba(245, 245, 245, 200));
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 10px 20px;
                text-align: center;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(240, 248, 255, 220),
                    stop:1 rgba(230, 240, 250, 200));
                border-color: #3498db;
                box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(220, 220, 220, 200),
                    stop:1 rgba(200, 200, 200, 180));
                border-color: #2980b9;
            }
        """
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _update_text(self):
        description, type_name = LetterType.get_type_description(self.letter_type)
        expand_indicator = "▼" if self.is_expanded else "▶"
        self.setText(f"{expand_indicator} {type_name}: {description}")

    def toggle_expansion(self):
        self.is_expanded = not self.is_expanded
        self._update_text()
