from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class ImageExportSettings:
    DEFAULT_IMAGE_EXPORT_SETTINGS = {
        "include_start_position": False,
        "add_info": True,
        "open_directory_on_export": True,
        "add_word": True,
        "add_difficulty_level": True,
        "add_beat_numbers": True,
        "add_reversal_symbols": True,
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_image_export_setting(self, key):
        # Retrieve the setting value or default to the dictionary's default value
        setting = self.settings.value(
            f"image_export/{key}", self.DEFAULT_IMAGE_EXPORT_SETTINGS.get(key)
        )
        if setting == "false":
            setting = False
        elif setting == "true":
            setting = True
        return setting

    def set_image_export_setting(self, key, value):
        # Set the value in QSettings
        self.settings.setValue(f"image_export/{key}", value)
