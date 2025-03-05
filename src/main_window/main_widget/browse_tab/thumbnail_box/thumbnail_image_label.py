from PyQt6.QtCore import Qt, QEvent, QRect
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent, QPainter, QColor, QPen
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING

from data.constants import BLUE
from main_window.main_widget.metadata_extractor import MetaDataExtractor

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox
from PyQt6.QtCore import QSize


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
        """Update the thumbnail only if resizing is necessary."""
        if not self.thumbnail_box.state.thumbnails or not (
            0 <= index < len(self.thumbnail_box.state.thumbnails)
        ):
            return  # Invalid index or no thumbnails

        # Calculate expected size before creating a new QPixmap
        expected_size = self._calculate_expected_size()
        if self.pixmap and self.pixmap.size() == expected_size:
            return  # Skip redundant updates if the size is correct
        if self.thumbnail_box.initialized == False:
            self.thumbnail_box.initialized = True
        # Create and scale only if necessary
        new_pixmap = QPixmap(self.thumbnail_box.state.thumbnails[index])
        if not new_pixmap.isNull():
            self._set_pixmap_to_fit(new_pixmap, expected_size)
        else:
            print(
                f"Failed to load thumbnail: {self.thumbnail_box.state.thumbnails[index]}"
            )

    def _calculate_expected_size(self):
        """Calculate the expected thumbnail size based on layout constraints."""
        nav_bar = self.thumbnail_box.sequence_picker.nav_sidebar
        if nav_bar.width() < 20:
            nav_bar.resize_sidebar()

        # Calculate available space
        scrollbar_width = (
            self.thumbnail_box.sequence_picker.scroll_widget.calculate_scrollbar_width()
        )
        scroll_widget_width = (
            self.thumbnail_box.main_widget.width() * 2 / 3
            - scrollbar_width
            - self.thumbnail_box.sequence_picker.nav_sidebar.width()
        )
        max_width = int(scroll_widget_width // 3 - (self.thumbnail_box.margin * 2))

        # Adjust width for single-length sequences
        seq_len = self.metadata_extractor.get_length(
            self.thumbnail_box.state.thumbnails[self.thumbnail_box.state.current_index]
        )
        if seq_len == 1:
            max_width = int(max_width * 0.6)

        # Maintain aspect ratio
        if self.pixmap:
            aspect_ratio = self.pixmap.width() / self.pixmap.height()
        else:
            aspect_ratio = 1  # Default to square if no pixmap available

        max_height = int(max_width / aspect_ratio)
        return QSize(max_width, max_height)  # Convert to QSize. Finally!

    def _set_pixmap_to_fit(self, pixmap: QPixmap, expected_size: QSize):
        """Set the pixmap only if resizing is needed."""
        max_width, max_height = expected_size.width(), expected_size.height()

        # Skip scaling if the new pixmap already matches the expected size
        if pixmap.width() == max_width and pixmap.height() == max_height:
            self.pixmap = pixmap
        else:
            self.pixmap = pixmap.scaled(
                max_width,
                max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        self.setPixmap(self.pixmap)
        self.update()

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
        self._border_color = "gold"  # Set border color on hover
        self.update()  # Trigger repaint
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent):
        self._border_color = (
            BLUE if self.is_selected else None
        )  # Set border color if selected
        self.update()  # Trigger repaint
        super().leaveEvent(event)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self._border_color = BLUE if selected else None  # Update border color
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        super().paintEvent(event)  # Draw the base QLabel content (pixmap)

        if self._border_color and self.pixmap:
            painter = QPainter(self)
            pen = QPen(QColor(self._border_color))
            pen.setWidth(self.border_width)  # Set pen width
            pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)  # Set hard edges
            painter.setPen(pen)

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
