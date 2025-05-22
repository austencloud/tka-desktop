# src/main_window/main_widget/sequence_card_tab/components/display/page_factory.py
from typing import List, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from ..pages.printable_factory import PrintablePageFactory
    from .page_layout_manager import PageLayoutManager


class PageFactory:
    """
    Creates and manages page instances for sequence card display.
    
    This class is responsible for:
    1. Creating new page instances with proper sizing
    2. Applying scale factors for consistent display
    3. Managing page properties and styling
    4. Adding pages to the preview grid
    """
    
    def __init__(
        self, 
        page_factory: "PrintablePageFactory",
        layout_manager: "PageLayoutManager",
        preview_grid = None
    ):
        self.page_factory = page_factory
        self.layout_manager = layout_manager
        self.preview_grid = preview_grid
        self.pages: List[QWidget] = []
        
    def set_preview_grid(self, preview_grid) -> None:
        """Set the preview grid for adding pages."""
        self.preview_grid = preview_grid
        
    def clear_pages(self) -> None:
        """Clear all pages."""
        self.pages = []
        
    def create_new_page(self) -> QWidget:
        """
        Create a new page for displaying images.

        This method:
        1. Creates a new page using the page factory
        2. Calculates the optimal size based on available width and column count
        3. Scales the page proportionally to fit the optimal size
        4. Adds the page to the preview grid
        5. Updates the page number label

        Returns:
            QWidget: The newly created page
        """
        # Create a new page
        new_page = self.page_factory.create_page()

        # Calculate the optimal page size based on available width and column count
        optimal_size = self.layout_manager.calculate_optimal_page_size()

        # Scale the page to the optimal size while maintaining aspect ratio
        original_size = new_page.size()

        print(
            f"DEBUG: create_new_page - original_size={original_size.width()}x{original_size.height()}"
        )
        print(
            f"DEBUG: create_new_page - optimal_size={optimal_size.width()}x{optimal_size.height()}"
        )

        # Calculate scale factor based on optimal size and original size
        scale_factor = self.layout_manager.calculate_scale_factor(original_size, optimal_size)

        print(
            f"DEBUG: create_new_page - scale_factor={scale_factor} (adjusted for {self.layout_manager.columns_per_row} columns)"
        )

        # Set the new size
        new_width = int(original_size.width() * scale_factor)
        new_height = int(original_size.height() * scale_factor)

        print(f"DEBUG: create_new_page - new_size={new_width}x{new_height}")

        # Apply the new size to the page
        new_page.setFixedSize(new_width, new_height)

        # Store the scale factor as a property on the page for use in image scaling
        new_page.setProperty("scale_factor", scale_factor)

        # Add to pages list
        self.pages.append(new_page)

        # Add to preview grid if available
        if self.preview_grid:
            row = len(self.pages) - 1
            col = row % self.layout_manager.columns_per_row
            row = row // self.layout_manager.columns_per_row

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

        # Force a UI update to ensure the page is properly displayed
        QApplication.processEvents()
        
        return new_page
        
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

        # Check if we've used all positions
        return current_position >= total_positions
