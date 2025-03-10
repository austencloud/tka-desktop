from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING, Literal
import os

from settings_manager.global_settings.app_context import AppContext
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
        font_size = self.thumbnail_box.width() // 18
        icon_size = QSize(font_size + 10, font_size + 10)
        self.setIconSize(icon_size)
        self.setFixedSize(icon_size.width(), icon_size.height())

    def showEvent(self, event):
        self.reload_favorite_icon()
        self.resize_favorite_icon()
        super().showEvent(event)
