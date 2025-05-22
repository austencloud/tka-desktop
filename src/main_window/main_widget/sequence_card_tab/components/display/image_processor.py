# src/main_window/main_widget/sequence_card_tab/components/display/image_processor.py
import os
from typing import Dict, Optional, TYPE_CHECKING
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QSize

if TYPE_CHECKING:
    from ..pages.printable_factory import PrintablePageFactory


class ImageProcessor:
    """
    Handles image loading, scaling, and caching for sequence card images.
    
    This class is responsible for:
    1. Loading images from disk
    2. Scaling images consistently based on grid dimensions and column count
    3. Maintaining aspect ratios during scaling
    4. Caching images for performance
    5. Applying proper margins and scaling adjustments
    """
    
    def __init__(self, page_factory: "PrintablePageFactory", columns_per_row: int = 2):
        self.page_factory = page_factory
        self.columns_per_row = columns_per_row
        self.image_cache: Dict[str, QPixmap] = {}
        
    def set_columns_per_row(self, columns: int) -> None:
        """
        Set the number of columns per row for scaling calculations.
        
        Args:
            columns: Number of columns (limited to 1-4)
        """
        if columns < 1:
            columns = 1
        elif columns > 4:
            columns = 4
            
        self.columns_per_row = columns
        
    def clear_cache(self) -> None:
        """Clear the image cache."""
        cache_size = len(self.image_cache)
        self.image_cache.clear()
        print(f"DEBUG: Cleared image cache ({cache_size} items)")
        
    def load_image_with_consistent_scaling(
        self, 
        image_path: str, 
        page_scale_factor: float = 1.0,
        current_page_index: int = -1
    ) -> QPixmap:
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
            page_scale_factor: Scale factor to apply (from the page)
            current_page_index: Current page index (-1 for first image)

        Returns:
            QPixmap: The scaled image
        """
        # Create a cache key that includes both grid dimensions AND column count
        # The columns_per_row setting SHOULD affect the image scaling to ensure proper proportional scaling
        grid_key = f"{self.page_factory.rows}x{self.page_factory.columns}"
        cache_key = f"{image_path}_{grid_key}_{self.columns_per_row}"

        print(
            f"DEBUG: load_image_with_consistent_scaling - path={os.path.basename(image_path)}, "
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
            if current_page_index == -1:
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
            
    def load_image(self, image_path: str, page_scale_factor: float = 1.0, current_page_index: int = -1) -> QPixmap:
        """
        Legacy method for backward compatibility.
        Use load_image_with_consistent_scaling instead.
        """
        return self.load_image_with_consistent_scaling(image_path, page_scale_factor, current_page_index)
