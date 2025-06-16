import json
import logging
import re
from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.data_updater.placement_data_cleaner import (
    PlacementDataCleaner,
)


class SpecialPlacementSaver:

    def save_json_data(self, data, file_path) -> None:
        """Write JSON data to a file with specific formatting."""
        data = PlacementDataCleaner.clean_placement_data(data)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(data, indent=2, ensure_ascii=False)
                formatted_json_str = re.sub(
                    r"\[\s+(-?\d+(?:\.\d+)?),\s+(-?\d+(?:\.\d+)?)\s+\]",
                    r"[\1, \2]",
                    formatted_json_str,
                )
                file.write(formatted_json_str)
        except IOError as e:
            logging.error(f"Failed to write to {file_path}: {e}")
