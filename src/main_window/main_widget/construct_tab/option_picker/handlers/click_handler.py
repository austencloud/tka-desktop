from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..widgets.option_picker_widget import OptionPickerWidget
    from base_widgets.pictograph.pictograph import Pictograph
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class OptionClickHandler:
    def __init__(
        self, option_picker: "OptionPickerWidget", beat_frame: "SequenceBeatFrame"
    ) -> None:
        self.option_picker = option_picker
        self.beat_frame = beat_frame
        self.add_to_sequence_manager = option_picker.add_to_sequence_manager

    def handle_option_click(self, clicked_option: "Pictograph") -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            new_beat = self.add_to_sequence_manager.create_new_beat(clicked_option)
            self.beat_frame.beat_adder.add_beat_to_sequence(new_beat)
            if new_beat.view:
                self.beat_frame.selection_overlay.select_beat_view(new_beat.view)
                QApplication.processEvents()
                self.option_picker.updater.refresh_options()
                new_beat.view.is_filled = True
                self.option_picker.choose_next_label.setText(
                    "Choose your next pictograph:"
                )
        finally:
            QApplication.restoreOverrideCursor()
