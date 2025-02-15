from typing import TYPE_CHECKING
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabUIUpdater:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab

        self.settings_manager = browse_tab.main_widget.main_window.settings_manager
        self.font_color_updater = browse_tab.main_widget.font_color_updater

    def update_and_display_ui(self, total_sequences: int):
        """
        1) Sort everything in final order
        2) Create & show all thumbnails instantly, skipping scaling
        3) (Optional) Wait ~0.5s
        4) Then do a top-down scaling pass
        """
        # No more progress bar or cursor override if you don't want them
        self.browse_tab.sequence_picker.progress_bar.setVisible(False)
        QApplication.restoreOverrideCursor()

        if total_sequences == 0:
            # Just clear or show "no results" if you want
            return

        # 1) Sort only (no actual widget creation)
        sort_method = self.settings_manager.browse_settings.get_sort_method()
        self.browse_tab.sequence_picker.sorter._sort_only(sort_method)

        # 2) Create & show in sorted order, skipping the scaling
        self._create_and_show_thumbnails_in_sorted_order(skip_scaling=True)

        # 3) Wait 500 ms so the user sees "everything loaded"
        QTimer.singleShot(500, self._resize_thumbnails_top_to_bottom)

    def _create_and_show_thumbnails_in_sorted_order(self, skip_scaling: bool = True):
        """
        Actually place the thumbnails into the layout according to their already-sorted order.
        If 'skip_scaling' = True, we skip the expensive thumbnail resizing at creation time.
        """
        sorter = self.browse_tab.sequence_picker.sorter
        # This calls _display_sorted_sections(...) above, which calls update_ui(...)
        sorter._display_sorted_sections(skip_scaling=skip_scaling)

        # Now apply styling for font color, etc.
        self._apply_font_color_styling()

    def _resize_thumbnails_top_to_bottom(self):
        """
        Iterate over each thumbnail box from top to bottom,
        triggering the actual 'update_thumbnail(...)' scaling
        so the user sees them gradually get scaled without a big re-sort.
        """
        scroll_area = self.browse_tab.sequence_picker.scroll_widget.scroll_area
        current_scroll_pos = scroll_area.verticalScrollBar().value()

        # If you want row-major order, you'll have to read the grid layout items directly.
        # For simplicity, this just uses the dictionary's values:
        boxes = list(
            self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values()
        )

        for tb in boxes:
            tb.image_label.update_thumbnail(tb.state.current_index)
            # Let the UI breathe so the scaling is visible
            QApplication.processEvents()

        # Restore the user's scroll position (prevents "jump to top")
        scroll_area.verticalScrollBar().setValue(current_scroll_pos)

    def _apply_font_color_styling(self):
        font_color = self.font_color_updater.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )

        for (
            tb
        ) in self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values():
            tb.word_label.setStyleSheet(f"color: {font_color};")
            tb.word_label.star_icon_empty_path = (
                "star_empty_white.png"
                if font_color == "white"
                else "star_empty_black.png"
            )
            tb.word_label.reload_favorite_icon()
            tb.variation_number_label.setStyleSheet(f"color: {font_color};")

    def _apply_sorting_and_styling(self):
        """Apply sorting to thumbnails and style elements based on current settings."""
        self.browse_tab.sequence_picker.sorter.sort_and_display_currently_filtered_sequences_by_method(
            self.settings_manager.browse_settings.get_sort_method()
        )

        font_color = self.font_color_updater.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )

        for (
            thumbnail_box
        ) in self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values():
            thumbnail_box.word_label.setStyleSheet(f"color: {font_color};")
            thumbnail_box.word_label.star_icon_empty_path = (
                "star_empty_white.png"
                if font_color == "white"
                else "star_empty_black.png"
            )
            thumbnail_box.word_label.reload_favorite_icon()
            thumbnail_box.variation_number_label.setStyleSheet(f"color: {font_color};")
