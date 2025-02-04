from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import (
        SequenceWorkbench,
    )

from PyQt6.QtWidgets import QWidget, QSplitter
from PyQt6.QtCore import Qt


class SequenceTabContainer(QWidget):
    def __init__(
        self, sequence_widget: "SequenceWorkbench", stacked_widget: QStackedWidget
    ):
        super().__init__()
        self.sequence_widget = sequence_widget
        self.stacked_widget = stacked_widget

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.sequence_widget)
        self.splitter.addWidget(self.stacked_widget)
        self.splitter.setSizes([1, 1])  # Set initial sizes equally

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.splitter)
        self.layout.setContentsMargins(0, 0, 0, 0)
