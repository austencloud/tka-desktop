# main_window/main_widget/construct_tab/option_picker/choose_your_next_pictograph_label.py
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QSize
from typing import Callable
from main_window.main_widget.construct_tab.option_picker.resizable_mixin import ResizableMixin

class ChooseYourNextPictographLabel(ResizableMixin, QLabel):
    def __init__(self, size_provider: Callable[[], QSize], parent=None):
        # Note: The mixin is first, so its __init__ will get called with the size_provider.
        super().__init__(size_provider, parent)
        self.setText("Choose your next pictograph:")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        h = self.update_size_and_style()  # Use the mixin’s logic
        self.setStyleSheet(
            f"background-color: rgba(255,255,255,200); border-radius: {h//2}px;"
        )
