# In generate_tab_settings.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSettings

from main_window.main_widget.generate_tab.circular.CAP_type import CAPType


# In GenerateTabSettings class
class GenerateTabSettings:
    SHARED_DEFAULTS = {
        "sequence_length": 16,
        "turn_intensity": 1,
        "level": 1,
        "prop_continuity": "continuous",
        "CAP_type": "strict_rotated",
    }

    def __init__(self, settings: QSettings):
        self.settings = settings

    def get_setting(self, key: str):
        """Get setting with proper fallback logic."""
        return self.settings.value(f"generator/{key}", self.SHARED_DEFAULTS.get(key))

    def set_setting(self, key: str, value):
        """Set setting in appropriate section"""

        prefix = "generator/"
        self.settings.setValue(prefix + key, value)

    def get_current_mode(self) -> str:
        return self.settings.value("generator/current_mode", "freeform")

    def set_current_mode(self, mode: str):
        self.settings.setValue("generator/current_mode", mode)

    def get_CAP_type(self) -> str:
        return CAPType.from_str(self.get_setting("CAP_type"))
