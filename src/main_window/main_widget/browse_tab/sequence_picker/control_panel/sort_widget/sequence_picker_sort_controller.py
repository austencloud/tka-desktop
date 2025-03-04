from typing import TYPE_CHECKING

from settings_manager.global_settings.app_context import AppContext
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ...sequence_picker import SequencePicker


class SequencePickerSortController:
    """Handles sorting logic for the Sequence Picker."""

    def __init__(self, sequence_picker: "SequencePicker"):
        self.sequence_picker = sequence_picker
        self.browse_tab = sequence_picker.browse_tab
        self.settings_manager = AppContext.settings_manager()

    def on_sort(self, method: str):
        """Sorts the sequences based on the given method."""
        # set overriden cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.settings_manager.browse_settings.set_sort_method(method)
        self.sequence_picker.sorter.sort_and_display_currently_filtered_sequences_by_method(
            method
        )
        self.browse_tab.sequence_picker.scroll_widget.scroll_area.verticalScrollBar().setValue(
            0
        )
        self.browse_tab.ui_updater.resize_thumbnails_top_to_bottom()
        QApplication.restoreOverrideCursor()
