# act_step_label.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from .....editable_label import EditableLabel

if TYPE_CHECKING:
    from .act_beat_frame import ActBeatFrame


class ActStepLabel(EditableLabel):
    def __init__(self, act_beat_frame: "ActBeatFrame", label_text=""):
        super().__init__(
            act_beat_frame,
            label_text,
            align=Qt.AlignmentFlag.AlignCenter,
            multi_line=True,
        )
        self.act_beat_frame = act_beat_frame

    def resizeEvent(self, event):
        """Resize the step label based on the beat frame's calculated sizes."""
        margin = int(self.act_beat_frame.beat_size // 8)
        self.apply_styles(margin)
        self.setFixedHeight(self.act_beat_frame.steps_label_height)
        self.setFixedWidth(self.act_beat_frame.beat_size)

        font_size = self.height() // 8
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)
        self.label.setFont(font)
        self.edit.setFont(font)

    def _hide_edit(self) -> None:
        super()._hide_edit()
        self.act_beat_frame.act_sheet.act_saver.save_act()
