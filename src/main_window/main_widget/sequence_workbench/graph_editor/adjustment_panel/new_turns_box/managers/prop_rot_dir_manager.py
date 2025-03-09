# === turns_box/managers/prop_rot_dir_manager.py ===
from typing import TYPE_CHECKING, Optional, Dict, List
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication

from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT

from ..domain.rotation_state import RotationState, str

if TYPE_CHECKING:
    from ..ui.turns_box import TurnsBox
    from objects.motion.motion import Motion
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
        TurnsValue,
    )
    from base_widgets.pictograph.pictograph import Pictograph


class PropRotDirManager(QObject):
    """Manager for handling prop rotation direction logic and state"""

    rotation_updated = pyqtSignal(dict)

    def __init__(self, turns_box: "TurnsBox"):
        super().__init__()
        self.turns_box = turns_box
        self.state = RotationState()
        self.current_motion: Optional["Motion"] = None

        # Connect signals
        self.state.state_changed.connect(self.turns_box.header.update_turns_box_header)

    def set_prop_rot_dir(self, prop_rot_dir: str) -> None:
        """Set the prop rotation direction and update related components"""
        # Skip if already in this state
        if self.state.current.get(prop_rot_dir, False):
            return

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        try:
            # Update state
            self.state.update_state(prop_rot_dir, True)

            # Update motion properties
            self._update_motion_properties(prop_rot_dir)

            # Update pictograph and JSON
            self._update_pictograph_and_json()

            # Refresh UI
            self.turns_box.graph_editor.sequence_workbench.main_widget.construct_tab.option_picker.updater.refresh_options()
        finally:
            QApplication.restoreOverrideCursor()

    def update_for_motion_change(self, motion: "Motion") -> None:
        """Update manager when motion changes"""
        self.current_motion = motion

        # Update header UI
        self.turns_box.header.update_turns_box_header()

        # Auto-set rotation direction if needed
        if motion.state.turns > 0 and motion.state.prop_rot_dir == NO_ROT:
            self.set_prop_rot_dir(self._get_default_prop_rot_dir())

    def update_for_turns_change(self, value: "TurnsValue") -> None:
        """Update rotation direction based on turns value changes"""
        if not self.current_motion:
            return

        motion = self.current_motion

        # Handle turns becoming zero or float
        if value.raw_value == 0 or value.raw_value == "fl":
            self.set_prop_rot_dir(NO_ROT)
        # Set default direction if needed
        elif motion.state.prop_rot_dir == NO_ROT:
            self.set_prop_rot_dir(self._get_default_prop_rot_dir())

        # Sync button states
        self.state.update_state(motion.state.prop_rot_dir, True)

        # Update pictograph and JSON
        self._update_pictograph_and_json()

        # Update header UI
        self.turns_box.header.update_turns_box_header()

    def update_buttons_for_prop_rot_dir(self, prop_rot_dir: str) -> None:
        """Update button UI to reflect the current rotation direction"""
        if prop_rot_dir == NO_ROT:
            # Clear all selections for NO_ROT
            self.state.update_state(CLOCKWISE, False)
            self.turns_box.header.unpress_prop_rot_dir_buttons()
        else:
            # Set the state for the given direction
            self.state.update_state(prop_rot_dir, True)

            # Update header buttons visually
            header = self.turns_box.header
            cw = CLOCKWISE
            ccw = COUNTER_CLOCKWISE

            if prop_rot_dir == cw:
                header.cw_button.set_selected(True)
                header.ccw_button.set_selected(False)
            else:  # COUNTER_CLOCKWISE
                header.cw_button.set_selected(False)
                header.ccw_button.set_selected(True)

            # Ensure buttons are visible
            header.show_prop_rot_dir_buttons()

    def _update_motion_properties(self, direction: str) -> None:
        """Update motion objects with the new rotation direction"""
        # Skip if no valid motion
        if not self.current_motion:
            return

        for pictograph in self._get_affected_pictographs():
            motion = pictograph.managers.get.motion_by_color(self.turns_box.color)

            # Skip if no motion found
            if not motion:
                continue

            # Update motion state
            motion.state.prop_rot_dir = direction
            motion.state.motion_type = self._determine_new_motion_type(motion)

    def _determine_new_motion_type(self, motion: "Motion") -> str:
        """Determine new motion type based on rotation direction change"""
        from data.constants import ANTI, PRO

        # Toggle between ANTI and PRO
        if motion.state.motion_type == ANTI:
            return PRO
        elif motion.state.motion_type == PRO:
            return ANTI

        # For other types, keep as is
        return motion.state.motion_type

    def _update_pictograph_and_json(self) -> None:
        """Update pictograph data and JSON after a change in rotation"""
        if not self.current_motion:
            return

        motion = self.current_motion

        # Get necessary references
        beat_frame = self.turns_box.graph_editor.sequence_workbench.beat_frame
        graph_editor = self.turns_box.graph_editor
        json_manager = graph_editor.main_widget.json_manager

        # Get pictograph index
        pictograph_index = beat_frame.get.index_of_currently_selected_beat()
        json_index = pictograph_index + 2  # JSON stores additional metadata

        from data.constants import MOTION_TYPE, PROP_ROT_DIR, END_ORI, TURNS

        for pictograph in self._get_affected_pictographs():
            # Get motion for this color
            motion = pictograph.managers.get.motion_by_color(self.turns_box.color)

            # Skip if no motion found
            if not motion:
                continue

            # Update pictograph data
            new_dict = {
                MOTION_TYPE: motion.state.motion_type,
                PROP_ROT_DIR: motion.state.prop_rot_dir,
                END_ORI: motion.state.end_ori,
                TURNS: motion.state.turns,
            }

            # Update pictograph
            pictograph.state.pictograph_data[motion.state.color + "_attributes"].update(
                new_dict
            )
            pictograph.managers.updater.update_pictograph(
                pictograph.state.pictograph_data
            )

            # Update JSON
            json_updater = json_manager.updater

            # Update motion type in JSON
            json_updater.motion_type_updater.update_motion_type_in_json(
                json_index, motion.state.color, motion.state.motion_type
            )

            # Update prop rotation direction in JSON
            json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                json_index, motion.state.color, motion.state.prop_rot_dir
            )

        # Update related UI components
        self.turns_box.turns_widget.motion_type_label.update_display(
            motion.state.motion_type
        )

        # Run validation and update UI
        json_manager.ori_validation_engine.run(is_current_sequence=True)
        beat_frame.updater.update_beats_from_current_sequence_json()
        graph_editor.main_widget.sequence_workbench.current_word_label.set_current_word(
            beat_frame.get.current_word()
        )

        # Update the letter
        self.update_pictograph_letter(pictograph)

    def update_pictograph_letter(self, pictograph: "Pictograph") -> None:
        """Update the letter representation after a change in rotation"""
        from data.constants import LETTER

        # Get letter determiner
        letter_determiner = self.turns_box.graph_editor.main_widget.letter_determiner

        # Determine new letter
        new_letter = letter_determiner.determine_letter(
            pictograph.state.pictograph_data, swap_prop_rot_dir=True
        )

        # Skip if no letter determined
        if not new_letter:
            return

        # Get references
        json_manager = (
            self.turns_box.graph_editor.sequence_workbench.main_widget.json_manager
        )
        beat_frame = (
            self.turns_box.graph_editor.sequence_workbench.main_widget.sequence_workbench.beat_frame
        )

        # Update pictograph letter
        pictograph.state.pictograph_data[LETTER] = new_letter.value
        pictograph.state.letter = new_letter
        pictograph.managers.updater.update_pictograph(pictograph.state.pictograph_data)

        # Update letter in JSON
        pictograph_index = beat_frame.get.index_of_currently_selected_beat()
        json_index = pictograph_index + 2
        json_manager.updater.letter_updater.update_letter_in_json_at_index(
            json_index, new_letter.value
        )

    def _get_affected_pictographs(self) -> List["Pictograph"]:
        """Get all pictographs that need to be updated"""
        # Get selected beat
        selected_beat = (
            self.turns_box.graph_editor.sequence_workbench.beat_frame.get.currently_selected_beat_view()
        )

        # Return empty list if no beat selected
        if not selected_beat:
            return []

        # Return both the beat and the graph editor's pictograph
        return [
            selected_beat.beat,
            self.turns_box.graph_editor.pictograph_container.GE_view.pictograph,
        ]

    def _get_default_prop_rot_dir(self) -> str:
        """Get the default rotation direction (clockwise)"""
        default_dir = CLOCKWISE
        self.state.update_state(default_dir, True)
        return default_dir
