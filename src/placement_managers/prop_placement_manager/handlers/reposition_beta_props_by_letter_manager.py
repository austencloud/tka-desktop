from typing import TYPE_CHECKING
from data.constants import ANTI, PRO
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class RepositionBetaByLetterHandler:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.pictograph = beta_prop_positioner.pictograph
        self.prop_placement_manager = beta_prop_positioner.prop_placement_manager
        self.beta_prop_positioner = beta_prop_positioner
        self.dir_calculator = self.beta_prop_positioner.dir_calculator

    def reposition_G_H(self) -> None:
        further_direction = self.dir_calculator.get_dir(
            self.pictograph.elements.red_motion
        )
        other_direction = self.dir_calculator.get_opposite_dir(further_direction)
        self.move_prop(self.pictograph.elements.red_prop, further_direction)
        self.move_prop(self.pictograph.elements.blue_prop, other_direction)

    def reposition_I(self) -> None:
        pro_prop = (
            self.pictograph.elements.red_prop
            if self.pictograph.elements.red_motion.state.motion_type == PRO
            else self.pictograph.elements.blue_prop
        )
        anti_prop = (
            self.pictograph.elements.red_prop
            if self.pictograph.elements.red_motion.state.motion_type == ANTI
            else self.pictograph.elements.blue_prop
        )
        pro_motion = self.pictograph.elements.motion_set[pro_prop.state.color]
        pro_direction = self.dir_calculator.get_dir(pro_motion)
        anti_direction = self.dir_calculator.get_opposite_dir(pro_direction)
        self.move_prop(pro_prop, pro_direction)
        self.move_prop(anti_prop, anti_direction)

    def reposition_J_K_L(self) -> None:

        red_dir = self.dir_calculator.get_dir(self.pictograph.elements.red_motion)
        blue_dir = self.dir_calculator.get_dir(self.pictograph.elements.blue_motion)

        if red_dir and blue_dir:
            self.move_prop(self.pictograph.elements.red_prop, red_dir)
            self.move_prop(self.pictograph.elements.blue_prop, blue_dir)

    def reposition_Y_Z(self) -> None:

        shift = (
            self.pictograph.elements.red_motion
            if self.pictograph.elements.red_motion.check.is_shift()
            else self.pictograph.elements.blue_motion
        )
        static_motion = (
            self.pictograph.elements.red_motion
            if self.pictograph.elements.red_motion.check.is_static()
            else self.pictograph.elements.blue_motion
        )

        direction = self.dir_calculator.get_dir(shift)
        if direction:
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.elements.props.values()
                    if prop.state.color == shift.state.color
                ),
                direction,
            )
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.elements.props.values()
                    if prop.state.color == static_motion.state.color
                ),
                self.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_Y_dash_Z_dash(self) -> None:
        shift = (
            self.pictograph.elements.red_motion
            if self.pictograph.elements.red_motion.check.is_shift()
            else self.pictograph.elements.blue_motion
        )
        dash = (
            self.pictograph.elements.red_motion
            if self.pictograph.elements.red_motion.check.is_dash()
            else self.pictograph.elements.blue_motion
        )

        direction = self.dir_calculator.get_dir(shift)
        if direction:
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.elements.props.values()
                    if prop.state.color == shift.state.color
                ),
                direction,
            )
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.elements.props.values()
                    if prop.state.color == dash.state.color
                ),
                self.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_psi(self) -> None:
        direction = self.dir_calculator.get_dir_for_non_shift(
            self.pictograph.elements.red_prop
        )
        if direction:
            self.move_prop(self.pictograph.elements.red_prop, direction)
            self.move_prop(
                self.pictograph.elements.blue_prop,
                self.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_psi_dash(self) -> None:
        direction = self.dir_calculator.get_dir_for_non_shift(
            self.pictograph.elements.red_prop
        )
        if direction:
            self.move_prop(self.pictograph.elements.red_prop, direction)
            self.move_prop(
                self.pictograph.elements.blue_prop,
                self.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_beta(self) -> None:
        direction = self.dir_calculator.get_dir_for_non_shift(
            self.pictograph.elements.red_prop
        )
        if direction:
            self.move_prop(self.pictograph.elements.red_prop, direction)
            self.move_prop(
                self.pictograph.elements.blue_prop,
                self.dir_calculator.get_opposite_dir(direction),
            )

    def move_prop(self, prop: Prop, direction: str) -> None:
        offset = self.beta_prop_positioner.beta_offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)
