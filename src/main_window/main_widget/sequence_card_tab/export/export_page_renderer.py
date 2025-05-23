# src/main_window/main_widget/sequence_card_tab/export/export_page_renderer.py
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter, QImage, QImageReader, QFont
from PyQt6.QtCore import Qt, QRect, QPoint, QSize

from .export_config import ExportConfig
from .export_grid_calculator import ExportGridCalculator


class ExportPageRenderer:
    """
    Renders high-quality sequence card pages for export.
    
    This class handles:
    1. Creating high-quality pages from original images
    2. Rendering pages to image files
    3. Applying proper scaling and quality settings
    """
    
    def __init__(self, export_config: ExportConfig, grid_calculator: ExportGridCalculator):
        self.config = export_config
        self.grid_calculator = grid_calculator
        self.logger = logging.getLogger(__name__)
        
        # Configure image reader for high quality
        QImageReader.setAllocationLimit(0)  # No memory limit for image loading
    
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
            
            # Save the pixmap as a high-quality image
            result = pixmap.save(
                filepath,
                self.config.get_export_setting("format", "PNG"),
                self.config.get_export_setting("quality", 100)
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
        
        if not sequence_items or not isinstance(sequence_items, list) or len(sequence_items) == 0:
            self.logger.warning("No sequence items found on page, falling back to direct rendering")
            return self._render_widget_directly(page)
        
        # Create a new pixmap with the print dimensions
        page_width = self.config.get_print_setting("page_width_pixels", 5100)
        page_height = self.config.get_print_setting("page_height_pixels", 6600)
        
        pixmap = QPixmap(page_width, page_height)
        pixmap.fill(self.config.get_export_setting("background_color", Qt.GlobalColor.white))
        
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
            
            # Calculate the row and column for this item
            row = idx // cols
            col = idx % cols
            
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
        self, painter: QPainter, sequence_data: Dict[str, Any], 
        cell_x: int, cell_y: int, cell_width: int, cell_height: int
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
        
        # Calculate the available space in the cell (accounting for padding)
        available_width, available_height = self.grid_calculator.calculate_available_cell_space(
            cell_width, cell_height
        )
        
        # Calculate the scaled image dimensions
        image_width, image_height = self.grid_calculator.calculate_image_dimensions(
            image.width(), image.height(), available_width, available_height
        )
        
        # Calculate the position to center the image in the cell
        image_x, image_y = self.grid_calculator.calculate_image_position_in_cell(
            cell_x, cell_y, cell_width, cell_height, image_width, image_height
        )
        
        # Draw the image
        painter.drawImage(
            QRect(image_x, image_y, image_width, image_height),
            image,
            QRect(0, 0, image.width(), image.height())
        )
        
        # Draw the sequence name
        word = sequence_data.get("word", "")
        if word:
            # Set up the font
            font = QFont("Arial", 14, QFont.Weight.Bold)
            painter.setFont(font)
            
            # Calculate the text position (centered below the image)
            text_rect = QRect(
                cell_x, 
                image_y + image_height + 10, 
                cell_width, 
                30
            )
            
            # Draw the text
            painter.drawText(
                text_rect, 
                Qt.AlignmentFlag.AlignCenter, 
                word
            )
    
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
        scale_factor = self.config.get_print_setting("dpi", 600) / 96  # Assuming screen DPI is 96
        
        # Create a pixmap with the scaled dimensions
        pixmap = QPixmap(
            int(widget_size.width() * scale_factor),
            int(widget_size.height() * scale_factor)
        )
        pixmap.fill(self.config.get_export_setting("background_color", Qt.GlobalColor.white))
        
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
