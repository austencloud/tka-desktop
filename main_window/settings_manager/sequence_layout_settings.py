# main_window/settings_manager/sequence_layout_settings.py
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager


class SequenceLayoutSettings:
    def __init__(self, settings_manager: "SettingsManager"):
        self.settings_manager = settings_manager
        self.settings = settings_manager.settings

    def get_layout_setting(self, beat_count: str) -> list[int]:
        layouts = self._load_layouts()
        default_value = layouts.get(beat_count, [1, int(beat_count)])  # Default to 1 column if unknown.

        override_str = self.settings.value(f"sequence_layout/overrides/{beat_count}", "")

        if override_str:
            try:
                return list(map(int, override_str.split(",")))
            except ValueError:
                pass  # Ignore invalid user settings.

        return default_value


    def set_layout_setting(self, beat_count: str, layout: list[int]):
        override_str = ",".join(map(str, layout))
        self.settings.setValue(f"sequence_layout/overrides/{beat_count}", override_str)

    def _load_layouts(self) -> dict:
        raw_val = self.settings.value("sequence_layout/default_layouts", "")

        if not raw_val:
            # load the values from the json file
            with open("data/default_layouts.json", "r") as file:
                layouts = json.load(file)
                return layouts
            

        if isinstance(raw_val, dict):
            return raw_val  # If it's already a dict, return it directly.

        try:
            return json.loads(raw_val)  # Convert string back to dictionary.
        except (ValueError, TypeError):
            return {}

    def _save_layouts(self, layouts: dict) -> None:
        json_str = json.dumps(layouts, indent=2)

        json_str = (
            json_str.replace("[\n    ", "[")
            .replace("\n  ]", "]")
            .replace(",\n    ", ", ")
        )

        self.settings.setValue("sequence_layout/default_layouts", json_str)
