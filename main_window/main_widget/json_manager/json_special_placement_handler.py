import json
import logging
import os
import re
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    pass


class JsonSpecialPlacementHandler:
    
    def load_json_data(self, file_path) -> dict[str, dict[dict[str, Any]]]:
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            return {}
        except Exception as e:
            logging.error(f"Error loading JSON data from {file_path}: {e}")
            return {}

    def write_json_data(self, data, file_path) -> None:
        """Write JSON data to a file with specific formatting."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(data, indent=2, ensure_ascii=False)
                formatted_json_str = re.sub(
                    r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", formatted_json_str
                )
                file.write(formatted_json_str)
        except IOError as e:
            logging.error(f"Failed to write to {file_path}: {e}")
