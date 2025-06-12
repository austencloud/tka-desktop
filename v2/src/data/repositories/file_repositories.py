import json
import os
from typing import Dict, Any, Optional
from ...domain.repositories.interfaces import (
    PictographRepository,
    BeatFrameLayoutRepository,
    ArrowPlacementRepository,
    ConfigurationRepository,
)


class JsonFileRepository:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def _load_json(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_json(self, filename: str, data: Dict[str, Any]) -> bool:
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False


class BeatFrameLayoutFileRepository(JsonFileRepository, BeatFrameLayoutRepository):
    def get_layout(self, layout_type: str) -> Dict[str, Any]:
        layouts = self._load_json("beat_frame_layout_options.json")
        return layouts.get(layout_type, {})

    def get_all_layouts(self) -> Dict[str, Dict[str, Any]]:
        return self._load_json("beat_frame_layout_options.json")


class ArrowPlacementFileRepository(JsonFileRepository, ArrowPlacementRepository):
    def get_placement_data(self, pictograph_type: str) -> Dict[str, Any]:
        return self._load_json(f"arrow_placement/{pictograph_type}/placement_data.json")


class ConfigurationFileRepository(JsonFileRepository, ConfigurationRepository):
    def get_default_settings(self) -> Dict[str, Any]:
        return self._load_json("default_layouts.json")

    def update_setting(self, key: str, value: Any) -> bool:
        settings = self.get_default_settings()
        settings[key] = value
        return self._save_json("default_layouts.json", settings)
