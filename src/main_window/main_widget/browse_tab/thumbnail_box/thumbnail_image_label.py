from PyQt6.QtCore import Qt, QEvent, QRect
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
    border_width = 4  # Define border width

    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box
        self.metadata_extractor = MetaDataExtractor()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self._border_color = None  # Initialize border color

    def update_thumbnail(self, index):
        if self.thumbnail_box.state.thumbnails and 0 <= index < len(
            self.thumbnail_box.state.thumbnails
        ):
            pixmap = QPixmap(self.thumbnail_box.state.thumbnails[index])
            self._set_pixmap_to_fit(pixmap)

    def _set_pixmap_to_fit(self, pixmap: QPixmap):
        nav_bar = self.thumbnail_box.sequence_picker.nav_sidebar
        if nav_bar.width() < 20:
            nav_bar.resize_sidebar()
        aspect_ratio = pixmap.width() / pixmap.height()
        scrollbar_width = (
            self.thumbnail_box.sequence_picker.scroll_widget.calculate_scrollbar_width()
        )
        scroll_widget_width = (
            self.thumbnail_box.main_widget.width() * 2 / 3
            - scrollbar_width
            - self.thumbnail_box.sequence_picker.nav_sidebar.width()
        )
        width = scroll_widget_width // 3
        max_width = int(width - (self.thumbnail_box.margin * 2))
        max_height = int(max_width / aspect_ratio)

        seq_len = self.metadata_extractor.get_length(
            self.thumbnail_box.state.thumbnails[self.thumbnail_box.state.current_index]
        )
        if seq_len == 1:
            max_width = int(max_width * 0.6)

        scaled_pm = pixmap.scaled(
            max_width,
            max_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.pixmap = scaled_pm  # Store scaled pixmap
        self.setPixmap(scaled_pm)

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
        if self.thumbnail_box.state.thumbnails:
            metadata = self.metadata_extractor.extract_metadata_from_file(
                self.thumbnail_box.state.thumbnails[0]
            )
            self.thumbnail_box.browse_tab.selection_handler.on_box_thumbnail_clicked(
                self, metadata
            )

        else:
            ValueError(f"No thumbnails for {self.thumbnail_box.word}")

    def enterEvent(self, event: QEvent):
        self._border_color = "gold"  # Set border color on hover
        self.update()  # Trigger repaint
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent):
        if self.is_selected:
            self._border_color = BLUE  # Set border color if selected
        else:
            self._border_color = None  # Remove border
        self.update()  # Trigger repaint
        super().leaveEvent(event)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        if selected:
            self._border_color = BLUE  # Set border color if selected
        else:
            self._border_color = None  # Remove border
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        super().paintEvent(event)  # Draw the base QLabel content (pixmap)

        if self._border_color and self.pixmap:
            painter = QPainter(self)
            pen = QPen(QColor(self._border_color))
            pen.setWidth(self.border_width)  # Set pen width
            pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)  # Set hard edges
            painter.setPen(pen)  # Use color name to get QColor

            # Calculate the top-center position for the pixmap
            x = (self.width() - self.pixmap.width()) // 2
            y = 0  # Align to the top

            rect = QRect(x, y, self.pixmap.width(), self.pixmap.height())
            painter.drawRect(
                rect.adjusted(
                    self.border_width // 2,
                    self.border_width // 2,
                    -self.border_width // 2,
                    -self.border_width // 2,
                )
            )
