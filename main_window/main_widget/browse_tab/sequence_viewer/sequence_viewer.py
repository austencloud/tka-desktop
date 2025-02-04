from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from .sequence_viewer_image_label import SequenceViewerImageLabel
from .placeholder_text_label import PlaceholderTextLabel
from .sequence_viewer_action_button_panel import SequenceViewerActionButtonPanel
from .sequence_viewer_word_label import SequenceViewerWordLabel
from .sequence_viewer_nav_buttons_widget import SequenceViewerNavButtonsWidget
from ..thumbnail_box.thumbnail_box import ThumbnailBox
from ..thumbnail_box.variation_number_label import VariationNumberLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..browse_tab import BrowseTab


class SequenceViewer(QWidget):
    thumbnails: list[str] = []
    current_index = 0
    sequence_json = None

    def __init__(self, browse_tab: "BrowseTab"):
        super().__init__(browse_tab)
        self.main_widget = browse_tab.main_widget
        self.browse_tab = browse_tab
        self.current_thumbnail_box: ThumbnailBox = None
        self._setup_components()
        self._setup_layout()
        self.clear()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.word_label)
        layout.addWidget(self.variation_number_label)
        layout.addWidget(self.stacked_widget)
        layout.addWidget(self.nav_buttons_widget)
        layout.addWidget(self.action_button_panel)
        layout.addStretch(1)
        self.setLayout(layout)

    def _setup_components(self):
        self.placeholder_label = PlaceholderTextLabel(self)
        self.image_label = SequenceViewerImageLabel(self)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.placeholder_label)
        self.stacked_widget.addWidget(self.image_label)

        self.variation_number_label = VariationNumberLabel(self)
        self.nav_buttons_widget = SequenceViewerNavButtonsWidget(self)
        self.word_label = SequenceViewerWordLabel(self)
        self.action_button_panel = SequenceViewerActionButtonPanel(self)

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        if self.current_index >= len(self.thumbnails):
            self.current_index = len(self.thumbnails) - 1

        self.update_preview(self.current_index)

        if len(self.thumbnails) > 1:
            self.nav_buttons_widget.show()
            self.variation_number_label.show()
        elif len(self.thumbnails) == 1:
            self.nav_buttons_widget.hide()
            if self.current_thumbnail_box:
                self.current_thumbnail_box.nav_buttons_widget.hide()
            self.variation_number_label.hide()
        elif len(self.thumbnails) == 0:
            self.clear()

    def update_preview(self, index):
        if index is None or not self.thumbnails:
            self.stacked_widget.setCurrentWidget(self.placeholder_label)
            self.variation_number_label.clear()
            return

        pixmap = QPixmap(self.thumbnails[index])
        if pixmap.height() != 0:
            self.image_label.scale_pixmap_to_label(pixmap)
            self.stacked_widget.setCurrentWidget(self.image_label)

        if self.current_thumbnail_box:
            metadata_extractor = (
                self.current_thumbnail_box.main_widget.metadata_extractor
            )
            self.sequence_json = metadata_extractor.extract_metadata_from_file(
                self.thumbnails[index]
            )

    def update_nav_buttons(self):
        self.nav_buttons_widget.current_index = self.current_index
        self.nav_buttons_widget.refresh()

    def clear(self):
        self.stacked_widget.setCurrentWidget(self.placeholder_label)
        self.variation_number_label.clear()
        self.word_label.clear()
        self.current_index = 0
        self.current_thumbnail_box = None
        self.thumbnails = []
        self.nav_buttons_widget.hide()
        self.variation_number_label.hide()
        min_height = self.height() // 5
        self.stacked_widget.setFixedHeight(min_height)
