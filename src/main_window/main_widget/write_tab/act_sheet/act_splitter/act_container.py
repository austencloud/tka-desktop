from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QFrame, QHBoxLayout
from .act_beat_scroll.act_beat_scroll import ActBeatScroll
from .cue_scroll.cue_scroll import CueScroll

if TYPE_CHECKING:
    from ..act_sheet import ActSheet


class ActContainer(QFrame):
    def __init__(self, act_sheet: "ActSheet") -> None:
        super().__init__(act_sheet)
        self.act_sheet = act_sheet
        self.write_tab = act_sheet.write_tab

        # Initialize scroll areas
        self.cue_scroll = CueScroll(self.act_sheet)
        self.beat_scroll = ActBeatScroll(self.act_sheet)
        self.layout: QHBoxLayout = QHBoxLayout(self)

        # Add widgets to the splitter
        self.layout.addWidget(self.cue_scroll, 1)
        self.layout.addWidget(self.beat_scroll, 8)
        self.setAcceptDrops(False)

        # Configure splitter appearance and behavior
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("margin: 0px; padding: 0px; spacing: 0px;")

    def get_cue_timestamp_for_row(self, row: int) -> tuple[str, str]:
        """Get the cue timestamp for the specified row."""
        cue_box = self.cue_scroll.cue_frame.cue_boxes[row]
        cue_text = cue_box.cue_label.label.text()
        timestamp_text = cue_box.timestamp.label.text()
        return cue_text, timestamp_text

    def save_scrollbar_state(self):
        settings = self.write_tab.main_widget.settings_manager.settings
        settings.setValue("act_sheet/scrollbar_state", self.sender().value())

    def restore_scrollbar_state(self):
        settings = self.write_tab.main_widget.settings_manager.settings
        beat_scrollbar_state = settings.value("act_sheet/scrollbar_state")
        if beat_scrollbar_state:
            self.beat_scroll.verticalScrollBar().setValue(int(beat_scrollbar_state))
        timestamp_scrollbar_state = settings.value("act_sheet/scrollbar_state")
        if timestamp_scrollbar_state:
            self.cue_scroll.verticalScrollBar().setValue(int(timestamp_scrollbar_state))

    def connect_scroll_sync(self):
        """Synchronize the scrollbars of the timestamp and beat scroll areas."""
        scroll_areas: list[tuple[QScrollArea, QScrollArea]] = [
            (self.beat_scroll, self.cue_scroll),
            (self.cue_scroll, self.beat_scroll),
        ]

        for source, target in scroll_areas:
            source.verticalScrollBar().valueChanged.connect(
                target.verticalScrollBar().setValue
            )
            source.verticalScrollBar().valueChanged.connect(self.save_scrollbar_state)

    def get_beats_in_row(self, row: int):
        """Get the beat views in the specified row."""
        return [
            beat_view
            for beat_view in self.beat_scroll.act_beat_frame.beats
            if self.beat_scroll.act_beat_frame.layout_manager.get_row(beat_view) == row
        ]
