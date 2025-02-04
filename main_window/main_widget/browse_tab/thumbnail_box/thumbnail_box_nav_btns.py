from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box import (
        ThumbnailBox,
    )


class ThumbnailBoxNavButtonsWidget(QWidget):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__(thumbnail_box)
        self.thumbnail_box = thumbnail_box
        self.thumbnails = thumbnail_box.thumbnails
        self.current_index = thumbnail_box.current_index
        self.thumbnail_label = thumbnail_box.image_label
        self.variation_number_label = thumbnail_box.variation_number_label
        self._setup_layout()
        self._setup_buttons()
        self.has_multiple_thumbnails = len(self.thumbnails) > 1
        if not self.has_multiple_thumbnails:
            self.hide()

    def _setup_buttons(self):
        button_texts = ["<", ">"]
        for text in button_texts:
            button = NavButton(text, self)
            self.layout.addWidget(button)

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(self.layout)

    def handle_button_click(self):
        sender: QPushButton = self.sender()
        if sender.text() == "<":
            self.thumbnail_box.current_index = (
                self.thumbnail_box.current_index - 1
            ) % len(self.thumbnails)
        elif sender.text() == ">":
            self.thumbnail_box.current_index = (
                self.thumbnail_box.current_index + 1
            ) % len(self.thumbnails)

        self.update_thumbnail(self.thumbnail_box.current_index)
        if (
            self.thumbnail_box.image_label
            == self.thumbnail_box.browse_tab.selection_handler.current_thumbnail
        ):
            sequence_viewer = self.thumbnail_box.browse_tab.sequence_viewer
            sequence_viewer.variation_number_label.setText(
                f"{self.thumbnail_box.current_index + 1}/{len(self.thumbnails)}"
            )
            sequence_viewer.current_index = self.thumbnail_box.current_index
            sequence_viewer.update_preview(self.thumbnail_box.current_index)

    def update_thumbnail(self, index):
        self.thumbnail_label.update_thumbnail(index)
        self.variation_number_label.update_index(index)

    def _setup_buttons(self):
        self.left_button = NavButton("<", self)
        self.right_button = NavButton(">", self)
        self.layout.addWidget(self.left_button)
        self.layout.addWidget(self.right_button)


class NavButton(QPushButton):
    def __init__(self, text: str, parent: ThumbnailBoxNavButtonsWidget):
        super().__init__(text, parent)
        self.clicked.connect(parent.handle_button_click)
        self.setStyleSheet("background-color: white;")
        self.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
