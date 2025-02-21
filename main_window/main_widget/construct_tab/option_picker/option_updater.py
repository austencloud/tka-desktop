import os
from typing import TYPE_CHECKING
from Enums.letters import LetterType
from main_window.main_widget.fade_manager.fade_manager import FadeManager
from main_window.settings_manager.global_settings.app_context import AppContext
from PyQt6.QtCore import QObject

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import (
        OptionPicker,
    )


class OptionUpdater(QObject):
    def __init__(self, op: "OptionPicker", fade_manager: "FadeManager"):
        super().__init__()
        self.option_picker = op
        self.scroll_area = op.option_scroll
        self.fade_manager = fade_manager
        self.json_loader = AppContext.json_manager().loader_saver
        self.app_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    def refresh_options(self):
        sequence = self.json_loader.load_current_sequence()
        if len(sequence) > 1:
            sections = self.scroll_area.sections
            frames = [sec.pictograph_frame for sec in sections.values()]
            self.fade_manager.widget_fader.fade_and_update(
                frames, self.update_options, 200
            )

    def update_options(self):
        sequence = self.json_loader.load_current_sequence()
        selected_filter = (
            self.option_picker.reversal_filter.reversal_combobox.currentData()
        )
        next_options = self.option_picker.option_getter.get_next_options(
            sequence, selected_filter
        )
        for section in self.option_picker.option_scroll.sections.values():
            section.clear_pictographs()
        for i, pictograph_data in enumerate(next_options):
            pictograph = self.option_picker.option_pool[i]
            pictograph.updater.update_pictograph(pictograph_data)
            pictograph.view.update_borders()
            self.scroll_area.sections[
                LetterType.get_letter_type(pictograph.letter)
            ].add_pictograph(pictograph)
