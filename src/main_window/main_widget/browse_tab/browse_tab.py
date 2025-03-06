from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer

from main_window.main_widget.browse_tab.browse_tab_filter_controller import (
    BrowseTabFilterController,
)
from main_window.main_widget.browse_tab.browse_tab_persistence_manager import (
    BrowseTabPersistenceManager,
)
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from settings_manager.global_settings.app_context import AppContext

from .sequence_picker.sequence_picker import SequencePicker
from .browse_tab_filter_manager import BrowseTabFilterManager
from .browse_tab_getter import BrowseTabGetter
from .browse_tab_ui_updater import BrowseTabUIUpdater
from .deletion_handler.browse_tab_deletion_handler import BrowseTabDeletionHandler
from .browse_tab_selection_handler import BrowseTabSelectionHandler
from .sequence_viewer.sequence_viewer import SequenceViewer
from .browse_tab_state import BrowseTabState

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BrowseTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_widget.splash.updater.update_progress("BrowseTab")

        self.browse_settings = AppContext.settings_manager().browse_settings
        self.state = BrowseTabState(self.browse_settings)
        self.metadata_extractor = MetaDataExtractor()

        self.ui_updater = BrowseTabUIUpdater(self)

        self.filter_manager = BrowseTabFilterManager(self)
        self.filter_controller = BrowseTabFilterController(self)

        self.sequence_picker = SequencePicker(self)
        self.sequence_viewer = SequenceViewer(self)

        self.deletion_handler = BrowseTabDeletionHandler(self)
        self.selection_handler = BrowseTabSelectionHandler(self)
        self.get = BrowseTabGetter(self)

        self.persistence_manager = BrowseTabPersistenceManager(self)

        QTimer.singleShot(0, self.persistence_manager.apply_saved_browse_state)
