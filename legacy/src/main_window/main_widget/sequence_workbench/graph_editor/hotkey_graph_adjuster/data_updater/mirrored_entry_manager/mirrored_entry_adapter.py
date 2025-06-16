import logging
from typing import TYPE_CHECKING, Optional

from data.constants import DASH, STATIC
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.rotation_angle_override_key_generator import ArrowRotAngleOverrideKeyGenerator
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
from objects.arrow.arrow import Arrow
from src.legacy_settings_manager.global_settings.app_context import AppContext

from .mirrored_entry_factory import MirroredEntryFactory
from .mirrored_entry_utils import MirroredEntryUtils

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.data_updater.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )


class MirroredEntryAdapter:
    """Adapter for integrating the new mirrored entry system with existing code."""

    def __init__(self, data_updater):
        """Initialize the adapter with the given data updater."""
        self.data_updater = data_updater
        self.utils = MirroredEntryUtils()
        self.factory = MirroredEntryFactory

    def update_mirrored_entry_in_json(self) -> None:
        """Update the mirrored entry in JSON."""
        selected_arrow = AppContext.get_selected_arrow()
        if not selected_arrow:
            logger.warning("No arrow selected, cannot update mirrored entry")
            return

        try:
            if MirroredEntryUtils.is_new_entry_needed(selected_arrow):
                self._create_new_entry(selected_arrow)
            else:
                self._update_existing_entry(selected_arrow)

            AppContext.special_placement_loader().reload()
        except Exception as e:
            logger.error(
                f"Failed to update mirrored entry in JSON: {str(e)}", exc_info=True
            )

    def _create_new_entry(self, arrow: Arrow) -> None:
        """Create a new mirrored entry for the given arrow."""
        service = self.factory.create_service(self.data_updater)
        service.update_mirrored_entry(arrow)

    def _update_existing_entry(self, arrow: Arrow) -> None:
        """Update an existing mirrored entry for the given arrow."""
        service = self.factory.create_service(self.data_updater)
        service.update_mirrored_entry(arrow)

    def rot_angle_manager(self):
        """Get a rotation angle processor for compatibility with old code."""
        data_updater = self.data_updater

        class RotationAngleManagerAdapter:
            def __init__(self):
                self.data_updater: "SpecialPlacementDataUpdater" = data_updater
                self.turns_tuple_generator = TurnsTupleGenerator()

            def update_rotation_angle_in_mirrored_entry(
                self, arrow: Arrow, updated_turn_data: dict
            ) -> None:
                if not self._should_handle_rotation_angle(arrow):
                    return

                rot_angle_override = self._check_for_rotation_angle_override(
                    updated_turn_data
                )
                if rot_angle_override is None:
                    return

                ori_key = (
                    self.data_updater.ori_key_generator.generate_ori_key_from_motion(
                        arrow.motion
                    )
                )
                letter = arrow.pictograph.state.letter
                grid_mode = arrow.pictograph.state.grid_mode

                # Use MirroredEntryUtils directly to match original behavior
                other_ori_key, other_letter_data = (
                    MirroredEntryUtils.get_keys_for_mixed_start_ori(
                        grid_mode, letter, ori_key
                    )
                )

                mirrored_turns_tuple = (
                    self.turns_tuple_generator.generate_mirrored_tuple(arrow)
                )

                # Handle the override exactly as in the original
                self._handle_mirrored_rotation_angle_override(
                    other_letter_data,
                    rot_angle_override,
                    mirrored_turns_tuple,
                )

                # Save the data using the data updater
                self.data_updater.update_specific_entry_in_json(
                    letter, other_letter_data, other_ori_key
                )

            def remove_rotation_angle_in_mirrored_entry(
                self, arrow: Arrow, hybrid_key: str
            ):
                letter = arrow.pictograph.state.letter
                ori_key = (
                    self.data_updater.ori_key_generator.generate_ori_key_from_motion(
                        arrow.motion
                    )
                )
                grid_mode = arrow.pictograph.state.grid_mode

                # Use MirroredEntryUtils directly to match original behavior
                other_ori_key, other_letter_data = (
                    MirroredEntryUtils.get_keys_for_mixed_start_ori(
                        grid_mode, letter, ori_key
                    )
                )

                mirrored_turns_tuple = (
                    self.turns_tuple_generator.generate_mirrored_tuple(arrow)
                )

                # Exactly match original deletion logic
                if (
                    mirrored_turns_tuple in other_letter_data
                    and hybrid_key in other_letter_data[mirrored_turns_tuple]
                ):
                    del other_letter_data[mirrored_turns_tuple][hybrid_key]

                # Save the updated data
                self.data_updater.update_specific_entry_in_json(
                    letter, other_letter_data, other_ori_key
                )

            def _handle_mirrored_rotation_angle_override(
                self, other_letter_data, rotation_angle_override, mirrored_turns_tuple
            ):
                key = ArrowRotAngleOverrideKeyGenerator().generate_rotation_angle_override_key(
                    AppContext.get_selected_arrow()
                )
                if mirrored_turns_tuple not in other_letter_data:
                    other_letter_data[mirrored_turns_tuple] = {}
                other_letter_data[mirrored_turns_tuple][key] = rotation_angle_override

            def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
                return arrow.motion.state.motion_type in [STATIC, DASH]

            def _check_for_rotation_angle_override(
                self, turn_data: dict
            ) -> Optional[int]:
                for key in turn_data.keys():
                    if "rot_angle_override" in key:
                        return turn_data[key]
                return None

        return RotationAngleManagerAdapter()
