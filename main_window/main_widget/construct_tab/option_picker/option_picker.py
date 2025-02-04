# option_picker.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from typing import TYPE_CHECKING

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.construct_tab.option_picker.option_picker_click_handler import (
    OptionPickerClickHandler,
)
from main_window.main_widget.construct_tab.option_picker.scroll_area.section_manager.option_picker_section_widget import (
    OptionPickerSectionWidget,
)
from .scroll_area.option_picker_scroll_area import OptionPickerScrollArea
from .option_view import OptionView
from .reversal_filter.option_picker_reversal_filter import OptionPickerReversalFilter
from .option_getter import OptionGetter
from .choose_your_next_pictograph_label import ChooseYourNextPictographLabel

if TYPE_CHECKING:
    from ..construct_tab import ConstructTab
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class OptionPicker(QWidget):
    """Contains the 'Choose Your Next Pictograph' label, filter combo box, and the OptionPickerScrollArea."""

    COLUMN_COUNT = 8
    MAX_PICTOGRAPHS = 36
    option_selected = pyqtSignal(str)

    def __init__(self, construct_tab: "ConstructTab"):
        super().__init__(construct_tab)
        self.construct_tab = construct_tab
        self.main_widget = construct_tab.main_widget
        self.json_manager = self.main_widget.json_manager
        self.fade_manager = self.main_widget.fade_manager
        self.disabled = False
        self.choose_your_next_pictograph_label = ChooseYourNextPictographLabel(self)
        self.option_getter = OptionGetter(self)
        self.scroll_area = OptionPickerScrollArea(self)
        self.reversal_filter = OptionPickerReversalFilter(self)
        self.click_handler = OptionPickerClickHandler(self)

        self.initialize_option_pool()
        self.setup_layout()

    def get_sections(self) -> list["OptionPickerSectionWidget"]:
        """Retrieve all OptionPickerSectionWidget instances."""
        return list(self.scroll_area.layout_manager.sections.values())

    def initialize_option_pool(self):
        self.option_pool: list[BasePictograph] = []
        for _ in range(self.MAX_PICTOGRAPHS):
            option = BasePictograph(self.main_widget)
            option.view = OptionView(self, option)
            self.option_pool.append(option)

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_your_next_pictograph_label.show()

        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_label_layout = QHBoxLayout()
        header_label_layout.addWidget(self.choose_your_next_pictograph_label)
        header_layout.addLayout(header_label_layout)

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.reversal_filter)
        self.layout.addWidget(self.scroll_area, 14)

    def update_option_picker(self, sequence=None):
        if self.disabled:
            return

        if sequence is None:
            sequence = self.json_manager.loader_saver.load_current_sequence_json()
        if len(sequence) > 1:

            views = [option.view for option in self.option_pool]
            self.fade_manager.widget_fader.fade_and_update(
                views, self._update_pictographs, 200
            )

    def _update_pictographs(self):
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        selected_filter = self.reversal_filter.reversal_combobox.currentData()
        next_options = self.option_getter.get_next_options(sequence, selected_filter)
        # for section in self.scroll_area.layout_manager.sections.values():
        #     section.pictographs = {}
        self.scroll_area.add_and_display_relevant_pictographs(next_options)



    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        spacing = 10
        for option in self.option_pool:
            view_width = int((self.width() // 8) - spacing)

            option.view.setFixedSize(view_width, view_width)
            option.view.view_scale = view_width / option.width()
            option.view.resetTransform()
            option.view.scale(option.view.view_scale, option.view.view_scale)
