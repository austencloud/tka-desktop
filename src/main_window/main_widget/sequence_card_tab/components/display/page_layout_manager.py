# src/main_window/main_widget/sequence_card_tab/components/display/page_layout_manager.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from ...tab import SequenceCardTab
    from ..pages.printable_factory import PrintablePageFactory


class PageLayoutManager:
    """
    Manages page layout calculations for the printable sequence card display.
    
    This class is responsible for:
    1. Calculating optimal page sizes based on available width and column count
    2. Applying scaling factors for different column configurations
    3. Maintaining aspect ratios during scaling
    4. Providing consistent sizing across all pages
    """
    
    def __init__(
        self, 
        sequence_card_tab: "SequenceCardTab",
        page_factory: "PrintablePageFactory",
        columns_per_row: int = 2,
        page_spacing: int = 20
    ):
        self.sequence_card_tab = sequence_card_tab
        self.page_factory = page_factory
        self.columns_per_row = columns_per_row
        self.page_spacing = page_spacing
        
    def set_columns_per_row(self, columns: int) -> None:
        """
        Set the number of page previews to display per row.
        
        Args:
            columns: Number of columns (limited to 1-4)
        """
        if columns < 1:
            columns = 1
        elif columns > 4:
            columns = 4
            
        self.columns_per_row = columns
        
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
        print(
            f"DEBUG: calculate_optimal_page_size called with columns_per_row={self.columns_per_row}"
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
            scaling_factor = 0.9   # Even smaller for 4 columns
            
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
        
    def calculate_scale_factor(self, original_size: QSize, optimal_size: QSize) -> float:
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
        
        # Apply a column-specific adjustment to ensure proper scaling with different column counts
        if self.columns_per_row == 3:
            # For 3 columns, apply a slight adjustment to ensure proper scaling
            scale_factor *= 0.98
        elif self.columns_per_row == 4:
            # For 4 columns, apply a more significant adjustment
            scale_factor *= 0.95
            
        return scale_factor
