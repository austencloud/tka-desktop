from datetime import datetime
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QApplication
from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box import ThumbnailBox

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.sequence_picker import (
        SequencePicker,
    )


class SequencePickerSorter:
    num_columns: int = 3

    def __init__(self, sequence_picker: "SequencePicker"):
        self.sequence_picker = sequence_picker
        self.browse_tab = sequence_picker.browse_tab
        self.metadata_extractor = self.browse_tab.main_widget.metadata_extractor
        self.main_widget = self.browse_tab.main_widget
        self.scroll_widget = self.sequence_picker.scroll_widget

    def sort_and_display_currently_filtered_sequences_by_method(
        self, sort_method: str
    ) -> None:
        self.section_manager = self.sequence_picker.section_manager
        self.scroll_widget.clear_layout()
        self.browse_tab.sequence_picker.sections = {}

        sort_key = self.get_sort_key(sort_method)
        self.sort_sequences(sort_key, sort_method)
        self.group_sequences_by_section(sort_method)
        sorted_sections = self.section_manager.get_sorted_sections(
            sort_method, self.browse_tab.sequence_picker.sections.keys()
        )
        self.update_ui(sorted_sections, sort_method)

    def get_sort_key(self, sort_method: str):
        return {
            "sequence_length": lambda x: x[2] if x[2] is not None else float("inf"),
            "date_added": lambda x: self.section_manager.get_date_added(x[1])
            or datetime.min,
        }.get(sort_method, lambda x: x[0])

    def sort_sequences(self, sort_key, sort_method: str):
        self.browse_tab.sequence_picker.currently_displayed_sequences.sort(
            key=sort_key, reverse=(sort_method == "date_added")
        )

    def group_sequences_by_section(self, sort_method: str):
        for (
            word,
            thumbnails,
            seq_length,
        ) in self.browse_tab.sequence_picker.currently_displayed_sequences:
            section = self.section_manager.get_section_from_word(
                word, sort_method, seq_length, thumbnails
            )
            self.browse_tab.sequence_picker.sections.setdefault(section, []).append(
                (word, thumbnails)
            )

    def update_ui(self, sorted_sections: list[str], sort_method: str):
        self.sequence_picker.nav_sidebar.update_sidebar(sorted_sections, sort_method)
        self.sequence_picker.control_panel.sort_widget.highlight_appropriate_button(
            sort_method
        )

        current_section = None
        row_index = 0
        for section in sorted_sections:
            if sort_method == "date_added" and section == "Unknown":
                continue

            row_index = self.add_section_headers(
                row_index, section, sort_method, current_section
            )
            current_section = (
                section if sort_method == "date_added" else current_section
            )

            column_index = 0
            for word, thumbnails in self.browse_tab.sequence_picker.sections[section]:
                self.add_thumbnail_box(
                    row_index, column_index, word, thumbnails, hidden=False
                )
                column_index = (column_index + 1) % self.num_columns
                if column_index == 0:
                    row_index += 1

        self.sequence_picker.control_panel.count_label.setText(
            f"Number of words: {len(self.browse_tab.sequence_picker.currently_displayed_sequences)}"
        )
        QApplication.restoreOverrideCursor()

    def add_section_headers(
        self, row_index: int, section: str, sort_method: str, current_section: str
    ):
        if sort_method == "date_added":
            day, month, year = section.split("-")
            formatted_day = f"{int(day)}-{int(month)}"

            if year != current_section:
                row_index += 1
                self.section_manager.add_header(row_index, self.num_columns, year)
                row_index += 1
                current_section = year

            row_index += 1
            self.section_manager.add_header(row_index, self.num_columns, formatted_day)
            row_index += 1
        else:
            row_index += 1
            self.section_manager.add_header(row_index, self.num_columns, section)
            row_index += 1
        return row_index

    def add_thumbnail_box(
        self,
        row_index: int,
        column_index: int,
        word: str,
        thumbnails: list[str],
        hidden: bool,
        skip_image: bool = False,
    ):
        if word not in self.scroll_widget.thumbnail_boxes:
            thumbnail_box = ThumbnailBox(self.browse_tab, word, thumbnails)
            self.scroll_widget.thumbnail_boxes[word] = thumbnail_box
        else:
            thumbnail_box = self.scroll_widget.thumbnail_boxes[word]

        if hidden:
            thumbnail_box.hide()

        self.scroll_widget.grid_layout.addWidget(thumbnail_box, row_index, column_index)

        if not hidden:
            thumbnail_box.show()
            if not skip_image:
                # The single call that triggers scaling:
                thumbnail_box.image_label.update_thumbnail(
                    thumbnail_box.state.current_index
                )

    def reload_currently_displayed_filtered_sequences(self):
        sort_method = (
            self.sequence_picker.control_panel.sort_widget.settings_manager.browse_settings.get_sort_method()
        )
        self.sort_and_display_currently_filtered_sequences_by_method(sort_method)
        self.update_ui(
            self.section_manager.get_sorted_sections(
                sort_method, self.browse_tab.sequence_picker.sections.keys()
            ),
            sort_method,
        )
