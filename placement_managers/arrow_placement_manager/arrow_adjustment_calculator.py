import logging
import re
from PyQt6.QtCore import QPointF
from Enums.letters import Letter
from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Optional

from .directional_tuple_manager.directional_tuple_manager import DirectionalTupleManager

if TYPE_CHECKING:
    from .arrow_placement_manager import ArrowPlacementManager
logger = logging.getLogger(__name__)


class ArrowAdjustmentCalculator:
    def __init__(
        self,
        placement_manager: "ArrowPlacementManager",
        special_placement_loader: "SpecialPlacementLoader",
    ) -> None:
        self.placement_manager = placement_manager
        self.special_placement_loader = special_placement_loader

    def get_adjustment(self, arrow: Arrow) -> QPointF:
        """Calculates the adjustment for an arrow based on special placements, motion type, and grid mode."""

        if not arrow.motion.pictograph.state.letter:
            logger.warning(
                f"Arrow '{arrow}' has no assigned letter. Defaulting to (0, 0)."
            )
            return QPointF(0, 0)

        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(
            self.placement_manager.pictograph
        )
        ori_key = (
            self.placement_manager.special_positioner.data_updater._generate_ori_key(
                arrow.motion
            )
        )

        special_placements = (
            self.special_placement_loader.load_special_placements().get(ori_key, {})
        )

        if self.placement_manager.pictograph.state.letter not in special_placements:
            logger.warning(
                f"No special placements found for letter {self.placement_manager.pictograph.state.letter}. Using fallback."
            )
            special_placements[self.placement_manager.pictograph.state.letter] = {}

        special_adjustment = self.get_adjustment_for_letter(
            self.placement_manager.pictograph.state.letter, arrow, turns_tuple, ori_key
        )

        if special_adjustment:
            logger.info(f"Using special adjustment for {arrow}: {special_adjustment}")
            x, y = special_adjustment
        else:
            x, y = self.placement_manager.default_positioner.get_default_adjustment(
                arrow
            )
            logger.info(f"Using default adjustment for {arrow}: {x, y}")

        # Ensure directional tuples are correct
        directional_tuple_manager = DirectionalTupleManager(arrow.motion)
        directional_adjustments = directional_tuple_manager.generate_directional_tuples(
            x, y
        )

        if not directional_adjustments:
            logger.error(
                f"Directional adjustments not found for motion type: {arrow.motion.motion_type}"
            )
            return QPointF(0, 0)

        quadrant_index = (
            self.placement_manager.quadrant_index_handler.get_quadrant_index(arrow)
        )

        if quadrant_index < 0 or quadrant_index >= len(directional_adjustments):
            logger.error(
                f"Quadrant index {quadrant_index} out of range for directional_adjustments with length {len(directional_adjustments)}."
            )
            return QPointF(0, 0)  # Return a default value or handle appropriately

        return QPointF(*directional_adjustments[quadrant_index])

    def _find_special_rotation(self, turn_data: dict) -> Optional[dict]:
        for key, value in turn_data.items():
            if re.match(r"^(cw|ccw)_static$", key):
                return value
        return None

    def get_adjustment_for_letter(
        self, letter: Letter, arrow: Arrow, turns_tuple: str, ori_key: str
    ) -> Optional[tuple[int, int]]:
        self.special_placements: dict[str, dict] = (
            self.special_placement_loader.load_special_placements()
            .get(arrow.pictograph.state.grid_mode)
            .get(ori_key, {})
        )
        letter_adjustments: dict[str, dict[str, list]] = self.special_placements.get(
            letter.value, {}
        ).get(turns_tuple, {})

        key = self.placement_manager.special_positioner.attr_key_generator.get_key(
            arrow
        )

        return letter_adjustments.get(key if isinstance(key, str) else key.value)
