# === turns_box/managers/turns_adjustment_manager.py ===
from typing import TYPE_CHECKING, Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal

from ..domain.turns_value import TurnsValue

if TYPE_CHECKING:
    from ..ui.turns_widget import TurnsWidget
    from objects.motion.motion import Motion
    from .prop_rot_dir_manager import PropRotDirManager


class TurnsAdjustmentManager(QObject):
    """Manager for handling turns value adjustments"""

    turns_changed = pyqtSignal(TurnsValue)

    def __init__(self, turns_widget: "TurnsWidget", color: str):
        super().__init__()
        self.turns_widget = turns_widget
        self.color = color
        self.current_value = TurnsValue(0)
        self.current_motion: Optional["Motion"] = None
        self.prop_rot_dir_manager: Optional["PropRotDirManager"] = None
        self._prefloat_motion_type: Optional[str] = None

    def connect_prop_rot_dir_manager(self, manager: "PropRotDirManager") -> None:
        """Connect to a prop rotation direction manager"""
        self.prop_rot_dir_manager = manager

    def set_current_motion(self, motion: "Motion") -> None:
        """Set the current motion and update the turns value"""
        self.current_motion = motion
        turns_value = TurnsValue(motion.state.turns)
        self.current_value = turns_value

        # Store motion type for float handling
        from data.constants import FLOAT

        if turns_value.is_float:
            self._prefloat_motion_type = None
        elif motion.state.motion_type != FLOAT:
            self._prefloat_motion_type = motion.state.motion_type

        # Update UI
        self.turns_widget.display_frame.update_turns_display(
            motion, turns_value.display_text
        )

        # Notify prop rotation manager
        if self.prop_rot_dir_manager:
            self.prop_rot_dir_manager.update_for_turns_change(turns_value)

    def adjust(self, amount: float) -> None:
        """Adjust turns by the given amount"""
        # Skip if no motion
        if not self.current_motion:
            return

        # Get old and new value
        old_value = self.current_value

        # Handle float case
        if old_value.is_float:
            # Can't adjust from float state
            return

        # Calculate new value
        new_value = old_value.add(amount)

        # Apply limits
        if new_value.raw_value < 0:
            new_value = TurnsValue(0)
        elif new_value.raw_value > 3:
            new_value = TurnsValue(3)

        # Skip if no change
        if new_value == old_value:
            return

        # Update current value
        self.current_value = new_value

        # Update motion
        self._update_motion_turns(new_value)

        # Update UI
        self.turns_widget.display_frame.update_turns_display(
            self.current_motion, new_value.display_text
        )

        # Notify prop rotation manager
        if self.prop_rot_dir_manager:
            self.prop_rot_dir_manager.update_for_turns_change(new_value)

        # Emit change signal
        self.turns_changed.emit(new_value)

    def direct_set(self, value: TurnsValue) -> None:
        """Directly set turns to a specific value"""
        # Skip if no motion
        if not self.current_motion:
            return

        # Skip if no change
        if value == self.current_value:
            return

        # Store old motion type when setting to float
        from data.constants import FLOAT

        if value.is_float and not self.current_value.is_float:
            self._prefloat_motion_type = self.current_motion.state.motion_type

        # Update current value
        self.current_value = value

        # Update motion
        self._update_motion_turns(value)

        # Update UI
        self.turns_widget.display_frame.update_turns_display(
            self.current_motion, value.display_text
        )

        # Notify prop rotation manager
        if self.prop_rot_dir_manager:
            self.prop_rot_dir_manager.update_for_turns_change(value)

        # Emit change signal
        self.turns_changed.emit(value)

    def _update_motion_turns(self, value: TurnsValue) -> None:
        """Update the motion with new turns value"""
        # Skip if no motion
        if not self.current_motion:
            return

        motion = self.current_motion

        # Update turns value
        motion.state.turns = value.raw_value

        # Handle special float case
        from data.constants import FLOAT

        if value.is_float:
            # Save current motion type
            if motion.state.motion_type != FLOAT:
                self._prefloat_motion_type = motion.state.motion_type
            # Set to FLOAT type
            motion.state.motion_type = FLOAT
        elif motion.state.motion_type == FLOAT and self._prefloat_motion_type:
            # Restore previous motion type
            motion.state.motion_type = self._prefloat_motion_type

        # Update JSON and pictograph
        self._update_json_and_pictograph()

    def _update_json_and_pictograph(self) -> None:
        """Update JSON and pictograph with current motion state"""
        # Skip if no motion
        if not self.current_motion:
            return

        motion = self.current_motion

        # Get references
        beat_frame = (
            self.turns_widget.turns_box.graph_editor.sequence_workbench.beat_frame
        )
        json_manager = self.turns_widget.turns_box.graph_editor.main_widget.json_manager

        # Get pictograph index
        pictograph_index = beat_frame.get.index_of_currently_selected_beat()
        json_index = pictograph_index + 2

        # Update JSON
        json_updater = json_manager.updater

        # Update turns in JSON
        json_updater.turns_updater.update_turns_in_json(
            json_index, motion.state.color, motion.state.turns
        )

        # Update motion type in JSON
        json_updater.motion_type_updater.update_motion_type_in_json(
            json_index, motion.state.color, motion.state.motion_type
        )

        # Update beats
        beat_frame.updater.update_beats_from_current_sequence_json()

    def _get_beat_index(self) -> Optional[int]:
        """Get the index of the current beat"""
        try:
            return (
                self.turns_widget.turns_box.graph_editor.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
            )
        except (AttributeError, ValueError):
            return None
