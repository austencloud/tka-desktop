from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class SequenceWorkbenchLayoutManager:
    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sw = sequence_workbench
        self.setup_layout()

    def setup_layout(self):
        self.setup_beat_frame_layout()
        self.setup_indicator_label_layout()
        self.main_layout: QVBoxLayout = QVBoxLayout(self.sw)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        current_word_layout = QVBoxLayout()
        current_word_layout.addWidget(self.sw.current_word_label)
        current_word_layout.addWidget(self.sw.difficulty_label)

        self.main_layout.addStretch(1)
        self.main_layout.addLayout(current_word_layout, 1)
        self.main_layout.addLayout(self.sw.beat_frame_layout, 12)
        self.main_layout.addWidget(self.sw.indicator_label, 1)
        self.main_layout.addWidget(self.sw.graph_editor.placeholder)

        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.sw.graph_editor.state.update_graph_editorvisibility()
        self.sw.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.sw.scroll_area.setWidget(self.sw.beat_frame)

        self.sw.setLayout(self.main_layout)

    def setup_beat_frame_layout(self):
        self.sw.beat_frame_layout = QHBoxLayout()
        self.sw.beat_frame_layout.addWidget(self.sw.scroll_area, 10)
        self.sw.beat_frame_layout.addWidget(self.sw.button_panel, 1)
        self.sw.beat_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.sw.beat_frame_layout.setSpacing(0)

    def setup_indicator_label_layout(self):
        self.sw.indicator_label_layout = QHBoxLayout()
        self.sw.indicator_label_layout.addStretch(1)
        self.sw.indicator_label_layout.addWidget(self.sw.indicator_label)
        self.sw.indicator_label_layout.addStretch(1)

    def apply_layout_options(self, cols, rows, num_beats):
        self.sw.beat_frame.layout_manager.rearrange_beats(num_beats, cols, rows)
        self.sw.current_word_label.update_current_word_label_from_beats()
