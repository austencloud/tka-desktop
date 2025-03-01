from typing import TYPE_CHECKING
from data.beat_frame_layouts import sequence_workbench_BEAT_FRAME_LAYOUTS
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.temp_beat_frame.temp_beat_frame import (
        TempBeatFrame,
    )


class TempBeatFrameLayoutManager:
    def __init__(self, temp_beat_frame: "TempBeatFrame"):
        self.beat_frame = temp_beat_frame
        self.settings_manager = AppContext.settings_manager()

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        return sequence_workbench_BEAT_FRAME_LAYOUTS.get(beat_count, (1, beat_count))

    def get_cols(self):
        layout = self.beat_frame.layout
        cols = 0
        for i in range(layout.columnCount()):
            if layout.itemAtPosition(0, i):
                cols += 1
        return cols - 1

    def get_rows(self):
        layout = self.beat_frame.layout
        rows = 0
        for i in range(layout.rowCount()):
            if layout.itemAtPosition(i, 1):
                rows += 1
        return rows

    def configure_beat_frame(self, num_beats):
        grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
        if grow_sequence:
            num_filled_beats = self.beat_frame.get.next_available_beat() or 0
            num_beats = num_filled_beats
        columns, rows = self.calculate_layout(num_beats)

        self.rearrange_beats(num_beats, columns, rows)

    def rearrange_beats(self, num_beats, columns, rows):
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        index = 0
        beats = self.beat_frame.beat_views
        for row in range(rows):
            for col in range(1, columns + 1):
                if index < num_beats:
                    beat_view = beats[index]
                    self.beat_frame.layout.addWidget(beat_view, row, col)
                    beat_view.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        index += 1

        self.beat_frame.adjustSize()
