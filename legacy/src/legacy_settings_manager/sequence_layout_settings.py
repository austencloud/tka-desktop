import json
import os
from typing import TYPE_CHECKING

from utils.path_helpers import get_data_path

if TYPE_CHECKING:
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager

OVERRIDES_FILE = get_data_path("beat_layout_overrides.json")


class SequenceLayoutSettings:
    def __init__(self, settings_manager: "LegacySettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = settings_manager.settings

    def get_layout_setting(self, beat_count: str) -> list[int]:
        layouts = self._load_layouts()
        default_value = layouts.get(beat_count, [1, int(beat_count)])

        overrides = self._load_overrides()
        return overrides.get(str(beat_count), default_value)

    def set_layout_setting(self, beat_count: str, layout: list[int]):
        overrides = self._load_overrides()
        overrides[str(beat_count)] = layout
        self._save_overrides(overrides)

    def _load_layouts(self) -> dict:
        raw_val = self.settings.value("sequence_layout/default_layouts", "")

        if not raw_val:
            try:
                with open((get_data_path("default_layouts.json")), "r") as file:
                    return json.load(file)
            except FileNotFoundError:
                return {}

        if isinstance(raw_val, dict):
            return raw_val

        try:
            return json.loads(raw_val)
        except (ValueError, TypeError):
            return {}

    def _load_overrides(self) -> dict:
        if not os.path.exists(OVERRIDES_FILE):
            return {}

        try:
            with open(OVERRIDES_FILE, "r") as file:
                content = file.read().strip()  # Strip whitespace and newlines

                if not content:
                    return {}  # Empty file, return an empty dictionary

                try:
                    return json.loads(content)  # Parse JSON from string instead of file
                except json.JSONDecodeError:
                    print(
                        f"⚠️ Warning: `beat_layout_overrides.json` contains invalid JSON. Resetting file."
                    )
                    return {}

        except FileNotFoundError:
            return {}

    def _save_overrides(self, overrides: dict):
        """Save overrides to `beat_layout_overrides.json` with inline lists formatting."""
        os.makedirs(os.path.dirname(OVERRIDES_FILE), exist_ok=True)

        class InlineListEncoder(json.JSONEncoder):
            def encode(self, obj):
                if isinstance(obj, dict):
                    formatted_items = []
                    for key, value in obj.items():
                        # Force inline lists while keeping dict indentation
                        if isinstance(value, list):
                            formatted_value = "[" + ", ".join(map(str, value)) + "]"
                        else:
                            formatted_value = json.dumps(value)

                        formatted_items.append(f'  "{key}": {formatted_value}')
                    return "{\n" + ",\n".join(formatted_items) + "\n}"
                return super().encode(obj)

        formatted_json = json.dumps(overrides, cls=InlineListEncoder, indent=2)

        with open(OVERRIDES_FILE, "w") as file:
            file.write(formatted_json + "\n")  # Write manually to ensure formatting

    def set_num_beats(self, new_length: int):
        self.settings.setValue("sequence_layout/num_beats", new_length)

    def get_num_beats(self):
        return self.settings.value("sequence_layout/num_beats", 8)
