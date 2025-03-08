# services/json_handler.py
from typing import TYPE_CHECKING, Protocol, Optional
from ..models.motion import MotionType, RotationDirection

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager


class LetterDeterminationJsonHandler:
    def __init__(self, json_manager: "JsonManager"):
        self.loader_saver = json_manager.loader_saver
        self.updater = json_manager.updater

    def get_json_prefloat_prop_rot_dir(
        self, index: int, color: str
    ) -> RotationDirection:
        return RotationDirection(
            self.loader_saver.get_json_prefloat_prop_rot_dir(index, color)
        )

    def get_json_prefloat_motion_type(self, index: int, color: str) -> MotionType:
        stored_value = self.loader_saver.get_json_prefloat_motion_type(index, color)
        if stored_value is None:
            raise ValueError("Invalid motion type value")
        return MotionType(stored_value)

    def update_prefloat_motion_type(self, index: int, color: str, motion_type):
        """Update JSON with prefloat motion type."""
        if isinstance(motion_type, str):
            motion_type = MotionType(motion_type)  # ✅ Convert string back to Enum
        self.updater.motion_type_updater.update_json_prefloat_motion_type(
            index, color, motion_type.value
        )

    def update_prefloat_prop_rot_dir(
        self, index: int, color: str, direction: RotationDirection
    ):
        """Update JSON with prefloat rotation direction."""

        # 🔥 Convert string to Enum if necessary
        if isinstance(direction, str):
            try:
                direction = RotationDirection(direction)  # Convert string to Enum
            except ValueError:
                raise ValueError(f"Invalid RotationDirection: {direction}")

        self.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            index, color, direction.value  # ✅ Now guaranteed to be an Enum
        )

    def save_beat(self, index: int, data: dict):
        self.loader_saver.save_current_sequence(
            self._update_sequence_with_data(index, data)
        )

    def _update_sequence_with_data(self, index: int, new_data: dict) -> list[dict]:
        current = self.loader_saver.load_current_sequence()
        current[index] = new_data
        return current

    def update_prefloat_rotation(
        self, index: int, color: str, rotation: RotationDirection
    ):
        self.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            index, color, rotation.value
        )
