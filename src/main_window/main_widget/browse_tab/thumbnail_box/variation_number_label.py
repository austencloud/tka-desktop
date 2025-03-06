from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from typing import TYPE_CHECKING, Union

from settings_manager.global_settings.app_context import AppContext


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
        if len(parent.state.thumbnails) > 1:
            self.setText(
                f"{parent.state.current_index + 1}/{len(parent.state.thumbnails)}"
            )
        else:
            self.hide()
        self.parent: Union["ThumbnailBox", "SequenceViewer"] = parent
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_index(self, index: int):
        if len(self.parent.state.thumbnails) > 1:
            self.setText(f"{index + 1}/{len(self.parent.state.thumbnails)}")
            self.show()
        else:
            self.hide()

    def clear(self) -> None:
        self.setText("")

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.parent.browse_tab.main_widget.width() // 100)
        font.setBold(True)
        self.setFont(font)
        color = AppContext.settings_manager().global_settings.get_current_font_color()
        self.setStyleSheet(f"color: {color};")

        super().resizeEvent(event)
