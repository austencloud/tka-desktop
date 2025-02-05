from typing import TYPE_CHECKING

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class SequenceWorkbenchIndicatorLabel(BaseIndicatorLabel):
    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench)
        self.sequence_workbench = sequence_workbench

    def resizeEvent(self, event) -> None:
        self.setFixedHeight(self.sequence_workbench.height() // 20)
        font = self.font()
        font.setPointSize(self.sequence_workbench.width() // 75)
        self.setFont(font)
