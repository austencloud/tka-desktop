from PyQt6.QtCore import QPointF
from data.constants import ANTI, DASH, FLOAT, PRO, STATIC
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class InitialPlacementStrategy:
    def __init__(self, pictograph: "LegacyPictograph"):
        self.pictograph = pictograph

    def compute_initial_position(self, arrow: Arrow) -> QPointF:
        """Determines the initial position of an arrow based on motion type and pictograph data."""
        motion_type = arrow.motion.state.motion_type

        if motion_type in [PRO, ANTI, FLOAT]:
            return self._get_shift_coords(arrow)
        elif motion_type in [STATIC, DASH]:
            return self._get_static_dash_coords(arrow)
        return QPointF(0, 0)

    def _get_shift_coords(self, arrow: Arrow) -> QPointF:
        """Retrieves shift coordinates from the pictograph."""
        point_name = f"{arrow.state.loc}_{self.pictograph.state.grid_mode}_layer2_point"
        coord = self.pictograph.elements.grid.grid_data.get_shift_coord(point_name)
        return coord if coord else QPointF(0, 0)

    def _get_static_dash_coords(self, arrow: Arrow) -> QPointF:
        """Retrieves static/dash coordinates from the pictograph."""
        point_name = f"{arrow.state.loc}_{self.pictograph.state.grid_mode}_hand_point"
        coord = self.pictograph.elements.grid.grid_data.get_static_dash_coord(
            point_name
        )
        return coord if coord else QPointF(0, 0)
