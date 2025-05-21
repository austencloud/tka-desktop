import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from utils.path_helpers import get_sequence_card_image_exporter_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )


class SequenceCardRefresher:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.nav_sidebar = sequence_card_tab.nav_sidebar
        self.image_displayer = sequence_card_tab.image_displayer
        self.pages_cache = sequence_card_tab.pages_cache
        self.pages = sequence_card_tab.pages
        self.cached_page_displayer = sequence_card_tab.cached_page_displayer
        self.currently_displayed_length = 16
        self.initialized = False

    def load_images(self):
        """Load sequence card images for the selected length."""
        selected_length = self.nav_sidebar.selected_length
        self.currently_displayed_length = selected_length

        print(f"Loading images for sequence length: {selected_length}")

        # If we have cached pages for this length, use them
        if selected_length in self.pages_cache:
            print(f"Using cached pages for length {selected_length}")
            self.cached_page_displayer.display_cached_pages(selected_length)
        else:
            # Otherwise, load images from the export directory
            export_path = get_sequence_card_image_exporter_path()
            print(f"Loading images from: {export_path}")

            # Get all images from the export directory
            images = self.get_all_images(export_path)
            print(f"Found {len(images)} total images")

            # Display the images filtered by the selected length
            self.image_displayer.display_images(images)

            # Cache the pages for future use
            self.pages_cache[selected_length] = self.pages.copy()
            print(f"Cached {len(self.pages)} pages for length {selected_length}")

    def get_all_images(self, path: str) -> list[str]:
        images = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    images.append(os.path.join(root, file))
        return images

    def refresh_sequence_cards(self):
        """Refresh the displayed sequence cards based on selected options."""
        self.scroll_layout = self.sequence_card_tab.scroll_layout
        self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)
        selected_length = self.nav_sidebar.selected_length

        # Update the description label to show the current length
        self.sequence_card_tab.description_label.setText(
            f"Viewing sequences with length {selected_length} - Select a length from the sidebar"
        )

        # If we already have this length cached and it's not the current display, just switch
        if (
            self.initialized
            and self.pages_cache
            and selected_length in self.pages_cache
            and selected_length != self.currently_displayed_length
        ):
            self.clear_scroll_layout()
            self.pages.clear()
            self.cached_page_displayer.display_cached_pages(selected_length)
            self.currently_displayed_length = selected_length
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
            return
        # If we're already displaying this length, do nothing
        elif selected_length == self.currently_displayed_length and self.initialized:
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
            return

        # Otherwise, we need to load the images
        self.clear_scroll_layout()
        self.pages.clear()
        self.load_images()
        self.initialized = True
        self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def clear_scroll_layout(self):
        """Clear all widgets from the scroll layout."""
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
