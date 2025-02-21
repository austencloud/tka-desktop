# option_picker_click_handler.py

from PyQt6.QtWidgets import QApplication
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from base_widgets.pictograph.pictograph_scene import PictographScene


class OptionPickerClickHandler:
    def __init__(self, option_picker: "OptionPicker") -> None:
        self.option_picker = option_picker
        self.construct_tab = self.option_picker.construct_tab
        self.main_widget = self.construct_tab.main_widget
        self.beat_frame = self.main_widget.sequence_workbench.sequence_beat_frame
        self.sequence_workbench = self.main_widget.sequence_workbench
        self.add_to_sequence_manager = self.construct_tab.add_to_sequence_manager
        self.settings_manager = self.main_widget.settings_manager
        self.layout_settings = self.settings_manager.sequence_layout
