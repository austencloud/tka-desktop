from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )


class SequenceCardCachedPageDisplayer:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab

    def display_cached_pages(self, selected_length: int):
        """Display the cached pages without recalculating."""
        # Clear the existing widgets before adding cached ones
        self.scroll_layout = self.sequence_card_tab.scroll_layout
        self.margin = 25  # Fixed margin between pages
        self.pages_cache = self.sequence_card_tab.pages_cache

        # Clear the scroll layout
        self._clear_scroll_layout()

        # Calculate the available width for two pages side by side
        scroll_area_width = self.sequence_card_tab.scroll_area.width()
        nav_sidebar_width = self.sequence_card_tab.nav_sidebar.width()
        available_width = (
            scroll_area_width - nav_sidebar_width - 40
        )  # Account for margins

        # Calculate the width for each page (A4 aspect ratio: 8.5:11)
        page_width = (available_width - self.margin) // 2
        page_height = int(page_width * 11 / 8.5)  # Maintain A4 aspect ratio

        # Update the page dimensions for all cached pages
        for page in self.pages_cache[selected_length]:
            page.setFixedSize(page_width, page_height)

        # Add cached pages back into the scroll layout
        for i in range(0, len(self.pages_cache[selected_length]), 2):
            # Create a new row layout for each pair of pages
            row_layout = QHBoxLayout()
            row_layout.setSpacing(self.margin)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            for j in range(2):  # Only add up to two items per row
                if i + j < len(self.pages_cache[selected_length]):
                    page_widget = self.pages_cache[selected_length][i + j]
                    row_layout.addWidget(page_widget)

            self.scroll_layout.addLayout(row_layout)

        self.sequence_card_tab.pages = self.sequence_card_tab.pages_cache[
            selected_length
        ]

    def _clear_scroll_layout(self):
        """Helper method to clear all widgets from the scroll layout."""
        for i in reversed(range(self.scroll_layout.count())):
            layout_item = self.scroll_layout.itemAt(i)
            widget = layout_item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                sub_layout = layout_item.layout()
                if sub_layout is not None:
                    while sub_layout.count():
                        sub_item = sub_layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget is not None:
                            sub_widget.setParent(None)
                    self.scroll_layout.removeItem(layout_item)
