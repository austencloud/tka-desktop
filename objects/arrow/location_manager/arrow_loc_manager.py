from typing import TYPE_CHECKING
from .loc_calculators.base_loc_calculator import BaseLocationCalculator
from .loc_calculators.dash_loc_calculator import DashLocationCalculator
from .loc_calculators.shift_loc_calculator import ShiftLocationCalculator
from .loc_calculators.static_loc_calculator import StaticLocationCalculator
from data.constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowLocationManager:
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow

    def _select_calculator(self) -> "BaseLocationCalculator":
        calculator_map = {
            PRO: ShiftLocationCalculator,
            ANTI: ShiftLocationCalculator,
            FLOAT: ShiftLocationCalculator,
            DASH: DashLocationCalculator,
            STATIC: StaticLocationCalculator,
        }
        calculator_class = calculator_map.get(
            self.arrow.motion.state.motion_type, BaseLocationCalculator
        )
        return calculator_class(self.arrow)

    def update_location(self) -> None:
        self.calculator = self._select_calculator()
        calculated_location = self.calculator.calculate_location()
        self.arrow.loc = calculated_location
