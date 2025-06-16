import json
from typing import TYPE_CHECKING

from utils.path_helpers import get_user_editable_resource_path

if TYPE_CHECKING:
    from .act_sheet import ActSheet


class ActSaver:
    def __init__(self, act_sheet: "ActSheet"):
        self.act_sheet = act_sheet

    def save_act(self, filename="current_act.json"):
        """Save the current act to a JSON file in the acts directory."""
        sequences = self.act_sheet.sequence_collector.collect_sequences()

        prop_type = self.act_sheet.write_tab.main_widget.prop_type.name
        title = self.act_sheet.act_header.get_title()

        sequences = {
            "title": title,
            "prop_type": prop_type,
            "sequences": sequences,
        }

        file_path = get_user_editable_resource_path(filename)

        with open(file_path, "w") as f:
            json.dump(sequences, f, indent=4)
