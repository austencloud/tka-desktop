from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget


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
        self.settings = self.main_widget.main_window.settings_manager.browse_settings

        self.filter_manager = BrowseTabFilterManager(self)
        # Components
        self.sequence_picker = SequencePicker(self)
        self.sequence_viewer = SequenceViewer(self)

        # Managers
        self.deletion_handler = BrowseTabDeletionHandler(self)
        self.selection_handler = BrowseTabSelectionManager(self)
        self.get = BrowseTabGetter(self)
        self.ui_updater = BrowseTabUIUpdater(self)
