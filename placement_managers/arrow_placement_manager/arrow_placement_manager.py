from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

from .arrow_adjustment_calculator import ArrowAdjustmentCalculator
from .arrow_initial_pos_calculator import ArrowInitialPosCalculator
from .quadrant_index_handler import QuadrantIndexHandler
from .special_arrow_positioner.special_arrow_positioner import SpecialArrowPositioner
from .default_arrow_positioner import DefaultArrowPositioner

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class ArrowPlacementManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

        # Positioners
        self.default_positioner = DefaultArrowPositioner(self)
        self.special_positioner = SpecialArrowPositioner(self)

        self.initial_pos_calculator = ArrowInitialPosCalculator(self)
        self.adjustment_calculator = ArrowAdjustmentCalculator(self)
        self.quadrant_index_handler = QuadrantIndexHandler(self)

    def update_arrow_placements(self) -> None:
        if self.pictograph.letter:
            for arrow in self.pictograph.arrows.values():
                self.update_arrow_position(arrow)

    def update_arrow_position(self, arrow: Arrow) -> None:
        initial_pos = self.initial_pos_calculator.get_initial_coords(arrow)
        adjustment = self.adjustment_calculator.get_adjustment(arrow)
        new_pos = initial_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)
        arrow.rot_angle_manager.update_rotation()
