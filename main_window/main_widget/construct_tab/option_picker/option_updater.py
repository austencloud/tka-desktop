from typing import TYPE_CHECKING
import os

from Enums.letters import LetterType

if TYPE_CHECKING:
    from .option_picker import OptionPicker


class OptionUpdater:
    def __init__(self, option_picker: "OptionPicker"):
        self.option_picker = option_picker
        self.scroll_area = option_picker.option_scroll
        self.json_loader = option_picker.main_widget.json_manager.loader_saver
        self.app_root = self._get_app_root()

    def _get_app_root(self) -> str:
        """Determine the root path of the application."""
        current_file_path = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

    def refresh_options(self):
        sequence = self.json_loader.load_current_sequence_json()
        if len(sequence) > 1:
            sections = self.scroll_area.sections
            pictograph_frames = [
                section.pictograph_frame for section in sections.values()
            ]

            self.option_picker.main_widget.fade_manager.widget_fader.fade_and_update(
                pictograph_frames, self.update_options, 200
            )

    def update_options(self):
        sequence = self.json_loader.load_current_sequence_json()
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
