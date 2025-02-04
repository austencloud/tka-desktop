from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from main_window.main_widget.construct_tab.option_picker.scroll_area.section_type_label import (
    SectionTypeLabel,
)


if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.scroll_area.section_manager.option_picker_section_widget import (
        OptionPickerSectionWidget,
    )


class OptionPickerSectionHeader(QWidget):
    def __init__(self, section: "OptionPickerSectionWidget") -> None:
        super().__init__()
        self.section = section
        self.type_label = SectionTypeLabel(section)
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.type_label)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
