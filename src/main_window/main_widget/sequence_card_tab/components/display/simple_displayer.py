# src/main_window/main_widget/sequence_card_tab/components/display/simple_displayer.py
import os
from typing import Dict, List, Any, TYPE_CHECKING
from PyQt6.QtWidgets import (
    QLabel,
    QGridLayout,
    QProgressDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSizePolicy,
    QApplication,
)
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtCore import Qt, QSize

from utils.path_helpers import get_sequence_card_image_exporter_path
from main_window.main_widget.metadata_extractor import MetaDataExtractor

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.tab import SequenceCardTab


class SimpleSequenceCardDisplayer:
    """
    A simple, synchronous sequence card displayer that avoids threading and complex caching.

    This class:
    1. Loads images directly from disk
    2. Creates pages as needed
    3. Displays images in a grid layout
    4. Processes events after each image to keep the UI responsive
    """

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.nav_sidebar = sequence_card_tab.nav_sidebar
        self.page_factory = sequence_card_tab.page_factory

        # Layout settings
        self.max_images_per_row = 3
        self.max_rows_per_page = 4
        self.image_card_margin = 10

        # Current page tracking
        self.current_page_index = -1
        self.current_row = 0
        self.current_col = 0

        # Simple in-memory cache for the current session
        self.image_cache: Dict[str, QPixmap] = {}

    def display_sequences(
        self, selected_length: int = None, show_progress_dialog: bool = True
    ):
        """
        Display sequence card images for the selected length.

        Args:
            selected_length: The length of sequences to display. If None, use the sidebar selection.
            show_progress_dialog: Whether to show a progress dialog during loading.
        """
        # Clear existing pages
        self._clear_existing_pages()

        # Get selected length from sidebar if not provided
        if selected_length is None:
            selected_length = self.nav_sidebar.selected_length

        # Update UI to show loading state
        self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)
        length_text = f"{selected_length}-step" if selected_length > 0 else "all"
        self.sequence_card_tab.description_label.setText(
            f"Loading {length_text} sequences..."
        )
        QApplication.processEvents()

        try:
            # Get all sequences from the sequence_card_images directory
            images_path = get_sequence_card_image_exporter_path()
            sequences = self._get_all_sequences(images_path)

            # Filter sequences by the selected length
            filtered_sequences = self._filter_sequences_by_length(
                sequences, selected_length
            )

            # Check if we have any sequences to display
            total_sequences = len(filtered_sequences)
            if total_sequences == 0:
                self.sequence_card_tab.description_label.setText(
                    f"No {length_text} sequences found"
                )
                return

            # Create progress tracking
            progress = None
            if (
                show_progress_dialog and total_sequences > 10
            ):  # Only show for larger sets
                progress = QProgressDialog(
                    f"Loading {length_text} sequences...",
                    "Cancel",
                    0,
                    total_sequences,
                    self.sequence_card_tab,
                )
                progress.setWindowTitle("Loading Sequences")
                progress.setWindowModality(Qt.WindowModality.WindowModal)
                progress.setMinimumDuration(500)  # Only show for operations > 500ms

            # Process each sequence
            for i, sequence in enumerate(filtered_sequences):
                # Check for cancellation if we have a progress dialog
                if progress and progress.wasCanceled():
                    break

                # Update progress if we have a dialog
                if progress:
                    progress.setValue(i)
                    progress.setLabelText(
                        f"Processing {sequence.get('word', 'Unknown')} ({i+1}/{total_sequences})"
                    )
                elif i % 10 == 0:  # Update description label periodically if no dialog
                    self.sequence_card_tab.description_label.setText(
                        f"Loading {length_text} sequences... ({i+1}/{total_sequences})"
                    )
                    QApplication.processEvents()

                # Load and display image
                try:
                    image_path = sequence.get("path", "")
                    if image_path and os.path.exists(image_path):
                        # Load image
                        pixmap = self._load_image(image_path)

                        if not pixmap.isNull():
                            # Create label and add to page
                            label = self._create_image_label(sequence, pixmap)
                            self._add_image_to_page(label, pixmap)
                except Exception as e:
                    print(f"Error processing {sequence.get('path', 'unknown')}: {e}")

                # Keep UI responsive
                QApplication.processEvents()

            # Update UI
            if progress:
                progress.setValue(total_sequences)

            # Update description label with final count
            self.sequence_card_tab.description_label.setText(
                f"Showing {len(filtered_sequences)} {length_text} sequences"
            )

        except Exception as e:
            print(f"Error displaying sequences: {e}")
            import traceback

            traceback.print_exc()
            self.sequence_card_tab.description_label.setText(f"Error: {str(e)}")
        finally:
            # Reset cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def _clear_existing_pages(self):
        """Clear all existing pages from the scroll layout."""
        # Reset page tracking
        self.current_page_index = -1
        self.current_row = 0
        self.current_col = 0

        # Clear the sequence_card_tab.pages list
        self.sequence_card_tab.pages = []

        # Clear the scroll layout
        if (
            hasattr(self.sequence_card_tab, "scroll_layout")
            and self.sequence_card_tab.scroll_layout
        ):
            while self.sequence_card_tab.scroll_layout.count():
                item = self.sequence_card_tab.scroll_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
                elif item.layout():
                    # Remove sublayouts
                    while item.layout().count():
                        subitem = item.layout().takeAt(0)
                        if subitem.widget():
                            subitem.widget().setParent(None)

    def _get_all_sequences(self, images_path: str) -> List[Dict[str, Any]]:
        """Get all sequences from the sequence_card_images directory."""
        sequences = []

        # Validate the images path
        if not os.path.exists(images_path):
            print(
                f"Warning: Sequence card images directory does not exist: {images_path}"
            )
            return sequences

        # Process each word folder
        for word in os.listdir(images_path):
            word_path = os.path.join(images_path, word)

            # Skip non-directories and special directories
            if not os.path.isdir(word_path) or word.startswith("__"):
                continue

            # Process each image file
            for file in os.listdir(word_path):
                if file.endswith(".png") and not file.startswith("__"):
                    file_path = os.path.join(word_path, file)

                    # Extract sequence length using the metadata extractor
                    try:
                        # Create a metadata extractor
                        metadata_extractor = MetaDataExtractor()

                        # Get the sequence length from the metadata
                        sequence_length = metadata_extractor.get_length(file_path)

                        # If we couldn't get the length from metadata, default to 0
                        if sequence_length is None:
                            sequence_length = 0

                    except Exception as e:
                        print(f"Error extracting metadata from {file_path}: {e}")
                        sequence_length = 0

                    sequences.append(
                        {
                            "path": file_path,
                            "word": word,
                            "metadata": {
                                "sequence_length": sequence_length,
                                "sequence": word,
                            },
                        }
                    )

        return sequences

    def _filter_sequences_by_length(
        self, sequences: List[Dict[str, Any]], length: int
    ) -> List[Dict[str, Any]]:
        """Filter sequences by the specified length."""
        if length == 0:
            return sequences

        filtered_sequences = []

        for sequence in sequences:
            metadata = sequence.get("metadata", {})
            sequence_length = metadata.get("sequence_length", 0)

            if sequence_length == length:
                filtered_sequences.append(sequence)

        return filtered_sequences

    def _load_image(self, image_path: str) -> QPixmap:
        """Load image with simple scaling."""
        # Check cache first
        if image_path in self.image_cache:
            return self.image_cache[image_path]

        try:
            # Load original image
            image = QImage(image_path)
            if image.isNull():
                return QPixmap()

            # Calculate target size
            target_width = (
                self.sequence_card_tab.width() // self.max_images_per_row
            ) - (self.image_card_margin * 2)

            # Calculate proportional height
            aspect_ratio = image.height() / image.width()
            target_height = int(target_width * aspect_ratio)

            # Scale image
            scaled_image = image.scaled(
                target_width,
                target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Convert to pixmap
            pixmap = QPixmap.fromImage(scaled_image)

            # Cache the pixmap
            self.image_cache[image_path] = pixmap

            return pixmap

        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return QPixmap()

    def _create_image_label(self, sequence: Dict[str, Any], pixmap: QPixmap) -> QLabel:
        """Create a label for displaying the image with metadata."""
        # Create a container widget with border
        container = QFrame()
        container.setFrameShape(QFrame.Shape.Box)
        container.setFrameShadow(QFrame.Shadow.Raised)
        container.setLineWidth(1)
        container.setStyleSheet(
            """
            QFrame {
                background-color: #2c3e50;
                border: 1px solid #34495e;
                border-radius: 5px;
            }
            """
        )

        # Create layout for container
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)

        # Create header with word
        word = sequence.get("word", "Unknown")
        header = QLabel(word)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(
            """
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                font-weight: bold;
            }
            """
        )

        # Create image label
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(False)

        # Add to layout
        layout.addWidget(header)
        layout.addWidget(image_label)

        # Set size policy
        container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        container.setFixedWidth(pixmap.width() + 20)  # Add margin

        return container

    def _add_image_to_page(self, label: QWidget, _: QPixmap = None):
        """Add image to page, creating new pages as needed."""
        # Check if we need to create a new page
        if self.current_page_index == -1 or self._is_current_page_full():
            self._create_new_page()

        # Get the current page layout
        page = self.sequence_card_tab.pages[self.current_page_index]
        page_layout = page.layout()

        # Add the label to the grid
        page_layout.addWidget(label, self.current_row, self.current_col)

        # Update position for next image
        self.current_col += 1
        if self.current_col >= self.max_images_per_row:
            self.current_col = 0
            self.current_row += 1

    def _create_new_page(self):
        """Create a new page for displaying images."""
        # Create a new page
        new_page = self.page_factory.create_page()

        # Add to pages list
        self.sequence_card_tab.pages.append(new_page)

        # Add to scroll layout
        self.sequence_card_tab.scroll_layout.addWidget(new_page)

        # Update current page index
        self.current_page_index += 1

        # Reset row and column
        self.current_row = 0
        self.current_col = 0

    def _is_current_page_full(self) -> bool:
        """Check if the current page is full."""
        return self.current_row >= self.max_rows_per_page
