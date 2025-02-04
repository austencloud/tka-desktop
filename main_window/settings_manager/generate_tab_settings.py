from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class GenerateTabSettings:
    DEFAULT_FREEFORM_SETTINGS = {
        "sequence_type": "freeform",
        "sequence_length": 16,
        "max_turn_intensity": 1,
        "sequence_level": 1,
        "continuous_rotation": False,
        "overwrite_sequence": False,
    }

    DEFAULT_CIRCULAR_SETTINGS = {
        "sequence_type": "circular",
        "sequence_length": 16,
        "max_turn_intensity": 1,
        "sequence_level": 1,
        "rotation_type": "quartered",
        "permutation_type": "rotated",
        "continuous_rotation": False,
        "overwrite_sequence": False,
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_sequence_generator_setting(self, key: str, builder_type: str):
        """Retrieve a setting for a specific builder type."""
        prefix = f"builder/sequence_generator/{builder_type}_sequence_generator/"
        default = (
            self.DEFAULT_FREEFORM_SETTINGS.get(key)
            if builder_type == "freeform"
            else self.DEFAULT_CIRCULAR_SETTINGS.get(key)
        )
        return self.settings.value(prefix + key, default)

    def set_sequence_generator_setting(self, key: str, value, builder_type: str):
        """Set a setting for a specific builder type."""
        prefix = f"builder/sequence_generator/{builder_type}_sequence_generator/"
        self.settings.setValue(prefix + key, value)

    def get_current_sequence_generator(self) -> str:
        return self.settings.value(
            "builder/sequence_generator/current_sequence_generator", "circular"
        )

    def update_current_sequence_generator(self, builder_type: str):
        self.settings.setValue(
            "builder/sequence_generator/current_sequence_generator", builder_type
        )
