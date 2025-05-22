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
        self.pages: List[QWidget] = []
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

        # Only update if the value has changed
        if self.columns_per_row != columns:
            self.columns_per_row = columns

            # If we have pages displayed, refresh the layout
            if self.pages:
                self.refresh_layout()

    def refresh_layout(self):
        """
        Refresh the layout with the current settings.

        This method:
        1. Clears existing pages and cache
        2. Completely removes all widgets from the layout
        3. Recreates the layout from scratch
        4. Updates grid dimensions based ONLY on sequence length
        5. Reloads all sequences with the new layout
        """
        # Store the current length and cursor
        current_length = self.nav_sidebar.selected_length
        self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)

        print(
            f"DEBUG: refresh_layout called with columns_per_row={self.columns_per_row}, length={current_length}"
        )

        try:
            # STEP 1: Clear existing pages and their widgets
            self._clear_existing_pages()

            # STEP 2: Clear the image cache completely since layout has changed
            cache_size = len(self.image_cache)
            self.image_cache.clear()
            print(f"DEBUG: Cleared image cache ({cache_size} items)")

            # STEP 3: Clear the scroll layout completely
            if hasattr(self.sequence_card_tab, "scroll_layout"):
                # First, store a reference to all items in the layout
                items_to_remove = []
                for i in range(self.sequence_card_tab.scroll_layout.count()):
                    items_to_remove.append(
                        self.sequence_card_tab.scroll_layout.itemAt(i)
                    )

                # Then remove each item
                for item in items_to_remove:
                    if item.widget():
                        widget = item.widget()
                        self.sequence_card_tab.scroll_layout.removeWidget(widget)
                        widget.setParent(None)
                        widget.deleteLater()
                    elif item.layout():
                        # Get the layout
                        layout = item.layout()

                        # Remove all widgets from the sublayout
                        while layout.count():
                            subitem = layout.takeAt(0)
                            if subitem and subitem.widget():
                                widget = subitem.widget()
                                if widget:
                                    widget.setParent(None)
                                    widget.deleteLater()

                        # Remove the layout itself
                        self.sequence_card_tab.scroll_layout.removeItem(item)

                print(f"DEBUG: Completely cleared scroll layout")

            # STEP 4: Force a UI update to ensure the layout is properly cleared
            QApplication.processEvents()

            # STEP 5: Create a new multi-column layout for page previews
            # This controls how many page previews are shown side-by-side in the UI
            self._create_multi_column_layout()
            print(
                f"DEBUG: Created new multi-column layout with {self.columns_per_row} columns per row"
            )

            # STEP 6: Update the page factory grid dimensions based ONLY on sequence length
            # This sets the layout within each page and is NOT affected by columns_per_row
            self._set_optimal_grid_dimensions(current_length)
            print(f"DEBUG: Set optimal grid dimensions for length {current_length}")

            # STEP 7: Re-display the sequences with the new layout
            print(f"DEBUG: Displaying sequences with length {current_length}")
            # Use display_sequences which will handle clearing and regenerating everything
            self.display_sequences(current_length)
        except Exception as e:
            print(f"ERROR in refresh_layout: {e}")
            import traceback

            traceback.print_exc()
        finally:
            # Reset cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def set_paper_size(self, paper_size: PaperSize):
        """Set the paper size for page previews."""
        self.page_factory.set_paper_size(paper_size)

    def set_orientation(self, orientation: PaperOrientation):
        """Set the orientation for page previews."""
        self.page_factory.set_orientation(orientation)

    def display_sequences(self, selected_length: int = None):
        """
        Display sequence card images in a print-friendly layout.

        Args:
            selected_length: The length of sequences to display. If None, use the sidebar selection.
        """
        # STEP 1: Completely clear existing pages and cache
        self._clear_existing_pages()
        self.image_cache.clear()  # Clear image cache to ensure fresh rendering

        # STEP 2: Clear the scroll layout completely
        if (
            hasattr(self.sequence_card_tab, "scroll_layout")
            and self.sequence_card_tab.scroll_layout
        ):
            while self.sequence_card_tab.scroll_layout.count():
                item = self.sequence_card_tab.scroll_layout.takeAt(0)
                if item and item.widget():
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()

        # Force a UI update to ensure the layout is properly cleared
        QApplication.processEvents()

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
            # STEP 3: Get all sequences from the sequence_card_images directory
            images_path = get_sequence_card_image_exporter_path()
            sequences = self._get_all_sequences(images_path)

            # STEP 4: Filter sequences by the selected length
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

            # STEP 5: Set optimal grid dimensions based ONLY on sequence length
            # This sets the layout within each page and is NOT affected by columns_per_row
            self._set_optimal_grid_dimensions(selected_length)

            # STEP 6: Create multi-column layout for page previews
            # This controls how many page previews are shown side-by-side in the UI
            self._create_multi_column_layout()

            # STEP 7: Process each sequence
            for i, sequence in enumerate(filtered_sequences):
                if i % 10 == 0:  # Update description label periodically
                    self.sequence_card_tab.description_label.setText(
                        f"Loading {length_text} sequences... ({i+1}/{total_sequences})"
                    )
                    QApplication.processEvents()

                # Load and display image
                try:
                    image_path = sequence.get("path", "")
                    if image_path and os.path.exists(image_path):
                        # Load image with consistent scaling
                        pixmap = self._load_image_with_consistent_scaling(image_path)

                        if not pixmap.isNull():
                            # Create label and add to page
                            label = self._create_image_label(sequence, pixmap)
                            self._add_image_to_page(label)
                except Exception as e:
                    print(f"Error processing {sequence.get('path', 'unknown')}: {e}")

                # Keep UI responsive
                QApplication.processEvents()

            # STEP 8: Update description label with final count and column information
            self.sequence_card_tab.description_label.setText(
                f"Showing {len(filtered_sequences)} {length_text} sequences across {len(self.pages)} pages in {self.columns_per_row} columns"
            )

        except Exception as e:
            print(f"Error displaying sequences: {e}")
            import traceback

            traceback.print_exc()
            self.sequence_card_tab.description_label.setText(f"Error: {str(e)}")
        finally:
            # Reset cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def _calculate_optimal_page_size(self) -> QSize:
        """
        Calculate the optimal page size based on available width and column count.

        This ensures that:
        1. All page previews fit within the available width
        2. Pages are smaller when more columns are selected
        3. The aspect ratio of each page is maintained
        4. Proper scaling is applied for different column counts

        Returns:
            QSize: The optimal size for each page preview
        """
        print(
            f"DEBUG: _calculate_optimal_page_size called with columns_per_row={self.columns_per_row}"
        )

        # Get the available width of the scroll area
        scroll_area_width = self.sequence_card_tab.scroll_area.width()
        print(f"DEBUG: scroll_area_width={scroll_area_width}")

        # Account for scroll bar width if vertical scrollbar is visible
        if self.sequence_card_tab.scroll_area.verticalScrollBar().isVisible():
            scroll_bar_width = (
                self.sequence_card_tab.scroll_area.verticalScrollBar().width()
            )
            scroll_area_width -= scroll_bar_width
            print(f"DEBUG: Adjusted for scrollbar: -{scroll_bar_width}px")

        # Account for margins and spacing
        side_margins = 40  # 20px margin on each side
        column_spacing = self.page_spacing * (self.columns_per_row - 1)
        available_width = scroll_area_width - side_margins - column_spacing

        print(f"DEBUG: Available width calculation:")
        print(f"DEBUG:   scroll_area_width: {scroll_area_width}")
        print(f"DEBUG:   side_margins: {side_margins}")
        print(f"DEBUG:   column_spacing: {column_spacing}")
        print(f"DEBUG:   available_width: {available_width}")

        # Calculate the maximum width for each page with a minimum size to prevent too small pages
        # Use a more aggressive scaling for higher column counts
        max_page_width = max(300, available_width // self.columns_per_row)

        # Apply a scaling factor based on column count to ensure proper proportional scaling
        # This helps maintain readability even with more columns
        scaling_factor = 1.0
        if self.columns_per_row == 3:
            scaling_factor = 0.95  # Slightly smaller for 3 columns
        elif self.columns_per_row == 4:
            scaling_factor = 0.9  # Even smaller for 4 columns

        max_page_width = int(max_page_width * scaling_factor)

        print(
            f"DEBUG: max_page_width={max_page_width} (available_width / columns_per_row * {scaling_factor})"
        )

        # Get the original page size and aspect ratio
        original_size = self.page_factory.page_layout.get_page_size_px()
        aspect_ratio = original_size.height() / original_size.width()
        print(
            f"DEBUG: original_size={original_size.width()}x{original_size.height()}, aspect_ratio={aspect_ratio}"
        )

        # Calculate the new height based on the aspect ratio
        new_height = int(max_page_width * aspect_ratio)
        print(f"DEBUG: new_height={new_height} (max_page_width * aspect_ratio)")

        # Return the new size
        new_size = QSize(max_page_width, new_height)
        print(
            f"DEBUG: Returning optimal page size: {new_size.width()}x{new_size.height()}"
        )
        return new_size

    def _create_multi_column_layout(self):
        """Create a multi-column layout for page previews."""
        # Clear the scroll layout
        if (
            hasattr(self.sequence_card_tab, "scroll_layout")
            and self.sequence_card_tab.scroll_layout
        ):
            while self.sequence_card_tab.scroll_layout.count():
                item = self.sequence_card_tab.scroll_layout.takeAt(0)
                if item and item.widget():
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()

        # Create a grid layout for the page previews
        self.preview_grid = QGridLayout()
        self.preview_grid.setSpacing(self.page_spacing)
        self.preview_grid.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        # Add the grid layout to the scroll layout
        self.sequence_card_tab.scroll_layout.addLayout(self.preview_grid)

    def _clear_existing_pages(self):
        """
        Clear all existing pages and remove them from the layout.

        This method:
        1. Removes all page widgets from the preview grid
        2. Resets page tracking variables
        3. Forces a UI update to ensure the layout is properly cleared
        """
        # First, remove all widgets from the preview grid if it exists
        if hasattr(self, "preview_grid") and self.preview_grid:
            # Get all widgets from the grid layout
            for i in range(self.preview_grid.count()):
                item = self.preview_grid.itemAt(i)
                if item and item.widget():
                    # Remove the widget from the layout and delete it
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()

            print(f"DEBUG: Removed all widgets from preview grid")

        # Reset page tracking
        self.pages = []
        self.current_page_index = -1
        self.current_position = 0

        # Force a UI update to ensure the layout is properly cleared
        QApplication.processEvents()

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

    def _set_optimal_grid_dimensions(self, sequence_length: int):
        """
        Set optimal grid dimensions based ONLY on sequence length.
        The grid layout within each page is hardcoded based on sequence length
        and is NOT affected by the UI preview columns setting.

        Optimized grid layouts by sequence length:
        - 4-beat sequences: 3×4 grid (12 per page) - Balanced layout with good readability
        - 8-beat sequences: 3×3 grid (9 per page) - Square layout for medium sequences
        - 16-beat sequences: 4×4 grid (16 per page) - Efficient layout for longer sequences
        - Other lengths: Dynamically calculated based on sequence length

        Args:
            sequence_length: The length of sequences being displayed
        """
        print(f"DEBUG: Setting optimal grid dimensions for length={sequence_length}")

        # Define grid dimensions based ONLY on sequence length
        if sequence_length == 4:
            # 4-beat sequences: 3×4 grid (12 per page)
            # This provides a more balanced layout with good readability
            self.page_factory.set_grid_dimensions(4, 3)

        elif sequence_length == 8:
            # 8-beat sequences: 3×3 grid (9 per page)
            # Square layout works well for medium-length sequences
            self.page_factory.set_grid_dimensions(3, 3)

        elif sequence_length == 16:
            # 16-beat sequences: 4×4 grid (16 per page)
            # More efficient layout for longer sequences
            self.page_factory.set_grid_dimensions(4, 4)

        elif sequence_length == 2:
            # 2-beat sequences: 2×3 grid (6 per page)
            # Simple layout for very short sequences
            self.page_factory.set_grid_dimensions(3, 2)

        elif sequence_length == 3:
            # 3-beat sequences: 2×3 grid (6 per page)
            self.page_factory.set_grid_dimensions(3, 2)

        elif sequence_length == 5:
            # 5-beat sequences: 3×2 grid (6 per page)
            self.page_factory.set_grid_dimensions(2, 3)

        elif sequence_length == 6:
            # 6-beat sequences: 3×2 grid (6 per page)
            self.page_factory.set_grid_dimensions(2, 3)

        elif sequence_length == 10:
            # 10-beat sequences: 3×4 grid (12 per page)
            self.page_factory.set_grid_dimensions(4, 3)

        elif sequence_length == 12:
            # 12-beat sequences: 3×4 grid (12 per page)
            self.page_factory.set_grid_dimensions(4, 3)

        else:
            # For other lengths, calculate a reasonable layout
            # For shorter sequences (< 8), use fewer cells per page
            if sequence_length < 8:
                self.page_factory.set_grid_dimensions(3, 2)  # 6 per page
            # For medium sequences (8-12), use a medium number of cells
            elif sequence_length <= 12:
                self.page_factory.set_grid_dimensions(3, 3)  # 9 per page
            # For longer sequences (>12), use more cells per page
            else:
                self.page_factory.set_grid_dimensions(4, 4)  # 16 per page

        print(
            f"DEBUG: Set grid dimensions to rows={self.page_factory.rows}, columns={self.page_factory.columns}"
        )

    def _load_image_with_consistent_scaling(self, image_path: str) -> QPixmap:
        """
        Load image with consistent scaling and high-quality transformation.

        This method ensures:
        1. Consistent relative sizing across all images based on grid dimensions and column count
        2. Proper margins around each image
        3. High-quality scaling using SmoothTransformation
        4. Efficient caching for performance
        5. Images fit completely within their grid cells
        6. Aspect ratio is maintained
        7. No overflow occurs
        8. Proper scaling adjustment based on preview columns

        Args:
            image_path: Path to the image file

        Returns:
            QPixmap: The scaled image
        """
        # Create a cache key that includes both grid dimensions AND column count
        # The columns_per_row setting SHOULD affect the image scaling to ensure proper proportional scaling
        grid_key = f"{self.page_factory.rows}x{self.page_factory.columns}"
        cache_key = f"{image_path}_{grid_key}_{self.columns_per_row}"

        print(
            f"DEBUG: _load_image_with_consistent_scaling - path={os.path.basename(image_path)}, "
            f"grid={grid_key}, columns={self.columns_per_row}"
        )

        # Check cache first with the grid and column-aware key
        if cache_key in self.image_cache:
            print(
                f"DEBUG: Using cached image for {os.path.basename(image_path)} with "
                f"grid {grid_key} and {self.columns_per_row} columns"
            )
            return self.image_cache[cache_key]

        try:
            # Load original image
            image = QImage(image_path)
            if image.isNull():
                print(f"ERROR: Failed to load image {image_path}")
                return QPixmap()

            # Get cell size from page factory - this will be based on current grid dimensions
            cell_size = self.page_factory.get_cell_size()
            print(f"DEBUG: Cell size: {cell_size.width()}x{cell_size.height()}")

            # Get the current page's scale factor if available
            page_scale_factor = 1.0

            # If we have a current page, use its scale factor
            if self.current_page_index >= 0 and self.current_page_index < len(
                self.pages
            ):
                current_page = self.pages[self.current_page_index]
                if current_page.property("scale_factor") is not None:
                    page_scale_factor = current_page.property("scale_factor")
                    print(f"DEBUG: Using page scale factor: {page_scale_factor}")
            # If we don't have a current page (first image), calculate the scale factor
            # that would be used for a new page to ensure consistent sizing
            elif self.current_page_index == -1:
                # Calculate what the scale factor would be for a new page
                # This ensures the first image is sized consistently with subsequent images
                original_size = self.page_factory.page_layout.get_page_size_px()
                optimal_size = self._calculate_optimal_page_size()

                # Calculate scale factor the same way as in _create_new_page
                temp_scale_factor = min(
                    optimal_size.width() / original_size.width(),
                    optimal_size.height() / original_size.height(),
                )

                # Apply column-specific adjustment
                if self.columns_per_row == 3:
                    temp_scale_factor *= 0.98
                elif self.columns_per_row == 4:
                    temp_scale_factor *= 0.95

                page_scale_factor = temp_scale_factor
                print(
                    f"DEBUG: Calculated scale factor for first image: {page_scale_factor}"
                )

            # Apply column-specific scaling adjustment
            column_adjustment = 1.0
            if self.columns_per_row == 3:
                column_adjustment = 0.98
            elif self.columns_per_row == 4:
                column_adjustment = 0.95

            # Calculate margins based on column count - use smaller margins for more columns
            margin_percent = 0.05  # Default 5% margin
            if self.columns_per_row == 3:
                margin_percent = 0.04  # 4% margin for 3 columns
            elif self.columns_per_row == 4:
                margin_percent = 0.03  # 3% margin for 4 columns

            # Calculate available space with consistent margins
            # Use smaller margins for denser layouts
            margin = min(
                15,
                max(
                    3, int(min(cell_size.width(), cell_size.height()) * margin_percent)
                ),
            )

            # Calculate target size to fit within the cell
            available_width = cell_size.width() - (margin * 2)
            available_height = cell_size.height() - (margin * 2)

            # Apply the page scale factor and column adjustment to the available space
            available_width = int(
                available_width * page_scale_factor * column_adjustment
            )
            available_height = int(
                available_height * page_scale_factor * column_adjustment
            )

            print(
                f"DEBUG: Available space: {available_width}x{available_height} with margin={margin}, "
                f"page_scale_factor={page_scale_factor}, column_adjustment={column_adjustment}"
            )

            # Get original aspect ratio
            original_width = image.width()
            original_height = image.height()
            aspect_ratio = original_height / original_width

            # Calculate target dimensions to fit within available space
            # while maintaining aspect ratio
            if available_width * aspect_ratio <= available_height:
                # Width-constrained
                target_width = available_width
                target_height = int(target_width * aspect_ratio)
            else:
                # Height-constrained
                target_height = available_height
                target_width = int(target_height / aspect_ratio)

            print(f"DEBUG: Target size: {target_width}x{target_height}")

            # Update card aspect ratio in page factory for future pages
            if self.current_page_index == -1:
                self.page_factory.update_card_aspect_ratio(
                    original_width / original_height
                )

            # Scale image with high-quality transformation
            scaled_image = image.scaled(
                target_width,
                target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Convert to pixmap
            pixmap = QPixmap.fromImage(scaled_image)

            print(f"DEBUG: Final pixmap size: {pixmap.width()}x{pixmap.height()}")

            # Cache the pixmap with the grid and column-aware key
            self.image_cache[cache_key] = pixmap

            return pixmap

        except Exception as e:
            print(f"ERROR loading image {image_path}: {e}")
            import traceback

            traceback.print_exc()
            return QPixmap()

    def _load_image(self, image_path: str) -> QPixmap:
        """
        Legacy method for backward compatibility.
        Use _load_image_with_consistent_scaling instead.
        """
        return self._load_image_with_consistent_scaling(image_path)

    def _create_image_label(self, sequence: Dict[str, Any], pixmap: QPixmap) -> QLabel:
        """
        Create a label for displaying the image without redundant header.

        Args:
            sequence: The sequence data (used for metadata if needed)
            pixmap: The image to display

        Returns:
            QLabel: A label containing the image
        """
        # Create a simple image label without the header
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(False)

        # Store sequence metadata in the label's properties for potential future use
        if sequence and "word" in sequence:
            image_label.setProperty("sequence_word", sequence["word"])
        if (
            sequence
            and "metadata" in sequence
            and "sequence_length" in sequence["metadata"]
        ):
            image_label.setProperty(
                "sequence_length", sequence["metadata"]["sequence_length"]
            )

        # Set size policy
        image_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        image_label.setFixedSize(pixmap.size())

        return image_label

    def _add_image_to_page(self, label: QWidget):
        """Add image to page, creating new pages as needed."""
        if self.current_page_index == -1 or self._is_current_page_full():
            self._create_new_page()

        if self.current_page_index < 0 or self.current_page_index >= len(self.pages):
            print(
                f"ERROR: Invalid page index {self.current_page_index}, pages length: {len(self.pages)}"
            )
            return

        page = self.pages[self.current_page_index]
        grid_layout = page.layout()

        positions = self.page_factory.get_grid_positions()
        if self.current_position < len(positions):
            row, col = positions[self.current_position]
            grid_layout.addWidget(label, row, col, Qt.AlignmentFlag.AlignCenter)
            self.current_position += 1
            print(
                f"DEBUG: Added image to page {self.current_page_index} at position ({row}, {col})"
            )
        else:
            print(
                f"ERROR: Invalid position {self.current_position}, max positions: {len(positions)}"
            )

    def _create_new_page(self):
        """
        Create a new page for displaying images.

        This method:
        1. Creates a new page using the page factory
        2. Calculates the optimal size based on available width and column count
        3. Scales the page proportionally to fit the optimal size
        4. Adds the page to the preview grid
        5. Updates the page number label
        """
        # Create a new page
        new_page = self.page_factory.create_page()

        # Calculate the optimal page size based on available width and column count
        optimal_size = self._calculate_optimal_page_size()

        # Scale the page to the optimal size while maintaining aspect ratio
        original_size = new_page.size()

        print(
            f"DEBUG: _create_new_page - original_size={original_size.width()}x{original_size.height()}"
        )
        print(
            f"DEBUG: _create_new_page - optimal_size={optimal_size.width()}x{optimal_size.height()}"
        )

        # CRITICAL: Calculate scale factor based on optimal size and original size
        # Use the minimum of width and height ratios to ensure the page fits completely
        # This ensures images are properly sized relative to the column count
        scale_factor = min(
            optimal_size.width() / original_size.width(),
            optimal_size.height() / original_size.height(),
        )

        # Apply a column-specific adjustment to ensure proper scaling with different column counts
        # This helps maintain readability even with more columns
        if self.columns_per_row == 3:
            # For 3 columns, apply a slight adjustment to ensure proper scaling
            scale_factor *= 0.98
        elif self.columns_per_row == 4:
            # For 4 columns, apply a more significant adjustment
            scale_factor *= 0.95

        print(
            f"DEBUG: _create_new_page - scale_factor={scale_factor} (adjusted for {self.columns_per_row} columns)"
        )

        # Set the new size
        new_width = int(original_size.width() * scale_factor)
        new_height = int(original_size.height() * scale_factor)

        print(f"DEBUG: _create_new_page - new_size={new_width}x{new_height}")

        # Apply the new size to the page
        new_page.setFixedSize(new_width, new_height)

        # Store the scale factor as a property on the page for use in image scaling
        new_page.setProperty("scale_factor", scale_factor)

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

            # Scale the font size based on the page size
            font = page_number_label.font()
            font.setPointSize(max(8, int(10 * scale_factor)))
            page_number_label.setFont(font)

            # Reposition the label at the bottom
            page_number_label.setGeometry(0, new_height - 20, new_width, 20)

        # Update current page index
        self.current_page_index = len(self.pages) - 1

        # Reset position within the page
        self.current_position = 0

        # Force a UI update to ensure the page is properly displayed
        QApplication.processEvents()

    def _is_current_page_full(self) -> bool:
        """Check if the current page is full."""
        # Get the total number of positions in the grid
        total_positions = len(self.page_factory.get_grid_positions())

        # Check if we've used all positions
        return self.current_position >= total_positions
