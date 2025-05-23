# src/main_window/main_widget/sequence_card_tab/export/page_exporter_refactored.py
import os
import time
import logging
from typing import TYPE_CHECKING, List, Optional, Dict, Any
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt

from .export_config import ExportConfig
from .export_ui_manager import ExportUIManager
from .page_image_data_extractor import PageImageDataExtractor
from .export_grid_calculator import ExportGridCalculator
from .export_page_renderer import ExportPageRenderer

if TYPE_CHECKING:
    from ..tab import SequenceCardTab


class SequenceCardPageExporter:
    """
    Exports sequence card pages as high-quality images.

    This class orchestrates the export process by coordinating the following components:
    1. ExportConfig: Manages print and export settings
    2. ExportUIManager: Handles file dialogs and progress updates
    3. PageImageDataExtractor: Extracts image paths and metadata from UI widgets
    4. ExportGridCalculator: Calculates optimal grid layouts
    5. ExportPageRenderer: Renders high-quality images
    """

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.config = ExportConfig()
        self.ui_manager = ExportUIManager(sequence_card_tab)
        self.data_extractor = PageImageDataExtractor(sequence_card_tab)
        self.grid_calculator = ExportGridCalculator(self.config)
        self.page_renderer = ExportPageRenderer(self.config, self.grid_calculator)

    def export_all_pages_as_images(self):
        """
        Export all currently displayed sequence card pages as high-quality print-ready images.

        This method:
        1. Prompts the user for a directory to save the images
        2. Creates high-quality images using original source files
        3. Saves the images with appropriate naming
        4. Shows progress during export
        """
        self.logger.info("Starting sequence card page export")

        # Get the pages to export - check both the tab's pages and the printable displayer's pages
        pages = self._get_pages_to_export()
        if not pages:
            self.ui_manager.show_warning_message(
                "No Pages to Export",
                "There are no sequence card pages to export. Please select a sequence length first."
            )
            return

        self.logger.info(f"Found {len(pages)} pages to export")

        # Get the export directory
        export_dir = self.ui_manager.get_export_directory()
        if not export_dir:
            return  # User cancelled

        # Export the pages
        self._export_pages(pages, export_dir)

    def _get_pages_to_export(self) -> List[QWidget]:
        """
        Get the pages to export from the sequence card tab.
        
        Returns:
            List[QWidget]: List of page widgets to export
        """
        # First try to get pages directly from the tab
        pages = self.sequence_card_tab.pages
        
        # If the tab's pages list is empty, try to get pages from the printable displayer
        if not pages and hasattr(self.sequence_card_tab, "printable_displayer"):
            if hasattr(self.sequence_card_tab.printable_displayer, "pages"):
                # Get pages directly from the PrintableDisplayer
                pages = self.sequence_card_tab.printable_displayer.pages
                self.logger.info("Using pages from PrintableDisplayer")
            elif hasattr(self.sequence_card_tab.printable_displayer, "manager"):
                # Get pages from the SequenceDisplayManager
                pages = self.sequence_card_tab.printable_displayer.manager.pages
                self.logger.info("Using pages from SequenceDisplayManager")
        
        return pages

    def _export_pages(self, pages: List[QWidget], export_dir: str):
        """
        Export the sequence card pages as high-quality print-ready images.

        Args:
            pages: List of page widgets to export
            export_dir: Directory to save the exported images
        """
        # Get the selected length
        selected_length = getattr(
            self.sequence_card_tab.nav_sidebar, "selected_length", 0
        )
        
        # Create a subdirectory for this export
        export_subdir = self.ui_manager.create_export_subdirectory(export_dir, selected_length)
        
        # Create a progress dialog
        progress = self.ui_manager.create_progress_dialog(len(pages))
        
        # Process each page
        for i, page in enumerate(pages):
            if self.ui_manager.cancel_requested:
                self.logger.info("Export cancelled by user")
                break
            
            # Update progress
            self.ui_manager.update_progress(
                i, f"Exporting page {i+1} of {len(pages)}..."
            )
            
            try:
                # Export the page
                filename = f"sequence_card_page_{i+1:03d}.png"
                filepath = os.path.join(export_subdir, filename)
                
                self.logger.info(f"Exporting page {i+1} to: {filepath}")
                
                # Extract sequence data from the page
                sequence_items = self.data_extractor.extract_sequence_data_from_page(page)
                
                # Store the sequence items on the page for the renderer to use
                page.setProperty("sequence_items", sequence_items)
                
                # Render the page as a high-quality print-ready image
                self.page_renderer.render_page_to_image(page, filepath)
                
                # Add a small delay to keep UI responsive
                time.sleep(0.1)
                QApplication.processEvents()
                
            except Exception as e:
                self.logger.error(f"Error exporting page {i+1}: {e}")
                self.ui_manager.show_error_message(
                    "Export Error",
                    f"Error exporting page {i+1}: {str(e)}"
                )
        
        # Close the progress dialog
        progress.close()
        
        # Show completion message
        if not self.ui_manager.cancel_requested:
            self.ui_manager.show_export_complete_message(export_subdir, len(pages))
            
            # Open the export directory
            os.startfile(export_subdir)
