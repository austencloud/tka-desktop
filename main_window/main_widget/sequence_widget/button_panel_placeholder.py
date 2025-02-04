from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QSizePolicy, QApplication


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget_button_panel import (
        SequenceWorkbenchButtonPanel,
    )


class ButtonPanelPlaceholder(QFrame):
    def __init__(self, button_panel: "SequenceWorkbenchButtonPanel"):
        super().__init__(button_panel)
        self.button_panel = button_panel
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(0)  # Start with a height of 0

    def set_height(self, new_height):
        """Dynamically sets the height of the button panel placeholder."""
        self.setFixedHeight(new_height)
        self.button_panel.updateGeometry()
        QApplication.processEvents()  # Update layout immediately
