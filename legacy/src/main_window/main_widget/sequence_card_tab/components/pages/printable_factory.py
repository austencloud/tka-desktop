# src/main_window/main_widget/sequence_card_tab/components/pages/printable_factory.py
from typing import TYPE_CHECKING, Tuple
from PyQt6.QtWidgets import QWidget, QGridLayout, QFrame, QLabel
from PyQt6.QtCore import Qt, QSize

from .printable_layout import PrintablePageLayout, PaperSize, PaperOrientation

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class PrintablePageFactory:
    """
    Factory for creating printable sequence card pages with standard paper sizes.

    This class creates pages that:
    1. Match standard paper dimensions (A4, Letter, etc.)
    2. Have proper margins for printing
    3. Use a grid layout optimized for the content
    4. Show visual indicators for printable areas
    """

    def __init__(
        self,
        sequence_card_tab: "SequenceCardTab",
        paper_size: PaperSize = PaperSize.A4,
        orientation: PaperOrientation = PaperOrientation.PORTRAIT,
    ):
        self.sequence_card_tab = sequence_card_tab
        self.page_layout = PrintablePageLayout(paper_size, orientation)

        # Default grid configuration
        self.rows = 3
        self.columns = 2

        # Track card aspect ratio for optimal layout
        self.card_aspect_ratio = 0.7  # Default, will be updated based on actual cards

    def set_paper_size(self, paper_size: PaperSize):
        """Set the paper size for new pages."""
        self.page_layout = PrintablePageLayout(paper_size, self.page_layout.orientation)

    def set_orientation(self, orientation: PaperOrientation):
        """Set the orientation for new pages."""
        self.page_layout = PrintablePageLayout(self.page_layout.paper_size, orientation)

    def set_grid_dimensions(self, rows: int, columns: int):
        """
        Set the grid dimensions for new pages.

        This determines the internal grid layout of each page (how many sequence images per page)
        and is NOT affected by the UI preview columns setting.

        Args:
            rows: Number of rows in the grid
            columns: Number of columns in the grid
        """
        self.rows = rows
        self.columns = columns

    def update_card_aspect_ratio(self, aspect_ratio: float):
        """Update the card aspect ratio and recalculate optimal grid."""
        self.card_aspect_ratio = aspect_ratio
        self.rows, self.columns = self.page_layout.calculate_optimal_grid(aspect_ratio)

    def create_page(self) -> QWidget:
        """
        Create a new printable page with proper dimensions and grid layout.

        Returns:
            QWidget: A new page widget with grid layout matching paper dimensions
        """
        # Create page widget with proper dimensions
        page = QFrame()
        page.setObjectName("printableSequenceCardPage")

        # Set the page size to match the paper size
        page_size = self.page_layout.get_page_size_px()
        page.setFixedSize(page_size)

        # Set up grid layout with proper margins
        content_rect = self.page_layout.get_content_rect_px()
        grid_layout = QGridLayout(page)
        grid_layout.setContentsMargins(
            content_rect.left(),
            content_rect.top(),
            page_size.width() - content_rect.right(),
            page_size.height() - content_rect.bottom(),
        )

        # Explicitly set the layout on the page - this is crucial
        page.setLayout(grid_layout)

        # Calculate spacing based on content area and grid dimensions
        # Reduced divisor to create smaller spacing between images
        h_spacing = content_rect.width() // (self.columns * 40)  # Reduced from 20 to 40
        v_spacing = content_rect.height() // (self.rows * 40)  # Reduced from 20 to 40
        grid_layout.setHorizontalSpacing(h_spacing)
        grid_layout.setVerticalSpacing(v_spacing)

        # Center the grid in the content area
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Apply styling for print preview
        page.setStyleSheet(
            """
            #printableSequenceCardPage {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """
        )

        # Add page number placeholder at the bottom
        self._add_page_number_placeholder(page)

        # Verify the layout was properly set
        if page.layout() is None:
            # Try again with a different approach
            emergency_layout = QGridLayout()
            emergency_layout.setContentsMargins(10, 10, 10, 10)
            emergency_layout.setSpacing(5)
            page.setLayout(emergency_layout)

        return page

    def _add_page_number_placeholder(self, page: QWidget):
        """Add a page number placeholder at the bottom of the page."""
        label = QLabel("Page #")
        label.setObjectName("pageNumberLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            """
            #pageNumberLabel {
                color: #7f8c8d;
                font-size: 10px;
                font-style: italic;
            }
        """
        )

        # Position at the bottom center of the page
        label.setParent(page)
        label.setGeometry(0, page.height() - 20, page.width(), 20)

    def create_empty_page(self, message: str = "No sequences found") -> QWidget:
        """
        Create an empty printable page with a message.

        Args:
            message: Message to display on the empty page

        Returns:
            QWidget: An empty page with a message
        """
        # Create a standard page
        page = self.create_page()

        # Add a message label in the center
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet(
            """
            color: #7f8c8d;
            font-size: 16px;
            font-style: italic;
        """
        )

        # Position in the center of the content area
        content_rect = self.page_layout.get_content_rect_px()
        label.setParent(page)
        label.setGeometry(content_rect)

        return page

    def get_cell_size(self) -> QSize:
        """Get the size of each grid cell based on current settings."""
        return self.page_layout.get_grid_cell_size(self.rows, self.columns)

    def get_grid_positions(self) -> list[Tuple[int, int]]:
        """Get all grid positions as (row, column) tuples."""
        positions = []
        for row in range(self.rows):
            for col in range(self.columns):
                positions.append((row, col))
        return positions
