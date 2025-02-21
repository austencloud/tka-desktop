from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal
from data.constants import FLOAT
from main_window.settings_manager.global_settings.app_context import AppContext
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget

# assign Turns as int |float | str
Turns = Union[int, float, str]


class TurnsAdjustmentManager(QObject):
    turns_adjusted = pyqtSignal(object)  # Signal can now handle any type

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.graph_editor = self.turns_widget.turns_box.graph_editor
        self.beat_frame = self.graph_editor.sequence_workbench.sequence_beat_frame
        self.main_widget = self.graph_editor.main_widget
        self.json_manager = AppContext.json_manager()
        self.json_validation_engine = self.json_manager.ori_validation_engine
        self.color = self.turns_widget.turns_box.color

        self.turns_adjusted.connect(
            self.beat_frame.updater.update_beats_from_current_sequence_json
        )

    def adjust_turns(self, adjustment: Union[int, float]) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        GE_view = self.graph_editor.pictograph_container.GE_view
        self.GE_pictograph = GE_view.pictograph
        self.reference_beat = GE_view.reference_beat

        current_turns = self.get_current_turns_value()
        GE_motion = self.GE_pictograph.motions[self.color]
        matching_motion = self.reference_beat.motions[self.color]

        if current_turns == "fl" and adjustment > 0:
            new_turns = 0
        elif current_turns == "fl" and adjustment < 0:
            QApplication.restoreOverrideCursor()
            return
        elif current_turns == 0 and adjustment < 0:
            new_turns = "fl"
        else:
            new_turns = self._clamp_turns(current_turns + adjustment)
            new_turns = self.convert_turn_floats_to_ints(new_turns)

        self.turns_widget.update_turns_display(matching_motion, new_turns)
        matching_motion.turns = new_turns
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        self.json_manager.updater.turns_updater.update_turns_in_json_at_index(
            pictograph_index + 2, self.color, new_turns, self.beat_frame
        )
        self.json_validation_engine.run(is_current_sequence=True)
        self.json_updater = self.json_manager.updater
        QApplication.processEvents()
        for pictograph in [self.reference_beat, self.GE_pictograph]:
            self.turns_widget.turns_updater.adjust_turns_for_pictograph(
                pictograph, new_turns
            )

        for motion in [matching_motion, GE_motion]:
            motion.turns = new_turns
            new_letter = self.get_new_letter(new_turns, motion)
            self.turns_widget.turns_box.prop_rot_dir_button_manager._update_pictograph_and_json(
                motion, new_letter
            )
            motion.prefloat_motion_type

        self.main_widget.construct_tab.option_picker.updater.update_options()
        sequence = self.json_manager.loader_saver.load_current_sequence()
        self.beat_frame.updater.update_beats_from(sequence)
        QApplication.restoreOverrideCursor()

    def get_new_letter(self, new_turns, motion):
        need_to_determine_new_letter: bool = self.determine_if_new_letter_is_needed(
            motion, new_turns
        )
        if need_to_determine_new_letter:
            new_letter = self.main_widget.letter_determiner.determine_letter(motion)
        else:
            new_letter = None
        return new_letter

    def determine_if_new_letter_is_needed(self, motion: Motion, new_turns) -> bool:
        if new_turns == "fl":
            return True
        if motion.turns == "fl" and new_turns >= 0:
            return True

    def _repaint_views(self):
        """Repaint the pictograph and GE pictograph views to reflect the change."""
        self.reference_beat.view.repaint()
        GE_pictograph = (
            self.turns_widget.turns_box.adjustment_panel.graph_editor.pictograph_container.GE_view.get_current_pictograph()
        )
        GE_pictograph.view.repaint()
        # GE_pictograph.updater.update_pictograph()
        QApplication.processEvents()

    def direct_set_turns(self, new_turns: int | float | str) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        GE_view = self.graph_editor.pictograph_container.GE_view
        self.GE_pictograph = GE_view.pictograph
        self.reference_beat = GE_view.reference_beat
        self._update_motion_properties(new_turns)

        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        self.json_manager.updater.turns_updater.update_turns_in_json_at_index(
            pictograph_index + 2, self.color, new_turns, self.beat_frame
        )
        self.reference_beat.motions[self.color].turns = new_turns
        # self.reference_beat.view.repaint()
        self.turns_widget.update_turns_display(
            self.reference_beat.motions[self.color], new_turns
        )

        for pictograph in [self.reference_beat, self.GE_pictograph]:
            self.turns_widget.turns_updater.adjust_turns_for_pictograph(
                pictograph, new_turns
            )

        matching_motion = self.reference_beat.motions[self.color]
        GE_motion = self.GE_pictograph.motions[self.color]

        for motion in [matching_motion, GE_motion]:
            motion.turns = new_turns
            self.turns_widget.turns_box.prop_rot_dir_button_manager._update_pictograph_and_json(
                motion
            )

        self.json_validation_engine.run(is_current_sequence=True)
        self.main_widget.construct_tab.option_picker.updater.update_options()
        self.turns_adjusted.emit(new_turns)
        QApplication.restoreOverrideCursor()

    def get_current_turns_value(self) -> Turns:
        return self._get_turns()

    def _get_turns(self) -> Turns:
        turns = self.turns_widget.display_frame.turns_label.text()
        if turns == "fl":
            return "fl"
        turns = self.convert_turns_from_str_to_num(turns)
        turns = self.convert_turn_floats_to_ints(turns)
        return turns

    def convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)

    def convert_turn_floats_to_ints(self, turns: Turns) -> Turns:
        if turns in [0.0, 1.0, 2.0, 3.0]:
            return int(turns)
        else:
            return turns

    def _clamp_turns(self, turns: Turns) -> Turns:
        if isinstance(turns, (int, float)):
            return max(0, min(3, turns))
        return turns

    def _update_turns_display(self, turns: Turns) -> None:
        self.turns_widget.update_turns_display(turns)

    def _update_motion_properties(self, new_turns) -> None:
        for motion in [
            self.reference_beat.motions[self.color],
            self.GE_pictograph.motions[self.color],
        ]:
            self.turns_widget.turns_updater.set_motion_turns(motion, new_turns)
