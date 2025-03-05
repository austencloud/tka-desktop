from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING


if TYPE_CHECKING:

    from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer_header import (
        SequenceViewerHeader,
    )
    from settings_manager.settings_manager import SettingsManager


class SequenceViewerWordLabel(QLabel):
    def __init__(
        self,
        text: str,
        header: "SequenceViewerHeader",
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

        available_width = self.header.width() - (
            self.header.favorite_button.width() * 5
        )
        fm = self.fontMetrics()
        while fm.horizontalAdvance(self.text()) > available_width and font_size > 1:
            font_size -= 1
            font.setPointSize(font_size)
            self.setFont(font)
            fm = self.fontMetrics()
        super().resizeEvent(event)

    def update_word_label(self, text: str):
        self.setText(text)
