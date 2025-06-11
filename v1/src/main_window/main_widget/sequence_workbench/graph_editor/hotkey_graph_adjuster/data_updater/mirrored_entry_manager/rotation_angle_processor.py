import logging
from typing import Dict, Any, Optional

from data.constants import DASH, STATIC
from objects.arrow.arrow import Arrow
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import (
    ArrowRotAngleOverrideKeyGenerator,
)

logger = logging.getLogger(__name__)


class RotationAngleProcessor:
    def __init__(self):
        self.key_generator = ArrowRotAngleOverrideKeyGenerator()

    def process_rotation_override(
        self, arrow, original_data, mirrored_data, mirrored_turns_tuple
    ):
        try:
            if not self._should_handle_rotation_angle(arrow):
                return

            rot_angle_override = self._find_rotation_angle_override(original_data)
            if rot_angle_override is None:
                return

            key = self.key_generator.generate_rotation_angle_override_key(arrow)

            if mirrored_turns_tuple not in mirrored_data:
                mirrored_data[mirrored_turns_tuple] = {}

            mirrored_data[mirrored_turns_tuple][key] = rot_angle_override

        except Exception as e:
            logger.error(
                f"Failed to process rotation angle override: {str(e)}", exc_info=True
            )

    def remove_rotation_angle_override(
        self,
        arrow: Arrow,
        mirrored_data: Dict[str, Any],
        mirrored_turns_tuple: str,
        hybrid_key: str,
    ) -> None:
        try:
            if mirrored_turns_tuple in mirrored_data:
                if hybrid_key in mirrored_data[mirrored_turns_tuple]:
                    del mirrored_data[mirrored_turns_tuple][hybrid_key]

                    if not mirrored_data[mirrored_turns_tuple]:
                        del mirrored_data[mirrored_turns_tuple]
        except Exception as e:
            logger.error(
                f"Failed to remove rotation angle override: {str(e)}", exc_info=True
            )

    def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
        return arrow.motion.state.motion_type in [STATIC, DASH]

    def _find_rotation_angle_override(self, data: Dict[str, Any]) -> Optional[Any]:
        for key, value in data.items():
            if "rot_angle_override" in key:
                return value
        return None
