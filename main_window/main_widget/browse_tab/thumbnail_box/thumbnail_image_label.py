from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box import (
        ThumbnailBox,
    )


class ThumbnailImageLabel(QLabel):
    target_width = 0
    is_selected = False
    index = None
    pixmap: QPixmap = None

    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box
        self.state = thumbnail_box.state
        self.metadata_extractor = thumbnail_box.main_widget.metadata_extractor
        self.setStyleSheet("border: 3px solid black;")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_thumbnail(self, index):
        if self.state.thumbnails and 0 <= index < len(self.state.thumbnails):
            pixmap = QPixmap(self.state.thumbnails[index])
            self.set_pixmap_to_fit(pixmap)

    def set_pixmap_to_fit(self, pixmap: QPixmap):
        current_index = self.state.current_index
        sequence_length = self.metadata_extractor.get_length(
            self.state.thumbnails[current_index]
        )

        target_width = self._get_target_width(sequence_length)

        scaled_pixmap = pixmap.scaledToWidth(
            target_width, Qt.TransformationMode.SmoothTransformation
        )

        self.setPixmap(scaled_pixmap)

    def _get_target_width(self, sequence_length):
        if sequence_length == 1:
            target_width = int(self.thumbnail_box.width() * 0.6) - int(
                self.thumbnail_box.margin * 2
            )
        else:
            target_width = self.thumbnail_box.width() - int(
                self.thumbnail_box.margin * 2
            )

        return target_width

    def mousePressEvent(self, event: "QMouseEvent"):
        if self.state.thumbnails:
            metadata = self.metadata_extractor.extract_metadata_from_file(
                self.state.thumbnails[0]
            )
            self.thumbnail_box.browse_tab.selection_handler.on_box_thumbnail_clicked(
                self, metadata
            )

        else:
            self.thumbnail_box.browse_tab.deletion_handler.delete_variation(
                self.thumbnail_box, self.state.current_index
            )

    def set_selected(self, selected: bool):
        self.is_selected = selected
        if selected:
            self.setStyleSheet("border: 3px solid blue;")
        else:
            self.setStyleSheet("border: 3px solid black;")

    def enterEvent(self, event: QEvent):
        self.setStyleSheet("border: 3px solid gold;")
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent):
        self.setStyleSheet(
            "border: 3px solid black;"
            if not self.is_selected
            else "border: 3px solid blue;"
        )
        super().leaveEvent(event)
