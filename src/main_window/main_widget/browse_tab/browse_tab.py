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
from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager

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
    def __init__(
        self,
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager,
    ) -> None:
        # Debug: Log the very start of browse tab creation
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🚀 BrowseTab.__init__ called!")
        logger.info(f"main_widget: {main_widget}")
        logger.info(f"settings_manager: {settings_manager}")
        logger.info(f"json_manager: {json_manager}")

        super().__init__()
        logger.info("✅ super().__init__() completed")

        self.main_widget = main_widget
        logger.info("✅ main_widget assigned")

        self.main_widget.splash_screen.updater.update_progress("BrowseTab")
        logger.info("✅ splash screen updated")

        self.settings_manager = settings_manager
        self.json_manager = json_manager
        self.browse_settings = settings_manager.browse_settings
        self.state = BrowseTabState(self.browse_settings)
        self.metadata_extractor = MetaDataExtractor()

        self.ui_updater = BrowseTabUIUpdater(self)

        self.filter_manager = BrowseTabFilterManager(self)
        self.filter_controller = BrowseTabFilterController(self)

        # Debug: Log sequence picker creation
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🎯 Creating SequencePicker in BrowseTab...")

        self.sequence_picker = SequencePicker(self)
        logger.info(f"✅ SequencePicker created: {self.sequence_picker}")

        logger.info("🎯 Creating SequenceViewer in BrowseTab...")
        self.sequence_viewer = SequenceViewer(self)
        logger.info(f"✅ SequenceViewer created: {self.sequence_viewer}")

        self._setup_browse_tab_layout()

        self.deletion_handler = BrowseTabDeletionHandler(self)
        self.selection_handler = BrowseTabSelectionHandler(self)
        self.get = BrowseTabGetter(self)

        self.persistence_manager = BrowseTabPersistenceManager(self)
        QTimer.singleShot(0, self.persistence_manager.apply_saved_browse_state)

    def _setup_browse_tab_layout(self):
        from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget

        # ARCHITECTURAL FIX: Create internal stack for filter_stack and sequence_picker
        # This eliminates the need for main widget to manage browse tab internals
        self.internal_left_stack = QStackedWidget()
        self.internal_left_stack.addWidget(
            self.sequence_picker.filter_stack
        )  # 0 - Filter selection
        self.internal_left_stack.addWidget(
            self.sequence_picker
        )  # 1 - Sequence list with control panel

        # Start with filter stack visible (filter selection mode)
        self.internal_left_stack.setCurrentIndex(0)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(
            self.internal_left_stack, 2
        )  # 2/3 width (66.7%) - Internal stack instead of sequence_picker
        layout.addWidget(self.sequence_viewer, 1)  # 1/3 width (33.3%)

        self.setLayout(layout)
