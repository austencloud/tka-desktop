import shutil
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSettings, QObject, pyqtSignal
from utils.path_helpers import get_settings_path
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

if TYPE_CHECKING:
    pass


import os
from PyQt6.QtCore import QSettings, QObject, pyqtSignal


class SettingsManager(QObject):
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

        # Tabs
        self.construct_tab_settings = ConstructTabSettings(self.settings)
        self.generate_tab_settings = GenerateTabSettings(self.settings)
        self.browse_settings = BrowseTabSettings(self)
        self.write_tab_settings = WriteTabSettings(self)

    def _ensure_settings_file_exists(self):
        """
        Ensure that `settings.ini` exists in the AppData directory. If not, create it
        by copying `default_settings.ini` from the source directory.
        """
        settings_path = get_settings_path()
        default_settings_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "src\\data\\default_settings.ini"
            )
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
