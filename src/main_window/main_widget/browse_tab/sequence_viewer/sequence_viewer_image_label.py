from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QSizePolicy
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .sequence_viewer import SequenceViewer


class SequenceViewerImageLabel(QLabel):
    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__(sequence_viewer)
        self.sequence_viewer = sequence_viewer
        self._original_pixmap: QPixmap | None = None

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(False)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_pixmap_with_scaling(self, pixmap: QPixmap):
        self._original_pixmap = pixmap
        self.set_pixmap_to_fit()

    def _calculate_available_space(self) -> tuple[int, int]:
        sequence_viewer = self.sequence_viewer
        available_height = int(sequence_viewer.main_widget.height() * 0.65)
        available_width = int(sequence_viewer.main_widget.width() * 1 / 3 * 0.95)

        return available_width, available_height

    def set_pixmap_to_fit(self):
        if not self._original_pixmap:
            return

        available_width, available_height = self._calculate_available_space()

        target_width = available_width
        aspect_ratio = self._original_pixmap.height() / self._original_pixmap.width()

        target_height = int(target_width * aspect_ratio)

        while target_height > available_height and target_width > 0:
            target_width -= 1
            target_height = int(target_width * aspect_ratio) - 1

        target_width = max(1, target_width)
        target_height = max(1, target_height)

        if target_width == available_width - 1:
            target_height = int(target_width * aspect_ratio)
        elif target_height == available_height - 1:
            target_width = int(target_height / aspect_ratio)

        scaled_pixmap = self._original_pixmap.scaled(
            target_width,
            target_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setFixedHeight(target_height)
        self.sequence_viewer.stacked_widget.setFixedHeight(target_height)
        self.setPixmap(scaled_pixmap)

    def update_thumbnail(self, index: int):
        if not self.sequence_viewer.state.thumbnails:
            return

        self.set_pixmap_with_scaling(
            QPixmap(self.sequence_viewer.state.thumbnails[index])
        )
        self.sequence_viewer.variation_number_label.update_index(index)
