from typing import Callable, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QSize
from main_window.settings_manager.global_settings.app_context import AppContext
from .reversal_combobox import ReversalCombobox

if TYPE_CHECKING:
    from ..option_picker import OptionPicker


class OptionPickerReversalFilter(QWidget):
    def __init__(self, mw_size_provider: Callable[[], QSize], update_options_callback: Callable
    ) -> None:
        super().__init__()
        self.settings = AppContext.settings_manager().construct_tab_settings
        self.size_provider = mw_size_provider
        self.update_options_callback = update_options_callback
        self.reversal_combobox = ReversalCombobox(self, mw_size_provider)

        self.combo_box_label = QLabel("Show:")
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.combo_box_label)
        self.layout.addWidget(self.reversal_combobox)

        self._load_filter()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        main_size = self.size_provider()
        width = main_size.width()  # Extract width from QSize

        font = self.font()
        font_size = int(width // 130)
        font.setPointSize(font_size)
        font.setFamily("Georgia")

        self.setFont(font)
        self.combo_box_label.setFont(font)

    def on_filter_changed(self):
        self.save_filter()
        #  update the option picker
        self.update_options_callback()    
        
    def save_filter(self):
        selected_filter = self.reversal_combobox.currentData()
        self.settings.set_filters(selected_filter)

    def _load_filter(self):
        selected_filter = self.settings.get_filters()
        index = self.reversal_combobox.findData(selected_filter)
        if index != -1:
            self.reversal_combobox.setCurrentIndex(index)
        else:
            self.reversal_combobox.setCurrentIndex(0)
