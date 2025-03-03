from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.widgets.option_picker_widget import (
        OptionPickerWidget,
    )


class OptionPickerLayoutManager:
    def __init__(self, op: "OptionPickerWidget"):
        self.op = op
        self.setup_layout()

    def setup_layout(self) -> None:
        layout = QVBoxLayout(self.op)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.op.choose_next_label)
        header_layout.addLayout(hlayout)
        layout.addLayout(header_layout)
        layout.addWidget(self.op.reversal_filter)
        layout.addWidget(self.op.option_scroll, 14)
        self.op.setLayout(layout)
