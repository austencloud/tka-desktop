from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING, Literal
import os

from settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer import (
        SequenceViewer,
    )


class SequenceViewerFavoriteSequenceButton(QPushButton):
    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__()
        self.sequence_viewer = sequence_viewer
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)

        icons_path = get_image_path("icons")
        self.star_icon_filled = QIcon(os.path.join(icons_path, "star_filled.png"))
        self.star_icon_empty_path = self.get_star_outline_icon()
        self.star_icon_empty = QIcon(
            os.path.join(icons_path, self.star_icon_empty_path)
        )

        self.clicked.connect(self.toggle_favorite_status)
        self.update_favorite_icon(self.sequence_viewer.favorites_manager.is_favorite())

    def toggle_favorite_status(self):
        self.sequence_viewer.favorites_manager.toggle_favorite_status()
        self.update_favorite_icon(self.sequence_viewer.favorites_manager.is_favorite())

    def update_favorite_icon(self, is_favorite: bool):
        self.setIcon(self.star_icon_filled if is_favorite else self.star_icon_empty)

    def get_star_outline_icon(
        self,
    ) -> None | Literal["black_star_outline.png"] | Literal["white_star_outline.png"]:
        settings_manager = AppContext.settings_manager()
        color = settings_manager.global_settings.get_current_font_color()
        return f"{color}_star_outline.png" if color in ["black", "white"] else None

    def resizeEvent(self, event):
        font_size = self.sequence_viewer.width() // 18
        icon_size = QSize(font_size + 10, font_size + 10)
        self.setIconSize(icon_size)
        self.setFixedSize(icon_size.width(), icon_size.height())
        super().resizeEvent(event)
