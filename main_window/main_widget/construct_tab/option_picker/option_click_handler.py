from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import SequenceBeatFrame

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from base_widgets.pictograph.pictograph_scene import PictographScene

class OptionClickHandler:
    def __init__(self, op: "OptionPicker", sequence_beat_frame: "SequenceBeatFrame"):
        self.option_picker = op
        self.sequence_beat_frame = sequence_beat_frame
        self.add_to_sequence_manager = op.add_to_sequence_manager

    def handle_click(self, clicked_option: "PictographScene") -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        new_beat = self.add_to_sequence_manager.create_new_beat(clicked_option)
        self.sequence_beat_frame.beat_adder.add_beat_to_sequence(new_beat)
        if new_beat.view:
            self.sequence_beat_frame.selection_overlay.select_beat(new_beat.view)
            QApplication.processEvents()
            self.option_picker.updater.refresh_options()
            new_beat.view.is_filled = True
            self.option_picker.choose_next_label.setText("Choose your next pictograph:")
        QApplication.restoreOverrideCursor()
