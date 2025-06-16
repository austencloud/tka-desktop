# act_beat_frame_initializer.py

from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from .act_beat_view import ActBeatView
from .act_step_label import ActStepLabel

if TYPE_CHECKING:
    from .act_beat_frame import ActBeatFrame


class ActBeatFrameInitializer:
    def __init__(self, beat_frame: "ActBeatFrame"):
        self.beat_frame = beat_frame
        self.act_sheet = beat_frame.act_sheet
        self.init_act(
            self.act_sheet.DEFAULT_COLUMNS,
            self.act_sheet.DEFAULT_ROWS,
        )

    def init_act(self, num_beats: int, num_rows: int):
        """Initialize the act with a grid of beats and labels."""
        self.num_columns = num_beats
        for row in range(num_rows):
            for col in range(num_beats):
                beat_view = ActBeatView(self.beat_frame)
                beat_view.setCursor(Qt.CursorShape.PointingHandCursor)
                self.beat_frame.beats.append(beat_view)
                self.beat_frame.layout.addWidget(beat_view, row * 2, col)
                beat_number = col + 1
                beat_view.add_beat_number(beat_number)

                step_label = ActStepLabel(self.beat_frame, "")
                self.beat_frame.step_labels.append(step_label)
                self.beat_frame.layout.addWidget(step_label, row * 2 + 1, col)

                self.beat_frame.beat_step_map[beat_view] = step_label
