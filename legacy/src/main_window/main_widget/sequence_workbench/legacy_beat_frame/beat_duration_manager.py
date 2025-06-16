from typing import TYPE_CHECKING

from data.constants import BEAT
from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.beat_view import LegacyBeatView
    from .legacy_beat_frame import LegacyBeatFrame


class BeatDurationManager:
    def __init__(self, beat_frame: "LegacyBeatFrame"):
        self.beat_frame = beat_frame
        self.json_duration_updater = AppContext.json_manager().updater.duration_updater

    def update_beat_duration(
        self, changed_beat_view: "LegacyBeatView", new_duration: int
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
        sequence_data = AppContext.json_manager().loader_saver.load_current_sequence()
        sequence_beats = sequence_data[1:]  # Skip metadata

        # Build a mapping from beat numbers to entries
        beat_entries = {beat[BEAT]: beat for beat in sequence_beats}

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
