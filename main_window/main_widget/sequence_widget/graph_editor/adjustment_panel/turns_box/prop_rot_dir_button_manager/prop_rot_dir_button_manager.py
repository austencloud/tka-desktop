from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon
from Enums.letters import Letter
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.sequence_widget.beat_frame.reversal_detector import (
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
        self.beat_frame = self.graph_editor.sequence_widget.beat_frame
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
        if self.turns_box.prop_rot_dir_btn_state[prop_rot_dir]:
            return
        selected_beat = (
            self.graph_editor.sequence_widget.beat_frame.get.currently_selected_beat_view()
        )
        both_beats: list[Beat] = [
            selected_beat.beat,
            self.graph_editor.pictograph_container.GE_view.pictograph,
        ]

        for pictograph in both_beats:
            for motion in pictograph.motions.values():
                if motion.color == self.turns_box.color:
                    motion.prop_rot_dir = prop_rot_dir
                    new_letter = self.graph_editor.main_widget.letter_determiner.determine_letter(
                        motion, swap_prop_rot_dir=True
                    )
                    self._update_pictograph_and_json(motion, new_letter)

            pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()

            sequence_so_far = (
                self.json_manager.loader_saver.load_current_sequence_json()[
                    : pictograph_index + 2
                ]
            )
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.pictograph_dict
            )
            pictograph.blue_reversal = reversal_info["blue_reversal"]
            pictograph.red_reversal = reversal_info["red_reversal"]
            pictograph.reversal_glyph.update_reversal_symbols()

        self._update_button_states(prop_rot_dir)
        self.option_picker = (
            self.turns_box.graph_editor.sequence_widget.main_widget.construct_tab.option_picker
        )
        self.option_picker.update_option_picker()
        self.graph_editor.pictograph_container.update_pictograph(pictograph)

    def _update_pictograph_and_json(
        self, motion: "Motion", new_letter: Letter = None
    ) -> None:
        """Update the pictograph and JSON with the new letter and motion attributes."""
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        beat = motion.pictograph
        beat.pictograph_dict[motion.color + "_attributes"].update(
            {
                "motion_type": motion.motion_type,
                "prop_rot_dir": motion.prop_rot_dir,
                "end_ori": motion.end_ori,
                "turns": motion.turns,
            }
        )

        if new_letter:
            beat.pictograph_dict["letter"] = new_letter.value
            beat.letter = new_letter

        beat.updater.update_pictograph(beat.pictograph_dict)

        json_index = pictograph_index + 2

        self.json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json_at_index(
            json_index, motion.color, motion.prop_rot_dir
        )
        self.json_manager.updater.motion_type_updater.update_motion_type_in_json_at_index(
            json_index, motion.color, motion.motion_type
        )
        if new_letter:
            self.json_manager.updater.letter_updater.update_letter_in_json_at_index(
                json_index, new_letter.value
            )
        self.turns_box.turns_widget.motion_type_label.update_motion_type_label(
            motion.motion_type
        )

        self.graph_editor.sequence_widget.beat_frame.updater.update_beats_from_current_sequence_json()
        # Running the validation engine
        self.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )

        # Triggering updates for UI components
        self.graph_editor.main_widget.sequence_widget.current_word_label.set_current_word(
            self.graph_editor.sequence_widget.beat_frame.get.current_word()
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
