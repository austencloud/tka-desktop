from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout

from .sequence_viewer_nav_button import SequenceViewerNavButton

if TYPE_CHECKING:
    from .sequence_viewer import SequenceViewer


class SequenceViewerNavButtonsWidget(QWidget):
    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__(sequence_viewer)
        self.sequence_viewer = sequence_viewer
        # Remove cached thumbnails reference
        self.state = sequence_viewer.state
        self.variation_number_label = sequence_viewer.variation_number_label
        self.image_label = sequence_viewer.image_label

        self._setup_buttons()
        self.has_multiple_thumbnails = len(self.state.thumbnails) > 1
        if not self.has_multiple_thumbnails:
            self.hide()
    def _setup_buttons(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(15)  # Adjust spacing between buttons

        self.left_button = SequenceViewerNavButton("⮜", self)  # Left Arrow
        self.right_button = SequenceViewerNavButton("⮞", self)  # Right Arrow

        layout.addStretch(1)
        layout.addWidget(self.left_button)
        layout.addWidget(self.variation_number_label)  # Centered label
        layout.addWidget(self.right_button)
        layout.addStretch(1)

        self.setLayout(layout)

    def handle_button_click(self):
        if not self.sequence_viewer.state.thumbnails:
            return
        sender: QPushButton = self.sender()
        if sender.text() in ("⮜", "←"):
            self.state.current_index = (self.state.current_index - 1) % len(
                self.sequence_viewer.state.thumbnails
            )
        else:
            self.state.current_index = (self.state.current_index + 1) % len(
                self.sequence_viewer.state.thumbnails
            )

        self.sequence_viewer.update_preview(self.state.current_index)
        self.sequence_viewer.variation_number_label.setText(
            f"{self.state.current_index + 1}/"
            f"{len(self.sequence_viewer.state.thumbnails)}"
        )
        thumbnail_box = self.sequence_viewer.current_thumbnail_box
        if thumbnail_box:
            thumbnail_box.state.current_index = self.state.current_index
            box_nav = self.sequence_viewer.current_thumbnail_box.nav_buttons_widget
            box_nav.thumbnail_box.state.current_index = self.state.current_index
            box_nav.update_thumbnail(self.state.current_index)

    def update_thumbnail(self):
        self.image_label.update_thumbnail(self.state.current_index)
        self.variation_number_label.update_index(self.state.current_index)

    def refresh(self):
        """Update the navigation buttons based on current state."""
        # Access current thumbnails directly from the sequence viewer's state
        thumbnails = self.sequence_viewer.state.thumbnails
        self.update_thumbnail()
        if len(thumbnails) == 1:
            self.variation_number_label.hide()
            self.hide()
        else:
            self.variation_number_label.show()
            self.show()
            # Ensure current_index is from the updated state
            current_index = self.sequence_viewer.state.current_index
            self.variation_number_label.update_index(current_index)

    def resizeEvent(self, event):
        # Ensure proper button and font sizing
        font_size = max(14, self.sequence_viewer.main_widget.width() // 75)
        button_size = self.sequence_viewer.main_widget.height() // 20
        for btn in (self.left_button, self.right_button):
            font = btn.font()
            font.setPointSize(font_size)
            btn.setFont(font)
            btn.setFixedSize(button_size, button_size)
        super().resizeEvent(event)
