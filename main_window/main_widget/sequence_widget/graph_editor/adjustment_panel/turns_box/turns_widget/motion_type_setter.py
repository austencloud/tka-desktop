from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from .turns_widget import TurnsWidget


class MotionTypeSetter:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget

    def set_motion_type(self, motion: "Motion", motion_type: str) -> None:
        """Set the motion type and update the pictograph."""
        if motion.motion_type == motion_type:
            return  # No change needed

        # Update the motion type
        motion.motion_type = motion_type
        # self.turns_widget.turns_updater.set_motion_turns(motion, motion.turns)
 
        # Update the motion type buttons in the UI
        self.turns_widget.motion_type_label.update_motion_type_label(motion_type)
