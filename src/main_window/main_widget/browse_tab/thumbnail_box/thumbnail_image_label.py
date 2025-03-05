from PyQt6.QtCore import Qt, QEvent, QRect, QSize
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent, QPainter, QColor, QPen
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING

from data.constants import BLUE
from main_window.main_widget.metadata_extractor import MetaDataExtractor

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class ThumbnailImageLabel(QLabel):
    target_width = 0
    is_selected = False
    index = None
    pixmap: QPixmap = None
    current_path = None
    border_width = 4

    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box
        self.metadata_extractor = MetaDataExtractor()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self._border_color = None

    def update_thumbnail(self, index):
        if not self.thumbnail_box.state.thumbnails or not (
            0 <= index < len(self.thumbnail_box.state.thumbnails)
        ):
            return
        if not self.thumbnail_box.initialized:
            self.thumbnail_box.initialized = True
        path = self.thumbnail_box.state.thumbnails[index]
        if not self.pixmap or not self.current_path or self.current_path != path:
            self.current_path = path
            self.pixmap = QPixmap(path)
        size = self._calculate_expected_size()
        if not self.pixmap.isNull():
            self._set_pixmap_to_fit(self.pixmap, size)
            self.setPixmap(self.pixmap)
            self.update()

    def _calculate_expected_size(self):
        nav_bar = self.thumbnail_box.sequence_picker.nav_sidebar
        if nav_bar.width() < 20:
            nav_bar.resize_sidebar()
        scrollbar_width = (
            self.thumbnail_box.sequence_picker.scroll_widget.calculate_scrollbar_width()
        )
        scroll_widget_width = (
            self.thumbnail_box.main_widget.width() * 2 / 3
            - scrollbar_width
            - nav_bar.width()
        )
        max_width = int(scroll_widget_width // 3 - (self.thumbnail_box.margin * 2))
        seq_len = self.metadata_extractor.get_length(
            self.thumbnail_box.state.thumbnails[self.thumbnail_box.state.current_index]
        )
        if seq_len == 1:
            max_width = int(max_width * 0.6)
        ar = self.pixmap.width() / self.pixmap.height() if self.pixmap else 1
        return QSize(max_width, int(max_width / ar))

    def _set_pixmap_to_fit(self, pixmap: QPixmap, expected_size: QSize):
        expected_width, expected_height = expected_size.width(), expected_size.height()
        width, height = self.pixmap.width(), self.pixmap.height()
        if (expected_width > width and expected_height > height) and self.current_path:
            fresh = QPixmap(self.current_path)
            if not fresh.isNull():
                self.pixmap = fresh
                width, height = self.pixmap.width(), self.pixmap.height()
        if width != expected_width or height != expected_height:
            self.pixmap = self.pixmap.scaled(
                expected_width,
                expected_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

    # def _set_pixmap_to_fit(self, pixmap: QPixmap, expected_size: QSize):
    #     """Set the pixmap only if resizing is needed."""
    #     expected_width, expected_height = expected_size.width(), expected_size.height()

    #     # Skip scaling if the new pixmap already matches the expected size
    #     if pixmap.width() == expected_width or pixmap.height() == expected_height:
    #         self.pixmap = pixmap
    #     else:
    #         self.pixmap = pixmap.scaled(
    #             expected_width,
    #             expected_height,
    #             Qt.AspectRatioMode.KeepAspectRatio,
    #             Qt.TransformationMode.SmoothTransformation,
    #         )

    def mousePressEvent(self, event: "QMouseEvent"):
        if not self.thumbnail_box.state.thumbnails:
            raise ValueError(f"No thumbnails for {self.thumbnail_box.word}")
        metadata = self.metadata_extractor.extract_metadata_from_file(
            self.thumbnail_box.state.thumbnails[0]
        )
        self.thumbnail_box.browse_tab.selection_handler.on_thumbnail_clicked(
            self, metadata
        )

    def enterEvent(self, event: QEvent):
        self._border_color = "gold"
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent):
        self._border_color = BLUE if self.is_selected else None
        self.update()
        super().leaveEvent(event)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self._border_color = BLUE if selected else None
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._border_color and self.pixmap:
            painter = QPainter(self)
            pen = QPen(QColor(self._border_color))
            pen.setWidth(self.border_width)
            pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
            painter.setPen(pen)
            x = (self.width() - self.pixmap.width()) // 2
            y = 0
            rect = QRect(x, y, self.pixmap.width(), self.pixmap.height())
            painter.drawRect(
                rect.adjusted(
                    self.border_width // 2,
                    self.border_width // 2,
                    -self.border_width // 2,
                    -self.border_width // 2,
                )
            )
