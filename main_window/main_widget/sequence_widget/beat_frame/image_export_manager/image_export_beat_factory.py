from typing import TYPE_CHECKING, Union

from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView


if TYPE_CHECKING:
    from .image_export_manager import ImageExportManager
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWorkbenchBeatFrame,
    )

    from main_window.main_widget.browse_tab.temp_beat_frame.temp_beat_frame import (
        TempBeatFrame,
    )


class ImageExportBeatFactory:
    def __init__(
        self,
        export_manager: "ImageExportManager",
        beat_frame_class: Union["SequenceWorkbenchBeatFrame", "TempBeatFrame"],
    ):
        self.export_manager = export_manager
        self.beat_frame_class = beat_frame_class

    def process_sequence_to_beats(self, sequence: list[dict]) -> list[BeatView]:
        if self.beat_frame_class.__name__ == "SequenceWorkbenchBeatFrame":
            temp_beat_frame = self.beat_frame_class(
                self.export_manager.main_widget.sequence_widget
            )
        elif self.beat_frame_class.__name__ == "TempBeatFrame":
            temp_beat_frame = self.beat_frame_class(
                self.export_manager.main_widget.browse_tab
            )

        filled_beats = []
        current_beat_number = 1  # Start beat numbering from 1

        for beat_data in sequence[2:]:  # Skip the metadata (first entry)
            if beat_data.get("is_placeholder"):
                continue  # Skip placeholder beats

            # Determine beat duration
            duration = beat_data.get("duration", 1)

            # Create the beat view and assign it the correct beat range
            beat_view = self.create_beat_view_from_data(
                beat_data, current_beat_number, temp_beat_frame
            )

            filled_beats.append(beat_view)

            # Increment beat number by the duration of the current beat
            current_beat_number += duration

        return filled_beats

    def create_beat_view_from_data(self, beat_data, number, temp_beat_frame):
        new_beat_view = BeatView(temp_beat_frame)
        beat = Beat(temp_beat_frame)
        beat.pictograph_dict = beat_data
        beat.updater.update_pictograph(beat_data)

        # Set the beat with the actual number, not the display text
        new_beat_view.set_beat(beat, number)
        return new_beat_view
