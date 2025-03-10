from datetime import datetime
import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

from main_window.main_widget.metadata_extractor import MetaDataExtractor
from utils.path_helpers import get_data_path

from ..control_panel.sequence_picker_go_back_button import SequencePickerGoBackButton

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.filter_stack.sequence_picker_filter_stack import (
        SequencePickerFilterStack,
    )


class FilterSectionBase(QWidget):
    def __init__(self, filter_selector: "SequencePickerFilterStack", label_text: str):
        super().__init__(filter_selector)
        self.filter_selector = filter_selector
        self.buttons: dict[str, QPushButton] = {}
        self.sequence_picker = filter_selector.sequence_picker
        self.browse_tab = filter_selector.browse_tab
        self.main_widget = filter_selector.browse_tab.main_widget
        self.metadata_extractor = MetaDataExtractor()
        self._setup_ui(label_text)

        self.initialized = False

    def _setup_ui(self, label_text: str):
        layout = QVBoxLayout(self)

        top_bar_layout = QHBoxLayout()
        self.go_back_button = SequencePickerGoBackButton(
            self.filter_selector.sequence_picker
        )
        self.go_back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.go_back_button.clicked.connect(
            self.filter_selector.show_filter_selection_widget
        )
        top_bar_layout.addWidget(
            self.go_back_button, alignment=Qt.AlignmentFlag.AlignLeft
        )
        top_bar_layout.addStretch(1)

        layout.addLayout(top_bar_layout)

        self.header_label = QLabel(label_text)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header_label)
        layout.addStretch(1)
        self.setLayout(layout)

        self.go_back_button.hide()
        self.header_label.hide()

    def get_sorted_base_words(self, sort_order) -> list[tuple[str, list[str], None]]:
        dictionary_dir = get_data_path("dictionary")
        base_words = [
            (
                d,
                self.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, d)
                ),
                None,
            )
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d)) and "__pycache__" not in d
        ]

        for i, (word, thumbnails, _) in enumerate(base_words):
            sequence_length = self.get_sequence_length_from_thumbnails(thumbnails)

            base_words[i] = (word, thumbnails, sequence_length)

        if sort_order == "sequence_length":
            base_words.sort(key=lambda x: x[2] if x[2] is not None else float("inf"))
        elif sort_order == "date_added":
            base_words.sort(
                key=lambda x: self.filter_selector.sequence_picker.section_manager.get_date_added(
                    x[1]
                )
                or datetime.min,
                reverse=True,
            )
        else:
            base_words.sort(key=lambda x: x[0])
        return base_words

    def get_sequence_length_from_thumbnails(self, thumbnails):
        """Extract the sequence length from the first available thumbnail metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_length(thumbnail)
            if length:
                return length
        return None
