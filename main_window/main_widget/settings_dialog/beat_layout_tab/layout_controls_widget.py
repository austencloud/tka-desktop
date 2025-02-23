from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from .layout_selector import LayoutSelector
from .length_selector import LengthSelector
from .default_layout_label import DefaultLayoutLabel
from .update_layout_button import UpdateLayoutButton

if TYPE_CHECKING:
    from .beat_layout_tab import BeatLayoutTab


class LayoutControlsWidget(QWidget):
    layout_selected = pyqtSignal(str)
    update_default_layout = pyqtSignal()

    def __init__(self, layout_tab: "BeatLayoutTab"):
        super().__init__(layout_tab)
        self.layout_tab = layout_tab
        self.beat_frame = layout_tab.beat_frame
        self.layout_settings = layout_tab.layout_settings

        # Widgets
        self.length_selector = LengthSelector(self)
        self.default_layout_label = DefaultLayoutLabel(self)
        self.layout_selector = LayoutSelector(self)
        self.update_layout_button = UpdateLayoutButton(self)

        self._setup_layout()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(self.layout_tab.width() // 50)
        layout.addWidget(self.length_selector)
        layout.addWidget(self.default_layout_label)
        layout.addWidget(self.layout_selector)
        layout.addWidget(self.update_layout_button)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font_size = max(12, self.width() // 50)
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)
