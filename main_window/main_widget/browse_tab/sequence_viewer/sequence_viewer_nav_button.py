from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer_nav_buttons_widget import (
        SequenceViewerNavButtonsWidget,
    )


class SequenceViewerNavButton(QPushButton):
    def __init__(self, text: str, parent: "SequenceViewerNavButtonsWidget"):
        super().__init__(text, parent)
        self.clicked.connect(parent.handle_button_click)
        self.setStyleSheet("background-color: white;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
