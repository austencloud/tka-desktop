from typing import TYPE_CHECKING
import os
from enums.letter.letter_type import LetterType
from main_window.main_widget.fade_manager.fade_manager import FadeManager
from interfaces.json_manager_interface import IJsonManager

if TYPE_CHECKING:
    from ..widgets.legacy_option_picker import LegacyOptionPicker


class OptionUpdater:
    def __init__(
        self,
        option_picker: "LegacyOptionPicker",
        fade_manager: FadeManager,
        json_manager: IJsonManager,
    ) -> None:
        self.option_picker = option_picker
        self.scroll_area = option_picker.option_scroll
        self.fade_manager = fade_manager
        self.json_loader = json_manager.loader_saver
        self.app_root = self._get_app_root()

    def _get_app_root(self) -> str:
        current_file = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

    def refresh_options(self) -> None:
        sequence = self.json_loader.load_current_sequence()
        if len(sequence) <= 1:
            return
        sections = self.scroll_area.sections
        frames = [section.pictograph_frame for section in sections.values()]

        self.fade_manager.widget_fader.fade_and_update(frames, self.update_options, 200)

    def update_options(self) -> None:
        sequence = self.json_loader.load_current_sequence()
        sequence_without_metdata = sequence[1:]

        # Get the selected filter if the reversal_filter is available
        selected_filter = None
        if hasattr(self.option_picker, "reversal_filter"):
            selected_filter = (
                self.option_picker.reversal_filter.reversal_combobox.currentData()
            )

        next_options = self.option_picker.option_getter.get_next_options(
            sequence_without_metdata, selected_filter
        )

        for section in self.option_picker.option_scroll.sections.values():
            section.clear_pictographs()

        for i, option_data in enumerate(next_options):
            if i >= len(self.option_picker.option_pool):
                break
            option = self.option_picker.option_pool[i]
            option.managers.updater.update_pictograph(option_data)
            option.elements.view.update_borders()
            letter_type = LetterType.get_letter_type(option.state.letter)
            section = self.option_picker.option_scroll.sections.get(letter_type)
            if section:
                section.add_pictograph(option)
