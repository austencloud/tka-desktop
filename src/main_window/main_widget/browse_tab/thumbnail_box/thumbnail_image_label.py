from PyQt6.QtCore import Qt, QRect, QSize, pyqtProperty
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent, QPainter, QColor, QPen
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING, Optional, Final

from data.constants import GOLD, BLUE
from main_window.main_widget.metadata_extractor import MetaDataExtractor

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class ThumbnailImageLabel(QLabel):
    BORDER_WIDTH_RATIO: Final = 0.01  # Border width as percentage of width
    SEQUENCE_VIEWER_BORDER_SCALE: Final = 0.8

    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        # Instance attributes
        self.thumbnail_box = thumbnail_box
        self.metadata_extractor = MetaDataExtractor()
        self.selected = False
        self.current_path: Optional[str] = None

        # Private attributes
        self._border_width = 4
        self._border_color: Optional[str] = None
        self._original_pixmap: Optional[QPixmap] = None
        self._cached_available_size: Optional[QSize] = None

        # Setup UI
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @property
    def border_width(self) -> int:
        return self._border_width

    @property
    def is_in_sequence_viewer(self) -> bool:
        return self.thumbnail_box.in_sequence_viewer

    @property
    def aspect_ratio(self) -> float:
        """Get aspect ratio of the original image"""
        return (
            self._original_pixmap.width() / self._original_pixmap.height()
            if self._original_pixmap and self._original_pixmap.height() > 0
            else 1
        )

    def update_thumbnail(self, index: int) -> None:
        """Update the displayed image based on the given index."""
        thumbnails = self.thumbnail_box.state.thumbnails
        if not thumbnails or not (0 <= index < len(thumbnails)):
            return

        path = thumbnails[index]
        if path != self.current_path:
            self.current_path = path
            self._original_pixmap = QPixmap(path)
            self._cached_available_size = None  # Reset cache when image changes

        self._resize_pixmap_to_fit()

    def _calculate_available_space(self) -> QSize:
        """Calculate available space for the image."""
        if self._cached_available_size:
            return self._cached_available_size

        if self.is_in_sequence_viewer:
            available_size = self._calculate_sequence_viewer_size()
        else:
            available_size = self._calculate_normal_view_size()

        self._cached_available_size = available_size
        return available_size

    def _calculate_sequence_viewer_size(self) -> QSize:
        """Calculate available space in sequence viewer mode."""
        sequence_viewer = self.thumbnail_box.browse_tab.sequence_viewer
        available_width = int(sequence_viewer.main_widget.width() * 1 / 3 * 0.95)
        available_height = int(sequence_viewer.main_widget.height() * 0.65)
        return QSize(available_width, available_height)

    def _calculate_normal_view_size(self) -> QSize:
        """Calculate available space in normal view mode."""
        nav_bar = self.thumbnail_box.sequence_picker.nav_sidebar
        if nav_bar.width() < 20:
            nav_bar.resize_sidebar()

        scroll_widget = self.thumbnail_box.sequence_picker.scroll_widget
        scrollbar_width = scroll_widget.calculate_scrollbar_width()
        main_widget_width = self.thumbnail_box.main_widget.width()

        scroll_widget_width = (
            (main_widget_width * 2 / 3) - scrollbar_width - nav_bar.width()
        )
        available_width = int(
            scroll_widget_width // 3 - (self.thumbnail_box.margin * 2)
        )
        available_height = int(available_width / self.aspect_ratio)

        return QSize(available_width, available_height)

    def _calculate_scaled_pixmap_size(self, available_size: QSize) -> QSize:
        """Calculate the optimal size for the pixmap while maintaining aspect ratio."""
        if not self._original_pixmap:
            return QSize(0, 0)

        aspect_ratio = self._original_pixmap.height() / self._original_pixmap.width()
        target_width = available_size.width()
        target_height = int(target_width * aspect_ratio)

        if target_height > available_size.height():
            target_height = available_size.height()
            target_width = int(target_height / aspect_ratio)

        return QSize(target_width, target_height)

    def _resize_pixmap_to_fit(self) -> None:
        """Resize the pixmap to fit the available space while maintaining aspect ratio."""
        if not self._original_pixmap:
            return

        available_size = self._calculate_available_space()
        scaled_size = self._calculate_scaled_pixmap_size(available_size)

        scaled_pixmap = self._original_pixmap.scaled(
            scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.setFixedSize(available_size)
        self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press events."""
        if not self.is_in_sequence_viewer:
            self.thumbnail_box.browse_tab.selection_handler.on_thumbnail_clicked(self)

    def enterEvent(self, event) -> None:
        """Highlight border on hover."""
        self._border_color = BLUE
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Remove border highlight when leaving hover."""
        self._border_color = GOLD if self.selected else None
        self.update()
        super().leaveEvent(event)

    def set_selected(self, selected: bool) -> None:
        """Set selection state."""
        self.selected = selected
        self._border_color = GOLD if selected else None
        self.update()

    def _draw_border(self, painter: QPainter) -> None:
        """Draw border around the thumbnail."""
        if not self._original_pixmap or not (
            self._border_color or self.is_in_sequence_viewer
        ):
            return

        # Setup pen
        color = QColor(GOLD if self.is_in_sequence_viewer else self._border_color)
        border_width = int(
            self.border_width
            * (self.SEQUENCE_VIEWER_BORDER_SCALE if self.is_in_sequence_viewer else 1)
        )

        pen = QPen(color)
        pen.setWidth(border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Calculate rectangle
        img_width, img_height = self.pixmap().width(), self.pixmap().height()
        x = (self.width() - img_width) // 2
        y = (self.height() - img_height) // 2
        rect = QRect(x, y, img_width, img_height)

        # Adjust rectangle for border width
        border_offset = border_width // 2
        adjusted_rect = rect.adjusted(
            border_offset, border_offset, -border_offset, -border_offset
        )

        painter.drawRect(adjusted_rect)

    def paintEvent(self, event) -> None:
        """Handle paint events."""
        super().paintEvent(event)

        if self.is_in_sequence_viewer or self._border_color:
            painter = QPainter(self)
            self._draw_border(painter)

    def resizeEvent(self, event) -> None:
        """Handle resize events."""
        self._cached_available_size = None  # Invalidate cache
        self._border_width = max(1, int(self.width() * self.BORDER_WIDTH_RATIO))
        super().resizeEvent(event)
