from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from .thumbnail_box.thumbnail_box import ThumbnailBox
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class ThumbnailUpdater:
    """Handles updating and styling of thumbnails."""

    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.font_color_updater = browse_tab.main_widget.font_color_updater

    def update_thumbnail_image(self, thumbnail_box: "ThumbnailBox"):
        """Updates the thumbnail image of a given thumbnail box."""
        thumbnail_box.image_label.update_thumbnail(thumbnail_box.state.current_index)

    def apply_thumbnail_styling(self, background_type):
        """Applies styling (font color, star icon) to all thumbnails."""
        font_color = self.font_color_updater.get_font_color(background_type)
        star_icon_path = (
            "star_empty_white.png" if font_color == "white" else "star_empty_black.png"
        )

        for (
            tb
        ) in self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values():
            self._apply_single_thumbnail_style(tb, font_color, star_icon_path)

    def _apply_single_thumbnail_style(
        self, tb: "ThumbnailBox", font_color, star_icon_path
    ):
        """Applies styling to a single thumbnail box."""
        tb.word_label.setStyleSheet(f"color: {font_color};")
        tb.word_label.star_icon_empty_path = star_icon_path
        tb.word_label.reload_favorite_icon()
        tb.variation_number_label.setStyleSheet(f"color: {font_color};")


class SidebarButtonUpdater:
    """Handles enabling/disabling navigation buttons."""

    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab

    def enable_button_for_section(self, section_key: str):
        """Enables the navigation button associated with the given section key."""
        for btn in self.browse_tab.sequence_picker.nav_sidebar.manager.buttons:
            if getattr(btn, "section_key", None) == section_key:
                btn.setEnabled(True)
                break

    def disable_all_buttons(self):
        """Disables all navigation buttons."""
        for button in self.browse_tab.sequence_picker.nav_sidebar.manager.buttons:
            button.setEnabled(False)


class BrowseTabUIUpdater:
    """Updates the Browse Tab UI, managing thumbnails and navigation."""

    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.settings_manager = AppContext.settings_manager()
        self.thumbnail_updater = ThumbnailUpdater(browse_tab)
        self.sidebar_button_updater = SidebarButtonUpdater(browse_tab)
        self._resize_job_id = 0
        self._last_window_width = None  # Track width for resize optimization

    def update_and_display_ui(self, total_sequences: int, skip_scaling: bool = True):
        """Updates and displays the UI based on the total number of sequences."""
        QApplication.restoreOverrideCursor()

        if total_sequences == 0:
            return

        self._sort_sequences()
        self._create_and_show_thumbnails(skip_scaling)

    def _sort_sequences(self):
        """Sorts the sequences in the sequence picker."""
        sort_method = self.settings_manager.browse_settings.get_sort_method()
        self.browse_tab.sequence_picker.sorter._sort_only(sort_method)

    def _create_and_show_thumbnails(self, skip_scaling: bool = True):
        """Creates and displays thumbnails, applying styling."""
        self.browse_tab.sequence_picker.sorter.display_sorted_sections(skip_scaling)
        background_type = self.settings_manager.global_settings.get_background_type()
        self.thumbnail_updater.apply_thumbnail_styling(background_type)

    def resize_thumbnails_top_to_bottom(self):
        """Resizes thumbnails from top to bottom, enabling navigation buttons."""
        sections_copy = dict(self.browse_tab.sequence_picker.sections)
        sort_method = self.settings_manager.browse_settings.get_sort_method()
        sorted_sections = (
            self.browse_tab.sequence_picker.section_manager.get_sorted_sections(
                sort_method, sections_copy.keys()
            )
        )

        # Disable navigation buttons during resize
        self.sidebar_button_updater.disable_all_buttons()

        scroll_widget = self.browse_tab.sequence_picker.scroll_widget
        for section in sorted_sections:
            if section not in sections_copy:
                return
            for word, _ in self.browse_tab.sequence_picker.sections.get(section, []):
                if word not in scroll_widget.thumbnail_boxes:
                    return
                thumbnail_box = scroll_widget.thumbnail_boxes[word]

                self.thumbnail_updater.update_thumbnail_image(thumbnail_box)
                QApplication.processEvents()

            # Handle date formatting for navigation buttons
            if sort_method == "date_added":
                month, day, _ = section.split("-")
                day = day.lstrip("0")
                month = month.lstrip("0")
                section = f"{month}-{day}"

            self._enable_button_for_section(section)

    def _enable_button_for_section(self, section_key: str):
        """Enables a specific navigation button by section key."""
        self.sidebar_button_updater.enable_button_for_section(section_key)
