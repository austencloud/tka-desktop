from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt


from base_widgets.base_pictograph.pictograph import Pictograph
from utilities.reversal_detector import ReversalDetector

from .section_manager.option_picker_layout_manager import OptionPickerLayoutManager
from .option_picker_display_manager import OptionPickerDisplayManager


if TYPE_CHECKING:
    pass

    from ..option_picker import OptionPicker


class OptionPickerScrollArea(QScrollArea):
    spacing = 3

    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.main_widget = option_picker.construct_tab.main_widget
        self.construct_tab = option_picker.construct_tab
        self.option_manager = self.option_picker.option_getter
        self.ori_calculator = self.main_widget.json_manager.ori_calculator
        self.json_manager = self.main_widget.json_manager
        self.json_loader = self.json_manager.loader_saver
        self.pictograph_cache: dict[str, Pictograph] = {}
        self.disabled = False

        self.configure_ui()

        self.layout_manager = OptionPickerLayoutManager(self)
        self.display_manager = OptionPickerDisplayManager(self)

    def configure_ui(self):
        self.setWidgetResizable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: transparent; border: none;")

        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.container = QWidget()
        self.container.setAutoFillBackground(True)
        self.container.setStyleSheet("background: transparent;")
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.container.setLayout(self.layout)
        self.setWidget(self.container)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def add_and_display_relevant_pictographs(self, next_options: list[dict]):
        for section in self.layout_manager.sections.values():
            section.clear_pictographs()
        for i, pictograph_data in enumerate(next_options):
            if i >= len(self.option_picker.option_pool):
                break
            pictograph = self.option_picker.option_pool[i]
            pictograph.updater.update_pictograph(pictograph_data)
            sequence_so_far = self.json_loader.load_current_sequence()
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.pictograph_data
            )
            pictograph.blue_reversal = reversal_info.get("blue_reversal", False)
            pictograph.red_reversal = reversal_info.get("red_reversal", False)
            self.display_manager.add_pictograph_to_section_layout(pictograph)
            pictograph.view.update_borders()
