from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QEvent

from .......editable_label import EditableLabel

if TYPE_CHECKING:
    from ..cue_box import CueBox

from typing import TYPE_CHECKING
from .timestamp_line_edit import TimestampLineEdit  # Import the custom line edit

if TYPE_CHECKING:
    from ..cue_box import CueBox


class Timestamp(EditableLabel):
    def __init__(self, cue_box: "CueBox", label_text="0:00"):
        super().__init__(
            cue_box, label_text, align=Qt.AlignmentFlag.AlignLeft, multi_line=False
        )
        self.cue_box = cue_box

        self.edit = TimestampLineEdit(self, label_text)
        self.layout.addWidget(self.edit)  # Add it to the layout

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setFixedWidth(self.sizeHint().width())
        self.edit.setFixedWidth(self.edit.sizeHint().width())

        font_size = int(
            self.cue_box.cue_frame.cue_scroll.act_sheet.write_tab.height() // 80
        )
        font = self.label.font()
        font.setPointSize(max(font_size, 8))
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)

    def eventFilter(self, source, event) -> bool:
        """Filter for Enter key to commit and align height in edit mode."""
        if (
            source == self.edit
            and event.type() == QEvent.Type.KeyPress
            and event.key() == Qt.Key.Key_Return
            and (
                not self.multi_line
                or event.modifiers() == Qt.KeyboardModifier.NoModifier
            )
        ):
            self._hide_edit()
            return True
        return super().eventFilter(source, event)
