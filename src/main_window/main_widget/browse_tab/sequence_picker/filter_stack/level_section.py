from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QEvent, QObject
from PyQt6.QtGui import QPixmap, QPainter, QPen
import os
from functools import partial

from utils.path_helpers import get_data_path, get_image_path
from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from .sequence_picker_filter_stack import SequencePickerFilterStack


class FilterByLevelSection(FilterSectionBase):
    LEVEL_DESCRIPTIONS = {
        1: "Base letters with no turns.",
        2: "Turns added with only radial orientations.",
        3: "Non-radial orientations.",
    }
    AVAILABLE_LEVELS = [1, 2, 3]
    IMAGE_DIR = get_image_path("level_images")

    def __init__(self, initial_selection_widget: "SequencePickerFilterStack"):
        super().__init__(initial_selection_widget, "Select by Difficulty Level:")
        self.main_widget = initial_selection_widget.browse_tab.main_widget
        self.buttons: dict[int, QPushButton] = {}
        self.description_labels: dict[int, QLabel] = {}
        self.level_images: dict[int, QLabel] = {}
        self.tally_labels: dict[int, QLabel] = {}
        self.original_pixmaps: dict[int, QPixmap] = {}
        self.sequence_counts: dict[int, int] = {}
        self.add_buttons()

    def add_buttons(self):
        """Initialize the UI components for the level selection."""
        self.go_back_button.show()
        self.header_label.show()
        layout: QVBoxLayout = self.layout()

        self.sequence_counts = self._get_sequence_counts_per_level()

        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.setHorizontalSpacing(50)
        grid_layout.setVerticalSpacing(30)

        for col, level in enumerate(self.AVAILABLE_LEVELS):
            level_vbox = self.create_level_vbox(level)
            grid_layout.addLayout(level_vbox, 0, col)

        layout.addLayout(grid_layout)
        layout.addStretch(1)
        # self.resizeEvent()

    def create_level_vbox(self, level: int) -> QVBoxLayout:
        """Create a vertical box layout containing all components for a level."""
        level_vbox = QVBoxLayout()
        level_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = self.create_level_button(level)
        description_label = self.create_description_label(level)
        image_placeholder = self.create_image_placeholder(level)
        sequence_count_label = self.create_sequence_count_label(level)

        level_vbox.addWidget(button)
        level_vbox.addWidget(description_label)
        level_vbox.addItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        level_vbox.addWidget(image_placeholder)
        level_vbox.addWidget(sequence_count_label)

        return level_vbox

    def create_level_button(self, level: int) -> QPushButton:
        """Create and configure the level selection button."""
        button = QPushButton(f"Level {level}")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(partial(self.handle_level_click, level))
        self.buttons[level] = button
        return button

    def create_description_label(self, level: int) -> QLabel:
        """Create a label for the level description."""
        description_label = QLabel(self.LEVEL_DESCRIPTIONS.get(level, ""))
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_labels[level] = description_label
        return description_label

    def create_image_placeholder(self, level: int) -> QLabel:
        """Create and configure the image placeholder for a level."""
        image_placeholder = QLabel()
        image_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_placeholder.setProperty("level", level)  # Associate level with the label
        self.level_images[level] = image_placeholder

        image_path = os.path.join(self.IMAGE_DIR, f"level_{level}.png")
        if os.path.exists(image_path):
            original_pixmap = QPixmap(image_path)
            self.original_pixmaps[level] = original_pixmap  # Store the original pixmap

            # Make the image clickable
            image_placeholder.setCursor(Qt.CursorShape.PointingHandCursor)
            image_placeholder.mousePressEvent = partial(self.handle_image_click, level)
            # Install event filter for hover effect
            image_placeholder.installEventFilter(self)
        else:
            image_placeholder.setText("No Image Available")

        return image_placeholder

    def create_sequence_count_label(self, level: int) -> QLabel:
        """Create a label displaying the sequence count for a level."""
        count = self.sequence_counts.get(level, 0)
        sequence_text = "sequence" if count == 1 else "sequences"
        sequence_count_label = QLabel(f"{count} {sequence_text}")
        sequence_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tally_labels[level] = sequence_count_label
        return sequence_count_label

    def handle_level_click(self, level: int):
        """Handle clicks on level buttons."""
        self.browse_tab.filter_controller.apply_filter({"level": level})

    def handle_image_click(self, level: int, event):
        """Handle clicks on level images."""
        self.handle_level_click(level)

    def _get_all_sequences_with_levels(self) -> list[tuple[str, list[str], int]]:
        """Retrieve and cache all sequences along with their levels."""
        if hasattr(self, "_all_sequences_with_levels"):
            return self._all_sequences_with_levels

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

        sequences_with_levels = []
        for word, thumbnails in base_words:
            level = self.get_sequence_level_from_thumbnails(thumbnails)
            if level is not None:
                sequences_with_levels.append((word, thumbnails, level))

        self._all_sequences_with_levels = sequences_with_levels
        return sequences_with_levels

    def _get_sequence_counts_per_level(self) -> dict[int, int]:
        """Compute the number of sequences available for each level."""
        level_counts: dict[int, int] = {}
        sequences_with_levels = self._get_all_sequences_with_levels()
        for _, _, level in sequences_with_levels:
            level_counts[level] = level_counts.get(level, 0) + 1
        return level_counts

    def get_sequences_that_are_a_specific_level(
        self, level: int
    ) -> list[tuple[str, list[str]]]:
        """Retrieve sequences that correspond to a specific level."""
        sequences_with_levels = self._get_all_sequences_with_levels()
        return [
            (word, thumbnails)
            for word, thumbnails, seq_level in sequences_with_levels
            if seq_level == level
        ]

    def get_sequence_level_from_thumbnails(self, thumbnails: list[str]) -> int:
        """Extract the level from the metadata of the thumbnails."""
        for thumbnail in thumbnails:
            level = self.metadata_extractor.get_level(thumbnail)
            if level is not None:
                return level
        return None

    def display_only_thumbnails_with_level(self, level: int):
        """Display only the thumbnails that match the selected level."""
        self.filter_selector.browse_tab.settings.set_current_filter({"level": level})
        self.browse_tab.filter_manager.prepare_ui_for_filtering(
            f"level {level} sequences"
        )

        sequences = self.get_sequences_that_are_a_specific_level(level)
        total_sequences = len(sequences)

        self.browse_tab.sequence_picker.currently_displayed_sequences = [
            (word, thumbnails, self.get_sequence_length_from_thumbnails(thumbnails))
            for word, thumbnails in sequences
        ]

        self.browse_tab.ui_updater.update_and_display_ui(total_sequences)

    def get_sequence_length_from_thumbnails(self, thumbnails: list[str]) -> int:
        """Extract the sequence length from the thumbnails' metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_length(thumbnail)
            if length is not None:
                return length
        return 0

    def apply_hover_effect(self, level: int, label: QLabel):
        """Add a border to the image when hovered."""
        original_pixmap = self.original_pixmaps.get(level)
        if original_pixmap:
            bordered_pixmap = self.add_border_to_pixmap(
                original_pixmap, 4, Qt.GlobalColor.yellow
            )
            scaled_pixmap = self.scale_pixmap(bordered_pixmap)
            label.setPixmap(scaled_pixmap)

    def remove_hover_effect(self, level: int, label: QLabel):
        """Remove the border from the image when not hovered."""
        original_pixmap = self.original_pixmaps.get(level)
        if original_pixmap:
            scaled_pixmap = self.scale_pixmap(original_pixmap)
            label.setPixmap(scaled_pixmap)

    def add_border_to_pixmap(
        self, pixmap: QPixmap, border_width: int, border_color: Qt.GlobalColor
    ) -> QPixmap:
        """Add a border around the pixmap."""
        bordered_pixmap = QPixmap(pixmap.size())
        bordered_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(bordered_pixmap)
        painter.drawPixmap(0, 0, pixmap)

        pen = QPen(border_color)
        pen.setWidth(border_width)
        painter.setPen(pen)
        painter.drawRect(
            border_width // 2,
            border_width // 2,
            pixmap.width() - border_width,
            pixmap.height() - border_width,
        )
        painter.end()
        return bordered_pixmap

    def scale_images(self):
        """Scale all images to fit the current widget size."""
        for level, label in self.level_images.items():
            original_pixmap = self.original_pixmaps.get(level)
            if original_pixmap:
                scaled_pixmap = self.scale_pixmap(original_pixmap)
                label.setPixmap(scaled_pixmap)

    def scale_pixmap(self, pixmap: QPixmap) -> QPixmap:
        """Scale a pixmap to the desired size."""
        size = max(1, self.main_widget.width() // 6)
        return pixmap.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def resizeEvent(self, event):
        """Handle resizing of the level section."""
        self.scale_images()
        self.resize_buttons()
        self.resize_labels()

    def resize_labels(self):
        """Adjust font sizes of labels during resizing."""
        font_size_description = max(10, self.main_widget.width() // 140)
        font_size_header = max(12, self.main_widget.width() // 100)

        for label in self.description_labels.values():
            font = label.font()
            font.setPointSize(font_size_description)
            label.setFont(font)

        for label in self.tally_labels.values():
            font = label.font()
            font.setPointSize(font_size_description)
            label.setFont(font)

        font = self.header_label.font()
        font.setPointSize(font_size_header)
        self.header_label.setFont(font)

    def resize_buttons(self):
        """Adjust button sizes and fonts during resizing."""
        button_width = max(1, self.main_widget.width() // 5)
        button_height = max(1, self.main_widget.height() // 20)
        font_size_button = max(10, self.main_widget.width() // 100)

        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(font_size_button)
            button.setFont(font)
            button.setFixedSize(button_width, button_height)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """Handle hover events to add or remove borders on images."""
        if isinstance(source, QLabel):
            level = source.property("level")
            if level is not None:
                if event.type() == QEvent.Type.Enter:
                    self.apply_hover_effect(level, source)
                    return True
                elif event.type() == QEvent.Type.Leave:
                    self.remove_hover_effect(level, source)
                    return True
        return super().eventFilter(source, event)
