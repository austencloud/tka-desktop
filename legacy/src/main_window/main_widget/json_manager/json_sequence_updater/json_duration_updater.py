from typing import TYPE_CHECKING

from data.constants import BEAT

if TYPE_CHECKING:
    from src.base_widgets.pictograph.elements.views.beat_view import (
        LegacyBeatView,
    )
    from .json_sequence_updater import JsonSequenceUpdater


class JsonDurationUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater") -> None:
        self.json_manager = json_updater.json_manager

    def update_beat_duration_in_json(
        self, beat_view: "LegacyBeatView", new_duration: int
    ) -> None:
        """Update beat duration and adjust subsequent beats in the sequence."""
        sequence_data = self._load_sequence_data()
        sequence_metadata, sequence_beats = self._extract_metadata_and_beats(
            sequence_data
        )

        sequence_before, current_beat_data, sequence_after = self._split_sequence(
            sequence_beats, beat_view
        )

        updated_beat_data = self._update_beat_data(current_beat_data, new_duration)
        sequence_before.append(updated_beat_data)

        if new_duration > 1:
            placeholders = self._generate_placeholders(beat_view.number, new_duration)
            sequence_before.extend(placeholders)
            sequence_after = self._shift_beats(sequence_after, shift=new_duration - 1)
        elif new_duration < current_beat_data.get("duration", 1):
            sequence_after = self._shift_beats(
                sequence_after, shift=new_duration - current_beat_data["duration"]
            )
            sequence_after = self._remove_placeholders(sequence_after, beat_view.number)

        sequence_beats = sequence_before + sequence_after
        self._finalize_and_save_sequence(sequence_metadata, sequence_beats)

    # --- Helper Methods ---

    def _load_sequence_data(self) -> list[dict]:
        """Load the current sequence JSON data."""
        return self.json_manager.loader_saver.load_current_sequence()

    def _extract_metadata_and_beats(
        self, sequence_data: list[dict]
    ) -> tuple[dict, list[dict]]:
        """Separate metadata from the sequence beats."""
        metadata = sequence_data[0] if "word" in sequence_data[0] else {}
        beats = sequence_data[1:]
        return metadata, beats

    def _split_sequence(
        self, sequence_beats: list[dict], beat_view: "LegacyBeatView"
    ) -> tuple[list[dict], dict, list[dict]]:
        """Split the sequence into parts before, at, and after the current beat."""
        before = []
        after = []
        current_beat_data = None

        for entry in sequence_beats:
            beat_num = entry.get(BEAT)
            if beat_num < beat_view.number:
                before.append(entry)
            elif beat_num == beat_view.number:
                current_beat_data = entry
            elif beat_num > beat_view.number:
                after.append(entry)

        return before, current_beat_data, after

    def _update_beat_data(self, beat_data: dict, new_duration: int) -> dict:
        """Update the beat's duration."""
        updated_data = beat_data.copy()
        updated_data["duration"] = new_duration
        return updated_data

    def _generate_placeholders(self, parent_beat_num: int, duration: int) -> list[dict]:
        """Create placeholder beats for the extended duration."""
        placeholders = [
            {
                BEAT: parent_beat_num + offset,
                "is_placeholder": True,
                "parent_beat": parent_beat_num,
            }
            for offset in range(1, duration)
        ]
        return placeholders

    def _shift_beats(self, beats: list[dict], shift: int) -> list[dict]:
        """Shift beat numbers by a specified amount and update BeatView numbers."""
        if shift == 0:
            return beats

        # Create a mapping of old beat numbers to new beat numbers
        beat_number_mapping = {}
        for beat in beats:
            old_beat_num = beat[BEAT]
            beat[BEAT] += shift
            if "parent_beat" in beat:
                beat["parent_beat"] += shift
            beat_number_mapping[old_beat_num] = beat[BEAT]

        # Update BeatView numbers based on the mapping
        self._update_beat_view_numbers(beat_number_mapping)
        return beats

    def _update_beat_view_numbers(self, beat_number_mapping: dict[int, int]) -> None:
        """Update the BeatView numbers based on the provided mapping."""
        for (
            beat_view
        ) in (
            self.json_manager.main_widget.sequence_workbench.sequence_beat_frame.beat_views
        ):
            if beat_view.number in beat_number_mapping:
                old_number = beat_view.number
                beat_view.number = beat_number_mapping[old_number]
                if beat_view.beat:
                    beat_view.beat.beat_number = beat_number_mapping[old_number]
                    beat_view.add_beat_number()

    def _remove_placeholders(
        self, beats: list[dict], parent_beat_num: int
    ) -> list[dict]:
        """Remove placeholders associated with a specific parent beat."""
        return [beat for beat in beats if beat.get("parent_beat") != parent_beat_num]

    def _finalize_and_save_sequence(
        self, metadata: dict, sequence_beats: list[dict]
    ) -> None:
        """Finalize beat numbering, remove duplicates, and save the sequence."""
        sequence_beats = self._remove_duplicate_beats(sequence_beats)
        sequence_beats.sort(key=lambda beat: beat[BEAT])
        beat_number_mapping = self._update_beat_numbers(sequence_beats)
        self._update_beat_view_numbers(beat_number_mapping)
        self._save_sequence(metadata, sequence_beats)

    def _remove_duplicate_beats(self, beats: list[dict]) -> list[dict]:
        """Eliminate duplicate beats, keeping the first occurrence."""
        unique_beats = {}
        for beat in beats:
            beat_num = beat[BEAT]
            if beat_num not in unique_beats:
                unique_beats[beat_num] = beat
        return list(unique_beats.values())

    def _update_beat_numbers(self, beats: list[dict]) -> dict[int, int]:
        """Ensure beat numbers are consecutive and update parent beat references."""
        beat_mapping = {}
        for index, beat in enumerate(beats):
            old_beat_num = beat[BEAT]
            beat_mapping[old_beat_num] = index
            beat[BEAT] = index

        for beat in beats:
            if "parent_beat" in beat:
                beat["parent_beat"] = beat_mapping.get(
                    beat["parent_beat"], beat["parent_beat"]
                )

        return beat_mapping

    def _save_sequence(self, metadata: dict, beats: list[dict]) -> None:
        """Save the updated sequence."""
        sequence_data = [metadata] + beats
        self.json_manager.loader_saver.save_current_sequence(sequence_data)
