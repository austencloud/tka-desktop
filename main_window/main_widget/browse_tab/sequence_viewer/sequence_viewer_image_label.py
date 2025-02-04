from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .sequence_viewer import SequenceViewer


class SequenceViewerImageLabel(QLabel):
    thumbnails: list[str] = []

    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__()
        self.sequence_viewer = sequence_viewer
        self.current_index = sequence_viewer.current_index
        self.metadata_extractor = sequence_viewer.main_widget.metadata_extractor
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(False)

    def scale_pixmap_to_label(self, pixmap: QPixmap):
        label_width = int(self.sequence_viewer.width() * 0.9)
        aspect_ratio = pixmap.height() / pixmap.width()
        new_height = int(label_width * aspect_ratio)
        if new_height > self.sequence_viewer.height() * 0.8:
            new_height = int(self.sequence_viewer.height() * 0.8)
            label_width = int(new_height / aspect_ratio)

        scaled_pixmap = pixmap.scaled(
            label_width,
            new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled_pixmap)
        self.setFixedHeight(new_height)
        self.sequence_viewer.stacked_widget.setFixedHeight(new_height)

    def update_thumbnail(self):
        self.thumbnails = self.sequence_viewer.thumbnails
        pixmap = QPixmap(self.thumbnails[self.sequence_viewer.current_index])
        self.set_pixmap_to_fit(pixmap)

    def set_pixmap_to_fit(self, pixmap: QPixmap):
        current_index = self.sequence_viewer.current_index
        sequence_length = self.metadata_extractor.get_sequence_length(
            self.thumbnails[current_index]
        )
        target_width = self._get_target_width(sequence_length)
        scaled_pixmap = pixmap.scaledToWidth(
            target_width, Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)

    def _get_target_width(self, sequence_length):
        if sequence_length == 1:
            return int(self.sequence_viewer.width() * 0.6)
        return int(self.sequence_viewer.width() * 0.9)

