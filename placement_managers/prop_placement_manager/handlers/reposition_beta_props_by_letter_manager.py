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
        further_direction = self.dir_calculator.get_dir(self.pictograph.red_motion)
        other_direction = self.dir_calculator.get_opposite_dir(further_direction)
        self.move_prop(self.pictograph.red_prop, further_direction)
        self.move_prop(self.pictograph.blue_prop, other_direction)

    def reposition_I(self) -> None:
        pro_prop = (
            self.pictograph.red_prop
            if self.pictograph.red_motion.motion_type == PRO
            else self.pictograph.blue_prop
        )
        anti_prop = (
            self.pictograph.red_prop
            if self.pictograph.red_motion.motion_type == ANTI
            else self.pictograph.blue_prop
        )
        pro_motion = self.pictograph.motions[pro_prop.color]
        pro_direction = self.dir_calculator.get_dir(pro_motion)
        anti_direction = self.dir_calculator.get_opposite_dir(pro_direction)
        self.move_prop(pro_prop, pro_direction)
        self.move_prop(anti_prop, anti_direction)

    def reposition_J_K_L(self) -> None:

        red_dir = self.dir_calculator.get_dir(self.pictograph.red_motion)
        blue_dir = self.dir_calculator.get_dir(self.pictograph.blue_motion)

        if red_dir and blue_dir:
            self.move_prop(self.pictograph.red_prop, red_dir)
            self.move_prop(self.pictograph.blue_prop, blue_dir)

    def reposition_Y_Z(self) -> None:

        shift = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.check.is_shift()
            else self.pictograph.blue_motion
        )
        static_motion = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.check.is_static()
            else self.pictograph.blue_motion
        )

        direction = self.dir_calculator.get_dir(shift)
        if direction:
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.props.values()
                    if prop.color == shift.color
                ),
                direction,
            )
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.props.values()
                    if prop.color == static_motion.color
                ),
                self.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_Y_dash_Z_dash(self) -> None:
        shift = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.check.is_shift()
            else self.pictograph.blue_motion
        )
        dash = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.check.is_dash()
            else self.pictograph.blue_motion
        )

        direction = self.dir_calculator.get_dir(shift)
        if direction:
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.props.values()
                    if prop.color == shift.color
                ),
                direction,
            )
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.props.values()
                    if prop.color == dash.color
                ),
                self.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_Ψ(self) -> None:
        direction = self.dir_calculator.get_dir_for_non_shift(self.pictograph.red_prop)
        if direction:
            self.move_prop(self.pictograph.red_prop, direction)
            self.move_prop(
                self.pictograph.blue_prop,
                self.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_Ψ_dash(self) -> None:
        direction = self.dir_calculator.get_dir_for_non_shift(self.pictograph.red_prop)
        if direction:
            self.move_prop(self.pictograph.red_prop, direction)
            self.move_prop(
                self.pictograph.blue_prop,
                self.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_β(self) -> None:
        direction = self.dir_calculator.get_dir_for_non_shift(self.pictograph.red_prop)
        if direction:
            self.move_prop(self.pictograph.red_prop, direction)
            self.move_prop(
                self.pictograph.blue_prop,
                self.dir_calculator.get_opposite_dir(direction),
            )

    def move_prop(self, prop: Prop, direction: str) -> None:
        offset = self.beta_prop_positioner.beta_offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)
