from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent, QPainter, QColor, QPen
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING, Optional

from data.constants import BLUE
from main_window.main_widget.metadata_extractor import MetaDataExtractor

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class ThumbnailImageLabel(QLabel):
    border_width = 4

    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box
        self.metadata_extractor = MetaDataExtractor()

        if self.thumbnail_box.in_sequence_viewer:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._border_color: Optional[str] = None
        self._original_pixmap: Optional[QPixmap] = None
        self.current_path: Optional[str] = None

    def update_thumbnail(self, index: int):
        """Update the displayed image based on the given index."""
        if not self.thumbnail_box.state.thumbnails or not (
            0 <= index < len(self.thumbnail_box.state.thumbnails)
        ):
            return

        if not self.thumbnail_box.initialized:
            self.thumbnail_box.initialized = True

        path = self.thumbnail_box.state.thumbnails[index]
        if path != self.current_path:
            self.current_path = path
            self._original_pixmap = QPixmap(path)

        self._resize_pixmap_to_fit()

    def _calculate_available_space(self) -> QSize:
        """Calculate available space for the image inside `SequenceViewer` or `ThumbnailBox`."""
        if self.thumbnail_box.in_sequence_viewer:
            sequence_viewer = self.thumbnail_box.browse_tab.sequence_viewer
            available_width = int(sequence_viewer.main_widget.width() * 1 / 3 * 0.95)
            available_height = int(sequence_viewer.main_widget.height() * 0.65)
        else:
            nav_bar = self.thumbnail_box.sequence_picker.nav_sidebar
            if nav_bar.width() < 20:
                nav_bar.resize_sidebar()
            scrollbar_width = (
                self.thumbnail_box.sequence_picker.scroll_widget.calculate_scrollbar_width()
            )
            scroll_widget_width = (
                (self.thumbnail_box.main_widget.width() * 2 / 3)
                - scrollbar_width
                - nav_bar.width()
            )
            available_width = int(
                scroll_widget_width // 3 - (self.thumbnail_box.margin * 2)
            )

            seq_len = self.metadata_extractor.get_length(
                self.thumbnail_box.state.thumbnails[
                    self.thumbnail_box.state.current_index
                ]
            )
            if seq_len == 1:
                available_width = int(available_width * 0.6)

            aspect_ratio = (
                self._original_pixmap.width() / self._original_pixmap.height()
                if self._original_pixmap
                else 1
            )
            available_height = int(available_width / aspect_ratio)

        return QSize(available_width, available_height)

    def _resize_pixmap_to_fit(self):
        """Resize the pixmap while maintaining its aspect ratio and centering it."""
        if not self._original_pixmap:
            return

        available_size = self._calculate_available_space()
        available_width, available_height = (
            available_size.width(),
            available_size.height(),
        )

        aspect_ratio = self._original_pixmap.height() / self._original_pixmap.width()
        target_width = available_width
        target_height = int(target_width * aspect_ratio)

        while target_height > available_height and target_width > 0:
            target_width -= 1
            target_height = int(target_width * aspect_ratio) - 1

        # Scale the pixmap
        scaled_pixmap = self._original_pixmap.scaled(
            target_width,
            target_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Update label size to fit the image and center it
        self.setFixedSize(available_width, available_height)
        self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event: QMouseEvent):
        if self.thumbnail_box.in_sequence_viewer:
            return
        if not self.thumbnail_box.state.thumbnails:
            raise ValueError(f"No thumbnails for {self.thumbnail_box.word}")
        metadata = self.metadata_extractor.extract_metadata_from_file(
            self.thumbnail_box.state.thumbnails[0]
        )
        self.thumbnail_box.browse_tab.selection_handler.on_thumbnail_clicked(
            self, metadata
        )

    def enterEvent(self, event):
        """Highlight border on hover."""
        self._border_color = "gold"
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Remove border highlight when leaving hover."""
        self._border_color = BLUE if self.thumbnail_box.state.current_index else None
        self.update()
        super().leaveEvent(event)

    def set_selected(self, selected: bool):
        """Set selection border color."""
        self._border_color = BLUE if selected else None
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.thumbnail_box.in_sequence_viewer:
            if self._original_pixmap:
                painter = QPainter(self)
                pen = QPen(QColor("gold"))
                pen.setWidth(self.border_width)
                pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
                painter.setPen(pen)
                img_width, img_height = self.pixmap().width(), self.pixmap().height()
                x = (self.width() - img_width) // 2
                y = (self.height() - img_height) // 2
                rect = QRect(x, y, img_width, img_height)
                painter.drawRect(
                    rect.adjusted(
                        self.border_width // 2,
                        self.border_width // 2,
                        -self.border_width // 2,
                        -self.border_width // 2,
                    )
                )
        else:
            if self._border_color and self._original_pixmap:
                painter = QPainter(self)
                pen = QPen(QColor(self._border_color))
                pen.setWidth(self.border_width)
                pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
                painter.setPen(pen)
                img_width, img_height = self.pixmap().width(), self.pixmap().height()
                x = (self.width() - img_width) // 2
                y = (self.height() - img_height) // 2
                rect = QRect(x, y, img_width, img_height)
                painter.drawRect(
                    rect.adjusted(
                        self.border_width // 2,
                        self.border_width // 2,
                        -self.border_width // 2,
                        -self.border_width // 2,
                    )
                )
