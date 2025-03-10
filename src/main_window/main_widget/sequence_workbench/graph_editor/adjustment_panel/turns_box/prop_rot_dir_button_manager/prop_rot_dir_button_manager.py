from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from data.constants import (
    END_ORI,
    LETTER,
    MOTION_TYPE,
    NO_ROT,
    PROP_ROT_DIR,
    TURNS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
    TurnsValue,
)
from base_widgets.pictograph.pictograph import Pictograph
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_btn_state import (
    PropRotationState,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_logic_handler import (
    PropRotDirLogicHandler,
)
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class PropRotDirButtonManager:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.state = PropRotationState()
        self.logic_handler = PropRotDirLogicHandler(turns_box, self.state)

        self.state.state_changed.connect(self.turns_box.header.update_turns_box_header)

    def update_buttons_for_prop_rot_dir(self, prop_rot_dir: str) -> None:
        if prop_rot_dir == NO_ROT:

            self.state.update_state(CLOCKWISE, False)
            if hasattr(self.turns_box.header, "unpress_prop_rot_dir_buttons"):
                self.turns_box.header.unpress_prop_rot_dir_buttons()
        else:

            self.state.update_state(prop_rot_dir, True)

            header = self.turns_box.header
            if prop_rot_dir == CLOCKWISE:
                if hasattr(header, "cw_button"):
                    header.cw_button.set_selected(True)
                if hasattr(header, "ccw_button"):
                    header.ccw_button.set_selected(False)
            else:
                if hasattr(header, "cw_button"):
                    header.cw_button.set_selected(False)
                if hasattr(header, "ccw_button"):
                    header.ccw_button.set_selected(True)

            if hasattr(header, "show_prop_rot_dir_buttons"):
                header.show_prop_rot_dir_buttons()

    def set_prop_rot_dir(self, prop_rot_dir: str) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        if self.turns_box.prop_rot_dir_btn_state[prop_rot_dir]:
            return

        self.logic_handler.update_rotation_states(prop_rot_dir)
        self.logic_handler.update_related_components()

        self.turns_box.graph_editor.sequence_workbench.main_widget.construct_tab.option_picker.updater.refresh_options()

        QApplication.restoreOverrideCursor()

    def update_for_motion_change(self, motion: "Motion") -> None:
        self.logic_handler.current_motion = motion

        self.turns_box.header.update_turns_box_header()

        if motion.state.turns > 0 and motion.state.prop_rot_dir == NO_ROT:
            self.set_prop_rot_dir(self.logic_handler._get_default_prop_rot_dir())

    def update_for_turns_change(self, value: "TurnsValue") -> None:

        if not self.logic_handler.current_motion:
            return

        motion = self.logic_handler.current_motion

        if value.raw_value == 0 or value.raw_value == "fl":
            self.set_prop_rot_dir(NO_ROT)

        elif motion.state.prop_rot_dir == NO_ROT:
            default_dir = self.logic_handler._get_default_prop_rot_dir()
            self.set_prop_rot_dir(default_dir)

        self.state.update_state(motion.state.prop_rot_dir, True)

        self._update_pictograph_and_json(motion)

        self.turns_box.header.update_turns_box_header()

    def set_motion(self, motion: "Motion") -> None:
        self.update_for_motion_change(motion)

    def update_pictograph_letter(self, pictograph: "Pictograph") -> None:
        new_letter = (
            self.turns_box.graph_editor.main_widget.letter_determiner.determine_letter(
                pictograph.state.pictograph_data, swap_prop_rot_dir=True
            )
        )
        self.json_manager = (
            self.turns_box.graph_editor.sequence_workbench.main_widget.json_manager
        )
        self.beat_frame = (
            self.turns_box.graph_editor.sequence_workbench.main_widget.sequence_workbench.beat_frame
        )
        if new_letter:
            pictograph.state.pictograph_data[LETTER] = new_letter.value
            pictograph.state.letter = new_letter
            pictograph.managers.updater.update_pictograph(
                pictograph.state.pictograph_data
            )

        if new_letter:
            json_updater = self.json_manager.updater
            pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
            json_index = pictograph_index + 2
            json_updater.letter_updater.update_letter_in_json_at_index(
                json_index, new_letter.value
            )

    def _update_pictograph_and_json(self, motion: "Motion") -> None:
        self.beat_frame = self.turns_box.graph_editor.sequence_workbench.beat_frame
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        self.graph_editor = self.turns_box.graph_editor
        self.json_manager = self.graph_editor.main_widget.json_manager
        beat = motion.pictograph
        new_dict = {
            MOTION_TYPE: motion.state.motion_type,
            PROP_ROT_DIR: motion.state.prop_rot_dir,
            END_ORI: motion.state.end_ori,
            TURNS: motion.state.turns,
        }

        beat.state.pictograph_data[motion.state.color + "_attributes"].update(new_dict)

        beat.managers.updater.update_pictograph(beat.state.pictograph_data)
        json_index = pictograph_index + 2
        json_updater = self.json_manager.updater
        self.turns_box.turns_widget.motion_type_label.update_display(
            motion.state.motion_type
        )
        json_updater.motion_type_updater.update_motion_type_in_json(
            json_index, motion.state.color, motion.state.motion_type
        )
        json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
            json_index, motion.state.color, motion.state.prop_rot_dir
        )
        self.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )
        self.graph_editor.sequence_workbench.beat_frame.updater.update_beats_from_current_sequence_json()
        self.graph_editor.main_widget.sequence_workbench.current_word_label.set_current_word(
            self.graph_editor.sequence_workbench.beat_frame.get.current_word()
        )
