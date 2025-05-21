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
        margin = 25  # Fixed margin between pages

        # Calculate the available width for two pages side by side
        scroll_area_width = self.sequence_card_tab.scroll_area.width()
        nav_sidebar_width = self.sequence_card_tab.nav_sidebar.width()
        available_width = (
            scroll_area_width - nav_sidebar_width - 40
        )  # Account for margins

        # Calculate the width for each page (A4 aspect ratio: 8.5:11)
        page_width = (available_width - margin) // 2
        page_height = int(page_width * 11 / 8.5)  # Maintain A4 aspect ratio

        # Store the calculated dimensions for use in other components
        self.image_displayer.page_width = page_width
        self.image_displayer.page_height = page_height
        self.image_displayer.margin = margin

        # Check if we need to create a new row layout or use an existing one
        if (
            not scroll_layout.count()
            or scroll_layout.itemAt(scroll_layout.count() - 1).layout().count() >= 2
        ):
            # Create a new row layout
            print("Creating new row layout")
            current_row_layout = QHBoxLayout()
            current_row_layout.setSpacing(margin)
            current_row_layout.setContentsMargins(0, 0, 0, 0)
            current_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scroll_layout.addLayout(current_row_layout)
        else:
            # Use the existing row layout
            print("Using existing row layout")
            current_row_layout = scroll_layout.itemAt(
                scroll_layout.count() - 1
            ).layout()

        # Create the page frame
        page_frame = QFrame(self.sequence_card_tab.scroll_content)

        # Use sizePolicy to make the page responsive
        size_policy = page_frame.sizePolicy()
        size_policy.setHorizontalPolicy(size_policy.Policy.Preferred)
        size_policy.setVerticalPolicy(size_policy.Policy.Preferred)
        page_frame.setSizePolicy(size_policy)

        # Set the size of the page
        page_frame.setFixedSize(page_width, page_height)

        # Style the page frame with a border and shadow
        page_frame.setStyleSheet(
            """
            background-color: white;
            border: 1px solid #aaaaaa;
            border-radius: 4px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
