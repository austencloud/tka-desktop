from PyQt6.QtCore import QSettings

from utils.path_helpers import get_settings_path


class SettingsProvider:
    _settings = None

    @classmethod
    def get_settings(cls) -> QSettings:
        if cls._settings is None:
            cls._settings = QSettings(
                get_settings_path(),
                QSettings.Format.IniFormat,
            )
        return cls._settings
