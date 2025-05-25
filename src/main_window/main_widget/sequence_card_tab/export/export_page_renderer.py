# src/main_window/main_widget/sequence_card_tab/export/export_page_renderer.py
import logging
from typing import Dict, Any
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter, QImage, QImageReader, QFont
from PyQt6.QtCore import Qt, QRect

# Try to import PIL for image enhancement, but make it optional
try:
    from PIL import Image, ImageEnhance

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from .export_config import ExportConfig
from .export_grid_calculator import ExportGridCalculator
from .color_manager import ColorManager


class ExportPageRenderer:
    """
    Renders high-quality sequence card pages for export.

    This class handles:
    1. Creating high-quality pages from original images
    2. Rendering pages to image files
    3. Applying proper scaling and quality settings
    """

    def __init__(
        self, export_config: ExportConfig, grid_calculator: ExportGridCalculator
    ):
        self.config = export_config
        self.grid_calculator = grid_calculator
        self.logger = logging.getLogger(__name__)

        # Configure image reader for high quality
        QImageReader.setAllocationLimit(0)  # No memory limit for image loading

        # Initialize color manager for color correction
        color_management_settings = self.config.get_export_setting(
            "color_management", {}
        )
        self.color_manager = ColorManager(color_management_settings)

        # Get image processing settings
        self.image_processing = self.config.get_export_setting("image_processing", {})
        self.scaling_algorithm = self.image_processing.get(
            "scaling_algorithm", Qt.TransformationMode.SmoothTransformation
        )
        self.maintain_larger_dimensions = self.image_processing.get(
            "maintain_larger_dimensions", True
        )
        self.upscale_factor = self.image_processing.get("upscale_factor", 1.2)

        # Only enable sharpening if PIL is available
        self.sharpen_after_scaling = (
            self.image_processing.get("sharpen_after_scaling", True) and PIL_AVAILABLE
        )

        if (
            self.image_processing.get("sharpen_after_scaling", True)
            and not PIL_AVAILABLE
        ):
            self.logger.warning(
                "PIL is not available. Image sharpening will be disabled."
            )

    def render_page_to_image(self, page: QWidget, filepath: str) -> bool:
        """
        Render a page as a high-quality print-ready image.

        Args:
            page: The page widget to render
            filepath: Path to save the rendered image

        Returns:
            bool: True if successful, False otherwise
        """
        self.logger.debug(f"Rendering page to image: {filepath}")

        try:
            # Create a high-quality page
            pixmap = self._create_high_quality_page(page)
            if pixmap.isNull():
                self.logger.error("Failed to create high-quality page")
                return False

            # Convert QPixmap to QImage for better color management
            image = pixmap.toImage()

            # Apply color management to the image
            self.logger.debug("Applying color management to the image")
            image = self.color_manager.process_image(image)

            # Convert back to QPixmap
            pixmap = QPixmap.fromImage(image)

            # Save the pixmap as a high-quality image with optimized settings
            self.logger.debug(
                f"Saving image with format: {self.config.get_export_setting('format', 'PNG')}, quality: {self.config.get_export_setting('quality', 100)}"
            )
            result = pixmap.save(
                filepath,
                self.config.get_export_setting("format", "PNG"),
                self.config.get_export_setting("quality", 100),
            )

            if result:
                self.logger.info(f"Successfully saved page to: {filepath}")
            else:
                self.logger.error(f"Failed to save page to: {filepath}")

            return result

        except Exception as e:
            self.logger.error(f"Error rendering page to image: {e}")
            return False

    def _create_high_quality_page(self, page: QWidget) -> QPixmap:
        """
        Create a high-quality page from scratch using original images.

        This method:
        1. Extracts sequence data from the page's widgets
        2. Finds the original high-resolution source images
        3. Creates a new page layout with these images
        4. Renders the page at ultra-high resolution

        Args:
            page: The page widget containing sequence data

        Returns:
            QPixmap: A high-quality rendered page
        """
        # Get the sequence data from the page
        sequence_items = page.property("sequence_items")

        if (
            not sequence_items
            or not isinstance(sequence_items, list)
            or len(sequence_items) == 0
        ):
            self.logger.warning(
                "No sequence items found on page, falling back to direct rendering"
            )
            return self._render_widget_directly(page)

        # Create a new pixmap with the print dimensions
        page_width = self.config.get_print_setting("page_width_pixels", 5100)
        page_height = self.config.get_print_setting("page_height_pixels", 6600)

        pixmap = QPixmap(page_width, page_height)
        pixmap.fill(
            self.config.get_export_setting("background_color", Qt.GlobalColor.white)
        )

        # Create a painter for the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        # Try to determine the sequence length from the metadata
        sequence_length = None
        if sequence_items and "sequence_data" in sequence_items[0]:
            metadata = sequence_items[0]["sequence_data"].get("metadata", {})
            if "sequence" in metadata and len(metadata["sequence"]) > 0:
                sequence_length = len(metadata["sequence"])
                self.logger.debug(f"Detected sequence length: {sequence_length}")

        # Calculate the optimal grid dimensions based on the number of items and sequence length
        rows, cols = self.grid_calculator.calculate_optimal_grid_dimensions(
            len(sequence_items), sequence_length
        )

        # Calculate the cell dimensions
        cell_dimensions = self.grid_calculator.calculate_cell_dimensions(rows, cols)
        cell_width = cell_dimensions["width"]
        cell_height = cell_dimensions["height"]

        # Render each sequence item in its grid cell
        for idx, item in enumerate(sequence_items):
            # Skip if we've processed all cells in the grid
            if idx >= rows * cols:
                self.logger.warning(
                    f"Skipping item {idx+1} as it exceeds grid capacity ({rows}x{cols})"
                )
                continue

            self.logger.debug(f"Processing sequence item {idx+1}/{len(sequence_items)}")

            # Get the sequence data
            sequence_data = item["sequence_data"]

            # Check if we have grid position information from the UI
            if (
                "grid_position" in item
                and item["grid_position"]["row"] >= 0
                and item["grid_position"]["column"] >= 0
            ):
                # Use the grid position from the UI
                row = item["grid_position"]["row"]
                col = item["grid_position"]["column"]
                self.logger.debug(
                    f"Using grid position from UI: row={row}, column={col}"
                )
            else:
                # Calculate the row and column for this item based on index
                row = idx // cols
                col = idx % cols
                self.logger.debug(
                    f"Using calculated grid position: row={row}, column={col}"
                )

            # Calculate the position of this cell
            cell_x, cell_y = self.grid_calculator.calculate_cell_position(
                row, col, cell_width, cell_height
            )

            # Render the sequence item in this cell
            self._render_sequence_item(
                painter, sequence_data, cell_x, cell_y, cell_width, cell_height
            )

        # End painting
        painter.end()

        return pixmap

    def _render_sequence_item(
        self,
        painter: QPainter,
        sequence_data: Dict[str, Any],
        cell_x: int,
        cell_y: int,
        cell_width: int,
        cell_height: int,
    ) -> None:
        """
        Render a sequence item in a grid cell.

        Args:
            painter: QPainter to use for rendering
            sequence_data: Sequence data dictionary
            cell_x: X position of the cell
            cell_y: Y position of the cell
            cell_width: Width of the cell
            cell_height: Height of the cell
        """
        import os  # Import os locally for path operations

        # Get the image path
        image_path = sequence_data.get("path")
        if not image_path or not os.path.exists(image_path):
            self.logger.warning(f"Image path not found: {image_path}")
            return

        # Load the original image at full resolution
        image = QImage(image_path)
        if image.isNull():
            self.logger.warning(f"Failed to load image: {image_path}")
            return

        # Apply color management to the image
        self.logger.debug(
            f"Applying color management to image: {os.path.basename(image_path)}"
        )

        # If this is a red pictograph, apply specific color correction
        if (
            "red" in sequence_data.get("word", "").lower()
            or sequence_data.get("color", "") == "red"
        ):
            self.logger.info(
                f"Detected red pictograph: {os.path.basename(image_path)}, applying enhanced red correction"
            )
            # Apply stronger red enhancement for red pictographs
            enhanced_image = self.color_manager.process_image(image)
        else:
            # Apply standard color management
            enhanced_image = self.color_manager.process_image(image)

        # If maintain_larger_dimensions is enabled, upscale the image before final scaling
        if self.maintain_larger_dimensions and self.upscale_factor > 1.0:
            # Upscale the image to preserve more detail
            original_width = enhanced_image.width()
            original_height = enhanced_image.height()
            upscaled_width = int(original_width * self.upscale_factor)
            upscaled_height = int(original_height * self.upscale_factor)

            self.logger.debug(
                f"Upscaling image from {original_width}x{original_height} to {upscaled_width}x{upscaled_height}"
            )
            enhanced_image = enhanced_image.scaled(
                upscaled_width,
                upscaled_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                self.scaling_algorithm,
            )

        # Calculate the available space in the cell (accounting for padding)
        available_width, available_height = (
            self.grid_calculator.calculate_available_cell_space(cell_width, cell_height)
        )

        # Calculate the scaled image dimensions
        image_width, image_height = self.grid_calculator.calculate_image_dimensions(
            enhanced_image.width(),
            enhanced_image.height(),
            available_width,
            available_height,
        )

        # Calculate the position to center the image in the cell
        image_x, image_y = self.grid_calculator.calculate_image_position_in_cell(
            cell_x, cell_y, cell_width, cell_height, image_width, image_height
        )

        # Apply sharpening if enabled (helps maintain detail after scaling)
        if self.sharpen_after_scaling:
            try:
                import tempfile
                import os

                # Create a temporary file for the conversion
                with tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False
                ) as temp_file:
                    temp_path = temp_file.name

                try:
                    # Save QImage to temporary file
                    self.logger.debug(
                        f"Saving image to temporary file for sharpening: {temp_path}"
                    )
                    enhanced_image.save(temp_path, "PNG")

                    # Open with PIL
                    pil_image = Image.open(temp_path)

                    # Apply sharpening
                    self.logger.debug("Applying sharpening with PIL")
                    sharpened = ImageEnhance.Sharpness(pil_image).enhance(
                        1.3
                    )  # Moderate sharpening

                    # Save sharpened image back to temporary file
                    sharpened.save(temp_path, "PNG")

                    # Load back into QImage
                    enhanced_image = QImage(temp_path)

                    if enhanced_image.isNull():
                        self.logger.warning(
                            "Failed to load sharpened image. Using original image."
                        )
                finally:
                    # Clean up the temporary file
                    try:
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                    except Exception as cleanup_error:
                        self.logger.warning(
                            f"Error cleaning up temporary file: {cleanup_error}"
                        )
            except Exception as e:
                # If PIL processing fails, continue with the unsharpened image
                self.logger.warning(
                    f"Error applying sharpening: {e}. Using unsharpened image."
                )

        # Draw the image with high-quality scaling
        painter.drawImage(
            QRect(image_x, image_y, image_width, image_height),
            enhanced_image,
            QRect(0, 0, enhanced_image.width(), enhanced_image.height()),
        )

        # Draw the sequence name
        word = sequence_data.get("word", "")
        if word:
            # Set up the font
            font = QFont("Arial", 14, QFont.Weight.Bold)
            painter.setFont(font)

            # Calculate the text position (centered below the image)
            text_rect = QRect(cell_x, image_y + image_height + 10, cell_width, 30)

            # Draw the text
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, word)

    def _render_widget_directly(self, widget: QWidget) -> QPixmap:
        """
        Render a widget directly to a pixmap.

        This is a fallback method when we can't extract sequence data.

        Args:
            widget: The widget to render

        Returns:
            QPixmap: The rendered pixmap
        """
        self.logger.debug("Rendering widget directly")

        # Get the widget size
        widget_size = widget.size()

        # Calculate the scale factor to match the print resolution
        scale_factor = (
            self.config.get_print_setting("dpi", 600) / 96
        )  # Assuming screen DPI is 96

        # Create a pixmap with the scaled dimensions
        pixmap = QPixmap(
            int(widget_size.width() * scale_factor),
            int(widget_size.height() * scale_factor),
        )
        pixmap.fill(
            self.config.get_export_setting("background_color", Qt.GlobalColor.white)
        )

        # Create a painter for the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        # Scale the painter
        painter.scale(scale_factor, scale_factor)

        # Render the widget
        widget.render(painter)

        # End painting
        painter.end()

        return pixmap
