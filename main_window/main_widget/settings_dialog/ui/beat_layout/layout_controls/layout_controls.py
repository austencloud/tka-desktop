from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

from ..length_selector.length_selector import LengthSelector
from .layout_selector.layout_selector import LayoutSelector
from .update_default_layout_button import UpdateDefaultLayoutButton
from .default_layout_label import DefaultLayoutLabel

if TYPE_CHECKING:
    from ..beat_layout_tab import BeatLayoutTab


class LayoutControls(QWidget):
    layout_selected = pyqtSignal(str)
    sequence_length_changed = pyqtSignal(int)
    update_default_layout = pyqtSignal()

    def __init__(self, layout_tab: "BeatLayoutTab"):
        super().__init__(layout_tab)
        self.layout_tab = layout_tab
        self.beat_frame = layout_tab.beat_frame
        self.layout_settings = layout_tab.layout_settings

        # Widgets
        self.layout_selector = LayoutSelector(self)
        self.length_selector = LengthSelector(self)
        self.default_layout_label = DefaultLayoutLabel(self)
        self.update_layout_button = UpdateDefaultLayoutButton(self)

        self._setup_layout()
        self._connect_signals()

    def _connect_signals(self):
        self.length_selector.value_changed.connect(self.sequence_length_changed.emit)
        self.layout_selector.layout_selected.connect(self.layout_selected.emit)
        self.update_layout_button.clicked.connect(self._save_layout_settings)

    def _save_layout_settings(self):
        layout_text = self.layout_selector.current_layout()
        self.layout_settings.set_layout_setting(
            str(self.layout_tab.num_beats), list(map(int, layout_text.split(" x ")))
        )
        self.default_layout_label.update_text(layout_text)

    def _setup_layout(self):
        layout = QHBoxLayout(self)

        # Length controls group
        length_group = QGroupBox("Sequence Length")
        length_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        length_layout = QVBoxLayout()
        length_layout.addWidget(self.length_selector.sequence_length_label)
        length_layout.addWidget(self.length_selector)
        length_layout.addWidget(self.default_layout_label)
        length_group.setLayout(length_layout)

        # Layout controls group
        layout_group = QGroupBox("Grid Configuration")
        layout_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_config = QVBoxLayout()
        layout_config.addWidget(self.layout_selector)
        layout_config.addWidget(self.update_layout_button)
        layout_group.setLayout(layout_config)

        layout.addWidget(length_group, 2)
        layout.addWidget(layout_group, 3)
