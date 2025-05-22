# src/main_window/main_widget/sequence_card_tab/components/display/image_processor.py
import os
import logging
import collections  # Import collections for OrderedDict
from typing import (
    Dict,
    Optional,
    TYPE_CHECKING,
    OrderedDict as OrderedDictType,
)  # For type hinting
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from ..pages.printable_factory import PrintablePageFactory

DEFAULT_IMAGE_CACHE_SIZE = (
    1000  # Defines a default maximum number of images in the LRU cache
)


class ImageProcessor:
    """
    Handles image loading, scaling, and caching for sequence card images.

    This class is responsible for:
    1. Loading images from disk
    2. Scaling images consistently based on grid dimensions and column count
    3. Maintaining aspect ratios during scaling
    4. Caching images for performance using a two-level LRU cache:
       - First level: Raw QImage objects keyed by image_path
       - Second level: Scaled QPixmap objects keyed by image_path + scaling parameters
    5. Applying proper margins and scaling adjustments
    """

    def __init__(
        self,
        page_factory: "PrintablePageFactory",
        columns_per_row: int = 2,
        cache_size: int = DEFAULT_IMAGE_CACHE_SIZE,
    ):
        self.page_factory = page_factory
        self.columns_per_row = columns_per_row

        # Two-level caching system:
        # Level 1: Raw image cache (path -> QImage)
        self.raw_image_cache: OrderedDictType[str, QImage] = collections.OrderedDict()

        # Level 2: Scaled image cache (cache_key -> QPixmap)
        self.scaled_image_cache: OrderedDictType[str, QPixmap] = (
            collections.OrderedDict()
        )

        # For backward compatibility
        self.image_cache = self.scaled_image_cache

        # Cache size limits
        self.raw_cache_size = cache_size // 2  # Half for raw images
        self.scaled_cache_size = cache_size  # Full size for scaled images
        self.cache_size = cache_size

        # Cache statistics
        self.cache_hits = 0
        self.cache_misses = 0

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
        # Count items before clearing (for logging)
        raw_count = len(self.raw_image_cache)
        scaled_count = len(self.scaled_image_cache)

        # Clear both cache levels
        self.raw_image_cache.clear()
        self.scaled_image_cache.clear()

        # Reset cache statistics
        self.cache_hits = 0
        self.cache_misses = 0

        # Log cache clearing
        logging.debug(
            f"Image cache cleared: {raw_count} raw items and {scaled_count} scaled items removed."
        )

    def load_image_with_consistent_scaling(
        self,
        image_path: str,
        page_scale_factor: float = 1.0,
        current_page_index: int = -1,  # Retained for update_card_aspect_ratio logic
    ) -> QPixmap:
        """
        Load image with consistent scaling and high-quality transformation.

        This method ensures:
        1. Consistent relative sizing across all images based on grid dimensions and column count
        2. Proper margins around each image
        3. High-quality scaling using SmoothTransformation
        4. Efficient LRU caching for performance
        5. Images fit completely within their grid cells
        6. Aspect ratio is maintained
        7. No overflow occurs
        8. Proper scaling adjustment based on preview columns

        Args:
            image_path: Path to the image file
            page_scale_factor: Scale factor to apply (from the page)
            current_page_index: Current page index (-1 for first image, used for aspect ratio update)

        Returns:
            QPixmap: The scaled image
        """
        # Get cell_size early as it's part of the cache key components
        cell_size = self.page_factory.get_cell_size()

        # Create a more robust cache key that captures all parameters affecting the final scaled pixmap:
        # 1. image_path
        # 2. cell_size (reflects on-page grid from page_factory.rows/cols and paper dimensions from page_layout)
        # 3. self.columns_per_row (UI preview columns, affecting column_adjustment and margin_percent)
        # 4. page_scale_factor (overall scaling of the page preview, influenced by UI layout)
        key_parts = (
            image_path,
            cell_size.width(),
            cell_size.height(),
            self.columns_per_row,
            f"{page_scale_factor:.4f}",  # Format float to ensure consistent string representation
        )
        cache_key = "_".join(map(str, key_parts))

        # Check Level 2 cache (scaled images) first
        if cache_key in self.scaled_image_cache:
            # Mark as recently used
            self.scaled_image_cache.move_to_end(cache_key)
            # Track cache hit
            self.cache_hits += 1
            logging.debug(f"L2 cache hit for {os.path.basename(image_path)}")
            return self.scaled_image_cache[cache_key]

        try:
            # Check Level 1 cache (raw images) before loading from disk
            if image_path in self.raw_image_cache:
                # Use cached raw image
                image = self.raw_image_cache[image_path]
                # Mark as recently used
                self.raw_image_cache.move_to_end(image_path)
                logging.debug(f"L1 cache hit for {os.path.basename(image_path)}")
                # We still need to scale the image, so this is a partial hit
            else:
                # Load from disk
                image = QImage(image_path)
                if image.isNull():
                    logging.error(f"Failed to load image {image_path}")
                    return QPixmap()  # Return an empty QPixmap

                # Add to Level 1 cache (raw images)
                self.raw_image_cache[image_path] = image
                self.raw_image_cache.move_to_end(image_path)

                # Track cache miss
                self.cache_misses += 1
                logging.debug(f"Cache miss for {os.path.basename(image_path)}")

                # Enforce Level 1 cache size limit
                if len(self.raw_image_cache) > self.raw_cache_size:
                    self.raw_image_cache.popitem(
                        last=False
                    )  # Remove least recently used

            # cell_size already fetched

            column_adjustment = 1.0
            if self.columns_per_row == 3:
                column_adjustment = 0.98
            elif self.columns_per_row == 4:
                column_adjustment = 0.95

            margin_percent = 0.05
            if self.columns_per_row == 3:
                margin_percent = 0.04
            elif self.columns_per_row == 4:
                margin_percent = 0.03

            margin = min(
                15,
                max(
                    3, int(min(cell_size.width(), cell_size.height()) * margin_percent)
                ),
            )

            available_width_for_image = cell_size.width() - (margin * 2)
            available_height_for_image = cell_size.height() - (margin * 2)

            # Apply the page scale factor and column adjustment to the available space for the image
            target_available_width = int(
                available_width_for_image * page_scale_factor * column_adjustment
            )
            target_available_height = int(
                available_height_for_image * page_scale_factor * column_adjustment
            )

            original_width = image.width()
            original_height = image.height()

            scaled_image: QImage
            if original_width <= 0 or original_height <= 0:
                # If original image has no dimensions, create a null scaled image
                scaled_image = QImage()
            else:
                aspect_ratio = original_height / original_width

                # Calculate target dimensions to fit within available space while maintaining aspect ratio
                if target_available_width * aspect_ratio <= target_available_height:
                    # Width-constrained
                    target_width = target_available_width
                    target_height = int(target_width * aspect_ratio)
                else:
                    # Height-constrained
                    target_height = target_available_height
                    target_width = int(target_height / aspect_ratio)

                # Ensure target dimensions are non-negative (image.scaled handles 0 dimensions by returning null image)
                target_width = max(0, target_width)
                target_height = max(0, target_height)

                scaled_image = image.scaled(
                    target_width,
                    target_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

            # Update card aspect ratio in page factory for the first image processed in a batch
            if current_page_index == -1:
                if (
                    original_width > 0 and original_height > 0
                ):  # Ensure valid dimensions for aspect ratio
                    self.page_factory.update_card_aspect_ratio(
                        original_width
                        / original_height  # This is card's width/height ratio
                    )

            pixmap = QPixmap.fromImage(
                scaled_image
            )  # Handles null scaled_image correctly (becomes null QPixmap)

            # Add to Level 2 cache (scaled images)
            self.scaled_image_cache[cache_key] = pixmap
            self.scaled_image_cache.move_to_end(cache_key)  # Mark as most recently used

            # Enforce Level 2 cache size limit
            if len(self.scaled_image_cache) > self.scaled_cache_size:
                self.scaled_image_cache.popitem(
                    last=False
                )  # Remove least recently used

            # Process UI events to keep the application responsive
            # This is moved to the end of the method to avoid interrupting the cache operations
            QApplication.processEvents()

            return pixmap

        except Exception as e:
            import traceback

            logging.error(f"Error loading image {image_path}: {e}")
            traceback.print_exc()

            # Create an error indicator pixmap
            return self._create_error_pixmap()

    def _create_error_pixmap(self, size: QSize = None) -> QPixmap:
        """
        Create a pixmap indicating an error loading the image.

        Args:
            size: Size of the error pixmap. If None, uses a default size.

        Returns:
            QPixmap: An error indicator pixmap
        """
        # Use a default size if none provided
        if size is None:
            size = QSize(100, 100)

        # Create a pixmap with a red background
        pixmap = QPixmap(size)
        pixmap.fill(QColor(220, 50, 50))  # Red background

        # Create a painter to draw on the pixmap
        painter = QPainter(pixmap)

        # Set up font and text color
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))  # White text

        # Draw error message
        text_rect = QRect(5, 5, size.width() - 10, size.height() - 10)
        painter.drawText(
            text_rect, Qt.AlignmentFlag.AlignCenter, "Error\nLoading\nImage"
        )

        # Finish painting
        painter.end()

        return pixmap

    def load_image(
        self,
        image_path: str,
        page_scale_factor: float = 1.0,
        current_page_index: int = -1,
    ) -> QPixmap:
        """
        Legacy method for backward compatibility.
        Use load_image_with_consistent_scaling instead.
        """
        return self.load_image_with_consistent_scaling(
            image_path, page_scale_factor, current_page_index
        )
