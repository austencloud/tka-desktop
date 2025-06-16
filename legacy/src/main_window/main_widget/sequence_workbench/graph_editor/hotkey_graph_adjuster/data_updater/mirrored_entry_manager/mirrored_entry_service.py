"""
Core functionality for managing mirrored entries in special placements.
"""

import logging
from typing import TYPE_CHECKING, Any
from data.constants import BLUE, IN, OUT, RED

from enums.letter.letter import Letter
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from objects.arrow.arrow import Arrow
from src.legacy_settings_manager.global_settings.app_context import AppContext

from .orientation_handler import OrientationHandler
from .turns_pattern_manager import TurnsPatternManager
from .special_placement_repository import SpecialPlacementRepository
from .rotation_angle_processor import RotationAngleProcessor

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.data_updater.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )


class MirroredEntryService:
    """Service for managing mirrored entries in special placements."""

    def __init__(self, data_updater: "SpecialPlacementDataUpdater") -> None:
        """Initialize with required dependencies."""
        self.data_updater = data_updater
        self.turns_manager = TurnsPatternManager()
        self.repository = SpecialPlacementRepository(data_updater.getter.grid_mode())
        self.rotation_processor = RotationAngleProcessor()
        self.orientation_handler = None

    def update_mirrored_entry(self, arrow: Arrow) -> None:
        """Update mirrored entry for the given arrow."""
        logger.debug(f"Updating mirrored entry for arrow: {arrow.state.color}")

        try:
            self.orientation_handler = OrientationHandler(arrow, self.turns_manager)
            letter = arrow.pictograph.state.letter
            ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_motion(
                arrow.motion
            )
            letter_data = self._load_letter_data(letter, ori_key)

            if self.orientation_handler.is_mixed_orientation():
                self._process_mixed_orientation_entry(
                    arrow, letter, ori_key, letter_data
                )
            else:
                self._process_standard_orientation_entry(
                    arrow, letter, ori_key, letter_data
                )

            AppContext.special_placement_loader().reload()

        except Exception as e:
            logger.error(f"Failed to update mirrored entry: {str(e)}", exc_info=True)
            raise

    def _load_letter_data(self, letter: Letter, ori_key: str) -> dict[str, Any]:
        """Load letter data for the given orientation key."""
        return self.repository.get_letter_data(letter, ori_key)

    def _process_mixed_orientation_entry(
        self, arrow: "Arrow", letter, ori_key, letter_data: dict[str, Any]
    ):
        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(arrow.pictograph)
        mirrored_tuple = TurnsTupleGenerator().generate_mirrored_tuple(arrow)
        mirror_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        mirror_letter_data = self.repository.get_letter_data(letter, mirror_ori_key)
        attribute_key = self.orientation_handler.get_mixed_attribute_key()
        if attribute_key in [RED, BLUE]:
            other_attribute_key = self.orientation_handler.get_other_attr_key(
                attribute_key
            )
        else:
            other_attribute_key = attribute_key
        if turns_tuple not in letter_data:
            letter_data[turns_tuple] = {}
        if attribute_key not in letter_data[turns_tuple]:
            letter_data[turns_tuple][attribute_key] = {}

        if mirrored_tuple not in mirror_letter_data:
            mirror_letter_data[mirrored_tuple] = {}

        mirror_letter_data[mirrored_tuple][attribute_key] = letter_data[
            turns_tuple
        ].get(other_attribute_key, {})

        self.rotation_processor.process_rotation_override(
            arrow, letter_data.get(turns_tuple, {}), mirror_letter_data, mirrored_tuple
        )

        self.data_updater.update_specific_entry_in_json(
            letter, mirror_letter_data, mirror_ori_key
        )

    def _process_standard_orientation_entry(
        self,
        arrow: Arrow,
        letter: Letter,
        ori_key: str,
        letter_data: dict[str, dict[str, Any]],
    ) -> None:
        """Process a standard orientation entry."""
        if (
            letter.value in ["S", "T", "β"]
            or letter in self.orientation_handler.get_hybrid_letters()
        ):
            return

        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(arrow.pictograph)
        mirrored_tuple = TurnsTupleGenerator().generate_mirrored_tuple(arrow)
        other_arrow = arrow.pictograph.managers.get.other_arrow(arrow)
        should_mirror = self.orientation_handler.should_create_standard_mirror(
            other_arrow
        )

        if not should_mirror:
            return

        attribute_key = self.orientation_handler.get_standard_attribute_key(other_arrow)
        source_data = letter_data.get(turns_tuple, {}).get(arrow.state.color, {})

        if mirrored_tuple not in letter_data:
            letter_data[mirrored_tuple] = {}

        letter_data[mirrored_tuple][attribute_key] = source_data

        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)
