from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.scroll_area.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )
    from main_window.main_widget.construct_tab.option_picker.scroll_area.section_manager.option_picker_section_widget import (
        OptionPickerSectionWidget,
    )


class OptionPickerSectionGroupWidget(QWidget):
    def __init__(self, scroll_area: "OptionPickerScrollArea") -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area

        # Create a horizontal layout with minimal spacing
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(5)  # Set very small spacing between sections
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the size policy to wrap tightly around its contents
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setLayout(self.layout)

    def add_section_widget(self, section: "OptionPickerSectionWidget") -> None:
        """Add a section widget to the group with minimal size policy."""
        # Enforce minimal size policy to keep the section tightly wrapped
        section.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        # Ensure the widget only takes up necessary space by limiting width
        section.setMinimumWidth(section.sizeHint().width())
        section.setMaximumWidth(section.sizeHint().width())

        self.layout.addWidget(section, alignment=Qt.AlignmentFlag.AlignCenter)
