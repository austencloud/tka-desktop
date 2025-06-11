from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QSizePolicy
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from main_window.main_widget.write_tab.act_browser.act_thumbnail_box import (
    ActThumbnailBox,
)

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class ActBrowser(QScrollArea):
    def __init__(self, act_tab: "WriteTab") -> None:
        super().__init__(act_tab)
        self.act_tab = act_tab
        self.main_widget = act_tab.main_widget
        self.thumbnail_boxes: list[ActThumbnailBox] = []
        self.metadata_extractor = MetaDataExtractor()

        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)

        # Set 0 margins and spacing to eliminate any implicit gaps
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        self.scroll_content.setLayout(self.grid_layout)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._setup_layout()
        # self.populate_favorites()
        self.setStyleSheet("background-color: rgba(0,0,0,0);")

    def _setup_layout(self):
        self.setWidgetResizable(True)
        self.setWidget(self.scroll_content)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

    def populate_favorites(self):
        for box in self.thumbnail_boxes:
            box.setParent(None)

        self.thumbnail_boxes = []

        sequences = self.act_tab.main_widget.browse_tab.get.all_sequences()

        row, col = 0, 0
        max_columns = 2

        for sequence in sequences:
            thumbnails = sequence[1]
            is_favorite = self.metadata_extractor.get_favorite_status(thumbnails[0])

            if is_favorite:
                thumbnail_box = ActThumbnailBox(self, sequence[0], thumbnails)

                self.thumbnail_boxes.append(thumbnail_box)
                self.grid_layout.addWidget(thumbnail_box, row, col)  # Remove AlignTop

                col += 1
                if col == max_columns:
                    col = 0
                    row += 1

    def resizeEvent(self, event):
        super().resizeEvent(event)
        scroll_bar_width = self.verticalScrollBar().width()
        browser_width = self.width() - scroll_bar_width
        self.scroll_content.setMinimumWidth(browser_width)
