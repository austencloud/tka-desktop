from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager


class ImageExportSettings:
    DEFAULT_IMAGE_EXPORT_SETTINGS = {
        "include_start_position": False,
        "add_user_info": True,
        "add_word": True,
        "add_difficulty_level": True,
        "add_beat_numbers": True,
        "add_reversal_symbols": True,
        "use_last_save_directory": False,
        "combined_grids": False,
    }

    def __init__(self, settings_manager: "LegacySettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_image_export_setting(self, key: str):
        """Get a specific image export setting."""
        value = self.settings.value(f"image_export/{key}")
        if value is None:
            default_value = self.DEFAULT_IMAGE_EXPORT_SETTINGS.get(key, False)
            return default_value
        result = value.lower() == "true"
        return result

    def set_image_export_setting(self, key: str, value: bool):
        """Set a specific image export setting."""
        self.settings.setValue(f"image_export/{key}", str(value).lower())
        self.settings.sync()
        # Verify the setting was saved
        saved_value = self.settings.value(f"image_export/{key}")

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

    def get_last_save_directory(self) -> str:
        """Get the last directory used for saving images."""
        # Force sync the settings before reading
        self.settings.sync()

        last_dir = self.settings.value("image_export/last_save_directory", "", type=str)
        print(f"Getting last save directory: {last_dir}")
        return last_dir

    def set_last_save_directory(self, directory: str) -> None:
        """Set the last directory used for saving images."""
        print(f"Setting last save directory to: {directory}")
        self.settings.setValue("image_export/last_save_directory", directory)
        self.settings.sync()
        # Verify the setting was saved
        saved_value = self.settings.value("image_export/last_save_directory", "")
        print(f"After setting, last save directory is: {saved_value}")
