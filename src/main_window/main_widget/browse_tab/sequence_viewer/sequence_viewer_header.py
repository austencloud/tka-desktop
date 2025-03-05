from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from typing import TYPE_CHECKING


from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer_favorite_sequence_button import (
    SequenceViewerFavoriteSequenceButton,
)
from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer_word_label import (
    SequenceViewerWordLabel,
)
from main_window.main_widget.browse_tab.thumbnail_box.favorite_sequence_button import (
    ThumbnailBoxFavoriteSequenceButton,
)
from settings_manager.global_settings.app_context import AppContext

from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer_difficulty_level import (
    SequenceViewerDifficultyLabel,
)

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_viewer.sequence_viewer import (
        SequenceViewer,
    )


class SequenceViewerHeader(QWidget):
    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__(sequence_viewer)
        self.sequence_viewer = sequence_viewer
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(60)
        self.settings_manager = AppContext.settings_manager()

        self.difficulty_label = SequenceViewerDifficultyLabel(sequence_viewer)
        self.word_label = SequenceViewerWordLabel(
            sequence_viewer.word, self, self.settings_manager
        )
        self.favorite_button = SequenceViewerFavoriteSequenceButton(sequence_viewer)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        layout.addWidget(self.difficulty_label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)
        layout.addWidget(self.word_label)
        layout.addStretch(1)
        layout.addWidget(self.favorite_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def resizeEvent(self, event: QEvent) -> None:
        self.difficulty_label.setFixedSize(self.favorite_button.size())
        super().resizeEvent(event)
