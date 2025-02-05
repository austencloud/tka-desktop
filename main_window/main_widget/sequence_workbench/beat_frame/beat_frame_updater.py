from copy import deepcopy
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QApplication
from utilities.reversal_detector import (
    ReversalDetector,
)

if TYPE_CHECKING:
    from .sequence_beat_frame import SequenceBeatFrame
    from main_window.main_widget.sequence_workbench.beat_frame.beat import Beat


class BeatFrameUpdater:
    def __init__(self, beat_frame: "SequenceBeatFrame") -> None:
        self.bf = beat_frame

    def update_beats_from_current_sequence_json(self) -> None:

        current_sequence_json = (
            self.bf.json_manager.loader_saver.load_current_sequence_json()
        )
        sequence_entries = current_sequence_json[1:]

        if sequence_entries and "sequence_start_position" in sequence_entries[0]:
            self.update_start_pos_from_current_sequence_json(sequence_entries[0])
            beat_entries = sequence_entries[1:]
        else:
            beat_entries = sequence_entries

        for entry in beat_entries:
            if entry.get("is_placeholder", False):
                continue

            beat_num = entry["beat"]
            beat_view = self.bf.get.beat_view_by_number(beat_num)

            if beat_view and beat_view.beat:
                beat_view.beat.updater.update_pictograph(entry)
                beat = beat_view.beat
                pictograph_index = self.bf.get.index_of_beat(beat_view)
                sequence_so_far = (
                    self.bf.json_manager.loader_saver.load_current_sequence_json()[
                        : pictograph_index + 2
                    ]
                )
                reversal_info = ReversalDetector.detect_reversal(
                    sequence_so_far, beat.pictograph_data
                )
                beat.blue_reversal = reversal_info["blue_reversal"]
                beat.red_reversal = reversal_info["red_reversal"]
                beat.reversal_glyph.update_reversal_symbols()
            else:
                print(
                    f"Beat with number {beat_num} not found in the beat frame. Skipping."
                )
        if beat_entries:
            self.bf.sequence_workbench.difficulty_label.update_difficulty_label()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry["red_attributes"]["start_ori"] = entry["red_attributes"]["end_ori"]
        entry["blue_attributes"]["start_ori"] = entry["blue_attributes"]["end_ori"]
        entry["start_pos"] = entry["end_pos"]
        self.bf.start_pos_view.start_pos.updater.update_pictograph(entry)

    def update_beats_from(self, modified_sequence_json: list[dict]):
        self.json_manager = self.bf.json_manager
        json_updater = self.json_manager.updater
        self.json_manager.loader_saver.clear_current_sequence_file()

        def update_beat(beat: "Beat", beat_dict: dict, start_pos: bool = False):
            beat.updater.update_pictograph(beat_dict)
            grid_mode = self.bf.main_widget.grid_mode_checker.get_grid_mode(beat_dict)
            beat.grid.hide()
            beat.grid.__init__(beat, beat.grid.grid_data, grid_mode)
            if not start_pos:
                json_updater.update_current_sequence_file_with_beat(beat)

        if len(modified_sequence_json) > 1:
            start_pos_dict = modified_sequence_json[1]
            start_pos = self.bf.start_pos_view.start_pos
            update_beat(start_pos, start_pos_dict, start_pos=True)
            self.json_manager.start_pos_handler.set_start_position_data(start_pos)

        for i, beat_dict in enumerate(modified_sequence_json[2:], start=0):
            if i < len(self.bf.beat_views) and self.bf.beat_views[i].is_filled:
                update_beat(self.bf.beat_views[i].beat, beat_dict)
            else:
                break

        self.bf.main_widget.sequence_workbench.graph_editor.update_graph_editor()

    def reset_beat_frame(self) -> None:
        for beat_view in self.bf.beat_views:
            beat_view.setScene(beat_view.blank_beat)
            beat_view.is_filled = False

        self.bf.start_pos_view.setScene(self.bf.start_pos_view.blank_beat)
        self.bf.start_pos_view.is_filled = False
        self.bf.selection_overlay.deselect_beat()

        self.bf.sequence_workbench.current_word_label.update_current_word_label_from_beats()
        # self.bf.layout_manager.setup_layout()  # Re-setup layout
        # self.bf.updateGeometry()               # Force layout recalculation
        QApplication.processEvents()           # Process pending events
