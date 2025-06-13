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
        # V1-style font: slightly larger and more prominent
        self.setFont(QFont("Arial", 13, QFont.Weight.Bold))

        # V1-style header styling: cleaner, more professional appearance
        self.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(248, 249, 250, 240),
                    stop:1 rgba(233, 236, 239, 220));
                border: 1px solid rgba(206, 212, 218, 180);
                border-radius: 4px;
                padding: 12px 16px;
                text-align: left;
                min-height: 16px;
                color: #495057;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(233, 236, 239, 240),
                    stop:1 rgba(222, 226, 230, 220));
                border-color: rgba(173, 181, 189, 200);
                color: #343a40;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(222, 226, 230, 220),
                    stop:1 rgba(206, 212, 218, 200));
                border-color: rgba(134, 142, 150, 220);
                color: #212529;
            }
        """
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _update_text(self):
        description, type_name = LetterType.get_type_description(self.letter_type)
        expand_indicator = "▼" if self.is_expanded else "▶"

        # CRITICAL FIX: Strip HTML tags from description to display clean text
        import re

        clean_description = re.sub(r"<[^>]+>", "", description)

        self.setText(f"{expand_indicator} {type_name}: {clean_description}")

    def toggle_expansion(self):
        self.is_expanded = not self.is_expanded
        self._update_text()
