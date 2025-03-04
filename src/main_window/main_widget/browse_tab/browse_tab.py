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
from PyQt6.QtCore import QTimer


class BrowseTab(QWidget):

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.initialized = False
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
        section_name = self.browse_settings.get_current_section()
        if not section_name or section_name == "":
            self.sequence_picker.filter_stack.show_filter_choice_widget()
        else:
            self.sequence_picker.filter_stack.show_section(section_name)

        filter_criteria = self.browse_settings.get_current_filter()
        if not self.initialized:
            selected_seq = self.browse_settings.get_selected_sequence()
            if selected_seq:
                word = selected_seq.get("word")
                var_index = selected_seq.get("variation_index", 0)
            self.reopen_thumbnail(word, var_index)
        if filter_criteria:
            self.filter_controller.apply_filter(filter_criteria, fade=False)
        self.initialized = True

    def reopen_thumbnail(self, word: str, var_index: int):
        if word in self.sequence_picker.scroll_widget.thumbnail_boxes:
            box = self.sequence_picker.scroll_widget.thumbnail_boxes[word]
            if 0 <= var_index < len(box.state.thumbnails):
                box.state.current_index = var_index
                selected_thumbnail = box.state.thumbnails[var_index]
                metadata = self.metadata_extractor.extract_metadata_from_file(
                    selected_thumbnail
                )
                self.selection_handler.on_thumbnail_clicked(box.image_label, metadata)
                return

        print(
            f"[INFO] '{word}' not found in the current filter. Searching full dictionary..."
        )

        dictionary_words = self.get.base_words()
        matching_entry = next(
            (entry for entry in dictionary_words if entry[0] == word), None
        )
        if matching_entry:
            thumbnails = matching_entry[1]

            if thumbnails:
                var_index = max(0, min(var_index, len(thumbnails) - 1))
                selected_thumbnail = thumbnails[var_index]

                self.sequence_viewer.update_thumbnails(thumbnails)
                self.sequence_viewer.update_preview(var_index)
                self.sequence_viewer.update_nav_buttons()
                self.sequence_viewer.word_label.update_word_label(word)
                self.sequence_viewer.variation_number_label.update_index(var_index)

                self.set_current_thumbnail_box(word)

                print(
                    f"[SUCCESS] Loaded missing sequence: {word} (variation {var_index})"
                )
                return

        print(f"[ERROR] Could not find sequence '{word}' in the dictionary.")

    def set_current_thumbnail_box(self, word):
        thumbnail_boxes = self.sequence_picker.scroll_widget.thumbnail_boxes
        if not thumbnail_boxes:
            return
        for box in thumbnail_boxes.values():
            if box.word == word:
                self.sequence_viewer.current_thumbnail_box = box
                index = self.sequence_viewer.state.current_index
                box.nav_buttons_widget.update_thumbnail(index)
                return
