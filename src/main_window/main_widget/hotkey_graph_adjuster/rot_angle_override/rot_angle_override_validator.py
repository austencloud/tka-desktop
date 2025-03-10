# rot_angle_override_validator.py (modifications)
from typing import TYPE_CHECKING
from data.constants import STATIC, DASH

if TYPE_CHECKING:
    from .rot_angle_override_manager import RotAngleOverrideManager


class RotAngleOverrideValidator:
    """Validates conditions for rotation overrides"""

    def __init__(self, manager: "RotAngleOverrideManager"):
        self.manager = manager
        self.state = manager.state  # Reference to centralized state

    def is_valid_override_condition(self) -> bool:
        selected_arrow = self.state.get_selected_arrow()
        return (
            selected_arrow is not None
            and selected_arrow.motion.state.motion_type in [STATIC, DASH]
        )