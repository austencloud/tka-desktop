from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from main_window.main_widget.browse_tab.thumbnail_box.favorites_manager import (
    FavoritesManager,
)
from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box_nav_btns import (
    ThumbnailBoxNavButtonsWidget,
)
from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_image_label import (
    ThumbnailImageLabel,
)

from .word_label import WordLabel
from .variation_number_label import VariationNumberLabel
from .thumbnail_box_state import ThumbnailBoxState

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class ThumbnailBox(QWidget):
    margin = 10

    def __init__(
        self, browse_tab: "BrowseTab", word: str, thumbnails: list[str]
    ) -> None:
        super().__init__(browse_tab)
        self.word = word
        self.main_widget = browse_tab.main_widget
        self.browse_tab = browse_tab
        self.sequence_picker = self.browse_tab.sequence_picker
        self.scroll_Area = self.sequence_picker.scroll_widget.scroll_area

        self.state = ThumbnailBoxState(thumbnails)

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.favorites_manager = FavoritesManager(self)
        self.word_label = WordLabel(self)
        self.image_label = ThumbnailImageLabel(self)
        self.variation_number_label = VariationNumberLabel(self)
        self.nav_buttons_widget = ThumbnailBoxNavButtonsWidget(self)

    def _setup_layout(self):
        self.setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.word_label, 1)
        layout.addWidget(self.image_label, 8)
        layout.addWidget(self.variation_number_label, 1)
        layout.addWidget(self.nav_buttons_widget, 1)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        scrollbar_width = self.scroll_Area.verticalScrollBar().width()
        scroll_widget_width = (
            self.main_widget.left_stack.width()
            - scrollbar_width
            - self.sequence_picker.nav_sidebar.width()
        )
        width = scroll_widget_width // 3
        self.setFixedWidth(width)

    def _get_our_sequence_length(self) -> int:
        if self.state.thumbnails:
            first_thumb = self.state.thumbnails[0]
            return (
                self.browse_tab.main_widget.metadata_extractor.get_length(first_thumb)
                or 0
            )
        return 0

    def update_thumbnails(self, thumbnails=[]):
        self.state.update_thumbnails(thumbnails)
        self.nav_buttons_widget.state.thumbnails = thumbnails
        self.image_label.state.thumbnails = thumbnails

        if self == self.browse_tab.sequence_viewer.current_thumbnail_box:
            self.browse_tab.sequence_viewer.update_thumbnails(self.state.thumbnails)

        self.variation_number_label.update_index()
