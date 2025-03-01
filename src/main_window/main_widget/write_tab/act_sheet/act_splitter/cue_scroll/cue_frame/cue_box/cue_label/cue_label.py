from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextOption, QFontMetrics
from .......editable_label import EditableLabel

if TYPE_CHECKING:
    from ..cue_box import CueBox


class CueLabel(EditableLabel):
    def __init__(self, cue_box: "CueBox", label_text=""):
        super().__init__(
            cue_box,
            label_text,
            align=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignTop,
            multi_line=True,
        )
        self.cue_box = cue_box

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = int(
            self.cue_box.cue_frame.cue_scroll.act_sheet.write_tab.main_widget.width()
            // 9
        )
        self.setFixedWidth(width)
        self.label.setFixedWidth(width)
        self.label.setWordWrap(True)
        self.edit.setFixedWidth(width)
        self.edit.setWordWrapMode(QTextOption.WrapMode.WordWrap)

        # Reapply your margins
        margin = int(self.cue_box.height() // 8)
        self.apply_styles(margin)

        # Dynamically adjust font size based on width
        font_size = self.calculate_font_size(width)
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)

    def calculate_font_size(self, width):
        """Calculate font size based on width without expanding height."""
        font = self.label.font()
        font_size = self.cue_box.cue_frame.cue_scroll.act_sheet.write_tab.width() // 150
        font.setPointSize(max(font_size, 8))
        font_metrics = QFontMetrics(font)
        text = self.label.text()
        text_width = font_metrics.boundingRect(text).width()
        while text_width > width:
            font_size -= 1
            font.setPointSize(min(font_size, 8))
            font_metrics = QFontMetrics(font)
            text_width = font_metrics.boundingRect(text).width()
        return max(font_size, 8)

    def _show_edit(self, event=None) -> None:
        super()._show_edit(event)
        self.edit.setFixedWidth(self.width() - 10)

    def _hide_edit(self) -> None:
        super()._hide_edit()
        self.cue_box.cue_frame.act_sheet.act_saver.save_act()
