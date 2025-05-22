# src/main_window/main_widget/sequence_card_tab/components/display/printable_displayer_coordinator.py
import os
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt

from utils.path_helpers import get_sequence_card_image_exporter_path
from ..pages.printable_layout import PaperSize, PaperOrientation

from .page_layout_manager import PageLayoutManager
from .image_processor import ImageProcessor
from .sequence_loader import SequenceLoader
from .grid_layout_manager import GridLayoutManager
from .page_factory import PageFactory
from .ui_layout_manager import UILayoutManager
from .image_label_factory import ImageLabelFactory

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class PrintableDisplayerCoordinator:
    """
    Coordinates all components for displaying printable sequence cards.
    
    This class:
    1. Initializes and manages all component classes
    2. Coordinates the display of sequence cards
    3. Handles user interactions and settings
    4. Maintains the state of the display
    """
    
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.nav_sidebar = sequence_card_tab.nav_sidebar
        
        # Create page factory from the tab
        self.page_factory = sequence_card_tab.page_factory
        
        # Initialize component managers
        self.layout_manager = PageLayoutManager(
            sequence_card_tab, 
            self.page_factory,
            columns_per_row=2,
            page_spacing=20
        )
        
        self.image_processor = ImageProcessor(
            self.page_factory,
            columns_per_row=2
        )
        
        self.sequence_loader = SequenceLoader()
        
        self.grid_layout_manager = GridLayoutManager(
            self.page_factory
        )
        
        self.ui_layout_manager = UILayoutManager(
            sequence_card_tab,
            page_spacing=20
        )
        
        self.page_manager = PageFactory(
            self.page_factory,
            self.layout_manager
        )
        
        self.image_label_factory = ImageLabelFactory()
        
        # State tracking
        self.pages: List[QWidget] = []
        self.current_page_index = -1
        self.current_position = 0
        self.columns_per_row = 2
        
    @property
    def columns_per_row(self) -> int:
        """Get the number of columns per row."""
        return self._columns_per_row
        
    @columns_per_row.setter
    def columns_per_row(self, value: int) -> None:
        """Set the number of columns per row."""
        self._columns_per_row = value
        self.layout_manager.set_columns_per_row(value)
        self.image_processor.set_columns_per_row(value)
        
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
            
        # Only update if the value has changed
        if self.columns_per_row != columns:
            self.columns_per_row = columns
            
            # If we have pages displayed, refresh the layout
            if self.pages:
                self.refresh_layout()
                
    def set_paper_size(self, paper_size: PaperSize) -> None:
        """
        Set the paper size for page previews.
        
        Args:
            paper_size: Paper size to use
        """
        self.page_factory.set_paper_size(paper_size)
        
    def set_orientation(self, orientation: PaperOrientation) -> None:
        """
        Set the orientation for page previews.
        
        Args:
            orientation: Paper orientation to use
        """
        self.page_factory.set_orientation(orientation)
        
    def refresh_layout(self) -> None:
        """
        Refresh the layout with the current settings.

        This method:
        1. Clears existing pages and cache
        2. Completely removes all widgets from the layout
        3. Recreates the layout from scratch
        4. Updates grid dimensions based ONLY on sequence length
        5. Reloads all sequences with the new layout
        """
        # Store the current length and cursor
        current_length = self.nav_sidebar.selected_length
        self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)

        print(
            f"DEBUG: refresh_layout called with columns_per_row={self.columns_per_row}, length={current_length}"
        )

        try:
            # STEP 1: Clear existing pages and their widgets
            self._clear_existing_pages()

            # STEP 2: Clear the image cache completely since layout has changed
            self.image_processor.clear_cache()

            # STEP 3: Clear the scroll layout completely
            self.ui_layout_manager._clear_scroll_layout()

            # STEP 4: Force a UI update to ensure the layout is properly cleared
            QApplication.processEvents()

            # STEP 5: Create a new multi-column layout for page previews
            # This controls how many page previews are shown side-by-side in the UI
            preview_grid = self.ui_layout_manager.create_multi_column_layout()
            self.page_manager.set_preview_grid(preview_grid)
            
            print(
                f"DEBUG: Created new multi-column layout with {self.columns_per_row} columns per row"
            )

            # STEP 6: Update the page factory grid dimensions based ONLY on sequence length
            # This sets the layout within each page and is NOT affected by columns_per_row
            self.grid_layout_manager.set_optimal_grid_dimensions(current_length)
            print(f"DEBUG: Set optimal grid dimensions for length {current_length}")

            # STEP 7: Re-display the sequences with the new layout
            print(f"DEBUG: Displaying sequences with length {current_length}")
            # Use display_sequences which will handle clearing and regenerating everything
            self.display_sequences(current_length)
        except Exception as e:
            print(f"ERROR in refresh_layout: {e}")
            import traceback

            traceback.print_exc()
        finally:
            # Reset cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
            
    def display_sequences(self, selected_length: Optional[int] = None) -> None:
        """
        Display sequence card images in a print-friendly layout.

        Args:
            selected_length: The length of sequences to display. If None, use the sidebar selection.
        """
        # STEP 1: Completely clear existing pages and cache
        self._clear_existing_pages()
        self.image_processor.clear_cache()

        # STEP 2: Clear the scroll layout completely
        self.ui_layout_manager._clear_scroll_layout()

        # Force a UI update to ensure the layout is properly cleared
        QApplication.processEvents()

        # Get selected length from sidebar if not provided
        if selected_length is None:
            selected_length = self.nav_sidebar.selected_length

        # Update UI to show loading state
        self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)
        length_text = f"{selected_length}-step" if selected_length > 0 else "all"
        self.sequence_card_tab.description_label.setText(
            f"Loading {length_text} sequences..."
        )
        QApplication.processEvents()

        try:
            # STEP 3: Get all sequences from the sequence_card_images directory
            images_path = get_sequence_card_image_exporter_path()
            sequences = self.sequence_loader.get_all_sequences(images_path)

            # STEP 4: Filter sequences by the selected length
            filtered_sequences = self.sequence_loader.filter_sequences_by_length(
                sequences, selected_length
            )

            # Check if we have any sequences to display
            total_sequences = len(filtered_sequences)
            if total_sequences == 0:
                self.sequence_card_tab.description_label.setText(
                    f"No {length_text} sequences found"
                )
                return

            # STEP 5: Set optimal grid dimensions based ONLY on sequence length
            # This sets the layout within each page and is NOT affected by columns_per_row
            self.grid_layout_manager.set_optimal_grid_dimensions(selected_length)

            # STEP 6: Create multi-column layout for page previews
            # This controls how many page previews are shown side-by-side in the UI
            preview_grid = self.ui_layout_manager.create_multi_column_layout()
            self.page_manager.set_preview_grid(preview_grid)

            # STEP 7: Process each sequence
            for i, sequence in enumerate(filtered_sequences):
                if i % 10 == 0:  # Update description label periodically
                    self.sequence_card_tab.description_label.setText(
                        f"Loading {length_text} sequences... ({i+1}/{total_sequences})"
                    )
                    QApplication.processEvents()

                # Load and display image
                try:
                    image_path = sequence.get("path", "")
                    if image_path and os.path.exists(image_path):
                        # Get the current page's scale factor if available
                        page_scale_factor = 1.0
                        if self.current_page_index >= 0 and self.current_page_index < len(self.pages):
                            current_page = self.pages[self.current_page_index]
                            if current_page.property("scale_factor") is not None:
                                page_scale_factor = current_page.property("scale_factor")
                        
                        # Load image with consistent scaling
                        pixmap = self.image_processor.load_image_with_consistent_scaling(
                            image_path, 
                            page_scale_factor,
                            self.current_page_index
                        )

                        if not pixmap.isNull():
                            # Create label and add to page
                            label = self.image_label_factory.create_image_label(sequence, pixmap)
                            self._add_image_to_page(label)
                except Exception as e:
                    print(f"Error processing {sequence.get('path', 'unknown')}: {e}")

                # Keep UI responsive
                QApplication.processEvents()

            # STEP 8: Update description label with final count and column information
            self.sequence_card_tab.description_label.setText(
                f"Showing {len(filtered_sequences)} {length_text} sequences across {len(self.pages)} pages in {self.columns_per_row} columns"
            )

        except Exception as e:
            print(f"Error displaying sequences: {e}")
            import traceback

            traceback.print_exc()
            self.sequence_card_tab.description_label.setText(f"Error: {str(e)}")
        finally:
            # Reset cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
            
    def _clear_existing_pages(self) -> None:
        """Clear all existing pages and reset page tracking."""
        # Clear existing pages in the UI
        self.ui_layout_manager.clear_existing_pages(self.pages)
        
        # Reset page tracking
        self.pages = []
        self.page_manager.clear_pages()
        self.current_page_index = -1
        self.current_position = 0
        
    def _add_image_to_page(self, label: QWidget) -> None:
        """
        Add image to page, creating new pages as needed.
        
        Args:
            label: The image label to add
        """
        # Check if we need to create a new page
        if self.current_page_index == -1 or self.page_manager.is_page_full(self.current_position):
            new_page = self.page_manager.create_new_page()
            self.pages.append(new_page)
            self.current_page_index = len(self.pages) - 1
            self.current_position = 0

        # Get the current page and its grid layout
        if self.current_page_index < 0 or self.current_page_index >= len(self.pages):
            print(
                f"ERROR: Invalid page index {self.current_page_index}, pages length: {len(self.pages)}"
            )
            return
            
        page = self.pages[self.current_page_index]
        grid_layout = page.layout()

        # Get the current position as row and column
        positions = self.page_factory.get_grid_positions()
        if self.current_position < len(positions):
            row, col = positions[self.current_position]

            # Add the label to the grid
            grid_layout.addWidget(label, row, col, Qt.AlignmentFlag.AlignCenter)

            # Update position for next image
            self.current_position += 1
            
            print(
                f"DEBUG: Added image to page {self.current_page_index} at position ({row}, {col})"
            )
        else:
            print(
                f"ERROR: Invalid position {self.current_position}, max positions: {len(positions)}"
            )
