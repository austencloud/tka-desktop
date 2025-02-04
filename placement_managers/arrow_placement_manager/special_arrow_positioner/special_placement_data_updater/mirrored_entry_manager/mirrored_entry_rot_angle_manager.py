import logging
import sys
from typing import Optional
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mirrored_entry_manager import MirroredEntryManager
from data.constants import DASH, STATIC


class MirroredEntryRotAngleManager:
    def __init__(self, manager: "MirroredEntryManager"):
        self.manager = manager

    def update_rotation_angle_in_mirrored_entry(
        self, arrow: Arrow, updated_turn_data: dict
    ) -> None:
        if not self._should_handle_rotation_angle(arrow):
            return

        rot_angle_override = self._check_for_rotation_angle_override(updated_turn_data)
        if rot_angle_override is None:
            return

        ori_key = self.manager.data_updater._generate_ori_key(arrow.motion)
        letter = arrow.pictograph.letter
        other_ori_key, other_letter_data = (
            self.manager.data_prep.get_keys_for_mixed_start_ori(letter, ori_key)
        )

        mirrored_turns_tuple = (
            self.manager.turns_tuple_generator.generate_mirrored_tuple(arrow)
        )

        self._handle_mirrored_rotation_angle_override(
            other_letter_data,
            rot_angle_override,
            mirrored_turns_tuple,
        )

        self.manager.data_updater.update_specific_entry_in_json(
            letter, other_letter_data, other_ori_key
        )

    def remove_rotation_angle_in_mirrored_entry(self, arrow: Arrow, hybrid_key: str):
        letter = arrow.pictograph.letter
        ori_key = self.manager.data_updater._generate_ori_key(arrow.motion)
        other_ori_key, other_letter_data = (
            self.manager.data_prep.get_keys_for_mixed_start_ori(letter, ori_key)
        )
        mirrored_turns_tuple = (
            self.manager.turns_tuple_generator.generate_mirrored_tuple(arrow)
        )

        if hybrid_key in other_letter_data.get(mirrored_turns_tuple, {}):
            del other_letter_data[mirrored_turns_tuple][hybrid_key]

        self.manager.data_updater.update_specific_entry_in_json(
            letter, other_letter_data, other_ori_key
        )

    def _handle_mirrored_rotation_angle_override(
        self, other_letter_data, rotation_angle_override, mirrored_turns_tuple
    ):
        key = self.manager.data_updater.positioner.pictograph.wasd_manager.rotation_angle_override_manager.key_generator.generate_rotation_angle_override_key(
            self.manager.data_updater.positioner.pictograph.main_widget.sequence_widget.graph_editor.selection_manager.selected_arrow
        )
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        other_letter_data[mirrored_turns_tuple][key] = rotation_angle_override

    def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
        return arrow.motion.motion_type in [STATIC, DASH]

    def _check_for_rotation_angle_override(self, turn_data: dict) -> Optional[int]:
        for key in turn_data.keys():
            if "rot_angle_override" in key:
                return turn_data[key]
        return None
