from typing import TYPE_CHECKING

from data.constants import CLOCK, COUNTER, IN, OUT


if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropChecker:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def is_radial(self) -> bool:
        return self.prop.state.ori in [IN, OUT]

    def is_nonradial(self) -> bool:
        return self.prop.state.ori in [CLOCK, COUNTER]

    def has_out_ori(self) -> bool:
        return self.prop.state.ori == OUT

    def has_in_ori(self) -> bool:
        return self.prop.state.ori == IN

    def has_clock_ori(self) -> bool:
        return self.prop.state.ori == CLOCK

    def has_counter_ori(self) -> bool:
        return self.prop.state.ori == COUNTER
