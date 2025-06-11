# src/main_window/main_widget/sequence_card_tab/components/display/layout_calculator.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSize


if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.components.display.sequence_display_manager import (
        DisplayConfig,
    )
    from ...tab import SequenceCardTab
    from ..pages.printable_factory import PrintablePageFactory


class LayoutCalculator:
    """
    Manages layout calculations for sequence card pages.

    This class combines the functionality of the former GridLayoutManager and
    PageLayoutManager classes into a single cohesive component responsible for:

    1. Calculating optimal page sizes based on available width and column count
    2. Determining optimal grid dimensions based on sequence length
    3. Applying scaling factors for different column configurations
    4. Maintaining aspect ratios during scaling
    5. Providing consistent sizing across all pages
    """

    def __init__(
        self,
        sequence_card_tab: "SequenceCardTab",
        page_factory: "PrintablePageFactory",
        config: "DisplayConfig",
    ):
        self.sequence_card_tab = sequence_card_tab
        self.page_factory = page_factory
        self.config = config

    def calculate_optimal_page_size(self) -> QSize:
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
        # Get the available width of the scroll area
        scroll_area_width = self.sequence_card_tab.content_area.scroll_area.width()

        # Account for scroll bar width if vertical scrollbar is visible
        if (
            self.sequence_card_tab.content_area.scroll_area.verticalScrollBar().isVisible()
        ):
            scroll_bar_width = (
                self.sequence_card_tab.content_area.scroll_area.verticalScrollBar().width()
            )
            scroll_area_width -= scroll_bar_width

        # MINIMAL MARGINS: Almost no side margins to maximize available width
        side_margins = 0  # Reduced from 4 to 0 to maximize available width
        column_spacing = self.config.page_spacing * (self.config.columns_per_row - 1)
        available_width = scroll_area_width - side_margins - column_spacing

        # Calculate the maximum width for each page with a minimum size to prevent too small pages
        # IMPORTANT: Use columns_per_row here because we're calculating the width of each PAGE PREVIEW
        # This is correct because we're determining how to fit multiple page previews side-by-side in the UI
        max_page_width = max(300, available_width // self.config.columns_per_row)

        # Apply a scaling factor based on column count to ensure proper proportional scaling
        # This helps maintain readability even with more columns

        max_page_width = int(max_page_width)

        # Get the original page size and aspect ratio
        original_size = self.page_factory.page_layout.get_page_size_px()
        aspect_ratio = original_size.height() / original_size.width()

        # Calculate the new height based on the aspect ratio
        new_height = int(max_page_width * aspect_ratio)

        # Return the new size
        return QSize(max_page_width, new_height)

    def calculate_scale_factor(
        self, original_size: QSize, optimal_size: QSize
    ) -> float:
        """
        Calculate the scale factor for a page based on original and optimal sizes.

        Args:
            original_size: The original size of the page
            optimal_size: The optimal size for display

        Returns:
            float: The calculated scale factor
        """
        # Calculate scale factor based on optimal size and original size
        # Use the minimum of width and height ratios to ensure the page fits completely
        scale_factor = min(
            optimal_size.width() / original_size.width(),
            optimal_size.height() / original_size.height(),
        )

        return scale_factor

    def set_optimal_grid_dimensions(self, sequence_length: int) -> None:
        grid_map = {
            2: (3, 2),
            3: (3, 2),
            4: (10, 2),
            5: (2, 3),
            6: (2, 3),
            8: (5, 2),
            10: (4, 3),
            12: (4, 3),
            16: (3, 2),
        }

        if sequence_length in grid_map:
            cols, rows = grid_map[sequence_length]
            self.page_factory.set_grid_dimensions(cols, rows)
        else:
            if sequence_length < 8:
                self.page_factory.set_grid_dimensions(3, 2)
            elif sequence_length <= 12:
                self.page_factory.set_grid_dimensions(3, 3)
            else:
                self.page_factory.set_grid_dimensions(4, 4)
