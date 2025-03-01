from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QGridLayout
from data.act_beat_frame_layouts import ACT_BEAT_FRAME_LAYOUTS
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.act_sheet.act_splitter.act_beat_scroll.act_beat_frame.act_beat_frame import (
        ActBeatFrame,
    )


class ActBeatFrameLayoutManager:
    def __init__(self, beat_frame: "ActBeatFrame"):
        self.beat_frame = beat_frame
        self.selection_manager = beat_frame.selection_overlay
        self.settings_manager = AppContext.settings_manager()
        self.setup_layout()

    def setup_layout(self) -> None:
        layout: QGridLayout = QGridLayout(self.beat_frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.beat_frame.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Arrange beats and labels
        for i, (beat, label) in enumerate(
            zip(self.beat_frame.beats, self.beat_frame.step_labels)
        ):
            row, col = divmod(i, self.beat_frame.act_sheet.DEFAULT_COLUMNS)
            layout.addWidget(beat, row * 2, col)
            layout.addWidget(label, row * 2 + 1, col)

        self.beat_frame.layout = layout

    def calculate_total_rows(self) -> int:
        """Calculate the total number of rows based on the layout configuration."""
        return (
            len(self.beat_frame.beats) + self.beat_frame.act_sheet.DEFAULT_COLUMNS - 1
        ) // self.beat_frame.act_sheet.DEFAULT_COLUMNS

    def rearrange_beats(self, num_beats, columns, rows):
        # Clear the current layout and hide widgets
        while self.beat_frame.layout.count():
            item = self.beat_frame.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()

        index = 0
        beats = self.beat_frame.beats
        labels = self.beat_frame.step_labels
        for row in range(rows):
            for col in range(columns):
                if index < num_beats:
                    beat_view = beats[index]
                    label = labels[index]
                    self.beat_frame.layout.addWidget(beat_view, row * 2, col)
                    self.beat_frame.layout.addWidget(label, row * 2 + 1, col)
                    beat_view.show()
                    label.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        labels[index].hide()
                        index += 1

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        return ACT_BEAT_FRAME_LAYOUTS.get(beat_count, (1, beat_count))

    def get_row(self, beat_view):
        return self.beat_frame.layout.getItemPosition(
            self.beat_frame.layout.indexOf(beat_view)
        )[0]
