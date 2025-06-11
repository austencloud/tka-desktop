from pathlib import Path
from typing import Dict, Any, Optional
import json
import os


class Config:
    DEFAULT_SETTINGS = {
        "theme": "dark",
        "auto_start": False,
        "minimize_to_tray": True,
        "check_updates": True,
        "console_max_lines": 1000,
        "grid_view_columns": 3,
        "compact_view_columns": 4,
        "window_geometry": None,
        "shortcuts": {"show_hide": "Ctrl+Space", "search": "Ctrl+F"},
    }

    def __init__(self):
        self.config_file = Path("launcher_config.json")
        self.favorites_file = Path("launcher_favorites.json")
        self._settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    loaded = json.load(f)
                    return {**self.DEFAULT_SETTINGS, **loaded}
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return self.DEFAULT_SETTINGS.copy()

    def save_settings(self) -> None:
        with open(self.config_file, "w") as f:
            json.dump(self._settings, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value
        self.save_settings()

    @property
    def theme(self) -> str:
        return self.get("theme", "dark")

    @property
    def grid_columns(self) -> int:
        return self.get("grid_view_columns", 3)


class Paths:
    ROOT = Path.cwd()
    V1_ROOT = ROOT / "the-kinetic-constructor-desktop-v1"
    V2_ROOT = ROOT / "the-kinetic-constructor-desktop-v2"
    V1_MAIN = V1_ROOT / "src" / "main.py"
    V2_DEMO = V2_ROOT / "demo_new_architecture.py"
    CACHE_DIR = ROOT / "cache"
    LOGS_DIR = ROOT / "logs"
