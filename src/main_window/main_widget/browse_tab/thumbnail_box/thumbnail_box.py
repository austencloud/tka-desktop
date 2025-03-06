from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box_favorites_manager import (
    ThumbnailBoxFavoritesManager,
)
from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box_nav_buttons_widget import (
    ThumbnailBoxNavButtonsWidget,
)
from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_image_label import (
    ThumbnailImageLabel,
)

from .thumbnail_box_header import ThumbnailBoxHeader
from .variation_number_label import VariationNumberLabel
from .thumbnail_box_state import ThumbnailBoxState

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class ThumbnailBox(QWidget):
    margin = 10

    def __init__(
        self,
        browse_tab: "BrowseTab",
        word: str,
        thumbnails: list[str],
        in_sequence_viewer=False,
    ) -> None:
        super().__init__(browse_tab)
        self.word = word
        self.main_widget = browse_tab.main_widget
        self.browse_tab = browse_tab
        self.sequence_picker = self.browse_tab.sequence_picker
        self.scroll_Area = self.sequence_picker.scroll_widget.scroll_area
        self.in_sequence_viewer = in_sequence_viewer
        self.state = ThumbnailBoxState(thumbnails)

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.favorites_manager = ThumbnailBoxFavoritesManager(self)
        self.header = ThumbnailBoxHeader(self)
        self.image_label = ThumbnailImageLabel(self)
        self.variation_number_label = VariationNumberLabel(self)
        self.nav_buttons_widget = ThumbnailBoxNavButtonsWidget(self)

    def _setup_layout(self):
        self.setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.header)
        layout.addWidget(self.image_label)
        layout.addWidget(self.nav_buttons_widget)
        layout.addStretch()
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_thumbnail_box()

    def resize_thumbnail_box(self):
        if self.in_sequence_viewer:
            self.setFixedWidth(self.browse_tab.sequence_viewer.width())
        else:
            nav_bar = self.sequence_picker.nav_sidebar
            if nav_bar.width() < 20:
                nav_bar.resize_sidebar()
            scrollbar_width = (
                self.sequence_picker.scroll_widget.calculate_scrollbar_width()
            )
            scroll_widget_width = (
                self.main_widget.width() * 2 / 3
                - scrollbar_width
                - self.sequence_picker.nav_sidebar.width()
            )
            width = int(scroll_widget_width // 3)
            self.setFixedWidth(width)

    def update_thumbnails(self, thumbnails=[]):
        self.state.update_thumbnails(thumbnails)
        self.nav_buttons_widget.state.thumbnails = thumbnails

        if self == self.browse_tab.sequence_viewer.state.matching_thumbnail_box:
            self.browse_tab.sequence_viewer.update_thumbnails(self.state.thumbnails)

        # self.variation_number_label.update_index(self.state.current_index)
        self.header.difficulty_label.update_difficulty_label()  # 🆕 Update difficulty!
        self.image_label.update_thumbnail(self.state.current_index)

