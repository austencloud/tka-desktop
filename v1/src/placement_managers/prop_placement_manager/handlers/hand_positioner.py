from typing import TYPE_CHECKING
from data.constants import LEFT, RIGHT
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from placement_managers.prop_placement_manager.handlers.beta_prop_positioner import (
        BetaPropPositioner,
    )


class HandPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.pictograph = beta_prop_positioner.pictograph

    def reposition_beta_hands(self) -> None:
        red_hand = self.pictograph.elements.red_prop
        blue_hand = self.pictograph.elements.blue_prop
        self.move_hand(red_hand, RIGHT)
        self.move_hand(blue_hand, LEFT)

    def move_hand(self, prop: Prop, direction: str) -> None:
        offset_calculator = self.beta_prop_positioner.beta_offset_calculator
        offset = offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)
