# src/main_window/main_widget/sequence_card_tab/components/display/ui_layout_manager.py
from typing import List, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QGridLayout, QApplication
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class UILayoutManager:
    """
    Manages UI layout for the sequence card display.
    
    This class is responsible for:
    1. Creating and managing the multi-column layout for page previews
    2. Clearing existing pages and layouts
    3. Handling UI updates and refreshes
    """
    
    def __init__(self, sequence_card_tab: "SequenceCardTab", page_spacing: int = 20):
        self.sequence_card_tab = sequence_card_tab
        self.page_spacing = page_spacing
        self.preview_grid = None
        
    def create_multi_column_layout(self) -> QGridLayout:
        """
        Create a multi-column layout for page previews.
        
        Returns:
            QGridLayout: The created grid layout
        """
        # Clear the scroll layout
        self._clear_scroll_layout()

        # Create a grid layout for the page previews
        self.preview_grid = QGridLayout()
        self.preview_grid.setSpacing(self.page_spacing)
        self.preview_grid.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        # Add the grid layout to the scroll layout
        self.sequence_card_tab.scroll_layout.addLayout(self.preview_grid)
        
        return self.preview_grid
        
    def clear_existing_pages(self, pages: List[QWidget]) -> None:
        """
        Clear all existing pages and remove them from the layout.

        This method:
        1. Removes all page widgets from the preview grid
        2. Forces a UI update to ensure the layout is properly cleared
        
        Args:
            pages: List of page widgets to clear
        """
        # First, remove all widgets from the preview grid if it exists
        if hasattr(self, "preview_grid") and self.preview_grid:
            # Get all widgets from the grid layout
            for i in range(self.preview_grid.count()):
                item = self.preview_grid.itemAt(i)
                if item and item.widget():
                    # Remove the widget from the layout and delete it
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()

            print(f"DEBUG: Removed all widgets from preview grid")

        # Force a UI update to ensure the layout is properly cleared
        QApplication.processEvents()
        
    def _clear_scroll_layout(self) -> None:
        """Clear the scroll layout completely."""
        if (
            hasattr(self.sequence_card_tab, "scroll_layout")
            and self.sequence_card_tab.scroll_layout
        ):
            while self.sequence_card_tab.scroll_layout.count():
                item = self.sequence_card_tab.scroll_layout.takeAt(0)
                if item and item.widget():
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()
                elif item and item.layout():
                    # Get the layout
                    layout = item.layout()

                    # Remove all widgets from the sublayout
                    while layout.count():
                        subitem = layout.takeAt(0)
                        if subitem and subitem.widget():
                            widget = subitem.widget()
                            if widget:
                                widget.setParent(None)
                                widget.deleteLater()

                    # Remove the layout itself
                    self.sequence_card_tab.scroll_layout.removeItem(item)
