from typing import TYPE_CHECKING
from copy import deepcopy
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from base_widgets.pictograph.pictograph import Pictograph

from .start_pos_beat import StartPositionBeat

if TYPE_CHECKING:
    from .sequence_beat_frame import SequenceBeatFrame


class StartPositionAdder:
    def __init__(self, beat_frame: "SequenceBeatFrame"):
        self.beat_frame = beat_frame
        self.sequence_workbench = beat_frame.sequence_workbench
        self.main_widget = beat_frame.main_widget
        self.json_manager = self.main_widget.json_manager

    def add_start_pos_to_sequence(self, clicked_start_option: "Pictograph") -> None:
        # Change cursor to busy
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        try:
            start_pos_beat = StartPositionBeat(self.beat_frame)

            start_pos_view = self.beat_frame.start_pos_view
            self.main_widget.construct_tab.last_beat = start_pos_beat
            self.construct_tab = self.main_widget.construct_tab
            start_pos_dict = clicked_start_option.pictograph_data
            graph_editor = self.sequence_workbench.graph_editor

            if not graph_editor.is_toggled:
                graph_editor.animator.toggle()
            start_pos_beat.updater.update_pictograph(deepcopy(start_pos_dict))
            clicked_start_option.updater.update_dict_from_attributes()
            self.json_manager.start_pos_handler.set_start_position_data(start_pos_beat)
            self.beat_frame.start_pos_view.set_start_pos(start_pos_beat)
            self.beat_frame.selection_overlay.select_beat(start_pos_view, False)
            self.construct_tab.transition_to_option_picker()
            self.construct_tab.option_picker.updater.update_options()
        finally:
            # Revert cursor back to default
            QApplication.restoreOverrideCursor()
