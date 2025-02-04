from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QWidget  # Import QWidget

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWorkbenchBeatFrame,
    )


class BeatFrameKeyEventHandler(QWidget):
    def __init__(self, beat_frame: "SequenceWorkbenchBeatFrame"):
        super().__init__(beat_frame)
        self.beat_frame = beat_frame

    def keyPressEvent(self, event: "QKeyEvent") -> None:
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.beat_frame.sequence_widget.beat_deleter.delete_selected_beat()
        else:
            super().keyPressEvent(event)
