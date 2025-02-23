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
        default_value = layouts.get(beat_count, [1, int(beat_count)])

        override_str = self.settings.value(
            f"sequence_layout/overrides/{beat_count}", ""
        )
        if override_str:
            try:
                row_col = list(map(int, override_str.split(",")))
                return row_col
            except:
                pass

        return default_value

    def set_layout_setting(self, beat_count: str, layout: list[int]):
        override_str = ",".join(map(str, layout))
        self.settings.setValue(f"sequence_layout/overrides/{beat_count}", override_str)

    def _load_layouts(self) -> dict:
        raw_val = self.settings.value("sequence_layout/default_layouts", "")

        if not raw_val:
            return {}

        if isinstance(raw_val, dict):
            json_str = json.dumps(raw_val)
            self.settings.setValue("sequence_layout/default_layouts", json_str)
            return raw_val

        try:
            return json.loads(raw_val)
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
