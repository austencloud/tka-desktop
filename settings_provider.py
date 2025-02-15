from PyQt6.QtCore import QSettings

from utilities.path_helpers import get_user_editable_resource_path


class SettingsProvider:
    _settings = None

    @classmethod
    def get_settings(cls) -> QSettings:
        if cls._settings is None:
            cls._settings = QSettings(
                get_user_editable_resource_path("settings.ini"),
                QSettings.Format.IniFormat,
            )
        return cls._settings
