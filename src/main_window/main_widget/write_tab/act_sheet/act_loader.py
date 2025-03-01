import json
import os
from typing import TYPE_CHECKING
from utils.path_helpers import get_user_editable_resource_path

if TYPE_CHECKING:
    from .act_sheet import ActSheet


class ActLoader:
    default_act = {"title": "Act", "prop_type": "Staff", "sequences": []}

    def __init__(self, act_sheet: "ActSheet") -> None:
        self.act_sheet = act_sheet
        self.load_act()

    def load_act(self, filename="json/current_act.json") -> None:
        """Load an act from a JSON file in the acts directory."""
        file_path = get_user_editable_resource_path(filename)
        if not os.path.isfile(file_path):
            # print(f"No saved act found at {file_path}")
            self.populate_act_from_data(self.default_act)
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                act_data = json.load(f)
                self.populate_act_from_data(act_data)
        except json.JSONDecodeError:
            print(
                f"Error decoding JSON from {file_path}, populating with default data."
            )

            self.populate_act_from_data(self.default_act)

    def populate_act_from_data(self, act_data):
        """Populate the act based on saved data, using sequence length to determine row spans."""
        beat_frame = self.act_sheet.act_container.beat_scroll.act_beat_frame

        current_row = 0  # Track the current row across sequences

        for sequence in act_data["sequences"]:
            sequence_length = sequence.get("sequence_length", 8)
            beats = sequence["beats"]

            # Calculate the number of rows needed to fit this sequence
            num_rows = (
                sequence_length + self.act_sheet.DEFAULT_COLUMNS - 1
            ) // self.act_sheet.DEFAULT_COLUMNS

            # Populate rows with beats for this sequence, adjusting `current_row` as needed
            for row_index in range(num_rows):
                start_idx = row_index * self.act_sheet.DEFAULT_COLUMNS
                end_idx = start_idx + self.act_sheet.DEFAULT_COLUMNS
                beat_data = beats[start_idx:end_idx]

                # Populate each row with the sliced beats, incrementing `current_row` for each row
                beat_frame.populator.populate_row_beats(current_row, beat_data)
                current_row += 1  # Move to the next row for the next part of the sequence or next sequence
