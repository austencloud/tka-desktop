from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )


class SequenceCardPageFactory:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab

    def create_page(self) -> QFrame:
        """Create a new page frame for displaying sequence card images."""
        print("Creating new sequence card page")

        # Get references to needed components
        self.image_displayer = self.sequence_card_tab.image_displayer
        scroll_layout = self.sequence_card_tab.scroll_layout
        margin = self.sequence_card_tab.image_displayer.margin

        # Check if we need to create a new row layout or use an existing one
        if (
            not scroll_layout.count()
            or scroll_layout.itemAt(scroll_layout.count() - 1).layout().count() >= 2
        ):
            # Create a new row layout
            print("Creating new row layout")
            current_row_layout = QHBoxLayout()
            current_row_layout.setSpacing(margin)
            current_row_layout.setContentsMargins(margin, margin, margin, margin)
            scroll_layout.addLayout(current_row_layout)
        else:
            # Use the existing row layout
            print("Using existing row layout")
            current_row_layout = scroll_layout.itemAt(
                scroll_layout.count() - 1
            ).layout()

        # Create the page frame
        page_frame = QFrame(self.sequence_card_tab.scroll_content)
        page_frame.setFixedSize(
            self.image_displayer.page_width, self.image_displayer.page_height
        )

        # Style the page frame
        page_frame.setStyleSheet(
            """
            background-color: white;
            border: 1px solid #aaaaaa;
            border-radius: 4px;
        """
        )

        # Create the layout for the page
        page_layout = QGridLayout(page_frame)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        # Add the page to the row layout
        current_row_layout.addWidget(page_frame)

        print(f"Created page with size: {page_frame.width()}x{page_frame.height()}")

        return page_frame  # Return the frame instead of the layout
