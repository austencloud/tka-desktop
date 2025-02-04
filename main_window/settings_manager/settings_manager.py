from typing import TYPE_CHECKING
from PyQt6.QtCore import QSettings, QObject, pyqtSignal

from main_window.settings_manager.construct_tab_settings import ConstructTabSettings
from main_window.settings_manager.generate_tab_settings import GenerateTabSettings
from .sequence_sharing_settings import SequenceShareSettings
from .act_tab_settings import WriteTabSettings
from .dictionary_settings import BrowseTabSettings
from .image_export_settings import ImageExportSettings
from .sequence_layout_settings import SequenceLayoutSettings
from .user_profile_settings.user_profile_settings import UserProfileSettings
from .global_settings.global_settings import GlobalSettings
from .visibility_settings.visibility_settings import VisibilitySettings

if TYPE_CHECKING:
    from main_window.main_window import MainWindow


class SettingsManager(QObject):
    background_changed = pyqtSignal(str)

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        self.main_window = main_window
        self.settings = QSettings("settings.ini", QSettings.Format.IniFormat)

        self.global_settings = GlobalSettings(self)
        
        if self.main_window:
            self.image_export = ImageExportSettings(self)
            self.users = UserProfileSettings(self)
            self.visibility = VisibilitySettings(self)
            self.sequence_layout = SequenceLayoutSettings(self)
            self.sequence_share_settings = SequenceShareSettings(self)

            # Tabs
            self.construct_tab_settings = ConstructTabSettings(self)
            self.generate_tab_settings = GenerateTabSettings(self)
            self.browse_settings = BrowseTabSettings(self)
            self.write_tab_settings = WriteTabSettings(self)
