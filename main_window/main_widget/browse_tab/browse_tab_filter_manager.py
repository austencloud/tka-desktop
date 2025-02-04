from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:

    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabFilterManager:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.main_widget = self.browse_tab.main_widget
        self.fade_manager = self.main_widget.fade_manager

    def show_favorites(self):
        """Show only favorite sequences."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("favorite sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        favorites = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if any(
                self.browse_tab.main_widget.metadata_extractor.get_favorite_status(
                    thumbnail
                )
                for thumbnail in thumbnails
            )
        ]

        self.browse_tab.sequence_picker.currently_displayed_sequences = favorites
        self.browse_tab.ui_updater.update_and_display_ui(len(favorites))

    def show_all_sequences(self):
        """Show all sequences."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("all sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        sequences = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
        ]

        self.browse_tab.sequence_picker.currently_displayed_sequences = sequences
        self.browse_tab.ui_updater.update_and_display_ui(len(sequences))

    def show_most_recent_sequences(self, date: datetime):
        """Show most recent sequences based on date."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("most recent sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        most_recent = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if self.browse_tab.sequence_picker.section_manager.get_date_added(
                thumbnails
            )
            >= date
        ]

        self.browse_tab.sequence_picker.currently_displayed_sequences = most_recent
        self.browse_tab.ui_updater.update_and_display_ui(len(most_recent))

    def show_browser_with_filters_from_settings(self):
        """Show browser with filters from settings."""
        current_filter = (
            self.browse_tab.main_widget.main_window.settings_manager.browse_settings.get_current_filter()
        )

        self.apply_filter(current_filter)

    def apply_filter(self, current_filter):
        self.browse_tab.settings.set_current_section("sequence_picker")
        self.current_filter = current_filter

        widgets_to_fade = [
            self.browse_tab.sequence_picker.filter_stack,
            self.browse_tab.sequence_picker,
        ]
        self.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            callback=self._apply_filter_logic,
        )

    def _apply_filter_logic(self):
        self.browse_tab.filter_manager.sort_and_display_thumbnail_boxes_by_current_filter(
            self.browse_tab.filter_manager.current_filter
        )
        # QApplication.processEvents()
        self.browse_tab.main_widget.left_stack.setCurrentIndex(
            self.browse_tab.main_widget.left_sequence_picker_index
        )
        # self.browse_tab.main_widget.left_stack.setGraphicsEffect(None)
        # self.browse_tab.sequence_picker.setGraphicsEffect(None)
        # self.main_widget.fade_manager.graphics_effect_remover.clear_graphics_effects()

    def sort_and_display_thumbnail_boxes_by_current_filter(
        self, initial_selection: dict
    ) -> None:

        filter_selector = self.browse_tab.sequence_picker.filter_stack
        starting_position_section = filter_selector.starting_position_section
        contains_letter_section = filter_selector.contains_letter_section
        starting_letter_section = filter_selector.starting_letter_section
        level_section = filter_selector.level_section
        length_section = filter_selector.length_section
        author_section = filter_selector.author_section
        grid_mode_section = filter_selector.grid_mode_section
        display_functions = {
            "starting_letter": starting_letter_section.display_only_thumbnails_starting_with_letter,
            "sequence_length": length_section.display_only_thumbnails_with_sequence_length,
            "level": level_section.display_only_thumbnails_with_level,
            "contains_letters": contains_letter_section.display_only_thumbnails_containing_letters,
            "starting_position": starting_position_section.display_only_thumbnails_with_starting_position,
            "author": author_section.display_only_thumbnails_by_author,
            "favorites": self.browse_tab.filter_manager.show_favorites,
            "most_recent": self.browse_tab.filter_manager.show_most_recent_sequences,
            "grid_mode": grid_mode_section.display_only_thumbnails_with_grid_mode,
            "show_all": self.browse_tab.filter_manager.show_all_sequences,
        }
        if initial_selection:
            for key, value in initial_selection.items():
                if key in display_functions:
                    if key in ["favorites", "show_all"]:
                        display_functions[key]()
                    else:
                        display_functions[key](value)

    def prepare_ui_for_filtering(self, description: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.browse_tab.sequence_picker.control_panel.currently_displaying_label.setText(
            ""
        )
        # QApplication.processEvents()
        self.browse_tab.sequence_picker.control_panel.currently_displaying_label.show_message(
            description
        )
        self.browse_tab.sequence_picker.control_panel.count_label.setText("")
        self.browse_tab.sequence_picker.scroll_widget.clear_layout()
        self.browse_tab.sequence_picker.scroll_widget.grid_layout.addWidget(
            self.browse_tab.sequence_picker.progress_bar,
            0,
            0,
            1,
            self.browse_tab.sequence_picker.sorter.num_columns,
            Qt.AlignmentFlag.AlignCenter,
        )
        self.browse_tab.sequence_picker.progress_bar.setVisible(True)
        self.browse_tab.sequence_picker.progress_bar.resize_progress_bar()

        # QApplication.processEvents()
