# settings_manager/image_export_settings.py
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

    def get_image_export_setting(self, key: str):
        """Get a specific image export setting"""
        value = self.settings.value(f"image_export/{key}")
        
        # Convert string values from QSettings to proper types
        if value == "true":
            return True
        elif value == "false":
            return False
        elif value is None:
            return self.DEFAULT_IMAGE_EXPORT_SETTINGS.get(key, False)
        return value

    def set_image_export_setting(self, key: str, value: bool):
        """Set a specific image export setting"""
        self.settings.setValue(f"image_export/{key}", value)
        self.settings.sync()  # Ensure changes are saved immediately

    def get_all_settings(self) -> dict:
        """Get all image export settings"""
        return {
            key: self.get_image_export_setting(key)
            for key in self.DEFAULT_IMAGE_EXPORT_SETTINGS.keys()
        }