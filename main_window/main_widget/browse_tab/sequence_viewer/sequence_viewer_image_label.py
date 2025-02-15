from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QResizeEvent
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
        """Set the pixmap and scale it to fit the available space within the SequenceViewer."""
        self._original_pixmap = pixmap
        self._scale_pixmap_to_fit()

    def _calculate_available_space(self) -> tuple[int, int]:
        sequence_viewer = self.sequence_viewer
        available_height = int(sequence_viewer.height() * 0.65)

        # Calculate the width available for the image
        available_width = sequence_viewer.width()

        return available_width, available_height

    def _scale_pixmap_to_fit(self):
        if not self._original_pixmap:
            return

        available_width, available_height = self._calculate_available_space()

        # Start with the available width
        target_width = available_width
        aspect_ratio = self._original_pixmap.height() / self._original_pixmap.width()

        # Calculate the height that would result from using the full available width
        target_height = int(target_width * aspect_ratio)

        # If height is too tall, reduce width iteratively until it fits
        while target_height > available_height and target_width > 0:
            target_width -= 1
            target_height = int(target_width * aspect_ratio) - 1

        # Final safeguard
        target_width = max(1, target_width)
        target_height = max(1, target_height)

        #  we need to change the taget_width or target_height according to the image's aspect ratio. Whichever is set to the available width/height should be kept, the other should be calculated based on the aspect ratio.
        if target_width == available_width - 1:
            target_height = int(target_width * aspect_ratio)
        elif target_height == available_height - 1:
            target_width = int(target_height / aspect_ratio)

        # Scale the pixmap accordingly
        scaled_pixmap = self._original_pixmap.scaled(
            target_width,
            target_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setFixedHeight(target_height)
        self.sequence_viewer.stacked_widget.setFixedHeight(target_height)
        self.setPixmap(scaled_pixmap)

    # def resizeEvent(self, event: QResizeEvent):
    #     self._scale_pixmap_to_fit()
    #     super().resizeEvent(event)

    def update_thumbnail(self, index: int):
        """Update the thumbnail to the one at the given index in the thumbnails list."""
        if not self.sequence_viewer.state.thumbnails:
            return

        self.set_pixmap_with_scaling(
            QPixmap(self.sequence_viewer.state.thumbnails[index])
        )
        self.sequence_viewer.variation_number_label.update_index(index)
