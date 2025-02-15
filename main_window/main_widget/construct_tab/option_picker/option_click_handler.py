from PyQt6.QtWidgets import QApplication
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_workbench.beat_frame.sequence_beat_frame import SequenceBeatFrame

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from base_widgets.base_pictograph.pictograph import Pictograph


class OptionClickHandler:
    def __init__(self, option_picker: "OptionPicker", beat_frame: "SequenceBeatFrame"):
        self.option_picker = option_picker
        self.construct_tab = self.option_picker.construct_tab
        self.beat_frame = beat_frame
        self.add_to_sequence_manager = self.construct_tab.add_to_sequence_manager

    def handle_click(self, clicked_option: "Pictograph") -> None:
        """Handle the logic when an option is clicked."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        new_beat = self.add_to_sequence_manager.create_new_beat(clicked_option)
        self.beat_frame.beat_adder.add_beat_to_sequence(new_beat)
        if new_beat.view:
            selection_manager = self.beat_frame.selection_overlay
            selection_manager.select_beat(new_beat.view)
            QApplication.processEvents()

            self.option_picker.updater.refresh_options()

            new_beat.view.is_filled = True
            self.option_picker.choose_next_label.set_default_text()
        QApplication.restoreOverrideCursor()
