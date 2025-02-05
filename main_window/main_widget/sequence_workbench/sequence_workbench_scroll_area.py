from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea

if TYPE_CHECKING:
    from .sequence_workbench import SequenceWorkbench


class SequenceWorkbenchScrollArea(QScrollArea):
    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea{background: transparent;}")
        self.setFrameShape(QScrollArea.Shape.NoFrame)
