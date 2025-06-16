# section_type_label.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from enums.letter.letter_type import LetterType
from utils.letter_type_text_painter import (
    LetterTypeTextPainter,
)

if TYPE_CHECKING:
    from .codex import Codex


class CodexSectionTypeLabel(QLabel):
    def __init__(self, codex: "Codex", letter_type: LetterType) -> None:
        super().__init__()
        self.codex = codex
        self.letter_type = letter_type
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_styled_text(letter_type)

    def set_styled_text(self, letter_type: LetterType) -> None:
        styled_description = LetterTypeTextPainter.get_colored_text(
            letter_type.description
        )
        type_name = "".join(
            [i if not i.isdigit() else f" {i}" for i in letter_type.name]
        )
        self.setText(f"{type_name}: {styled_description}")

    def get_font_size(self):
        return max(12, self.codex.main_widget.height() // 45)

    def resizeEvent(self, event):
        self.label_height = self.get_font_size() * 2
        self.setFixedHeight(self.label_height)
        # self.setFixedWidth(self.fontMetrics().horizontalAdvance(self.text()))
        border_style = "2px solid black"
        self.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  border-radius: {self.label_height // 2}px;"
            f"  font-size: {self.get_font_size()}px;"
            f"  font-weight: bold;"
            f"  border: {border_style};"
            f"  padding: 0 10px;"
            f"}}"
        )
