from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from .reversal_combobox import ReversalCombobox

if TYPE_CHECKING:
    from ..option_picker import OptionPicker


class OptionPickerReversalFilter(QWidget):
    def __init__(self, option_picker: "OptionPicker"):
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.settings = self.option_picker.construct_tab.settings
        self.reversal_combobox = ReversalCombobox(self)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.combo_box_label: QLabel = QLabel("Show:")
        self.layout.addWidget(self.combo_box_label)
        self.layout.addWidget(self.reversal_combobox)
        self._load_filter()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font = self.font()
        font_size = int(self.option_picker.construct_tab.main_widget.width() // 130)
        font.setPointSize(font_size)
        font.setFamily("Georgia")
        self.setFont(font)
        self.combo_box_label.setFont(font)

    def on_filter_changed(self):
        """Called when the filter combo box selection changes."""
        self.save_filter()
        self.option_picker.updater.refresh_options()

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
