from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.browse_tab.browse_tab_filter_controller import (
    BrowseTabFilterController,
)
from main_window.settings_manager.global_settings.app_context import AppContext


from .sequence_picker.sequence_picker import SequencePicker
from .browse_tab_filter_manager import BrowseTabFilterManager
from .browse_tab_getter import BrowseTabGetter
from .browse_tab_ui_updater import BrowseTabUIUpdater
from .deletion_handler.browse_tab_deletion_handler import BrowseTabDeletionHandler
from .browse_tab_selection_handler import BrowseTabSelectionManager
from .sequence_viewer.sequence_viewer import SequenceViewer

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BrowseTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_widget.splash.updater.update_progress("BrowseTab")

        self.settings_manager = AppContext.settings_manager().browse_settings
        self.ui_updater = BrowseTabUIUpdater(self)

        # Refactored Filtering Components
        self.filter_manager = BrowseTabFilterManager(self)
        self.filter_controller = BrowseTabFilterController(self)
        self.sequence_picker = SequencePicker(self)

        # Components
        self.sequence_viewer = SequenceViewer(self)

        # Managers
        self.deletion_handler = BrowseTabDeletionHandler(self)
        self.selection_handler = BrowseTabSelectionManager(self)
        self.get = BrowseTabGetter(self)
