from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


class CurrentlyDisplayingLabel(QLabel):
    def __init__(self, sequence_picker: "SequencePicker") -> None:
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_message(self, description):
        self.setText(f"Currently displaying {description}.")

    def resizeEvent(self, event):
        font = self.font()
        font_size = self.sequence_picker.main_widget.width() // 100
        font.setPointSize(font_size)
        self.setFont(font)
        super().resizeEvent(event)
