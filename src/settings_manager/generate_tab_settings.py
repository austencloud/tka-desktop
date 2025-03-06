# In generate_tab_settings.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSettings

if TYPE_CHECKING:
    pass


# In GenerateTabSettings class
class GenerateTabSettings:
    SHARED_DEFAULTS = {
        "sequence_length": 16,
        "max_turn_intensity": 1,
        "level": 1,
        "prop_continuity": False,
        "overwrite_sequence": False,
    }

    MODE_SPECIFIC_DEFAULTS = {
        "freeform": {
            "selected_letter_types": [
                "Dual-Shift",
                "Shift",
                "Cross-Shift",
                "Dash",
                "Dual-Dash",
                "Static",
            ]
        },
        "circular": {"rotation_type": "quartered", "CAP_type": "rotated"},
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
