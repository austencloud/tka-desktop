from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.act_sheet.act_sheet import ActSheet


class SequenceCollector:
    def __init__(self, act_sheet: "ActSheet"):
        self.act_sheet = act_sheet
        self.act_container = act_sheet.act_container

    def collect_sequences(self):
        sequences = []
        total_rows = self.act_sheet.DEFAULT_ROWS

        for row in range(total_rows):
            sequence_data: dict[str, Union[str, int, list[dict]]] = {
                "sequence_start_marker": row == 0,
                "cue": "",
                "timestamp": "",
                "beats": [],
            }

            beat_views = self.act_sheet.act_container.get_beats_in_row(row)
            for beat_view in beat_views:
                if not beat_view.is_populated():
                    continue

                raw_beat_data = beat_view.extract_metadata()
                sequence_data["beats"].append(
                    {
                        "beat_number": beat_view.beat_number,
                        "pictograph_data": raw_beat_data["pictograph_data"],
                        "step_label": (
                            self.act_container.beat_scroll.act_beat_frame.beat_step_map[
                                beat_view
                            ].label.text()
                            if beat_view
                            in self.act_container.beat_scroll.act_beat_frame.beat_step_map
                            else ""
                        ),
                    }
                )

            if sequence_data["beats"]:
                sequences.append(sequence_data)

        return sequences

    def _collect_sequence_data(self, start_row):
        """Collect data for a single sequence starting from `start_row`.
        Determines length based on filled beats and collects relevant metadata.
        """
        sequence_data = {
            "sequence_start_marker": True,
            "sequence_length": 0,
            "cue": "",
            "timestamp": "",
            "beats": [],
        }

        total_beats_collected = 0
        current_row = start_row

        # Gather beats while rows are populated
        while current_row < self.act_sheet.DEFAULT_ROWS:
            beat_views = self.act_container.get_beats_in_row(current_row)

            row_filled = any(beat_view.is_populated() for beat_view in beat_views)
            if not row_filled:
                break  # End sequence if the row has no filled beats

            for beat_index, beat_view in enumerate(beat_views):
                if not beat_view.is_populated():
                    continue

                # Collect metadata for each populated beat
                beat_data = {
                    "beat_number": total_beats_collected + 1,
                    "pictograph_data": beat_view.extract_metadata(),
                    "step_label": (
                        self.act_container.beat_scroll.act_beat_frame.beat_step_map[
                            beat_view
                        ].label.text()
                        if beat_view
                        in self.act_container.beat_scroll.act_beat_frame.beat_step_map
                        else ""
                    ),
                }
                sequence_data["beats"].append(beat_data)
                total_beats_collected += 1

            current_row += 1

        # Set sequence length and metadata after collection
        sequence_data["sequence_length"] = total_beats_collected
        cue, timestamp = self.act_container.get_cue_timestamp_for_row(start_row)
        sequence_data["cue"] = cue
        sequence_data["timestamp"] = timestamp

        return sequence_data, total_beats_collected
