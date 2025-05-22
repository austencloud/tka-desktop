# src/main_window/main_widget/sequence_card_tab/components/display/printable_displayer.py
import os
from typing import Dict, List, Any, Tuple, Optional, TYPE_CHECKING
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
    QScrollArea,
)
from PyQt6.QtGui import QPixmap, QImage, QFont, QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QSize, QRect, QPoint

from utils.path_helpers import get_sequence_card_image_exporter_path
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from ..pages.printable_layout import PrintablePageLayout, PaperSize, PaperOrientation
from ..pages.printable_factory import PrintablePageFactory

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class PrintableDisplayer:
    """
    Displays sequence cards in a print-friendly layout with multiple page previews side-by-side.

    This class:
    1. Arranges sequence cards in a grid optimized for printing
    2. Shows multiple page previews side-by-side
    3. Implements vertical scrolling for browsing pages
    4. Removes redundant headers from card containers
    5. Ensures the layout matches standard paper sizes
    """

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.nav_sidebar = sequence_card_tab.nav_sidebar

        # Create printable page factory
        self.page_factory = PrintablePageFactory(sequence_card_tab)

        # Layout settings
        self.columns_per_row = 2  # Number of page previews per row
        self.page_spacing = 20  # Spacing between page previews

        # Current page tracking
        self.pages = []
        self.current_page_index = -1
        self.current_position = 0  # Position within the current page

        # Simple in-memory cache for the current session
        self.image_cache: Dict[str, QPixmap] = {}

    def set_columns_per_row(self, columns: int):
        """Set the number of page previews to display per row."""
        if columns < 1:
            columns = 1
        elif columns > 4:
            columns = 4
        self.columns_per_row = columns

    def set_paper_size(self, paper_size: PaperSize):
        """Set the paper size for page previews."""
        self.page_factory.set_paper_size(paper_size)

    def set_orientation(self, orientation: PaperOrientation):
        """Set the orientation for page previews."""
        self.page_factory.set_orientation(orientation)

    def display_sequences(
        self, selected_length: int = None, show_progress_dialog: bool = True
    ):
        """
        Display sequence card images in a print-friendly layout.

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

            # Create multi-column layout for page previews
            self._create_multi_column_layout()

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
                            self._add_image_to_page(label)
                except Exception as e:
                    print(f"Error processing {sequence.get('path', 'unknown')}: {e}")

                # Keep UI responsive
                QApplication.processEvents()

            # Update UI
            if progress:
                progress.setValue(total_sequences)

            # Update description label with final count
            self.sequence_card_tab.description_label.setText(
                f"Showing {len(filtered_sequences)} {length_text} sequences across {len(self.pages)} pages"
            )

        except Exception as e:
            print(f"Error displaying sequences: {e}")
            import traceback

            traceback.print_exc()
            self.sequence_card_tab.description_label.setText(f"Error: {str(e)}")
        finally:
            # Reset cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def _create_multi_column_layout(self):
        """Create a multi-column layout for page previews."""
        # Clear the scroll layout
        if hasattr(self.sequence_card_tab, "scroll_layout"):
            while self.sequence_card_tab.scroll_layout.count():
                item = self.sequence_card_tab.scroll_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)

        # Create a grid layout for the page previews
        self.preview_grid = QGridLayout()
        self.preview_grid.setSpacing(self.page_spacing)
        self.preview_grid.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        # Add the grid layout to the scroll layout
        self.sequence_card_tab.scroll_layout.addLayout(self.preview_grid)

    def _clear_existing_pages(self):
        """Clear all existing pages."""
        # Reset page tracking
        self.pages = []
        self.current_page_index = -1
        self.current_position = 0

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

            # Get cell size from page factory
            cell_size = self.page_factory.get_cell_size()

            # Calculate target size to fit within the cell
            # Leave some margin within the cell
            margin = 10
            target_width = cell_size.width() - (margin * 2)

            # Calculate proportional height
            aspect_ratio = image.height() / image.width()
            target_height = int(target_width * aspect_ratio)

            # If the height exceeds the cell height, scale down
            if target_height > (cell_size.height() - (margin * 2)):
                target_height = cell_size.height() - (margin * 2)
                target_width = int(target_height / aspect_ratio)

            # Update card aspect ratio in page factory for future pages
            if self.current_page_index == -1:
                self.page_factory.update_card_aspect_ratio(
                    image.width() / image.height()
                )

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
        """Create a label for displaying the image without redundant header."""
        # Create a simple image label without the header
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(False)

        # Set size policy
        image_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        image_label.setFixedSize(pixmap.size())

        return image_label

    def _add_image_to_page(self, label: QWidget):
        """Add image to page, creating new pages as needed."""
        # Check if we need to create a new page
        if self.current_page_index == -1 or self._is_current_page_full():
            self._create_new_page()

        # Get the current page and its grid layout
        page = self.pages[self.current_page_index]
        grid_layout = page.layout()

        # Get the current position as row and column
        positions = self.page_factory.get_grid_positions()
        if self.current_position < len(positions):
            row, col = positions[self.current_position]

            # Add the label to the grid
            grid_layout.addWidget(label, row, col, Qt.AlignmentFlag.AlignCenter)

            # Update position for next image
            self.current_position += 1

    def _create_new_page(self):
        """Create a new page for displaying images."""
        # Create a new page
        new_page = self.page_factory.create_page()

        # Add to pages list
        self.pages.append(new_page)

        # Add to preview grid
        row = len(self.pages) - 1
        col = row % self.columns_per_row
        row = row // self.columns_per_row

        self.preview_grid.addWidget(new_page, row, col)

        # Update page number label
        page_number_label = new_page.findChild(QLabel, "pageNumberLabel")
        if page_number_label:
            page_number_label.setText(f"Page {len(self.pages)}")

        # Update current page index
        self.current_page_index = len(self.pages) - 1

        # Reset position within the page
        self.current_position = 0

    def _is_current_page_full(self) -> bool:
        """Check if the current page is full."""
        # Get the total number of positions in the grid
        total_positions = len(self.page_factory.get_grid_positions())

        # Check if we've used all positions
        return self.current_position >= total_positions
