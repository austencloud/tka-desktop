import shutil
import os
from typing import TYPE_CHECKING, Any
from PyQt6.QtCore import QSettings, QObject, pyqtSignal
from utils.path_helpers import get_settings_path
from interfaces.settings_manager_interface import ISettingsManager
from .construct_tab_settings import ConstructTabSettings
from .generate_tab_settings import GenerateTabSettings
from .sequence_sharing_settings import SequenceShareSettings
from .act_tab_settings import WriteTabSettings
from .browse_tab_settings import BrowseTabSettings
from .image_export_settings import ImageExportSettings
from .sequence_layout_settings import SequenceLayoutSettings
from .user_profile_settings.user_profile_settings import UserProfileSettings
from .global_settings.global_settings import GlobalSettings
from .visibility_settings.visibility_settings import VisibilitySettings
from .codex_exporter_settings import CodexExporterSettings
from .sequence_card_tab_settings import SequenceCardTabSettings


class LegacySettingsManager(
    QObject
):  # ISettingsManager is a Protocol, no need to inherit
    background_changed = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self._ensure_settings_file_exists()

        # Load settings
        self.settings = QSettings(get_settings_path(), QSettings.Format.IniFormat)

        # Load other settings categories
        self.global_settings = GlobalSettings(self)
        self.image_export = ImageExportSettings(self)
        self.users = UserProfileSettings(self)
        self.visibility = VisibilitySettings(self)
        self.sequence_layout = SequenceLayoutSettings(self)
        self.sequence_share_settings = SequenceShareSettings(self)
        self.codex_exporter = CodexExporterSettings(self)
        self.sequence_card_tab = SequenceCardTabSettings(self)

        # Tabs
        self.construct_tab_settings = ConstructTabSettings(self.settings)
        self.generate_tab_settings = GenerateTabSettings(self.settings)
        self.browse_tab_settings = BrowseTabSettings(self)
        self.write_tab_settings = WriteTabSettings(self)

    def _ensure_settings_file_exists(self):
        """
        Ensure that `settings.ini` exists in the AppData directory. If not, create it
        by copying `default_settings.ini` from the source directory.
        """
        settings_path = get_settings_path()
        default_settings_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "default_settings.ini")
        )

        # Ensure the settings directory exists
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)

        if not os.path.exists(settings_path):
            print("[INFO] No settings.ini found. Creating default settings file...")

            if os.path.exists(default_settings_path):
                try:
                    shutil.copy(default_settings_path, settings_path)
                    print(f"[SUCCESS] Default settings.ini copied to {settings_path}")
                except Exception as e:
                    print(f"[ERROR] Failed to copy default settings.ini: {e}")
            else:
                print(
                    "[ERROR] Default settings.ini is missing. Please ensure it's included in the installation package."
                )

    # ISettingsManager interface implementation
    def get_setting(self, section: str, key: str, default_value: Any = None) -> Any:
        """Get a setting value from the specified section."""
        return self.settings.value(f"{section}/{key}", default_value)

    def set_setting(self, section: str, key: str, value: Any) -> None:
        """Set a setting value in the specified section."""
        self.settings.setValue(f"{section}/{key}", value)

    def get_global_settings(self):
        """Get the global settings object."""
        return self.global_settings

    def get_construct_tab_settings(self):
        """Get the construct tab settings object."""
        return self.construct_tab_settings

    def get_generate_tab_settings(self):
        """Get the generate tab settings object."""
        return self.generate_tab_settings

    @property
    def browse_settings(self):
        """Get the browse tab settings object."""
        return self.browse_tab_settings
