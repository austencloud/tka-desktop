# In generate_tab_settings.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


# In GenerateTabSettings class
class GenerateTabSettings:
    SHARED_DEFAULTS = {
        "sequence_length": 16,
        "max_turn_intensity": 1,
        "sequence_level": 1,
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
        "circular": {"rotation_type": "quartered", "permutation_type": "rotated"},
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings

    def get_setting(self, key: str, mode: str = None):
        """Get setting with fallback to unified defaults"""
        if mode and key in self.MODE_SPECIFIC_DEFAULTS.get(mode, {}):
            prefix = f"generator/{mode}/"
            default = self.MODE_SPECIFIC_DEFAULTS[mode].get(key)
        else:
            prefix = "generator/"
            default = self.SHARED_DEFAULTS.get(key)

        return self.settings.value(prefix + key, default)

    def set_setting(self, key: str, value, mode: str = None):
        """Set setting in appropriate section"""
        if mode and key in self.MODE_SPECIFIC_DEFAULTS.get(mode, {}):
            prefix = f"generator/{mode}/"
        else:
            prefix = "generator/"

        self.settings.setValue(prefix + key, value)

    def get_current_mode(self) -> str:
        return self.settings.value(
            "generator/current_mode", "freeform"
        )

    def set_current_mode(self, mode: str):
        self.settings.setValue("generator/current_mode", mode)
