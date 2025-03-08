from typing import TYPE_CHECKING

from data.constants import BEAT
from settings_manager.global_settings.app_context import AppContext
from utils.reversal_detector import (
    ReversalDetector,
)

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.beat_view import (
        Beat,
    )
    from .sequence_beat_frame import SequenceBeatFrame


class BeatAdder:
    def __init__(self, beat_frame: "SequenceBeatFrame"):
        self.beat_frame = beat_frame
        self.beats = beat_frame.beat_views
        self.sequence_workbench = beat_frame.sequence_workbench
        self.main_widget = beat_frame.main_widget

    def add_beat_to_sequence(
        self,
        new_beat: "Beat",
        override_grow_sequence=False,
        update_word=True,
        update_level=True,
        select_beat=True,
        update_image_export_preview=True,
    ) -> None:
        next_beat_number = self.calculate_next_beat_number()
        grow_sequence = (
            AppContext.settings_manager().global_settings.get_grow_sequence()
        )

        next_beat_index = self.beat_frame.get.next_available_beat()
        if next_beat_number == 65:
            self.sequence_workbench.indicator_label.show_message(
                "The sequence is full at 64 beats."
            )
            return

        if next_beat_index is not None and not self.beats[next_beat_index].is_filled:
            sequence_so_far = (
                AppContext.json_manager().loader_saver.load_current_sequence()
            )
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, new_beat.state.pictograph_data
            )
            new_beat.state.blue_reversal = reversal_info.get("blue_reversal", False)
            new_beat.state.red_reversal = reversal_info.get("red_reversal", False)
            self.beats[next_beat_index].set_beat(new_beat, next_beat_number)
            new_beat.state.pictograph_data[BEAT] = next_beat_number
            if grow_sequence and not override_grow_sequence:
                self._adjust_layout_and_update_sequence_builder(next_beat_index)
            elif not grow_sequence or override_grow_sequence:
                self._update_sequence_builder(next_beat_index)

            new_beat.managers.updater.update_pictograph()
            if select_beat:
                self.beat_frame.selection_overlay.select_beat_view(
                    self.beats[next_beat_index], toggle_animation=False
                )
            AppContext.json_manager().updater.update_current_sequence_file_with_beat(
                self.beats[next_beat_index].beat
            )
            if update_word:
                self.sequence_workbench.current_word_label.update_current_word_label()
        if update_image_export_preview:
            self.beat_frame.emit_update_image_export_preview()
        if next_beat_number and update_level == True:
            self.sequence_workbench.difficulty_label.update_difficulty_label()

    def _adjust_layout_and_update_sequence_builder(self, index: int) -> None:
        self.beat_frame.layout_manager.adjust_layout_to_sequence_length()
        self._update_sequence_builder(index)

    def _update_sequence_builder(self, index: int) -> None:
        self.main_widget.construct_tab.last_beat = self.beats[index].beat

    def calculate_next_beat_number(self) -> int:
        """
        Calculate the next beat number by summing up the durations of all filled beats.
        """
        current_beat_number = 1
        for beat_view in self.beats:
            if beat_view.is_filled and beat_view.beat:
                current_beat_number += beat_view.beat.duration
            else:
                break
        return current_beat_number
