from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent, QPainter, QColor, QPen
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING, Optional

from data.constants import GOLD, BLUE
from main_window.main_widget.metadata_extractor import MetaDataExtractor

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class ThumbnailImageLabel(QLabel):
    border_width = 4
    selected = False

    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box
        self.metadata_extractor = MetaDataExtractor()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._border_color: Optional[str] = None
        self._original_pixmap: Optional[QPixmap] = None
        self.current_path: Optional[str] = None
        self._cached_available_size: Optional[QSize] = None

    def update_thumbnail(self, index: int):
        """Update the displayed image based on the given index."""
        if not self.thumbnail_box.state.thumbnails or not (
            0 <= index < len(self.thumbnail_box.state.thumbnails)
        ):
            return

        path = self.thumbnail_box.state.thumbnails[index]
        if path != self.current_path:
            self.current_path = path
            self._original_pixmap = QPixmap(path)

        self._resize_pixmap_to_fit()

    def _calculate_available_space(self) -> QSize:
        """Calculate available space for the image."""
        if self._cached_available_size:
            return self._cached_available_size  # Use cached size if available

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

            available_height = int(available_width / self._get_aspect_ratio())

        self._cached_available_size = QSize(available_width, available_height)
        return self._cached_available_size

    def _get_aspect_ratio(self):
        return (
            self._original_pixmap.width() / self._original_pixmap.height()
            if self._original_pixmap
            else 1
        )

    def _calculate_scaled_pixmap_size(
        self, available_width: int, available_height: int
    ) -> QSize:
        aspect_ratio = self._original_pixmap.height() / self._original_pixmap.width()
        target_width = available_width
        target_height = int(target_width * aspect_ratio)
        while target_height > available_height and target_width > 0:
            target_width -= 1
            target_height = int(target_width * aspect_ratio) - 1
        return QSize(target_width, target_height)

    def _resize_pixmap_to_fit(self):
        if not self._original_pixmap:
            return
        available_size = self._calculate_available_space()
        scaled_size = self._calculate_scaled_pixmap_size(
            available_size.width(), available_size.height()
        )
        scaled_pixmap = self._original_pixmap.scaled(
            scaled_size.width(),
            scaled_size.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setFixedSize(available_size)
        self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event: QMouseEvent):
        """Delegate selection logic to `BrowseTabSelectionManager`."""
        if self.thumbnail_box.in_sequence_viewer:
            return
        self.thumbnail_box.browse_tab.selection_handler.on_thumbnail_clicked(self)

    def enterEvent(self, event):
        """Highlight border on hover."""
        self._border_color = BLUE
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Remove border highlight when leaving hover."""
        self._border_color = GOLD if self.selected else None
        self.update()
        super().leaveEvent(event)

    def set_selected(self, selected: bool):
        """Set selection border color."""
        self._border_color = GOLD if selected else None
        self.selected = selected
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.thumbnail_box.in_sequence_viewer:
            if self._original_pixmap:
                painter = QPainter(self)
                pen = QPen(QColor(GOLD))
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

    def resizeEvent(self, event):
        """Clear cached size on resize so it recalculates next time."""
        self._cached_available_size = None  # Invalidate cache
        self.border_width = self.width() // 100
        super().resizeEvent(event)



