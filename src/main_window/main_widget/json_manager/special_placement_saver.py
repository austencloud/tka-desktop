import json
import logging
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class SpecialPlacementSaver:

    def save_json_data(self, data, file_path) -> None:
        """Write JSON data to a file with specific formatting."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(data, indent=2, ensure_ascii=False)
                formatted_json_str = re.sub(
                    r"\[\s+(-?\d+(?:\.\d+)?),\s+(-?\d+(?:\.\d+)?)\s+\]", r"[\1, \2]", formatted_json_str
                )
                file.write(formatted_json_str)
        except IOError as e:
            logging.error(f"Failed to write to {file_path}: {e}")

