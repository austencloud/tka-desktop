from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.tab_indices import LeftStackIndex
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabFilterController:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.filter_manager = browse_tab.filter_manager
        self.ui_updater = browse_tab.ui_updater
        self.fade_manager = browse_tab.main_widget.fade_manager

    def apply_filter(self, filter_criteria: Union[str, dict]):
        """
        Apply a filter based on a string like 'favorites' or a dictionary like {'starting_letter': 'A'}.
        """
        description = self._get_filter_description(filter_criteria)

        widgets_to_fade = [
            self.browse_tab.sequence_picker.filter_stack,
            self.browse_tab.sequence_picker,
        ]

        self.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            lambda: self._execute_filter_and_update_ui(filter_criteria, description),
        )

    def _execute_filter_and_update_ui(self, filter_criteria, description: str):
        self._prepare_ui_for_filtering(description)

        results = []

        if isinstance(filter_criteria, str):
            results = self._handle_string_filter(filter_criteria)
        elif isinstance(filter_criteria, dict):
            results = self._handle_dict_filter(filter_criteria)
        else:
            raise ValueError(
                f"Invalid filter type: {type(filter_criteria)}. Must be str or dict."
            )

        self.browse_tab.sequence_picker.currently_displayed_sequences = results
        self.ui_updater.update_and_display_ui(len(results))

        self.browse_tab.main_widget.left_stack.setCurrentIndex(
            LeftStackIndex.SEQUENCE_PICKER
        )
 
    def _handle_string_filter(self, filter_name: str) -> list[tuple[str, list[str], int]]:
        if filter_name == "favorites":
            return self.filter_manager.filter_favorites()
        elif filter_name == "all":
            return self.filter_manager.filter_all_sequences()
        elif filter_name == "most_recent":
            date = datetime.now()
            return self.filter_manager.filter_most_recent(date)
        elif filter_name.startswith("tag:"):
            tag = filter_name.split("tag:")[1].strip()
            return self.filter_manager.filter_by_tag(tag)

        raise ValueError(f"Unknown string filter: {filter_name}")

    def _handle_dict_filter(self, filter_criteria: dict) -> list[tuple[str, list[str], int]]:
        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = self.browse_tab.get.base_words(dictionary_dir)

        if len(filter_criteria) != 1:
            raise ValueError(
                "Dictionary filter must contain exactly one key-value pair."
            )

        filter_key, filter_value = list(filter_criteria.items())[0]

        if filter_key == "starting_letter":
            return [
                (
                    word,
                    thumbnails,
                    self.filter_manager._get_sequence_length(thumbnails[0]),
                )
                for word, thumbnails in base_words
                if word.startswith(filter_value)
            ]

        elif filter_key == "contains_letters":
            return [
                (
                    word,
                    thumbnails,
                    self.filter_manager._get_sequence_length(thumbnails[0]),
                )
                for word, thumbnails in base_words
                if any(char in word for char in filter_value)
            ]

        elif filter_key == "length":
            try:
                target_length = int(filter_value)
            except ValueError:
                raise ValueError(
                    f"Invalid length value '{filter_value}'. Expected an integer."
                )

            return [
                (
                    word,
                    thumbnails,
                    self.filter_manager._get_sequence_length(thumbnails[0]),
                )
                for word, thumbnails in base_words
                if self.filter_manager._get_sequence_length(thumbnails[0])
                == target_length
            ]

        elif filter_key == "level":
            return [
                (
                    word,
                    thumbnails,
                    self.filter_manager._get_sequence_length(thumbnails[0]),
                )
                for word, thumbnails in base_words
                if self.browse_tab.main_widget.metadata_extractor.get_level(
                    thumbnails[0]
                )
                == filter_value
            ]

        elif filter_key == "author":
            return [
                (
                    word,
                    thumbnails,
                    self.filter_manager._get_sequence_length(thumbnails[0]),
                )
                for word, thumbnails in base_words
                if self.browse_tab.main_widget.metadata_extractor.get_author(
                    thumbnails[0]
                )
                == filter_value
            ]

        elif filter_key == "starting_position":
            filtered_by_starting_position = []
            for word, thumbnails in base_words:
                thumbnail = thumbnails[0]
                sequence_length = self.filter_manager._get_sequence_length(thumbnail)
                start_pos = (
                    self.browse_tab.main_widget.metadata_extractor.get_start_pos(
                        thumbnail
                    )
                )

                if start_pos == filter_value.lower():
                    filtered_by_starting_position.append(
                        (word, thumbnails, sequence_length)
                    )

            return filtered_by_starting_position

        elif filter_key == "favorites":
            return [
                (
                    word,
                    thumbnails,
                    self.filter_manager._get_sequence_length(thumbnails[0]),
                )
                for word, thumbnails in base_words
                if any(
                    self.browse_tab.main_widget.metadata_extractor.get_favorite_status(
                        thumbnail
                    )
                    for thumbnail in thumbnails
                )
            ]
        elif filter_key == "most_recent":
            return self.filter_manager.filter_most_recent()

        elif filter_key == "grid_mode":
            return [
                (
                    word,
                    thumbnails,
                    self.filter_manager._get_sequence_length(thumbnails[0]),
                )
                for word, thumbnails in base_words
                if self.browse_tab.main_widget.metadata_extractor.get_grid_mode(
                    thumbnails[0]
                )
                == filter_value
            ]
        elif filter_key == "show_all":
            return self.filter_manager.filter_all_sequences()
        raise ValueError(f"Unknown dictionary filter key: {filter_key}")

    def _get_filter_description(self, filter_criteria: Union[str, dict]) -> str:
        """Generates a user-friendly description for the filter being applied."""
        if isinstance(filter_criteria, str):
            if filter_criteria == "all":
                return "all sequences"
            elif filter_criteria.startswith("tag:"):
                tag_name = filter_criteria.split("tag:")[1].strip()
                return f"sequences with tag '{tag_name}'"
            return filter_criteria.replace("_", " ").capitalize()

        if isinstance(filter_criteria, dict):
            key, value = list(filter_criteria.items())[0]

            description_map = {
                "starting_letter": f"sequences starting with {value}",
                "contains_letters": (
                    f"sequences containing {', '.join(value[:-1]) + ', or ' + value[-1]}"
                    if isinstance(value, list) and len(value) > 2
                    else (
                        f"sequences containing {value[0]} or {value[1]}"
                        if isinstance(value, list) and len(value) == 2
                        else (
                            f"sequences containing {value}"
                            if isinstance(value, str)
                            else "sequences containing specific letters"
                        )
                    )
                ),
                "length": f"sequences with length {value}",
                "level": f"sequences with level {value}",
                "author": f"sequences by {value}",
                "starting_position": f"sequences starting at position {value}",
                "favorites": "favorite sequences",
                "most_recent": "most recent sequences",
                "grid_mode": f"sequences in {value} mode",
                "show_all": "all sequences",
            }

            return description_map.get(key, "Unknown Filter")

        return "Unknown Filter"

    def _prepare_ui_for_filtering(self, description: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        control_panel = self.browse_tab.sequence_picker.control_panel
        control_panel.currently_displaying_label.setText(f"Displaying {description}")
        control_panel.count_label.setText("")
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
