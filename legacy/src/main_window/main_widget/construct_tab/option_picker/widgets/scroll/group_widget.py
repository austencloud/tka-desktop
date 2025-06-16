from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt


from main_window.main_widget.construct_tab.option_picker.widgets.scroll.section_widget import OptionPickerSectionWidget

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.widgets.scroll.option_scroll import OptionScroll



class OptionPickerSectionGroupWidget(QWidget):
    def __init__(self, scroll_area: "OptionScroll") -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setLayout(self.layout)

    def add_section_widget(self, section: "OptionPickerSectionWidget") -> None:
        """Add a section widget to the group with minimal size policy."""
        section.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        section.setMinimumWidth(section.sizeHint().width())
        section.setMaximumWidth(section.sizeHint().width())

        self.layout.addWidget(section, alignment=Qt.AlignmentFlag.AlignCenter)
