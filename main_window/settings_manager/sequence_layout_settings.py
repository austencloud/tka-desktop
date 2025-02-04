from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class SequenceLayoutSettings:
    DEFAULT_LAYOUT_SETTINGS = {
        "grow_sequence": True,
        "num_beats": 16,
        "layout_option": "4 x 4",
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_layout_setting(self, key: str):
        return self.settings.value(
            f"sequence_layout/{key}", self.DEFAULT_LAYOUT_SETTINGS.get(key)
        )

    def set_layout_setting(self, key: str, value):
        self.settings.setValue(f"sequence_layout/{key}", value)
