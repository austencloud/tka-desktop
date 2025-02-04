from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from Enums.letters import LetterConditions
from data.constants import *

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographChecker:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph

    def ends_with_beta(self) -> bool:

        return (
            self.pictograph.letter
            in self.pictograph.letter.get_letters_by_condition(
                LetterConditions.BETA_ENDING
            )
        )

    def ends_with_alpha(self) -> bool:
        return (
            self.pictograph.letter
            in self.pictograph.letter.get_letters_by_condition(
                LetterConditions.ALPHA_ENDING
            )
        )

    def ends_with_gamma(self) -> bool:
        return (
            self.pictograph.letter
            in self.pictograph.letter.get_letters_by_condition(
                LetterConditions.GAMMA_ENDING
            )
        )

    def ends_with_layer1(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[RED],
            self.pictograph.props[BLUE],
        )
        return red_prop.check.is_radial() == blue_prop.check.is_radial()

    def ends_with_layer2(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[RED],
            self.pictograph.props[BLUE],
        )
        return red_prop.check.is_nonradial() and blue_prop.check.is_nonradial()

    def ends_with_layer3(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[RED],
            self.pictograph.props[BLUE],
        )
        return red_prop.check.is_radial() != blue_prop.check.is_radial()

    def ends_with_non_hybrid_ori(self) -> bool:
        return self.ends_with_layer1() or self.ends_with_layer2()

    def ends_with_in_out_ori(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[RED],
            self.pictograph.props[BLUE],
        )
        if red_prop.ori == IN and blue_prop.ori == OUT:
            return True
        elif red_prop.ori == OUT and blue_prop.ori == IN:
            return True
        return False

    def ends_with_clock_counter_ori(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[RED],
            self.pictograph.props[BLUE],
        )
        return (red_prop.ori in [CLOCK] and blue_prop.ori in [COUNTER]) or (
            red_prop.ori in [COUNTER] and blue_prop.ori in [CLOCK]
        )

    def ends_with_radial_ori(self) -> bool:
        return all(prop.check.is_radial() for prop in self.pictograph.props.values())

    def ends_with_nonradial_ori(self) -> bool:
        return all(prop.check.is_nonradial() for prop in self.pictograph.props.values())

    def has_a_dash(self) -> bool:
        for motion in self.pictograph.motions.values():
            if motion.motion_type == DASH:
                return True
        return False

    def has_a_static_motion(self) -> bool:
        for motion in self.pictograph.motions.values():
            if motion.motion_type == STATIC:
                return True
        return False

    def is_pictograph_dict_complete(self, pictograph_dict: dict) -> bool:
        required_keys = [
            "letter",
            "start_pos",
            "end_pos",
            "timing",
            "direction",
            "blue_attributes",
            "red_attributes",
        ]
        nested_blue_required_keys = [
            "motion_type",
            "prop_rot_dir",
            "start_loc",
            "end_loc",
            "start_ori",
            "turns",
        ]
        nested_red_required_keys = nested_blue_required_keys.copy()

        if not all(key in pictograph_dict for key in required_keys):
            return False

        for key in nested_blue_required_keys:
            if key not in pictograph_dict["blue_attributes"]:
                return False

        for key in nested_red_required_keys:
            if key not in pictograph_dict["red_attributes"]:
                return False

        return True

    def starts_from_mixed_orientation(self) -> bool:
        if (
            self.pictograph.red_motion.start_ori in [CLOCK, COUNTER]
            and self.pictograph.blue_motion.start_ori in [OUT, IN]
            or self.pictograph.red_motion.start_ori in [OUT, IN]
            and self.pictograph.blue_motion.start_ori in [CLOCK, COUNTER]
        ):
            return True
        elif (
            self.pictograph.red_motion.start_ori in [CLOCK, COUNTER]
            and self.pictograph.blue_motion.start_ori in [CLOCK, COUNTER]
            or self.pictograph.red_motion.start_ori in [OUT, IN]
            and self.pictograph.blue_motion.start_ori in [OUT, IN]
        ):
            return False

    def ends_in_mixed_orientation(self) -> bool:
        if (
            self.pictograph.red_motion.end_ori in [CLOCK, COUNTER]
            and self.pictograph.blue_motion.end_ori in [OUT, IN]
            or self.pictograph.red_motion.end_ori in [OUT, IN]
            and self.pictograph.blue_motion.end_ori in [CLOCK, COUNTER]
        ):
            return True
        elif (
            self.pictograph.red_motion.end_ori in [CLOCK, COUNTER]
            and self.pictograph.blue_motion.end_ori in [CLOCK, COUNTER]
            or self.pictograph.red_motion.end_ori in [OUT, IN]
            and self.pictograph.blue_motion.end_ori in [OUT, IN]
        ):
            return False

    def starts_from_standard_orientation(self) -> bool:
        return (
            self.pictograph.red_motion.start_ori in [IN, OUT]
            and self.pictograph.blue_motion.start_ori in [IN, OUT]
        ) or (
            self.pictograph.red_motion.start_ori in [CLOCK, COUNTER]
            and self.pictograph.blue_motion.start_ori in [CLOCK, COUNTER]
        )

    def starts_from_radial_orientation(self) -> bool:
        return self.pictograph.red_motion.start_ori in [
            IN,
            OUT,
        ] and self.pictograph.blue_motion.start_ori in [IN, OUT]

    def starts_from_nonradial_orientation(self) -> bool:
        return self.pictograph.red_motion.start_ori in [
            CLOCK,
            COUNTER,
        ] and self.pictograph.blue_motion.start_ori in [CLOCK, COUNTER]

    def has_hybrid_motions(self) -> bool:
        return (
            self.pictograph.red_motion.motion_type
            != self.pictograph.blue_motion.motion_type
        )



    def has_all_props_of_type(self, prop_type: PropType) -> bool:
        return all(
            prop.prop_type == prop_type for prop in self.pictograph.props.values()
        )

    def has_strictly_placed_props(self) -> bool:
        strict_props = [
            PropType.Bigdoublestar,
            PropType.Bighoop,
            PropType.Bigbuugeng,
        ]
        return any(self.has_all_props_of_type(prop_type) for prop_type in strict_props)

    def has_one_float(self) -> bool:
        return any(
            motion.motion_type == FLOAT for motion in self.pictograph.motions.values()
        )

    def has_two_floats(self) -> bool:
        return all(
            motion.motion_type == FLOAT for motion in self.pictograph.motions.values()
        )
