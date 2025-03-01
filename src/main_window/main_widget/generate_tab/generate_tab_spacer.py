from PyQt6.QtWidgets import QSizePolicy, QWidget
from PyQt6.QtCore import QSize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GenerateTabSpacer(QWidget):
    def __init__(self, tab: "GenerateTab"):
        super().__init__(tab)
        self.tab = tab
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.update_size()

    def update_size(self):
        """Update the spacer height based on the parent tab's size."""
        height = self.tab.main_widget.height() // 20
        self.setFixedSize(QSize(self.width(), height))

    def resizeEvent(self, event):
        """Resize the spacer whenever the parent is resized."""
        self.update_size()
        super().resizeEvent(event)
