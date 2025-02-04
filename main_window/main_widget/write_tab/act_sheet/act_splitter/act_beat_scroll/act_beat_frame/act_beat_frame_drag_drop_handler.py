# act_beat_frame_drag_drop_handler.py

from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .act_beat_frame import ActBeatFrame


class ActBeatFrameDragDropHandler:
    def __init__(self, beat_frame: "ActBeatFrame"):
        self.beat_frame = beat_frame

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasFormat("application/sequence-data"):
            data = event.mimeData().data("application/sequence-data")
            data_str = bytes(data).decode("utf-8")
            sequence_dict = json.loads(data_str)

            if isinstance(sequence_dict, dict):
                self.beat_frame.populator.populate_beats(sequence_dict)
                event.acceptProposedAction()
            else:
                event.ignore()
