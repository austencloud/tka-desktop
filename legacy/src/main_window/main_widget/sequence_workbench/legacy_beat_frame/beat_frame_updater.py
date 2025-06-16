from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from data.constants import (
    BEAT,
    BLUE_ATTRS,
    END_ORI,
    END_POS,
    RED_ATTRS,
    SEQUENCE_START_POSITION,
    START_ORI,
    START_POS,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext
from utils.reversal_detector import (
    ReversalDetector,
)

if TYPE_CHECKING:
    from .legacy_beat_frame import LegacyBeatFrame
    from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat


class BeatFrameUpdater:
    def __init__(self, beat_frame: "LegacyBeatFrame") -> None:
        self.bf = beat_frame
        self.json_manager = AppContext.json_manager()

    def update_beats_from_current_sequence_json(self) -> None:

        current_sequence_json = self.json_manager.loader_saver.load_current_sequence()
        sequence_entries = current_sequence_json[1:]

        if sequence_entries and SEQUENCE_START_POSITION in sequence_entries[0]:
            self.update_start_pos_from_current_sequence_json(sequence_entries[0])
            beat_entries = sequence_entries[1:]
        else:
            beat_entries = sequence_entries

        for entry in beat_entries:
            if entry.get("is_placeholder", False):
                continue

            beat_num = entry[BEAT]
            beat_view = self.bf.get.beat_view_by_number(beat_num)

            if beat_view and beat_view.beat:
                beat_view.beat.managers.updater.update_pictograph(entry)
                beat = beat_view.beat
                pictograph_index = self.bf.get.index_of_beat(beat_view)
                sequence_so_far = (
                    self.json_manager.loader_saver.load_current_sequence()[
                        : pictograph_index + 2
                    ]
                )
                reversal_info = ReversalDetector.detect_reversal(
                    sequence_so_far, beat.state.pictograph_data
                )
                beat.state.blue_reversal = reversal_info["blue_reversal"]
                beat.state.red_reversal = reversal_info["red_reversal"]
                beat.elements.reversal_glyph.update_reversal_symbols()
            else:
                pass
        if beat_entries:
            self.bf.sequence_workbench.difficulty_label.update_difficulty_label()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry[RED_ATTRS][START_ORI] = entry[RED_ATTRS][END_ORI]
        entry[BLUE_ATTRS][START_ORI] = entry[BLUE_ATTRS][END_ORI]
        entry[START_POS] = entry[END_POS]
        self.bf.start_pos_view.start_pos.managers.updater.update_pictograph(entry)

    def update_beats_from(self, modified_sequence_json: list[dict]):
        self.json_manager.loader_saver.clear_current_sequence_file()

        def update_beat(beat: "Beat", beat_data: dict, start_pos: bool = False):
            beat.managers.updater.update_pictograph(beat_data)

            if not start_pos:
                self.json_manager.updater.update_current_sequence_file_with_beat(
                    beat, beat_data
                )

        # Start position update
        if len(modified_sequence_json) > 1:
            start_pos_dict = modified_sequence_json[1]
            start_pos = self.bf.start_pos_view.start_pos
            update_beat(start_pos, start_pos_dict, start_pos=True)
            self.json_manager.start_pos_handler.set_start_position_data(
                start_pos, start_pos_dict
            )

        # Update beats
        for i, beat_data in enumerate(modified_sequence_json[2:], start=0):
            if i < len(self.bf.beat_views) and self.bf.beat_views[i].is_filled:
                update_beat(self.bf.beat_views[i].beat, beat_data)
            else:
                break

        sequence_workbench = self.bf.main_widget.get_widget("sequence_workbench")
        if sequence_workbench:
            sequence_workbench.graph_editor.update_graph_editor()

    def reset_beat_frame(self) -> None:
        for beat_view in self.bf.beat_views:
            beat_view.setScene(beat_view.blank_beat)
            beat_view.is_filled = False

        self.bf.start_pos_view.setScene(self.bf.start_pos_view.blank_beat)
        self.bf.start_pos_view.is_filled = False
        self.bf.selection_overlay.deselect_beat()

        self.bf.sequence_workbench.current_word_label.update_current_word_label()
        QApplication.processEvents()
