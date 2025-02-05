import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager


class SequenceLayoutSettings:
    LAYOUTS_FILE = Path("data/default_layouts.json")

    def __init__(self, settings_manager: "SettingsManager"):
        self.settings_manager = settings_manager

    def get_layout_setting(self, beat_count: str) -> list[int]:
        """Retrieve layout setting for a specific beat count."""
        layouts = self._load_layouts()
        return layouts.get(beat_count, [1, int(beat_count)])

    def set_layout_setting(self, beat_count: str, layout: list[int]):
        """Update the layout setting for a specific beat count."""
        layouts = self._load_layouts()
        layouts[beat_count] = layout
        self._save_layouts(layouts)

    def _load_layouts(self):
        """Load layouts from JSON."""
        if not self.LAYOUTS_FILE.exists():
            return {}
        with open(self.LAYOUTS_FILE, "r") as file:
            return json.load(file)

    def _save_layouts(self, layouts):
        """Save layouts to JSON with inline lists and readable formatting."""
        with open(self.LAYOUTS_FILE, "w") as file:
            # Generate a JSON string with pre-formatted lists
            formatted_json = json.dumps(layouts, indent=2)
            # Post-process to ensure lists are inline
            formatted_json = (
                formatted_json.replace("[\n    ", "[")
                .replace("\n  ]", "]")
                .replace(",\n    ", ", ")
            )
            file.write(formatted_json)
