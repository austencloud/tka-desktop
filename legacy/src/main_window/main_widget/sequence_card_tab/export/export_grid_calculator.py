# src/main_window/main_widget/sequence_card_tab/export/export_grid_calculator.py
import math
import logging
from typing import Tuple, Dict, List, Any, Optional, TYPE_CHECKING

from .export_config import ExportConfig

if TYPE_CHECKING:
    from ..tab import SequenceCardTab


class ExportGridCalculator:
    """
    Calculates grid layouts for sequence card page exports.

    This class handles:
    1. Calculating optimal grid dimensions based on sequence length
    2. Calculating cell positions and sizes
    3. Determining optimal page layouts
    4. Ensuring consistency with UI grid dimensions
    """

    def __init__(
        self,
        export_config: ExportConfig,
        sequence_card_tab: Optional["SequenceCardTab"] = None,
    ):
        self.config = export_config
        self.sequence_card_tab = sequence_card_tab
        self.logger = logging.getLogger(__name__)

    def calculate_optimal_grid_dimensions(
        self, item_count: int, sequence_length: Optional[int] = None
    ) -> Tuple[int, int]:
        """
        Calculate the optimal grid dimensions based on the number of items and sequence length.

        This method prioritizes consistency with the UI by:
        1. First checking if UI grid dimensions are available from the SequenceDisplayManager
        2. Falling back to predefined grid dimensions based on sequence length
        3. Only calculating dimensions if no other source is available

        Args:
            item_count: Number of sequence items to display
            sequence_length: Length of the sequence (number of beats)

        Returns:
            Tuple[int, int]: (rows, columns) for the grid layout
        """
        self.logger.debug(
            f"Calculating optimal grid dimensions for {item_count} items with sequence length {sequence_length}"
        )

        # First try to get grid dimensions from the UI (SequenceDisplayManager)
        if self.sequence_card_tab is not None:
            try:
                # Check if we can access the PrintableDisplayer and its manager
                if hasattr(self.sequence_card_tab, "printable_displayer"):
                    printable_displayer = self.sequence_card_tab.printable_displayer

                    # Check if the PrintableDisplayer has a manager
                    if hasattr(printable_displayer, "manager"):
                        # Get the page factory from the manager
                        page_factory = printable_displayer.manager.page_factory

                        # Get the grid dimensions from the page factory
                        rows = page_factory.rows
                        cols = page_factory.columns

                        self.logger.info(
                            f"Using UI grid dimensions from PrintableDisplayer: {rows}x{cols}"
                        )
                        return rows, cols

                # If we can't access the manager, try to access the page factory directly
                elif hasattr(self.sequence_card_tab, "page_factory"):
                    page_factory = self.sequence_card_tab.page_factory
                    rows = page_factory.rows
                    cols = page_factory.columns

                    self.logger.info(
                        f"Using UI grid dimensions from page_factory: {rows}x{cols}"
                    )
                    return rows, cols

            except Exception as e:
                self.logger.warning(
                    f"Error accessing UI grid dimensions: {e}. Falling back to predefined dimensions."
                )

        # If we have a specific sequence length, use the predefined grid dimensions
        if sequence_length is not None:
            rows, cols = self.config.get_grid_dimensions(sequence_length)
            self.logger.debug(
                f"Using predefined grid dimensions for length {sequence_length}: {rows}x{cols}"
            )
            return rows, cols

        # Otherwise, calculate based on the number of items
        # Start with a square-ish grid
        cols = math.ceil(math.sqrt(item_count))
        rows = math.ceil(item_count / cols)

        # Adjust for better aspect ratio on the page
        page_aspect = self.config.get_print_setting(
            "page_width_pixels", 5100
        ) / self.config.get_print_setting("page_height_pixels", 6600)

        # If the grid is too wide, make it taller
        if cols / rows > page_aspect * 1.2:
            cols = max(2, math.ceil(math.sqrt(item_count * page_aspect)))
            rows = math.ceil(item_count / cols)

        # If the grid is too tall, make it wider
        elif rows / cols > 1 / (page_aspect * 0.8):
            rows = max(2, math.ceil(math.sqrt(item_count / page_aspect)))
            cols = math.ceil(item_count / rows)

        self.logger.debug(f"Calculated grid dimensions: {rows}x{cols}")
        return rows, cols

    def calculate_cell_position(
        self, row: int, col: int, cell_width: int, cell_height: int
    ) -> Tuple[int, int]:
        """
        Calculate the position of a cell in the grid.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            cell_width: Width of each cell
            cell_height: Height of each cell

        Returns:
            Tuple[int, int]: (x, y) position of the cell
        """
        content_area = self.config.get_content_area()
        cell_spacing = self.config.get_export_setting("cell_spacing", 75)

        # Calculate the position
        x = content_area["x"] + col * (cell_width + cell_spacing)
        y = content_area["y"] + row * (cell_height + cell_spacing)

        return x, y

    def calculate_cell_dimensions(self, rows: int, cols: int) -> Dict[str, int]:
        """
        Calculate the dimensions of each cell in the grid.

        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid

        Returns:
            Dict[str, int]: Dictionary with cell dimensions
        """
        return self.config.get_cell_dimensions(rows, cols)

    def calculate_image_position_in_cell(
        self,
        cell_x: int,
        cell_y: int,
        cell_width: int,
        cell_height: int,
        image_width: int,
        image_height: int,
    ) -> Tuple[int, int]:
        """
        Calculate the position of an image within a cell, centering it.

        Args:
            cell_x: X position of the cell
            cell_y: Y position of the cell
            cell_width: Width of the cell
            cell_height: Height of the cell
            image_width: Width of the image
            image_height: Height of the image

        Returns:
            Tuple[int, int]: (x, y) position of the image within the cell
        """
        # Center the image in the cell
        x = cell_x + (cell_width - image_width) // 2
        y = cell_y + (cell_height - image_height) // 2

        return x, y

    def calculate_image_dimensions(
        self, original_width: int, original_height: int, max_width: int, max_height: int
    ) -> Tuple[int, int]:
        """
        Calculate the dimensions of an image, scaling it to fit within max dimensions.

        Args:
            original_width: Original width of the image
            original_height: Original height of the image
            max_width: Maximum width available
            max_height: Maximum height available

        Returns:
            Tuple[int, int]: (width, height) of the scaled image
        """
        # Calculate the aspect ratio
        aspect_ratio = original_height / original_width if original_width > 0 else 1.0

        # Scale the image to fit within the available space
        if original_width <= max_width and original_height <= max_height:
            # Image is already small enough, no scaling needed
            return original_width, original_height

        # Scale based on the limiting dimension
        if max_width * aspect_ratio <= max_height:
            # Width is the limiting factor
            width = max_width
            height = int(width * aspect_ratio)
        else:
            # Height is the limiting factor
            height = max_height
            width = int(height / aspect_ratio)

        return width, height

    def calculate_available_cell_space(
        self, cell_width: int, cell_height: int
    ) -> Tuple[int, int]:
        """
        Calculate the available space within a cell, accounting for padding.

        Args:
            cell_width: Width of the cell
            cell_height: Height of the cell

        Returns:
            Tuple[int, int]: (width, height) of the available space
        """
        cell_padding = self.config.get_export_setting("cell_padding", 30)

        # Calculate available space
        available_width = cell_width - 2 * cell_padding
        available_height = cell_height - 2 * cell_padding

        return available_width, available_height
