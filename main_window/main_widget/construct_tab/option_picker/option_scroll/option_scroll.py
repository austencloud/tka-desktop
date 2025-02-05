from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from .section_widget.option_picker_section_widget import OptionPickerSectionWidget

from .option_scroll_layout_manager import OptionScrollLayoutManager
from Enums.Enums import LetterType

if TYPE_CHECKING:
    from ..option_picker import OptionPicker


class OptionScroll(QScrollArea):
    spacing = 3
    layout: QVBoxLayout
    container: QWidget
    sections: dict["LetterType", "OptionPickerSectionWidget"] = {}

    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.main_widget = option_picker.main_widget
        self.construct_tab = option_picker.construct_tab
        self.layout_manager = OptionScrollLayoutManager(self)
