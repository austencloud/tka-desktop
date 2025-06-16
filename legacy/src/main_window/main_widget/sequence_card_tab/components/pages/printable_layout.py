# src/main_window/main_widget/sequence_card_tab/components/pages/printable_layout.py
from enum import Enum
from typing import Tuple
from PyQt6.QtCore import QSize, QRect


class PaperSize(Enum):
    """Standard paper sizes in points (1/72 inch)."""

    A4 = (595, 842)  # 210mm x 297mm at 72 DPI
    LETTER = (612, 792)  # 8.5" x 11" at 72 DPI
    LEGAL = (612, 1008)  # 8.5" x 14" at 72 DPI
    TABLOID = (792, 1224)  # 11" x 17" at 72 DPI


class PaperOrientation(Enum):
    """Paper orientation options."""

    PORTRAIT = 0
    LANDSCAPE = 1


class PrintablePageLayout:
    """
    Manages layout calculations for printable pages with standard paper sizes.

    This class handles:
    1. Standard paper size dimensions
    2. Margins and content area calculations
    3. Grid layout for sequence cards
    4. Scaling calculations for display vs. print
    """

    # Default margins in points (1/72 inch)
    DEFAULT_MARGINS = (
        18,
        36,
        18,
        36,
    )  # left, top, right, bottom (reduced horizontal margins)

    # Default DPI for screen display
    SCREEN_DPI = 96

    # Default DPI for printing
    PRINT_DPI = 300

    def __init__(
        self,
        paper_size: PaperSize = PaperSize.A4,
        orientation: PaperOrientation = PaperOrientation.PORTRAIT,
        margins: Tuple[int, int, int, int] = DEFAULT_MARGINS,
        screen_dpi: int = SCREEN_DPI,
        print_dpi: int = PRINT_DPI,
    ):
        self.paper_size = paper_size
        self.orientation = orientation
        self.margins = margins
        self.screen_dpi = screen_dpi
        self.print_dpi = print_dpi

        # Calculate page dimensions
        self._calculate_dimensions()

    def _calculate_dimensions(self):
        """Calculate page dimensions based on paper size and orientation."""
        width, height = self.paper_size.value

        # Swap dimensions for landscape orientation
        if self.orientation == PaperOrientation.LANDSCAPE:
            width, height = height, width

        self.page_width_pts = width
        self.page_height_pts = height

        # Calculate content area (excluding margins)
        left, top, right, bottom = self.margins
        self.content_width_pts = width - left - right
        self.content_height_pts = height - top - bottom

        # Calculate screen dimensions (for display)
        scale_factor = self.screen_dpi / 72  # Convert from points to pixels
        self.page_width_px = int(width * scale_factor)
        self.page_height_px = int(height * scale_factor)
        self.content_width_px = int(self.content_width_pts * scale_factor)
        self.content_height_px = int(self.content_height_pts * scale_factor)

    def get_page_size_px(self) -> QSize:
        """Get the page size in pixels for screen display."""
        return QSize(self.page_width_px, self.page_height_px)

    def get_content_rect_px(self) -> QRect:
        """Get the content rectangle in pixels for screen display."""
        left, top, _, _ = self.margins
        left_px = int(left * self.screen_dpi / 72)
        top_px = int(top * self.screen_dpi / 72)
        return QRect(left_px, top_px, self.content_width_px, self.content_height_px)

    def get_grid_cell_size(self, rows: int, cols: int) -> QSize:
        """
        Calculate the size of each grid cell based on the number of rows and columns.

        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid

        Returns:
            QSize: Size of each grid cell in pixels
        """
        content_rect = self.get_content_rect_px()
        cell_width = content_rect.width() // cols
        cell_height = content_rect.height() // rows
        return QSize(cell_width, cell_height)

    def calculate_optimal_grid(self, card_aspect_ratio: float) -> Tuple[int, int]:
        """
        Calculate the optimal grid layout (rows x columns) for the given card aspect ratio.

        Args:
            card_aspect_ratio: Width/height ratio of the sequence cards

        Returns:
            Tuple[int, int]: Optimal (rows, columns) for the grid
        """
        # Start with a reasonable default
        best_rows, best_cols = 2, 2
        best_utilization = 0

        # Try different grid configurations
        for rows in range(1, 6):  # Try 1 to 5 rows
            for cols in range(1, 6):  # Try 1 to 5 columns
                # Calculate cell size
                cell_size = self.get_grid_cell_size(rows, cols)

                # Calculate cell aspect ratio
                cell_aspect_ratio = cell_size.width() / cell_size.height()

                # Calculate how well this grid utilizes the page
                # (higher is better, perfect match would be 1.0)
                aspect_match = min(
                    cell_aspect_ratio / card_aspect_ratio,
                    card_aspect_ratio / cell_aspect_ratio,
                )

                # Calculate space utilization (percentage of page filled)
                total_cells = rows * cols
                page_area = self.content_width_px * self.content_height_px
                cells_area = total_cells * cell_size.width() * cell_size.height()
                space_utilization = min(cells_area / page_area, 1.0)

                # Combined score (weighted toward space utilization)
                utilization = (aspect_match * 0.4) + (space_utilization * 0.6)

                if utilization > best_utilization:
                    best_utilization = utilization
                    best_rows, best_cols = rows, cols

        return best_rows, best_cols
