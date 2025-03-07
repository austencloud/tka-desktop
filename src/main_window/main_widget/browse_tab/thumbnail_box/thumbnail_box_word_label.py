from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from utils.word_simplifier import WordSimplifier


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box_header import (
        ThumbnailBoxHeader,
    )
    from settings_manager.settings_manager import SettingsManager

WORD_LENGTH = 8


class ThumbnailBoxWordLabel(QLabel):
    def __init__(
        self,
        text: str,
        header: "ThumbnailBoxHeader",
        settings_manager: "SettingsManager",
    ):
        super().__init__(text, header)
        self.header = header
        self.settings_manager = settings_manager
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Georgia", 12, QFont.Weight.DemiBold))

    def resizeEvent(self, event: QEvent) -> None:
        font_size = self.header.width() // 18
        font = QFont("Georgia", font_size, QFont.Weight.DemiBold)
        self.setFont(font)

        color = self.settings_manager.global_settings.get_current_font_color()
        self.setStyleSheet(f"color: {color};")

        available_width = self.header.width() * 0.8
        fm = self.fontMetrics()
        while fm.horizontalAdvance(self.text()) > available_width and font_size > 1:
            font_size -= 1
            font.setPointSize(font_size)
            self.setFont(font)
            fm = self.fontMetrics()
        super().resizeEvent(event)

    def set_current_word(self, word: str):
        self.simplified_word = WordSimplifier.simplify_repeated_word(word)
        self.current_word = self.simplified_word

        # Get the first 8 letter characters of the word, including the dash
        count = 0
        result = []
        for char in self.simplified_word:
            if char.isalpha():
                count += 1
            result.append(char)
            if count == WORD_LENGTH:
                break

        # Join the result list to form the final string
        truncated_word = "".join(result)

        # Add "..." if the count is higher than WORD_LENGTH
        word_without_dashes = self.simplified_word.replace("-", "")
        truncated_word_without_dashes = truncated_word.replace("-", "")

        if count == WORD_LENGTH and len(word_without_dashes) > len(
            truncated_word_without_dashes
        ):
            truncated_word += "..."

        self.line_edit.setText(truncated_word)
        self.resizeEvent(None)
