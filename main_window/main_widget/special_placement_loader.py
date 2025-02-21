import json
import os
from typing import TYPE_CHECKING
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SpecialPlacementLoader:
    """Loads special placements for the arrow placement manager."""
    SUBFOLDERS = [
        "from_layer1",
        "from_layer2",
        "from_layer3_blue2_red1",
        "from_layer3_blue1_red2",
    ]
    SUPPORTED_MODES = ["diamond", "box"]

    def __init__(self) -> None:
        self.special_placements: dict[str, dict[str, dict]] = {}

    def load_special_placements(self) -> dict[str, dict[str, dict]]:
        # If we've already loaded everything, just return it!
        if self.special_placements:
            return self.special_placements

        for mode in self.SUPPORTED_MODES:
            self.special_placements[mode] = self._load_mode_subfolders(mode)
        return self.special_placements

    def _load_mode_subfolders(self, mode: str) -> dict[str, dict]:
        mode_data: dict[str, dict] = {}
        for subfolder in self.SUBFOLDERS:
            mode_data[subfolder] = {}
            directory = get_images_and_data_path(
                f"data/arrow_placement/{mode}/special/{subfolder}"
            )
            if not os.path.isdir(directory):
                continue
            for file_name in os.listdir(directory):
                if file_name.endswith("_placements.json"):
                    path = os.path.join(directory, file_name)
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        mode_data[subfolder].update(data)
        return mode_data
