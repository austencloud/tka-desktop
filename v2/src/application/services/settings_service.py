import json
import os
from typing import Any, Dict
from PyQt6.QtCore import QSettings

from ...core.interfaces.settings_interfaces import ISettingsService


class SettingsService(ISettingsService):
    def __init__(self, app_name: str = "KineticConstructorV2"):
        self.settings = QSettings(app_name, "Settings")
        self._cache: Dict[str, Any] = {}
        self._load_cache()

    def _load_cache(self):
        """Load all settings into cache for performance"""
        for key in self.settings.allKeys():
            self._cache[key] = self.settings.value(key)

    def get_setting(self, key: str, default: Any = None) -> Any:
        if key in self._cache:
            return self._cache[key]

        value = self.settings.value(key, default)
        self._cache[key] = value
        return value

    def set_setting(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self.settings.setValue(key, value)

    def get_all_settings(self) -> Dict[str, Any]:
        return self._cache.copy()

    def save_settings(self) -> None:
        self.settings.sync()
