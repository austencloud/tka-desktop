# src/main_window/main_widget/sequence_card_tab/components/display/grid_layout_manager.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pages.printable_factory import PrintablePageFactory


class GridLayoutManager:
    """
    Manages grid layout dimensions for sequence card pages.
    
    This class is responsible for:
    1. Determining optimal grid dimensions based on sequence length
    2. Setting grid dimensions on the page factory
    3. Providing consistent grid layouts for different sequence lengths
    """
    
    def __init__(self, page_factory: "PrintablePageFactory"):
        self.page_factory = page_factory
        
    def set_optimal_grid_dimensions(self, sequence_length: int) -> None:
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
