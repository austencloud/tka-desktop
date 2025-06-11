# services/json_handler.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager


class LetterDeterminationJsonHandler:
    def __init__(self, json_manager: "JsonManager"):
        if json_manager is None:
            # Handle the case where json_manager is None (fallback scenario)
            self.loader_saver = None
            self.updater = None
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "LetterDeterminationJsonHandler initialized with None json_manager"
            )
        else:
            self.loader_saver = json_manager.loader_saver
            self.updater = json_manager.updater

    def get_json_prefloat_prop_rot_dir(self, index: int, color: str) -> str:
        if self.loader_saver is None:
            return "clockwise"  # Default fallback value
        return str(self.loader_saver.get_json_prefloat_prop_rot_dir(index, color))

    def get_json_prefloat_motion_type(self, index: int, color: str) -> str:
        if self.loader_saver is None:
            return "pro"  # Default fallback value
        stored_value = self.loader_saver.get_json_prefloat_motion_type(index, color)
        if stored_value is None:
            raise ValueError("Invalid motion type value")
        return str(stored_value)

    def update_prefloat_motion_type(self, index: int, color: str, motion_type: str):
        """Update JSON with prefloat motion type."""
        if self.updater is None:
            return  # Silently ignore if updater is not available
        self.updater.motion_type_updater.update_prefloat_motion_type_in_json(
            index, color, motion_type
        )

    def update_prefloat_prop_rot_dir(self, index: int, color: str, prop_rot_dir: str):
        """Update JSON with prefloat rotation direction."""
        if self.updater is None:
            return  # Silently ignore if updater is not available
        self.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            index, color, prop_rot_dir  # ✅ Now guaranteed to be an Enum
        )

    def save_beat(self, index: int, data: dict):
        if self.loader_saver is None:
            return  # Silently ignore if loader_saver is not available
        self.loader_saver.save_current_sequence(
            self._update_sequence_with_data(index, data)
        )

    def _update_sequence_with_data(self, index: int, new_data: dict) -> list[dict]:
        if self.loader_saver is None:
            return []  # Return empty list if loader_saver is not available
        current = self.loader_saver.load_current_sequence()
        current[index] = new_data
        return current

    def update_prefloat_rotation(self, index: int, color: str, rotation: str):
        if self.updater is None:
            return  # Silently ignore if updater is not available
        self.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            index, color, rotation.value
        )
