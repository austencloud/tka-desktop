from typing import TYPE_CHECKING
from data.constants import ANTI, DASH, FLOAT, PRO, STATIC
from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from .arrow_placement_manager import ArrowPlacementManager
    from base_widgets.pictograph.pictograph import Pictograph


class ArrowInitialPosCalculator:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.pictograph: "Pictograph" = placement_manager.pictograph

    def get_initial_coords(self, arrow: Arrow) -> QPointF:
        if arrow.motion.motion_type in [PRO, ANTI, FLOAT]:
            return self._get_shift_coords(arrow)
        elif arrow.motion.motion_type in [STATIC, DASH]:
            return self._get_static_dash_coords(arrow)

    def _get_shift_coords(self, arrow: Arrow) -> QPointF:
        """
        Retrieves the coordinates for a given layer2 point name.
        """
        point_name = f"{arrow.loc}_{arrow.pictograph.state.grid_mode}_layer2_point"
        coord = self.pictograph.elements.grid.grid_data.get_shift_coord(point_name)
        if coord:
            return coord
        else:
            return QPointF(0, 0)

    def _get_static_dash_coords(self, arrow: Arrow) -> QPointF:
        """
        Retrieves the coordinates for a given static point name.
        """
        point_name = f"{arrow.loc}_{arrow.pictograph.state.grid_mode}_hand_point"
        coord = self.pictograph.elements.grid.grid_data.get_static_dash_coord(
            point_name
        )
        if coord:
            return coord
        else:
            return QPointF(0, 0)  # Example default
