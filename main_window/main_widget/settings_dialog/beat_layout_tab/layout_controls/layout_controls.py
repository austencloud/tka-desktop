from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

from main_window.main_widget.settings_dialog.beat_layout_tab.layout_controls.layout_selector.layout_selector import (
    LayoutSelector,
)
from main_window.main_widget.settings_dialog.beat_layout_tab.length_selector.length_selector import (
    LengthSelector,
)
from main_window.main_widget.settings_dialog.beat_layout_tab.layout_controls.update_layout_button import (
    UpdateLayoutButton,
)
from .default_layout_label import DefaultLayoutLabel

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.beat_layout_tab.beat_layout_tab import (
        BeatLayoutTab,
    )


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
        self.update_layout_button = UpdateLayoutButton(self)

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
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.length_selector)
        layout.addWidget(self.default_layout_label)
        layout.addWidget(self.layout_selector)
        layout.addWidget(self.update_layout_button)
