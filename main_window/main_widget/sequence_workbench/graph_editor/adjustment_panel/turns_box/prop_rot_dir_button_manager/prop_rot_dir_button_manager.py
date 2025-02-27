from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from Enums.letters import Letter
from data.constants import (
    ANTI,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    END_ORI,
    FLOAT,
    ICON_DIR,
    NO_ROT,
    PRO,
    STATIC, MOTION_TYPE, PROP_ROT_DIR, TURNS, LETTER
)
from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat
from utilities.reversal_detector import (
    ReversalDetector,
)
from utilities.path_helpers import get_images_and_data_path
from .prop_rot_dir_button import PropRotDirButton

if TYPE_CHECKING:
    from ..turns_box import TurnsBox
    from objects.motion.motion import Motion


class PropRotDirButtonManager:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.previous_turns = 0
        self.prop_rot_dir_buttons = self._setup_prop_rot_dir_buttons()
        self.buttons = self.prop_rot_dir_buttons
        self.graph_editor = turns_box.graph_editor
        self.beat_frame = self.graph_editor.sequence_workbench.sequence_beat_frame
        self.main_widget = self.graph_editor.main_widget
        self.json_manager = self.graph_editor.main_widget.json_manager

    def _setup_prop_rot_dir_buttons(self) -> list[PropRotDirButton]:
        cw_path = get_images_and_data_path(f"{ICON_DIR}clock/clockwise.png")
        ccw_path = get_images_and_data_path(f"{ICON_DIR}clock/counter_clockwise.png")
        self.cw_button: PropRotDirButton = self.create_prop_rot_dir_button(
            cw_path,
            lambda: self._set_prop_rot_dir(CLOCKWISE),
            CLOCKWISE,
        )
        self.ccw_button: PropRotDirButton = self.create_prop_rot_dir_button(
            ccw_path,
            lambda: self._set_prop_rot_dir(COUNTER_CLOCKWISE),
            COUNTER_CLOCKWISE,
        )
        self.cw_button.unpress()
        self.ccw_button.unpress()
        self.cw_button.hide()
        self.ccw_button.hide()
        return [self.cw_button, self.ccw_button]

    def create_prop_rot_dir_button(
        self, icon_path: str, callback, prop_rot_dir
    ) -> PropRotDirButton:
        button = PropRotDirButton(self.turns_box, prop_rot_dir)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def _set_prop_rot_dir(self, prop_rot_dir: str) -> None:
        """Set the prop rotation direction and update the motion and letter."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if self.turns_box.prop_rot_dir_btn_state[prop_rot_dir]:
            return
        selected_beat = (
            self.graph_editor.sequence_workbench.sequence_beat_frame.get.currently_selected_beat_view()
        )
        both_pictographs: list[Beat] = [
            selected_beat.beat,
            self.graph_editor.pictograph_container.GE_view.pictograph,
        ]

        for pictograph in both_pictographs:
            for motion in pictograph.elements.motions.values():
                if motion.state.color == self.turns_box.color:
                    motion.state.prop_rot_dir = prop_rot_dir
                    motion.state.motion_type = self._get_new_motion_type(motion)
                    new_letter = self.graph_editor.main_widget.letter_determiner.determine_letter(
                        motion, swap_prop_rot_dir=True
                    )
                    self._update_pictograph_and_json(motion, new_letter)
                    pictograph.update()

            pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()

            sequence_so_far = self.json_manager.loader_saver.load_current_sequence()[
                : pictograph_index + 2
            ]
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.state.pictograph_data
            )
            pictograph.state.blue_reversal = reversal_info["blue_reversal"]
            pictograph.state.red_reversal = reversal_info["red_reversal"]
            pictograph.elements.reversal_glyph.update_reversal_symbols()

        self._update_button_states(prop_rot_dir)
        self.option_picker = (
            self.turns_box.graph_editor.sequence_workbench.main_widget.construct_tab.option_picker
        )
        self.option_picker.updater.refresh_options()
        QApplication.restoreOverrideCursor()

    def _get_new_motion_type(self, motion: "Motion"):
        motion_type = motion.state.motion_type
        if motion_type == ANTI:
            new_motion_type = PRO
            motion.state.motion_type = new_motion_type
        elif motion_type == PRO:
            new_motion_type = ANTI
            motion.state.motion_type = new_motion_type
        else:
            new_motion_type = motion_type
        return new_motion_type

    def _update_pictograph_and_json(
        self, motion: "Motion", new_letter: Letter = None
    ) -> None:
        """Update the pictograph and JSON with the new letter and motion attributes."""
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        beat = motion.pictograph
        new_dict = {
            MOTION_TYPE: motion.state.motion_type,
            PROP_ROT_DIR: motion.state.prop_rot_dir,
            END_ORI: motion.state.end_ori,
            TURNS: motion.state.turns,
        }

        beat.state.pictograph_data[motion.state.color + "_attributes"].update(new_dict)

        if new_letter:
            beat.state.pictograph_data[LETTER] = new_letter.value
            beat.state.letter = new_letter

        beat.managers.updater.update_pictograph(beat.state.pictograph_data)
        json_index = pictograph_index + 2
        json_updater = self.json_manager.updater
        if new_letter:
            json_updater.letter_updater.update_letter_in_json_at_index(
                json_index, new_letter.value
            )
        self.turns_box.turns_widget.motion_type_label.update_display(
            motion.state.motion_type
        )
        json_updater.motion_type_updater.update_json_motion_type(
            json_index, motion.state.color, motion.state.motion_type
        )
        json_updater.prop_rot_dir_updater.update_json_prop_rot_dir(
            json_index, motion.state.color, motion.state.prop_rot_dir
        )
        self.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )
        self.graph_editor.sequence_workbench.sequence_beat_frame.updater.update_beats_from_current_sequence_json()
        self.graph_editor.main_widget.sequence_workbench.current_word_label.set_current_word(
            self.graph_editor.sequence_workbench.sequence_beat_frame.get.current_word()
        )

    def _update_button_states(
        self,
        prop_rot_dir: str,
    ) -> None:
        for button in self.prop_rot_dir_buttons:
            if button.prop_rot_dir == prop_rot_dir:
                button.press()
                button.update_state_dict(self.turns_box.prop_rot_dir_btn_state, True)
            else:
                button.unpress()
                button.update_state_dict(self.turns_box.prop_rot_dir_btn_state, False)

    def show_prop_rot_dir_buttons(self) -> None:
        self.cw_button.show()
        self.ccw_button.show()

    def hide_prop_rot_dir_buttons(self) -> None:
        for button in self.prop_rot_dir_buttons:
            button.hide()

    def _opposite_prop_rot_dir(self, prop_rot_dir: str) -> str:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)

    def unpress_prop_rot_dir_buttons(self) -> None:
        self.cw_button.unpress()
        self.ccw_button.unpress()

    def update_prop_rotation_buttons(self, motion: "Motion", new_turns: int) -> None:
        """Adjust prop rotation direction buttons based on the new turns value."""
        if new_turns == 0:
            self._handle_zero_turns(motion)
        elif new_turns == "fl":
            self._handle_float_turn_buttons(motion)
        elif new_turns > 0:
            self._handle_positive_turns(motion)

    def _handle_zero_turns(self, motion: "Motion") -> None:
        """Handle button states when turns are zero."""
        if motion.state.motion_type in [DASH, STATIC]:
            motion.state.prop_rot_dir = NO_ROT
            self.unpress_prop_rot_dir_buttons()
            self.hide_prop_rot_dir_buttons()
        elif motion.state.motion_type in [PRO, ANTI]:
            self.show_prop_rot_dir_buttons()

    def _handle_float_turn_buttons(self, motion: "Motion") -> None:
        """Handle button states when turns are 'float'."""
        self.unpress_prop_rot_dir_buttons()
        self.hide_prop_rot_dir_buttons()
        motion.state.motion_type = FLOAT
        motion.state.prop_rot_dir = NO_ROT

    def _handle_positive_turns(self, motion: "Motion") -> None:
        """Handle button states when turns are positive."""
        self.show_prop_rot_dir_buttons()
        if motion.state.prop_rot_dir == NO_ROT:
            motion.state.prop_rot_dir = self._get_default_prop_rot_dir()
            self.show_prop_rot_dir_buttons()

    def _get_default_prop_rot_dir(self) -> str:
        """Set default prop rotation direction to clockwise."""
        self._set_prop_rot_dir_state_default()
        self.show_prop_rot_dir_buttons()
        self.cw_button.press()
        return CLOCKWISE

    def _set_prop_rot_dir_state_default(self) -> None:
        """Set the prop rotation direction state to clockwise by default."""
        self.turns_box.prop_rot_dir_btn_state[CLOCKWISE] = True
        self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE] = False
