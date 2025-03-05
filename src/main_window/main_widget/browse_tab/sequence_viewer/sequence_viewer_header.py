from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from typing import TYPE_CHECKING


from settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer import (
        SequenceViewer,
    )


class SequenceViewerHeader(QWidget):
    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__(sequence_viewer)
        self.sv = sequence_viewer
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(60)
        self.settings_manager = AppContext.settings_manager()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        layout.addWidget(
            self.sv.difficulty_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        layout.addStretch(1)
        layout.addWidget(self.sv.word_label)
        layout.addStretch(1)
        layout.addWidget(
            self.sv.favorite_button, alignment=Qt.AlignmentFlag.AlignRight
        )

        self.setLayout(layout)

    def resizeEvent(self, event: QEvent) -> None:
        self.sv.difficulty_label.setFixedSize(
            self.sv.favorite_button.size()
        )
        super().resizeEvent(event)
