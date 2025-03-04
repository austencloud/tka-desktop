from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from typing import TYPE_CHECKING, Optional

from main_window.main_widget.metadata_extractor import MetaDataExtractor

from .sequence_viewer_state import SequenceViewerState
from .sequence_viewer_image_label import SequenceViewerImageLabel
from .placeholder_text_label import PlaceholderTextLabel
from .sequence_viewer_action_button_panel import SequenceViewerActionButtonPanel
from .sequence_viewer_word_label import SequenceViewerWordLabel
from .sequence_viewer_nav_buttons_widget import SequenceViewerNavButtonsWidget
from ..thumbnail_box.thumbnail_box import ThumbnailBox
from ..thumbnail_box.variation_number_label import VariationNumberLabel


if TYPE_CHECKING:
    from ..browse_tab import BrowseTab


class SequenceViewer(QWidget):
    def __init__(self, browse_tab: "BrowseTab"):
        super().__init__(browse_tab)
        self.main_widget = browse_tab.main_widget
        self.browse_tab = browse_tab

        self.current_thumbnail_box: Optional[ThumbnailBox] = None
        self.state = SequenceViewerState()
        self._setup_components()
        self._setup_layout()
        self.clear()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.word_label)
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

    def update_thumbnails(self, thumbnails: list[str]):
        self.state.update_thumbnails(thumbnails)
        current_thumbnail = self.state.get_current_thumbnail_str()
        if current_thumbnail:
            self.update_preview(self.state.current_index)
        else:
            self.clear()
        self.variation_number_label.update_index(self.state.current_index)

    def update_preview(self, index: int):
        self.state.set_current_index(index)
        current_thumbnail = self.state.get_current_thumbnail_str()

        if current_thumbnail:
            pixmap = QPixmap(current_thumbnail)
            if not pixmap.isNull():
                self.image_label.set_pixmap_with_scaling(pixmap)
                self.stacked_widget.setCurrentWidget(self.image_label)

                if self.current_thumbnail_box:
                    metadata_extractor = MetaDataExtractor()
                    self.state.sequence_json = (
                        metadata_extractor.extract_metadata_from_file(current_thumbnail)
                    )

        else:
            self.stacked_widget.setCurrentWidget(self.placeholder_label)
            self.variation_number_label.clear()
        self.variation_number_label.update_index(index)

    def update_nav_buttons(self):
        self.nav_buttons_widget.current_index = self.state.current_index
        self.nav_buttons_widget.refresh()

    def clear(self):
        self.state.clear()
        self.stacked_widget.setCurrentWidget(self.placeholder_label)
        self.variation_number_label.clear()
        self.word_label.clear()
        self.nav_buttons_widget.hide()
        self.variation_number_label.hide()
        self.current_thumbnail_box = None

    def get_thumbnail_at_current_index(self) -> Optional[str]:
        return self.state.get_current_thumbnail_str()
