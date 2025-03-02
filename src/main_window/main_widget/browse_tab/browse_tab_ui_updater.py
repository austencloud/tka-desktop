from typing import TYPE_CHECKING
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabUIUpdater:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.settings_manager = AppContext.settings_manager()
        self.font_color_updater = browse_tab.main_widget.font_color_updater

    def update_and_display_ui(self, total_sequences: int):
        self.browse_tab.sequence_picker.progress_bar.setVisible(False)
        QApplication.restoreOverrideCursor()

        if total_sequences == 0:
            return

        sort_method = self.settings_manager.browse_settings.get_sort_method()
        self.browse_tab.sequence_picker.sorter._sort_only(sort_method)

        self._create_and_show_thumbnails(skip_scaling=True)
        # QTimer.singleShot(500, self.resize_thumbnails_top_to_bottom)

    def _create_and_show_thumbnails(self, skip_scaling: bool = True):
        self.browse_tab.sequence_picker.sorter._display_sorted_sections(
            skip_scaling=True
        )
        self._apply_thumbnail_styling()

    def resize_thumbnails_top_to_bottom(self):
        # Make a separate list so we don’t mutate while iterating
        thumbnail_box_list = list(
            self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values()
        )
        for tb in thumbnail_box_list:
            tb.image_label.update_thumbnail(tb.state.current_index)

    def _apply_thumbnail_styling(self):
        font_color = self.font_color_updater.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )
        star_icon_path = (
            "star_empty_white.png" if font_color == "white" else "star_empty_black.png"
        )

        for (
            tb
        ) in self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values():
            tb.word_label.setStyleSheet(f"color: {font_color};")
            tb.word_label.star_icon_empty_path = star_icon_path
            tb.word_label.reload_favorite_icon()
            tb.variation_number_label.setStyleSheet(f"color: {font_color};")
