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
        self._resize_job_id = 0

    def update_and_display_ui(self, total_sequences: int, skip_scaling: bool = True):
        self.browse_tab.sequence_picker.progress_bar.setVisible(False)
        QApplication.restoreOverrideCursor()

        if total_sequences == 0:
            return

        sort_method = self.settings_manager.browse_settings.get_sort_method()
        self.browse_tab.sequence_picker.sorter._sort_only(sort_method)

        self._create_and_show_thumbnails(skip_scaling)

    def _create_and_show_thumbnails(self, skip_scaling: bool = True):
        self.browse_tab.sequence_picker.sorter._display_sorted_sections(skip_scaling)
        self._apply_thumbnail_styling()

    def resize_thumbnails_top_to_bottom(self):
        self._resize_job_id += 1
        current_job_id = self._resize_job_id

        sections_copy = dict(self.browse_tab.sequence_picker.sections)
        sort_method = self.settings_manager.browse_settings.get_sort_method()
        sorted_sections = (
            self.browse_tab.sequence_picker.section_manager.get_sorted_sections(
                sort_method, sections_copy.keys()
            )
        )

        for button in self.browse_tab.sequence_picker.nav_sidebar.manager.buttons:
            button.set_button_enabled(False)

        scroll_widget = self.browse_tab.sequence_picker.scroll_widget
        counter = 0
        for section in sorted_sections:
            if current_job_id != self._resize_job_id:
                return

            if section not in sections_copy:
                return
            for word, _ in self.browse_tab.sequence_picker.sections.get(section, []):
                if current_job_id != self._resize_job_id:
                    return
                if word not in scroll_widget.thumbnail_boxes:
                    return
                thumbnail_box = scroll_widget.thumbnail_boxes[word]
                thumbnail_box.image_label.update_thumbnail(
                    thumbnail_box.state.current_index
                )
                counter += 1
                if counter > 6:
                    QApplication.processEvents()

            self._enable_button_for_section(section)

        # QApplication.processEvents()

    def cancel_resize_job(self):
        self._resize_job_id += 1

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
                btn.set_button_enabled(True)
                break
