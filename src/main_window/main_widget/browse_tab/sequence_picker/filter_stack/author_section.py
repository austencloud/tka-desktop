from typing import TYPE_CHECKING, Tuple
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
from functools import partial

from main_window.main_widget.metadata_extractor import MetaDataExtractor
from utils.path_helpers import get_data_path, get_image_path
from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from .sequence_picker_filter_stack import SequencePickerFilterStack


class AuthorSection(FilterSectionBase):
    IMAGE_DIR = get_image_path("author_images")
    MAX_COLUMNS = 3

    def __init__(self, initial_selection_widget: "SequencePickerFilterStack"):
        super().__init__(initial_selection_widget, "Select by Author:")
        self.main_widget = initial_selection_widget.browse_tab.main_widget
        self.buttons: dict[str, QPushButton] = {}
        self.tally_labels: dict[str, QLabel] = {}
        self.author_labels: dict[str, QLabel] = {}
        self.original_pixmaps: dict[str, QPixmap] = {}
        self.sequence_counts: dict[str, int] = {}
        self.add_buttons()

    def add_buttons(self):
        """Initialize the UI components for the author selection."""
        self.go_back_button.show()
        self.header_label.show()
        layout: QVBoxLayout = self.layout()

        # Get unique authors and their sequence counts
        self.sequence_counts = self._get_sequence_counts_per_author()
        self.authors = sorted(self.sequence_counts.keys())

        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(20)

        row, col = 0, 0
        for author in self.authors:
            author_vbox = self.create_author_vbox(author)
            grid_layout.addLayout(author_vbox, row, col)

            col += 1
            if col >= self.MAX_COLUMNS:
                col = 0
                row += 1

        layout.addLayout(grid_layout)
        layout.addStretch(1)

    def create_author_vbox(self, author: str) -> QVBoxLayout:
        """Create a vertical box layout containing all components for an author."""
        author_vbox = QVBoxLayout()
        author_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = self.create_author_button(author)
        sequence_count_label = self.create_sequence_count_label(author)

        author_vbox.addWidget(button)
        author_vbox.addItem(
            QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        author_vbox.addWidget(sequence_count_label)

        return author_vbox

    def create_author_button(self, author: str) -> QPushButton:
        """Create and configure the author selection button."""
        button = QPushButton(author)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(partial(self.handle_author_click, author))
        self.buttons[author] = button
        return button

    def create_sequence_count_label(self, author: str) -> QLabel:
        """Create a label displaying the sequence count for an author."""
        count = self.sequence_counts.get(author, 0)
        sequence_text = "sequence" if count == 1 else "sequences"
        sequence_count_label = QLabel(f"{count} {sequence_text}")
        sequence_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tally_labels[author] = sequence_count_label
        return sequence_count_label

    def handle_author_click(self, author: str):
        """Handle clicks on author buttons."""
        self.browse_tab.filter_controller.apply_filter({"author": author})

    def _get_all_sequences_with_authors(self) -> list[Tuple[str, list[str], str]]:
        """Retrieve and cache all sequences along with their authors."""
        if hasattr(self, "_all_sequences_with_authors"):
            return self._all_sequences_with_authors

        dictionary_dir = get_data_path("generated_data\dictionary")
        base_words = [
            (
                word,
                self.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, word)
                ),
            )
            for word in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, word))
            and "__pycache__" not in word
        ]

        sequences_with_authors = []
        for word, thumbnails in base_words:
            author = self.get_sequence_author(thumbnails)
            if author is not None:
                sequences_with_authors.append((word, thumbnails, author))

        self._all_sequences_with_authors = sequences_with_authors
        return sequences_with_authors

    def _get_sequence_counts_per_author(self) -> dict[str, int]:
        """Compute the number of sequences available for each author."""
        author_counts: dict[str, int] = {}
        sequences_with_authors = self._get_all_sequences_with_authors()
        for _, _, author in sequences_with_authors:
            author_counts[author] = author_counts.get(author, 0) + 1
        return author_counts

    def get_sequences_by_author(self, author: str) -> list[Tuple[str, list[str]]]:
        """Retrieve sequences that correspond to a specific author."""
        sequences_with_authors = self._get_all_sequences_with_authors()
        return [
            (word, thumbnails)
            for word, thumbnails, seq_author in sequences_with_authors
            if seq_author == author
        ]

    def get_sequence_author(self, thumbnails: list[str]) -> str:
        """Extract the author from the metadata of the thumbnails."""
        for thumbnail in thumbnails:
            author = MetaDataExtractor().get_author(thumbnail)
            if author:
                return author
        return None

    def get_sequence_length_from_thumbnails(self, thumbnails: list[str]) -> int:
        """Extract the sequence length from the thumbnails' metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_length(thumbnail)
            if length is not None:
                return length
        return 0

    def resizeEvent(self, event):
        """Handle resizing of the author section."""
        self.resize_buttons()
        self.resize_labels()
        super().resizeEvent(event)

    def resize_labels(self):
        """Adjust font sizes of labels during resizing."""
        font_size_label = max(10, self.main_widget.width() // 140)
        font_size_header = max(12, self.main_widget.width() // 100)

        for label in self.tally_labels.values():
            font = label.font()
            font.setPointSize(font_size_label)
            label.setFont(font)

        font = self.header_label.font()
        font.setPointSize(font_size_header)
        self.header_label.setFont(font)

    def resize_buttons(self):
        """Adjust button sizes and fonts during resizing."""
        button_width = max(1, self.main_widget.width() // 6)
        button_height = max(1, self.main_widget.height() // 16)
        font_size_button = max(10, self.main_widget.width() // 100)

        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(font_size_button)
            button.setFont(font)
            button.setFixedSize(button_width, button_height)
