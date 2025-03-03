from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabUIUpdater:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.settings_manager = AppContext.settings_manager()
        self.font_color_updater = browse_tab.main_widget.font_color_updater
        self._resize_job_id = 0
        self._last_window_width = None  # Track width for resize optimization

    def update_and_display_ui(self, total_sequences: int, skip_scaling: bool = True):
        QApplication.restoreOverrideCursor()

        if total_sequences == 0:
            return

        sort_method = self.settings_manager.browse_settings.get_sort_method()
        self.browse_tab.sequence_picker.sorter._sort_only(sort_method)

        self._create_and_show_thumbnails(skip_scaling)

    def _create_and_show_thumbnails(self, skip_scaling: bool = True):
        self.browse_tab.sequence_picker.sorter.display_sorted_sections(skip_scaling)
        self._apply_thumbnail_styling()

    def resize_thumbnails_top_to_bottom(self):
        current_window_width = self.browse_tab.sequence_picker.main_widget.width()

        # Skip resize if width hasn't changed
        if current_window_width == self._last_window_width:
            return

        sections_copy = dict(self.browse_tab.sequence_picker.sections)
        sort_method = self.settings_manager.browse_settings.get_sort_method()
        sorted_sections = (
            self.browse_tab.sequence_picker.section_manager.get_sorted_sections(
                sort_method, sections_copy.keys()
            )
        )

        # Disable navigation buttons during resize
        for button in self.browse_tab.sequence_picker.nav_sidebar.manager.buttons:
            button.setEnabled(False)

        scroll_widget = self.browse_tab.sequence_picker.scroll_widget
        for section in sorted_sections:
            if section not in sections_copy:
                return
            for word, _ in self.browse_tab.sequence_picker.sections.get(section, []):
                if word not in scroll_widget.thumbnail_boxes:
                    return
                thumbnail_box = scroll_widget.thumbnail_boxes[word]

                thumbnail_box.image_label.update_thumbnail(
                    thumbnail_box.state.current_index
                )
                QApplication.processEvents()

            # Handle date formatting for navigation buttons
            if sort_method == "date_added":
                month, day, _ = section.split("-")
                day = day.lstrip("0")
                month = month.lstrip("0")
                section = f"{month}-{day}"

            self._enable_button_for_section(section)

        self._last_window_width = current_window_width

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

    def _enable_button_for_section(self, section_key: str):
        nav_buttons = self.browse_tab.sequence_picker.nav_sidebar.manager.buttons
        for btn in nav_buttons:
            if getattr(btn, "section_key", None) == section_key:
                btn.setEnabled(True)
                break
