from typing import TYPE_CHECKING
from data.constants import *
from .calculators.float_rot_angle_calculator import FloatRotAngleCalculator
from .calculators.pro_rot_angle_calculator import ProRotAngleCalculator
from .calculators.anti_rot_angle_calculator import AntiRotAngleCalculator
from .calculators.dash_rot_angle_calculator import DashRotAngleCalculator
from .calculators.static_rot_angle_calculator import StaticRotAngleCalculator
from .calculators.base_rot_angle_calculator import BaseRotAngleCalculator

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowRotAngleManager:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow
        self.calculator_class = self._select_calculator_class()

    def _select_calculator_class(self):
        calculator_class_map = {
            PRO: ProRotAngleCalculator,
            ANTI: AntiRotAngleCalculator,
            DASH: DashRotAngleCalculator,
            STATIC: StaticRotAngleCalculator,
            FLOAT: FloatRotAngleCalculator,
        }
        return calculator_class_map.get(self.arrow.motion.state.motion_type)

    def update_rotation(self) -> None:
        self.calculator_class = self._select_calculator_class()
        calculator: BaseRotAngleCalculator = self.calculator_class(self.arrow)
        calculator.apply_rotation()
