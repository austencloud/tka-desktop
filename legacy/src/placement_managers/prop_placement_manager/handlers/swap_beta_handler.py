from typing import TYPE_CHECKING
from enums.letter.letter_type import LetterType

from enums.prop_type import PropType
from enums.letter.letter import Letter

from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from src.legacy_settings_manager.global_settings.app_context import AppContext
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class SwapBetaHandler:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.pictograph = beta_prop_positioner.pictograph
        self.ppm = beta_prop_positioner.prop_placement_manager
        self.blue_prop = self.pictograph.elements.blue_prop
        self.red_prop = self.pictograph.elements.red_prop
        self.dir_calculator = self.beta_prop_positioner.dir_calculator
        self.swap_handlers = {
            LetterType.Type1: self._handle_type1_swap,
            LetterType.Type2: self._handle_type2_swap,
            LetterType.Type3: self._handle_type3_swap,
            LetterType.Type4: self._handle_type4_swap,
            LetterType.Type5: self._handle_type5_swap,
            LetterType.Type6: self._handle_type6_swap,
        }

    def _swap_props(
        self, prop_a: Prop, prop_b: Prop, direction_a: str, direction_b: str
    ) -> None:
        """Yes, this DOES have to be called twice for each prop to swap them. It's complicated."""
        self.beta_prop_positioner.move_prop(prop_a, direction_a)
        self.beta_prop_positioner.move_prop(prop_a, direction_a)
        self.beta_prop_positioner.move_prop(prop_b, direction_b)
        self.beta_prop_positioner.move_prop(prop_b, direction_b)

    def swap_beta(self) -> None:
        if (
            (
                self.pictograph.managers.check.ends_with_in_out_ori()
                or self.pictograph.managers.check.ends_with_clock_counter_ori()
            )
            and len(self.beta_prop_positioner.classifier.small_uni) == 2
        ) or self.pictograph.managers.check.ends_with_layer3():
            return
        if self.pictograph.elements.red_motion.prop.prop_type_str == PropType.Hand:
            return

        letter_type = LetterType.get_letter_type(self.pictograph.state.letter)
        swap_handler = self.swap_handlers.get(letter_type)
        if swap_handler:
            swap_handler()

    def _handle_type1_swap(self) -> None:
        if self.pictograph.state.letter in [Letter.G, Letter.H]:
            further_direction = self.dir_calculator.get_dir(
                self.pictograph.elements.red_motion
            )
            other_direction = self.dir_calculator.get_opposite_dir(further_direction)

            self._swap_props(
                self.pictograph.elements.red_prop,
                self.pictograph.elements.blue_prop,
                other_direction,
                further_direction,
            )

        else:
            red_direction = self.dir_calculator.get_dir(
                self.pictograph.elements.red_motion
            )
            blue_direction = self.dir_calculator.get_dir(
                self.pictograph.elements.blue_motion
            )

            self._swap_props(
                self.pictograph.elements.red_prop,
                self.pictograph.elements.blue_prop,
                blue_direction,
                red_direction,
            )

    def _handle_type6_swap(self) -> None:

        red_direction = self.dir_calculator.get_dir(self.pictograph.elements.red_motion)
        blue_direction = self.dir_calculator.get_dir(
            self.pictograph.elements.blue_motion
        )
        if self.pictograph.elements.red_motion.prop.prop_type_str != "Hand":
            self._swap_props(
                self.pictograph.elements.red_prop,
                self.pictograph.elements.blue_prop,
                blue_direction,
                red_direction,
            )

    def _handle_type2_swap(self) -> None:
        shift = self.pictograph.managers.get.shift()
        static = self.pictograph.managers.get.static()

        shift_direction = self.dir_calculator.get_dir(shift)
        static_direction = self.dir_calculator.get_opposite_dir(shift_direction)

        self._swap_props(shift.prop, static.prop, static_direction, shift_direction)

    def _handle_type3_swap(self) -> None:
        shift = self.pictograph.managers.get.shift()
        dash = self.pictograph.managers.get.dash()

        direction = self.dir_calculator.get_dir(shift)

        if direction:
            self._swap_props(
                self.pictograph.elements.props[shift.state.color],
                self.pictograph.elements.props[dash.state.color],
                self.dir_calculator.get_opposite_dir(direction),
                direction,
            )

    def _handle_type4_swap(self) -> None:
        dash = self.pictograph.managers.get.dash()
        static = self.pictograph.managers.get.static()

        dash_direction = self.dir_calculator.get_dir(dash)
        static_direction = self.dir_calculator.get_opposite_dir(dash_direction)
        self._swap_props(dash.prop, static.prop, static_direction, dash_direction)

    def _handle_type5_swap(self) -> None:
        red_direction = self.dir_calculator.get_dir(self.pictograph.elements.red_motion)
        blue_direction = self.dir_calculator.get_dir(
            self.pictograph.elements.blue_motion
        )

        self._swap_props(
            self.pictograph.elements.red_prop,
            self.pictograph.elements.blue_prop,
            blue_direction,
            red_direction,
        )

    def _generate_override_key(self, prop_loc, beta_ori) -> str:
        return (
            f"swap_beta_{prop_loc}_{beta_ori}_"
            f"blue_{self.blue_prop.motion.state.motion_type}_{self.blue_prop.motion.arrow.state.loc}_"
            f"red_{self.red_prop.motion.state.motion_type}_{self.red_prop.motion.arrow.state.loc}"
        )

    def swap_beta_if_needed(self) -> None:
        ori_key = self.pictograph.managers.arrow_placement_manager.data_updater.ori_key_generator.generate_ori_key_from_motion(
            self.pictograph.elements.blue_motion
        )
        grid_mode = self.pictograph.state.grid_mode
        if ori_key:
            letter_data: dict = (
                AppContext.special_placement_loader()
                .load_or_return_special_placements()[grid_mode][ori_key]
                .get(self.pictograph.state.letter.value)
            )

            turns_tuple = TurnsTupleGenerator().generate_turns_tuple(self.pictograph)
            prop_loc = self.pictograph.elements.blue_prop.state.loc
            if self.pictograph.managers.check.ends_with_radial_ori():
                beta_ori = "radial"
            elif self.pictograph.managers.check.ends_with_nonradial_ori():
                beta_ori = "nonradial"
            else:
                return
            override_key = self._generate_override_key(prop_loc, beta_ori)
            if letter_data:
                turn_data: dict = letter_data.get(turns_tuple, {})
                if beta_ori:
                    if turn_data.get(override_key):
                        self.swap_beta()
