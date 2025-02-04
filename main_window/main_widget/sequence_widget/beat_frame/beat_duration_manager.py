from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beat_view import BeatView
    from .sequence_widget_beat_frame import SequenceWorkbenchBeatFrame


class BeatDurationManager:
    def __init__(self, beat_frame: "SequenceWorkbenchBeatFrame"):
        self.beat_frame = beat_frame
        self.json_duration_updater = beat_frame.json_manager.updater.duration_updater

    def update_beat_duration(
        self, changed_beat_view: "BeatView", new_duration: int
    ) -> None:
        """
        Update the beat duration, adjust beat numbering, and update the JSON file.
        """
        # Update the beat duration in the view
        current_beat = changed_beat_view.beat
        current_beat.duration = new_duration
        changed_beat_view.add_beat_number()

        # Delegate JSON update to JsonDurationUpdater
        self.json_duration_updater.update_beat_duration_in_json(
            changed_beat_view, new_duration
        )

        # After JSON update, refresh beat numbers in the UI
        self.update_beat_numbers()

    def update_beat_numbers(self) -> None:
        """
        Update beat numbers for all beats based on the JSON data.
        """
        sequence_data = (
            self.beat_frame.json_manager.loader_saver.load_current_sequence_json()
        )
        sequence_beats = sequence_data[1:]  # Skip metadata

        # Build a mapping from beat numbers to entries
        beat_entries = {beat["beat"]: beat for beat in sequence_beats}

        # Update BeatView numbers
        for beat_view in self.beat_frame.beat_views:
            if beat_view.beat:
                beat_number = beat_view.number
                if beat_number in beat_entries:
                    beat_view.beat.beat_number = beat_number
                    beat_view.add_beat_number()
            else:
                # Handle blank beats or placeholders if necessary
                pass
