from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


class SequencePickerCountLabel(QLabel):
    def __init__(self, sequence_picker: "SequencePicker") -> None:
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_count(self, count: int):
        """Update the label with the count of displayed sequences."""
        self.setText(f"Sequences displayed: {count}")

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.sequence_picker.width() // 80)
        self.setFont(font)
