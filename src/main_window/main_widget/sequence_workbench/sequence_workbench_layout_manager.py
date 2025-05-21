from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

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

        self.main_layout = QVBoxLayout(self.sw)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        word_layout = QHBoxLayout()
        word_layout.setContentsMargins(0, 0, 0, 0)
        word_layout.setSpacing(10)

        self.dummy_widget = QWidget(self.sw)
        self.dummy_widget.setFixedSize(self.sw.difficulty_label.size())

        word_layout.addStretch(2)
        word_layout.addWidget(self.sw.circular_indicator)
        word_layout.addWidget(self.sw.difficulty_label)
        word_layout.addStretch(1)
        word_layout.addWidget(self.sw.current_word_label)
        word_layout.addStretch(1)
        word_layout.addWidget(self.dummy_widget)
        word_layout.addStretch(2)

        self.sw.scroll_area.setWidget(self.sw.beat_frame)

        self.main_layout.addStretch(2)
        self.main_layout.addLayout(word_layout, 4)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.sw.beat_frame_layout, 20)
        self.main_layout.addWidget(self.sw.indicator_label, 4)
        self.main_layout.addWidget(self.sw.graph_editor.placeholder)

        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

    def update_dummy_size(self):
        self.dummy_widget.setFixedSize(self.sw.difficulty_label.size())
