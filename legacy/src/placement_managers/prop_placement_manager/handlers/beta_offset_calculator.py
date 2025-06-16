from enums.prop_type import PropType
from data.constants import (
    LEFT,
    RIGHT,
    UP,
    DOWN,
    DOWNRIGHT,
    UPLEFT,
    DOWNLEFT,
    UPRIGHT,
)
from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING

from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.prop_placement_override_manager import (
        PropPlacementOverrideManager,
    )
    from placement_managers.prop_placement_manager.handlers.beta_prop_positioner import (
        BetaPropPositioner,
    )

_large_offset = 60
_medium_offset = 50
_small_offset = 45


class BetaOffsetCalculator:
    def __init__(self, override_manager: "PropPlacementOverrideManager") -> None:
        self.position_offsets_cache: dict[PropType, dict[tuple[str, str], QPointF]] = {}
        self.beta_positioner = override_manager

    def calculate_new_position_with_offset(
        self, current_position: QPointF, direction: str
    ) -> QPointF:
        prop_type_map = {
            PropType.Club: _large_offset,
            PropType.Eightrings: _large_offset,
            PropType.BigEightRings: _large_offset,
            PropType.Doublestar: _medium_offset,
            PropType.Bigdoublestar: _medium_offset,
        }
        prop_type = AppContext.settings_manager().global_settings.get_prop_type()
        self.beta_offset = 950 / prop_type_map.get(prop_type, _small_offset)

        diagonal_offset = self.beta_offset / (
            2**0.5
        )  # Suspect: Is this halving too much?

        offset_map = {
            LEFT: QPointF(-self.beta_offset, 0),
            RIGHT: QPointF(self.beta_offset, 0),
            UP: QPointF(0, -self.beta_offset),
            DOWN: QPointF(0, self.beta_offset),
            DOWNRIGHT: QPointF(diagonal_offset, diagonal_offset),
            UPLEFT: QPointF(-diagonal_offset, -diagonal_offset),
            DOWNLEFT: QPointF(-diagonal_offset, diagonal_offset),
            UPRIGHT: QPointF(diagonal_offset, -diagonal_offset),
        }

        offset = offset_map.get(direction, QPointF(0, 0))
        return current_position + offset
