from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box import (
        ThumbnailBox,
    )
    from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer import (
        SequenceViewer,
    )


class VariationNumberLabel(QLabel):
    def __init__(self, parent: Union["ThumbnailBox", "SequenceViewer"]):
        super().__init__(parent)
        if len(parent.thumbnails) > 1:
            self.setText(f"{parent.current_index + 1}/{len(parent.thumbnails)}")
        else:
            self.hide()
        self.parent: Union["ThumbnailBox", "SequenceViewer"] = parent
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_index(self, index: int):
        if len(self.parent.thumbnails) > 1:
            self.setText(f"{index + 1}/{len(self.parent.thumbnails)}")
        else:
            self.hide()

    def clear(self) -> None:
        self.setText("")

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.parent.browse_tab.main_widget.width() // 100)
        font.setBold(True)
        self.setFont(font)
        color = (
            self.parent.main_widget.main_window.settings_manager.global_settings.get_current_font_color()
        )
        self.setStyleSheet(f"color: {color};")

        super().resizeEvent(event)
