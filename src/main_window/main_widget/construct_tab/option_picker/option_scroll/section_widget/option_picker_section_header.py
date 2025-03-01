from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from main_window.main_widget.construct_tab.option_picker.option_scroll.section_widget.option_picker_section_type_label import OptionPickerSectionTypeButton

if TYPE_CHECKING:
    from .option_picker_section_widget import OptionPickerSectionWidget


class OptionPickerSectionHeader(QWidget):
    def __init__(self, section: "OptionPickerSectionWidget") -> None:
        super().__init__()
        self.section = section
        self.type_button = OptionPickerSectionTypeButton(section)
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.type_button)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
