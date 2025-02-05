from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QSizePolicy


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench_button_panel import (
        SequenceWorkbenchButtonPanel,
    )


class ButtonPanelPlaceholder(QFrame):
    def __init__(self, button_panel: "SequenceWorkbenchButtonPanel"):
        super().__init__(button_panel)
        self.button_panel = button_panel
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(0)  # Start with a height of 0
