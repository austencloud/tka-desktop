from datetime import datetime
from typing import TYPE_CHECKING, Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.tab_indices import LeftStackIndex

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabFilterController:
    """Handles all 'apply filter' operations for the BrowseTab.
    
    Splits logic between simple (string) filters and dictionary-based (complex) filters.
    """

    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.filter_manager = browse_tab.filter_manager
        self.ui_updater = browse_tab.ui_updater
        self.fade_manager = browse_tab.main_widget.fade_manager

    # -------------------------------------------------------------------------
    # Public Method
    # -------------------------------------------------------------------------
    def apply_filter(self, filter_criteria: Union[str, dict]):
        """Fade out certain widgets, run the filtering logic, then update UI."""
        description = self._get_filter_description(filter_criteria)

        widgets_to_fade = [
            self.browse_tab.sequence_picker.filter_stack,
            self.browse_tab.sequence_picker,
        ]

        self.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            lambda: self._apply_filter_after_fade(filter_criteria, description),
        )

    # -------------------------------------------------------------------------
    # Internals
    # -------------------------------------------------------------------------
    def _apply_filter_after_fade(self, filter_criteria, description: str):
        """UI + filter pipeline after fade is done."""
        self._prepare_ui_for_filtering(description)    # sets wait cursor, etc.

        # Step 1: compute the results
        if isinstance(filter_criteria, str):
            results = self._handle_string_filter(filter_criteria)
        elif isinstance(filter_criteria, dict):
            results = self._handle_dict_filter(filter_criteria)
        else:
            raise ValueError(f"Invalid filter type: {type(filter_criteria)} (must be str or dict).")

        # Step 2: update the main widget state
        self.browse_tab.sequence_picker.currently_displayed_sequences = results

        # Step 3: re-render the UI
        self.ui_updater.update_and_display_ui(len(results))
        self.browse_tab.main_widget.left_stack.setCurrentIndex(LeftStackIndex.SEQUENCE_PICKER)

    def _prepare_ui_for_filtering(self, description: str):
        """Sets up the UI to reflect that a filter is being applied (cursor, labels, etc.)."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        control_panel = self.browse_tab.sequence_picker.control_panel
        control_panel.currently_displaying_label.setText(f"Displaying {description}")
        control_panel.count_label.setText("")
        self.browse_tab.sequence_picker.scroll_widget.clear_layout()

        # Show a progress bar in the grid if you want
        sp = self.browse_tab.sequence_picker
        sp.scroll_widget.grid_layout.addWidget(
            sp.progress_bar, 0, 0, 1, sp.sorter.num_columns, Qt.AlignmentFlag.AlignCenter
        )
        sp.progress_bar.setVisible(True)
        sp.progress_bar.resize_progress_bar()

    # -------------------------------------------------------------------------
    # Filter Logic
    # -------------------------------------------------------------------------
    def _handle_string_filter(self, filter_name: str):
        """Run a known string-based filter using the FilterManager."""
        fm = self.filter_manager

        if filter_name == "favorites":
            return fm.filter_favorites()
        elif filter_name == "all":
            return fm.filter_all_sequences()
        elif filter_name == "most_recent":
            return fm.filter_most_recent(datetime.now())
        elif filter_name.startswith("tag:"):
            tag = filter_name.split("tag:")[1].strip()
            return fm.filter_by_tag(tag)
        else:
            raise ValueError(f"Unknown string filter: {filter_name}")

    def _handle_dict_filter(self, criteria: dict):
        """Dispatch to a submethod based on the single filter_key in 'criteria'."""
        if len(criteria) != 1:
            raise ValueError("Dictionary filter must contain exactly one key-value pair.")
        (filter_key, filter_value) = next(iter(criteria.items()))

        # Instead of a big chain, let's dispatch to a dictionary of submethods
        dispatch_map = {
            "starting_letter":    self._dict_filter_starting_letter,
            "contains_letters":   self._dict_filter_contains_letters,
            "length":             self._dict_filter_length,
            "level":              self._dict_filter_level,
            "author":             self._dict_filter_author,
            "starting_position":  self._dict_filter_starting_pos,
            "favorites":          self._dict_filter_favorites,
            "most_recent":        self._dict_filter_most_recent,
            "grid_mode":          self._dict_filter_grid_mode,
            "show_all":           self._dict_filter_show_all,
        }

        if filter_key not in dispatch_map:
            raise ValueError(f"Unknown dictionary filter key: {filter_key}")

        return dispatch_map[filter_key](filter_value)

    # -------------------------------------------------------------------------
    # Dictionary Sub-Filters (each one is small + readable)
    # -------------------------------------------------------------------------
    def _dict_filter_starting_letter(self, letter):
        base_words = self._base_words()
        fm = self.filter_manager
        return [
            (word, thumbs, fm._get_sequence_length(thumbs[0]))
            for word, thumbs in base_words
            if word.startswith(letter)
        ]

    def _dict_filter_contains_letters(self, letters):
        base_words = self._base_words()
        fm = self.filter_manager
        return [
            (word, thumbs, fm._get_sequence_length(thumbs[0]))
            for word, thumbs in base_words
            if any(char in word for char in letters)
        ]

    def _dict_filter_length(self, length_value):
        base_words = self._base_words()
        fm = self.filter_manager
        try:
            target_length = int(length_value)
        except ValueError:
            raise ValueError(f"Invalid length '{length_value}'; expected integer.")
        return [
            (word, thumbs, fm._get_sequence_length(thumbs[0]))
            for word, thumbs in base_words
            if fm._get_sequence_length(thumbs[0]) == target_length
        ]

    def _dict_filter_level(self, level_value):
        base_words = self._base_words()
        extractor = self.browse_tab.main_widget.metadata_extractor
        fm = self.filter_manager
        return [
            (w, t, fm._get_sequence_length(t[0]))
            for w, t in base_words
            if extractor.get_level(t[0]) == level_value
        ]

    def _dict_filter_author(self, author_value):
        base_words = self._base_words()
        extractor = self.browse_tab.main_widget.metadata_extractor
        fm = self.filter_manager
        return [
            (w, t, fm._get_sequence_length(t[0]))
            for w, t in base_words
            if extractor.get_author(t[0]) == author_value
        ]

    def _dict_filter_starting_pos(self, pos_value):
        base_words = self._base_words()
        extractor = self.browse_tab.main_widget.metadata_extractor
        fm = self.filter_manager
        result = []
        for w, t in base_words:
            if extractor.get_start_pos(t[0]) == pos_value.lower():
                result.append((w, t, fm._get_sequence_length(t[0])))
        return result

    def _dict_filter_favorites(self, _unused):
        # This is effectively the same as "fm.filter_favorites()", so let's just do that:
        return self.filter_manager.filter_favorites()

    def _dict_filter_most_recent(self, _unused):
        # Same approach, no param needed
        return self.filter_manager.filter_most_recent()

    def _dict_filter_grid_mode(self, grid_mode_value):
        base_words = self._base_words()
        extractor = self.browse_tab.main_widget.metadata_extractor
        fm = self.filter_manager
        return [
            (w, t, fm._get_sequence_length(t[0]))
            for w, t in base_words
            if extractor.get_grid_mode(t[0]) == grid_mode_value
        ]

    def _dict_filter_show_all(self, _unused):
        return self.filter_manager.filter_all_sequences()

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _base_words(self):
        """Just a convenience function so we don't keep repeating ourselves."""
        from utilities.path_helpers import get_images_and_data_path
        dictionary_dir = get_images_and_data_path("dictionary")
        return self.browse_tab.get.base_words(dictionary_dir)

    # -------------------------------------------------------------------------
    # Description Helpers
    # -------------------------------------------------------------------------
    def _get_filter_description(self, filter_criteria: Union[str, dict]) -> str:
        """Generates a user-friendly description for the filter being applied."""
        if isinstance(filter_criteria, str):
            if filter_criteria == "all":
                return "all sequences"
            elif filter_criteria.startswith("tag:"):
                tag_name = filter_criteria.split("tag:")[1].strip()
                return f"sequences with tag '{tag_name}'"
            return filter_criteria.replace("_", " ").capitalize()

        # It's a dictionary
        return self._description_for_dict_filter(filter_criteria)

    def _description_for_dict_filter(self, filter_criteria: dict) -> str:
        """Helper for describing dictionary-based filters."""
        if len(filter_criteria) != 1:
            return "Unknown Filter"
        key, value = list(filter_criteria.items())[0]

        desc_map = {
            "starting_letter":     f"sequences starting with {value}",
            "contains_letters":    f"sequences containing {value}",
            "length":              f"sequences with length {value}",
            "level":               f"sequences with level {value}",
            "author":              f"sequences by {value}",
            "starting_position":   f"sequences starting at position {value}",
            "favorites":           "favorite sequences",
            "most_recent":         "most recent sequences",
            "grid_mode":           f"sequences in {value} mode",
            "show_all":            "all sequences",
        }
        return desc_map.get(key, "Unknown Filter")
