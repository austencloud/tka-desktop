from typing import TYPE_CHECKING
from .calculators.base_location_calculator import BaseLocationCalculator
from .calculators.dash_location_calculator import DashLocationCalculator
from .calculators.shift_location_calculator import ShiftLocationCalculator
from .calculators.static_location_calculator import StaticLocationCalculator
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

    def update_location(self, location: str = None) -> None:
        self.calculator = self._select_calculator()
        if location:
            self.arrow.state.loc = location
        else:
            calculated_location = self.calculator.calculate_location()
            self.arrow.state.loc = calculated_location
