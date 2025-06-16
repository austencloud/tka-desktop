import logging
from PyQt6.QtCore import QPointF
from enums.letter.letter import Letter

from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Optional

from placement_managers.arrow_placement_manager.directional_tuple_generator import (
    DirectionalTupleGenerator,
)


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
            # logger.warning(
            #     f"Arrow '{arrow}' has no assigned letter. Defaulting to (0, 0)."
            # )
            return QPointF(0, 0)

        adjustment = self._calculate_adjustment(arrow)
        return adjustment

    def _calculate_adjustment(self, arrow: Arrow) -> QPointF:
        """Calculates the adjustment based on special placements or defaults."""

        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(
            self.placement_manager.pictograph
        )
        ori_key = self.placement_manager.data_updater.ori_key_generator.generate_ori_key_from_motion(
            arrow.motion
        )

        special_placements = self._get_special_placements(arrow, ori_key)

        special_adjustment = self.get_adjustment_for_letter(
            special_placements,
            self.placement_manager.pictograph.state.letter,
            arrow,
            turns_tuple,
        )

        if special_adjustment:
            x, y = special_adjustment
        else:
            default_adjustment = (
                self.placement_manager.default_strategy.get_default_adjustment(arrow)
            )

            # ✅ Fix: Extract x() and y() instead of unpacking
            x, y = default_adjustment.x(), default_adjustment.y()

        directional_adjustments = self._get_directional_adjustments(arrow, x, y)
        quadrant_index = (
            self.placement_manager.quadrant_index_handler.get_quadrant_index(arrow)
        )

        final_adjustment = self._get_final_adjustment(
            arrow, directional_adjustments, quadrant_index
        )

        return final_adjustment

    def _get_special_placements(self, arrow: Arrow, ori_key: str) -> dict:
        """Loads and prepares special placements for the current grid mode and letter."""

        special_placements_all_modes = (
            self.special_placement_loader.load_or_return_special_placements()
        )
        special_placements_for_current_grid_mode = special_placements_all_modes.get(
            arrow.pictograph.state.grid_mode, {}
        ).get(ori_key, {})

        if (
            self.placement_manager.pictograph.state.letter.value
            not in special_placements_for_current_grid_mode
        ):
            special_placements_for_current_grid_mode[
                self.placement_manager.pictograph.state.letter
            ] = {}

        return special_placements_for_current_grid_mode

    def _get_directional_adjustments(self, arrow: Arrow, x: float, y: float) -> list:
        """Generates directional adjustments for the arrow."""

        directional_tuple_manager = DirectionalTupleGenerator(arrow.motion)
        directional_adjustments = directional_tuple_manager.get_directional_tuples(x, y)

        if not directional_adjustments:
            logger.error(
                f"Directional adjustments not found for motion type: {arrow.motion.state.motion_type}"
            )
            return [(0, 0)] * 4

        return directional_adjustments

    def _get_final_adjustment(
        self, arrow: Arrow, directional_adjustments: list, quadrant_index: int
    ) -> QPointF:
        """Returns the final QPointF adjustment based on directional adjustments and quadrant index."""

        if directional_adjustments is None:
            return QPointF(0, 0)

        if quadrant_index < 0 or quadrant_index >= len(directional_adjustments):
            logger.error(
                f"Quadrant index {quadrant_index} out of range for directional_adjustments with length {len(directional_adjustments)}."
            )
            return QPointF(*directional_adjustments[-1])  # Use the last available tuple

        return QPointF(*directional_adjustments[quadrant_index])

    def get_adjustment_for_letter(
        self,
        special_placements: dict[str, dict[str, dict[str, dict]]],
        letter: Letter,
        arrow: Arrow,
        turns_tuple: str,
    ) -> Optional[tuple[int, int]]:

        letter_adjustments: dict[str, dict[str, list]] = special_placements.get(
            letter.value, {}
        ).get(turns_tuple, {})

        key = self.placement_manager.special_strategy.attr_key_generator.get_key_from_arrow(
            arrow
        )

        return letter_adjustments.get(key, None)
