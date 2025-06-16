from typing import Callable
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QSize
from interfaces.settings_manager_interface import ISettingsManager
from .reversal_combobox import ReversalCombobox


class OptionPickerReversalFilter(QWidget):
    def __init__(
        self,
        mw_size_provider: Callable[[], QSize],
        update_options_callback: Callable,
        settings_manager: ISettingsManager,
    ) -> None:
        super().__init__()
        self.settings = settings_manager.get_construct_tab_settings()
        self.size_provider = mw_size_provider
        self.update_options_callback = update_options_callback
        self.reversal_combobox = ReversalCombobox(self, mw_size_provider)
        self.combo_box_label = QLabel("Show:")
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.combo_box_label)
        layout.addWidget(self.reversal_combobox)
        self.setLayout(layout)
        self._load_filter()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.size_provider().width()
        font = self.font()
        font.setPointSize(int(w // 130))
        font.setFamily("Georgia")
        self.setFont(font)
        self.combo_box_label.setFont(font)

    def on_filter_changed(self):
        self.save_filter()
        self.update_options_callback()

    def save_filter(self):
        selected = self.reversal_combobox.currentData()
        self.settings.set_filters(selected)

    def _load_filter(self):
        selected = self.settings.get_filters()
        index = self.reversal_combobox.findData(selected)
        self.reversal_combobox.setCurrentIndex(index if index != -1 else 0)
