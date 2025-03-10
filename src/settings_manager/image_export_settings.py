from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class ImageExportSettings:
    DEFAULT_IMAGE_EXPORT_SETTINGS = {
        "include_start_position": False,
        "add_user_info": True,
        "add_word": True,
        "add_difficulty_level": True,
        "add_beat_numbers": True,
        "add_reversal_symbols": True,
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_image_export_setting(self, key: str):
        """Get a specific image export setting."""
        value = self.settings.value(f"image_export/{key}")
        if value is None:
            return self.DEFAULT_IMAGE_EXPORT_SETTINGS.get(key, False)
        return value.lower() == "true"

    def set_image_export_setting(self, key: str, value: bool):
        """Set a specific image export setting."""
        self.settings.setValue(f"image_export/{key}", str(value).lower())
        self.settings.sync()

    def get_all_image_export_options(self) -> dict:
        """Get all image export settings as a dictionary."""
        return {
            key: self.get_image_export_setting(key)
            for key in self.DEFAULT_IMAGE_EXPORT_SETTINGS.keys()
        }

    def get_custom_note(self) -> str:
        """Get the current custom note."""
        return self.settings.value("image_export/custom_note", "", type=str)

    def set_custom_note(self, note: str) -> None:
        """Set the custom note."""
        self.settings.setValue("image_export/custom_note", note)
