# src/main_window/main_widget/sequence_card_tab/components/pages/factory.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QGridLayout, QFrame
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class SequenceCardPageFactory:
    """
    Factory for creating sequence card pages with consistent styling and layout.
    """
    
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
    
    def create_page(self) -> QWidget:
        """
        Create a new page widget with proper styling and layout.
        
        Returns:
            QWidget: A new page widget with grid layout
        """
        # Create page widget
        page = QFrame()
        page.setObjectName("sequenceCardPage")
        
        # Set up grid layout
        grid_layout = QGridLayout(page)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(10)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Apply styling
        page.setStyleSheet("""
            #sequenceCardPage {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)
        
        return page
    
    def create_empty_page(self, message: str = "No sequences found") -> QWidget:
        """
        Create an empty page with a message.
        
        Args:
            message: Message to display on the empty page
            
        Returns:
            QWidget: An empty page with a message
        """
        from PyQt6.QtWidgets import QLabel, QVBoxLayout
        
        # Create page widget
        page = self.create_page()
        
        # Replace grid layout with vertical layout
        grid_layout = page.layout()
        if grid_layout:
            # Remove the grid layout
            while grid_layout.count():
                item = grid_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            
            # Delete the grid layout
            grid_layout.setParent(None)
        
        # Create vertical layout
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create message label
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet("""
            color: #7f8c8d;
            font-size: 16px;
            font-style: italic;
        """)
        
        # Add label to layout
        layout.addWidget(label)
        
        return page
