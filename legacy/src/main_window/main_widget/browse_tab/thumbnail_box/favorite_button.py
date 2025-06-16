from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING, Literal
import os

from src.settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class FavoriteButton(QPushButton):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box
        if self.thumbnail_box.in_sequence_viewer:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)

        icons_path = get_image_path("icons")
        self.star_icon_filled = QIcon(os.path.join(icons_path, "star_filled.png"))
        self.star_icon_empty_path = self.get_star_outline_icon()
        self.star_icon_empty = QIcon(
            os.path.join(icons_path, self.star_icon_empty_path)
        )

        self.clicked.connect(self.toggle_favorite_status)
        self.update_favorite_icon(self.thumbnail_box.favorites_manager.is_favorite())

    def toggle_favorite_status(self):
        sequence_viewer = self.thumbnail_box.browse_tab.sequence_viewer
        self.thumbnail_box.favorites_manager.toggle_favorite_status()
        is_favorite = self.thumbnail_box.favorites_manager.is_favorite()
        self.update_favorite_icon(is_favorite)

        if self.thumbnail_box.in_sequence_viewer:
            matching_box = sequence_viewer.state.matching_thumbnail_box
            matching_box.favorites_manager.toggle_favorite_status()
            favorite_button = matching_box.header.favorite_button
            favorite_button.update_favorite_icon(is_favorite)
        else:
            sequence_viewer_word = sequence_viewer.thumbnail_box.word
            thumbnail_box_word = self.thumbnail_box.word
            if sequence_viewer_word != thumbnail_box_word:
                return
            sequence_viewer_box = sequence_viewer.thumbnail_box
            sequence_viewer_box.favorites_manager.toggle_favorite_status()
            favorite_button = sequence_viewer_box.header.favorite_button
            favorite_button.update_favorite_icon(is_favorite)

    def update_favorite_icon(self, is_favorite: bool):
        self.setIcon(self.star_icon_filled if is_favorite else self.star_icon_empty)

    def reload_favorite_icon(self):
        self.star_icon_empty_path = self.get_star_outline_icon()
        self.star_icon_empty = QIcon(
            os.path.join(get_image_path("icons"), self.star_icon_empty_path)
        )
        self.update_favorite_icon(self.thumbnail_box.favorites_manager.is_favorite())

    def get_star_outline_icon(
        self,
    ) -> None | Literal["black_star_outline.png"] | Literal["white_star_outline.png"]:
        settings_manager = AppContext.settings_manager()
        color = settings_manager.global_settings.get_current_font_color()
        return f"{color}_star_outline.png" if color in ["black", "white"] else None

    def resizeEvent(self, event):
        self.resize_favorite_icon()
        super().resizeEvent(event)

    def resize_favorite_icon(self):
        # FAVORITES BUTTON SIZING FIX: Use intended final layout dimensions
        # instead of current thumbnail box width to ensure consistent sizing
        intended_width = self._get_intended_thumbnail_width()
        font_size = intended_width // 18
        icon_size = QSize(font_size + 10, font_size + 10)
        self.setIconSize(icon_size)
        self.setFixedSize(icon_size.width(), icon_size.height())

    def _get_intended_thumbnail_width(self):
        """Calculate the intended final width for thumbnail boxes in the 3-column grid."""
        try:
            if self.thumbnail_box.in_sequence_viewer:
                # For sequence viewer, use the current calculation
                return self.thumbnail_box.width()

            # For browse tab, calculate the intended width based on final layout
            scroll_widget = self.thumbnail_box.sequence_picker.scroll_widget
            scroll_widget_width = scroll_widget.width()

            # Use the same calculation as thumbnail_box.resize_thumbnail_box()
            scrollbar_width = scroll_widget.calculate_scrollbar_width()

            # Account for ALL horizontal spacing elements (same as thumbnail_box)
            total_margins = (
                3 * self.thumbnail_box.margin * 2
            ) + 10  # 3 boxes * 20px margins + 10px buffer

            # Calculate usable width for thumbnails
            usable_width = scroll_widget_width - scrollbar_width - total_margins

            # Divide by 3 for 3 columns, ensuring minimum width
            intended_width = max(150, int(usable_width // 3))

            return intended_width

        except (AttributeError, TypeError, ZeroDivisionError):
            # Fallback to current width if calculation fails
            return max(150, self.thumbnail_box.width())

    def showEvent(self, event):
        self.reload_favorite_icon()
        self.resize_favorite_icon()
        super().showEvent(event)
