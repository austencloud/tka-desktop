import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from utilities.path_helpers import get_sequence_card_image_exporter_path

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
        selected_length = self.nav_sidebar.selected_length
        self.currently_displayed_length = selected_length

        if selected_length in self.pages_cache:
            self.cached_page_displayer.display_cached_pages(selected_length)
        else:
            export_path = get_sequence_card_image_exporter_path()
            images = self.get_all_images(export_path)
            self.image_displayer.display_images(images)
            self.pages_cache[selected_length] = self.pages.copy()

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
        if (
            self.initialized
            and self.pages_cache
            and selected_length in self.pages_cache
        ):
            if selected_length == self.currently_displayed_length:
                return

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

        self.pages.clear()
        self.load_images()
        self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)
