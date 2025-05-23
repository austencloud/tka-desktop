# src/main_window/main_widget/sequence_card_tab/components/display/page_renderer.py
import logging
from typing import List, Dict, Any, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy, QGridLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.components.display.sequence_display_manager import (
        DisplayConfig,
    )
    from ..pages.printable_factory import PrintablePageFactory
    from .layout_calculator import LayoutCalculator


class PageRenderer:
    """
    Creates and manages page instances and image labels for sequence card display.

    This class combines the functionality of the former ImageLabelFactory and PageFactory
    classes into a single cohesive component responsible for:

    1. Creating new page instances with proper sizing
    2. Creating and configuring image labels
    3. Applying scale factors for consistent display
    4. Managing page properties and styling
    5. Adding pages to the preview grid
    """

    def __init__(
        self,
        page_factory: "PrintablePageFactory",
        layout_calculator: "LayoutCalculator",
        config: "DisplayConfig",
        preview_grid=None,
    ):
        self.page_factory = page_factory
        self.layout_calculator = layout_calculator
        self.config = config
        self.preview_grid = preview_grid
        self.pages: List[QWidget] = []

        if self.preview_grid is None:
            logging.warning(
                "Preview grid not provided to PageRenderer. Pages will not be displayed in the UI."
            )

    def set_preview_grid(self, preview_grid: QGridLayout) -> None:
        """Set the preview grid for adding pages."""
        logging.debug(
            f"Setting preview grid: {preview_grid}, type: {type(preview_grid)}"
        )
        self.preview_grid = preview_grid
        logging.debug(f"After setting, self.preview_grid: {self.preview_grid}")

    def clear_pages(self) -> None:
        """Clear all pages."""
        self.pages = []

    def create_new_page(self) -> QWidget:
        """
        Create a new page for displaying images.
        Ensures the page has a QGridLayout for its internal content.
        """
        # Create a new page using the page factory
        new_page = self.page_factory.create_page()

        # --- ENHANCED LAYOUT VALIDATION: Ensure page has a layout ---
        if new_page.layout() is None:
            # If the factory didn't provide a page with a layout, create and set one.
            page_internal_layout = QGridLayout(
                new_page
            )  # Sets 'page_internal_layout' on 'new_page'
            page_internal_layout.setSpacing(5)  # Set spacing for items on the page
            page_internal_layout.setContentsMargins(10, 10, 10, 10)
            page_internal_layout.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
            )
            logging.warning(
                f"Page widget created by factory (object: {new_page}) had no layout. "
                f"A new QGridLayout ({page_internal_layout}) was added by PageRenderer."
            )
        else:
            # Verify the layout is a QGridLayout
            if not isinstance(new_page.layout(), QGridLayout):
                logging.warning(
                    f"Page has a layout but it's not a QGridLayout. Replacing it."
                )
                old_layout = new_page.layout()
                # Remove the old layout
                while old_layout.count():
                    item = old_layout.takeAt(0)
                    if item.widget():
                        item.widget().setParent(None)

                # Create a new QGridLayout
                page_internal_layout = QGridLayout(new_page)
                page_internal_layout.setSpacing(5)
                page_internal_layout.setContentsMargins(10, 10, 10, 10)
                page_internal_layout.setAlignment(
                    Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
                )
            else:
                logging.debug(f"Page already has a QGridLayout: {new_page.layout()}")
        # --- END ENHANCED LAYOUT VALIDATION ---

        # Calculate the optimal page size based on available width and column count
        optimal_size = self.layout_calculator.calculate_optimal_page_size()

        # Scale the page to the optimal size while maintaining aspect ratio
        original_size = new_page.size()

        scale_factor = self.layout_calculator.calculate_scale_factor(
            original_size, optimal_size
        )

        new_width = int(original_size.width() * scale_factor)
        new_height = int(original_size.height() * scale_factor)
        new_page.setFixedSize(new_width, new_height)
        new_page.setProperty("scale_factor", scale_factor)

        # Store the page in our internal list
        self.pages.append(new_page)
        page_index = len(self.pages) - 1
        logging.debug(f"Created page {page_index} with layout: {new_page.layout()}")

        # Add to preview grid if available (this is the grid of pages, not the page's internal grid)
        if self.preview_grid is not None and hasattr(self.preview_grid, "addWidget"):
            row = page_index // self.config.columns_per_row
            col = page_index % self.config.columns_per_row
            try:
                self.preview_grid.addWidget(new_page, row, col)
                logging.debug(
                    f"Successfully added page to preview grid at position ({row}, {col})"
                )
            except Exception as e:
                logging.error(f"Error adding page to preview grid: {e}")
        else:
            logging.error(
                f"Preview grid is None or invalid in PageRenderer. Cannot add page to UI. Grid: {self.preview_grid}"
            )

        # Update page number label if it exists
        page_number_label = new_page.findChild(QLabel, "pageNumberLabel")
        if page_number_label:
            # Remove the page number label from its current parent
            page_number_label.setParent(None)

            # Get the page's layout
            page_layout = new_page.layout()

            # Create a proper layout for the page that includes the page number at the bottom
            if isinstance(page_layout, QGridLayout):
                # Create a new vertical layout to contain both the grid and the page number

                # Take all widgets from the grid layout
                grid_items = []
                while page_layout.count():
                    item = page_layout.takeAt(0)
                    grid_items.append(item)

                # Create a new grid layout for the content
                content_grid = QGridLayout()
                content_grid.setSpacing(page_layout.spacing())
                content_grid.setContentsMargins(page_layout.contentsMargins())

                # Add the items back to the content grid
                for item in grid_items:
                    if item.widget():
                        row, column, rowSpan, columnSpan = page_layout.getItemPosition(
                            page_layout.indexOf(item.widget())
                        )
                        content_grid.addWidget(
                            item.widget(), row, column, rowSpan, columnSpan
                        )

                # Create a new vertical layout
                vbox = QVBoxLayout(new_page)
                vbox.setContentsMargins(page_layout.contentsMargins())
                vbox.setSpacing(5)

                # Add the content grid and page number to the vertical layout
                vbox.addLayout(content_grid, 1)  # Content grid takes most of the space

                # Update the page number label
                page_number_label.setText(f"Page {len(self.pages)}")
                font = page_number_label.font()
                font.setPointSize(max(8, int(10 * scale_factor)))
                page_number_label.setFont(font)
                page_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Add the page number label to the bottom of the vertical layout
                vbox.addWidget(page_number_label, 0, Qt.AlignmentFlag.AlignCenter)
            else:
                # Fallback to the old method if the layout is not a QGridLayout
                page_number_label.setText(f"Page {len(self.pages)}")
                font = page_number_label.font()
                font.setPointSize(max(8, int(10 * scale_factor)))
                page_number_label.setFont(font)
                page_number_label.setParent(new_page)
                page_number_label.setGeometry(0, new_height - 20, new_width, 20)
                page_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Final validation before returning
        if new_page.layout() is None:
            logging.error(
                f"CRITICAL: Page {page_index} still has no layout after all attempts to add one!"
            )
            # Last resort emergency fix
            emergency_layout = QGridLayout(new_page)
            emergency_layout.setContentsMargins(10, 10, 10, 10)
            emergency_layout.setSpacing(5)
            logging.warning(
                f"Emergency layout {emergency_layout} added to page {page_index}"
            )

        return new_page

    def create_image_label(self, sequence: Dict[str, Any], pixmap: QPixmap) -> QLabel:
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

    def is_page_full(self, current_position: int) -> bool:
        """
        Check if the current page is full.

        Args:
            current_position: Current position within the page

        Returns:
            bool: True if the page is full, False otherwise
        """
        # Get the total number of positions in the grid
        total_positions = len(self.page_factory.get_grid_positions())

        # Log the check for debugging
        logging.debug(
            f"Checking if page is full: position {current_position} of {total_positions} positions"
        )

        # Check if we've used all positions
        is_full = current_position >= total_positions

        if is_full:
            logging.debug(f"Page is full at position {current_position}")

        return is_full
