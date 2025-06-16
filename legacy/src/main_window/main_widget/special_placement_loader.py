import json
import logging
import os
from typing import TYPE_CHECKING, Any
from data.constants import BOX, DIAMOND
from utils.path_helpers import get_data_path


class SpecialPlacementLoader:
    """Loads special placements for the arrow placement manager."""

    SUBFOLDERS = [
        "from_layer1",
        "from_layer2",
        "from_layer3_blue2_red1",
        "from_layer3_blue1_red2",
    ]
    SUPPORTED_MODES = [DIAMOND, BOX]

    def __init__(self) -> None:
        self.special_placements: dict[str, dict[str, dict]] = {}

    def load_json_data(self, file_path) -> dict[str, dict[dict[str, Any]]]:
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            return {}
        except Exception as e:
            logging.error(f"Error loading JSON data from {file_path}: {e}")
            return {}

    def load_or_return_special_placements(self) -> dict[str, dict[str, dict]]:
        if self.special_placements:
            return self.special_placements
        else:
            return self.load_special_placements_fresh()

    def load_special_placements_fresh(self):
        for mode in self.SUPPORTED_MODES:
            self.special_placements[mode] = self._load_mode_subfolders(mode)
        return self.special_placements

    def reload(self) -> None:
        """Manually clear the cache so that special placements are reloaded on next call."""
        self.special_placements = {}

    def _load_mode_subfolders(self, mode: str) -> dict[str, dict]:
        mode_data: dict[str, dict] = {}
        for subfolder in self.SUBFOLDERS:
            mode_data[subfolder] = {}
            directory = get_data_path(f"arrow_placement/{mode}/special/{subfolder}")
            if not os.path.isdir(directory):
                continue
            for file_name in os.listdir(directory):
                if file_name.endswith("_placements.json"):
                    path = os.path.join(directory, file_name)
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        mode_data[subfolder].update(data)
        return mode_data
