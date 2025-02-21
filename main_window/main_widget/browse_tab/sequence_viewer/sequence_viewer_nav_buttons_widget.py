from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout

from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer_nav_button import (
    SequenceViewerNavButton,
)


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer import (
        SequenceViewer,
    )


class SequenceViewerNavButtonsWidget(QWidget):
    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__(sequence_viewer)
        self.sequence_viewer = sequence_viewer
        self.thumbnails = sequence_viewer.state.thumbnails
        self.state = sequence_viewer.state
        self.current_index = self.state.current_index
        self.variation_number_label = sequence_viewer.variation_number_label
        self.image_label = sequence_viewer.image_label
        self._setup_buttons()
        self.has_multiple_thumbnails = len(self.thumbnails) > 1
        if not self.has_multiple_thumbnails:
            self.hide()

    def _setup_buttons(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.buttons: list[SequenceViewerNavButton] = []
        self.left_button = SequenceViewerNavButton("<", self)
        self.right_button = SequenceViewerNavButton(">", self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.left_button, 6)
        self.layout.addWidget(self.right_button, 6)
        self.layout.addStretch(1)

    def handle_button_click(self):
        if not self.sequence_viewer.state.thumbnails:
            return
        sender: QPushButton = self.sender()
        if sender.text() == "<":
            self.state.current_index = (self.state.current_index - 1) % len(
                self.sequence_viewer.state.thumbnails
            )
        elif sender.text() == ">":
            self.state.current_index = (self.state.current_index + 1) % len(
                self.sequence_viewer.state.thumbnails
            )
        self.sequence_viewer.update_preview(self.state.current_index)
        self.sequence_viewer.variation_number_label.setText(
            f"{self.state.current_index + 1}/{len(self.sequence_viewer.state.thumbnails)}"
        )

        self.sequence_viewer.current_thumbnail_box.state.current_index = (
            self.state.current_index
        )
        box_nav_buttons_widget = (
            self.sequence_viewer.current_thumbnail_box.nav_buttons_widget
        )
        box_nav_buttons_widget.thumbnail_box.state.current_index = (
            self.state.current_index
        )
        box_nav_buttons_widget.update_thumbnail(self.state.current_index)

    def update_thumbnail(self):
        # self.image_label.current_index = self.current_index
        self.image_label.update_thumbnail(self.current_index)
        self.variation_number_label.update_index(self.current_index)

    def refresh(self):
        thumbnails = self.sequence_viewer.state.thumbnails

        self.update_thumbnail()
        if len(thumbnails) == 1:
            self.variation_number_label.hide()
            self.hide()
        else:
            self.variation_number_label.show()
            self.show()
            self.variation_number_label.update_index(self.current_index + 1)

    def resizeEvent(self, event):
        font_size = self.sequence_viewer.main_widget.width() // 20
        for button in self.buttons:
            button.setFont(QFont("Georgia", font_size, QFont.Weight.Bold))
        super().resizeEvent(event)
