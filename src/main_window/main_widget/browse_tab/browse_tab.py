from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer

from main_window.main_widget.browse_tab.browse_tab_filter_controller import (
    BrowseTabFilterController,
)
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from settings_manager.global_settings.app_context import AppContext

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

        self.browse_settings = AppContext.settings_manager().browse_settings
        self.metadata_extractor = MetaDataExtractor()

        self.ui_updater = BrowseTabUIUpdater(self)

        self.filter_manager = BrowseTabFilterManager(self)
        self.filter_controller = BrowseTabFilterController(self)
        self.sequence_picker = SequencePicker(self)

        self.sequence_viewer = SequenceViewer(self)

        self.deletion_handler = BrowseTabDeletionHandler(self)
        self.selection_handler = BrowseTabSelectionManager(self)
        self.get = BrowseTabGetter(self)

        QTimer.singleShot(0, self._apply_saved_browse_state)

    def _apply_saved_browse_state(self):
        left_index = self.browse_settings.get_browse_left_stack_index()
        self.main_widget.left_stack.setCurrentIndex(left_index)

        section_name = self.browse_settings.get_current_section()
        if not section_name or section_name == "":
            self.sequence_picker.filter_stack.show_filter_choice_widget()
        else:
            self.sequence_picker.filter_stack.show_section(section_name)

        filter_criteria = self.browse_settings.get_current_filter()
        if filter_criteria:
            self.filter_controller.apply_filter(filter_criteria)

        selected_seq = self.browse_settings.get_selected_sequence()
        if selected_seq:
            word = selected_seq.get("word")
            var_index = selected_seq.get("variation_index", 0)

            from PyQt6.QtCore import QTimer

            QTimer.singleShot(1000, lambda: self._reopen_sequence(word, var_index))

    def _reopen_sequence(self, word: str, var_index: int):
        if word in self.sequence_picker.scroll_widget.thumbnail_boxes:
            box = self.sequence_picker.scroll_widget.thumbnail_boxes[word]
            if 0 <= var_index < len(box.state.thumbnails):
                box.state.current_index = var_index
                metadata = self.metadata_extractor.extract_metadata_from_file(
                    box.state.thumbnails[var_index]
                )
                self.selection_handler.on_box_thumbnail_clicked(
                    box.image_label, metadata
                )

    def resize_thumbnail_boxes(self):
        for tb in self.sequence_picker.scroll_widget.thumbnail_boxes.values():
            tb.resize_thumbnail_box()
