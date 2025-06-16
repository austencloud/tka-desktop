from typing import TYPE_CHECKING
from data.constants import *
from enums.letter.letter_condition import LetterCondition
from enums.prop_type import PropType

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class PictographChecker:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph

    def ends_with_beta(self) -> bool:

        return (
            self.pictograph.state.letter
            in self.pictograph.state.letter.get_letters_by_condition(
                LetterCondition.BETA_ENDING
            )
        )

    def ends_with_alpha(self) -> bool:
        return (
            self.pictograph.state.letter
            in self.pictograph.state.letter.get_letters_by_condition(
                LetterCondition.ALPHA_ENDING
            )
        )

    def ends_with_gamma(self) -> bool:
        return (
            self.pictograph.state.letter
            in self.pictograph.state.letter.get_letters_by_condition(
                LetterCondition.GAMMA_ENDING
            )
        )

    def ends_with_layer1(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.elements.props[RED],
            self.pictograph.elements.props[BLUE],
        )
        return red_prop.check.is_radial() == blue_prop.check.is_radial()

    def ends_with_layer2(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.elements.props[RED],
            self.pictograph.elements.props[BLUE],
        )
        return red_prop.check.is_nonradial() and blue_prop.check.is_nonradial()

    def ends_with_layer3(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.elements.props[RED],
            self.pictograph.elements.props[BLUE],
        )
        return red_prop.check.is_radial() != blue_prop.check.is_radial()

    def ends_with_non_hybrid_ori(self) -> bool:
        return self.ends_with_layer1() or self.ends_with_layer2()

    def ends_with_in_out_ori(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.elements.props[RED],
            self.pictograph.elements.props[BLUE],
        )
        if red_prop.state.ori == IN and blue_prop.state.ori == OUT:
            return True
        elif red_prop.state.ori == OUT and blue_prop.state.ori == IN:
            return True
        return False

    def ends_with_clock_counter_ori(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.elements.props[RED],
            self.pictograph.elements.props[BLUE],
        )
        return (red_prop.state.ori in [CLOCK] and blue_prop.state.ori in [COUNTER]) or (
            red_prop.state.ori in [COUNTER] and blue_prop.state.ori in [CLOCK]
        )

    def ends_with_radial_ori(self) -> bool:
        return all(
            prop.check.is_radial() for prop in self.pictograph.elements.props.values()
        )

    def ends_with_nonradial_ori(self) -> bool:
        return all(
            prop.check.is_nonradial()
            for prop in self.pictograph.elements.props.values()
        )

    def has_a_dash(self) -> bool:
        for motion in self.pictograph.elements.motion_set.values():
            if motion.state.motion_type == DASH:
                return True
        return False

    def has_a_static_motion(self) -> bool:
        for motion in self.pictograph.elements.motion_set.values():
            if motion.state.motion_type == STATIC:
                return True
        return False

    def is_pictograph_data_complete(self, pictograph_data: dict) -> bool:
        required_keys = [
            LETTER,
            START_POS,
            END_POS,
            TIMING,
            DIRECTION,
            BLUE_ATTRS,
            RED_ATTRS,
        ]
        nested_blue_required_keys = [
            MOTION_TYPE,
            PROP_ROT_DIR,
            START_LOC,
            END_LOC,
            START_ORI,
            TURNS,
        ]
        nested_red_required_keys = nested_blue_required_keys.copy()

        if not all(key in pictograph_data for key in required_keys):
            return False

        for key in nested_blue_required_keys:
            if key not in pictograph_data[BLUE_ATTRS]:
                return False

        for key in nested_red_required_keys:
            if key not in pictograph_data[RED_ATTRS]:
                return False

        return True

    def starts_from_mixed_orientation(self) -> bool:
        if (
            self.pictograph.elements.red_motion.state.start_ori in [CLOCK, COUNTER]
            and self.pictograph.elements.blue_motion.state.start_ori in [OUT, IN]
            or self.pictograph.elements.red_motion.state.start_ori in [OUT, IN]
            and self.pictograph.elements.blue_motion.state.start_ori in [CLOCK, COUNTER]
        ):
            return True
        elif (
            self.pictograph.elements.red_motion.state.start_ori in [CLOCK, COUNTER]
            and self.pictograph.elements.blue_motion.state.start_ori in [CLOCK, COUNTER]
            or self.pictograph.elements.red_motion.state.start_ori in [OUT, IN]
            and self.pictograph.elements.blue_motion.state.start_ori in [OUT, IN]
        ):
            return False

    def ends_in_mixed_orientation(self) -> bool:
        if (
            self.pictograph.elements.red_motion.state.end_ori in [CLOCK, COUNTER]
            and self.pictograph.elements.blue_motion.state.end_ori in [OUT, IN]
            or self.pictograph.elements.red_motion.state.end_ori in [OUT, IN]
            and self.pictograph.elements.blue_motion.state.end_ori in [CLOCK, COUNTER]
        ):
            return True
        elif (
            self.pictograph.elements.red_motion.state.end_ori in [CLOCK, COUNTER]
            and self.pictograph.elements.blue_motion.state.end_ori in [CLOCK, COUNTER]
            or self.pictograph.elements.red_motion.state.end_ori in [OUT, IN]
            and self.pictograph.elements.blue_motion.state.end_ori in [OUT, IN]
        ):
            return False

    def starts_from_standard_orientation(self) -> bool:
        return (
            self.pictograph.elements.red_motion.state.start_ori in [IN, OUT]
            and self.pictograph.elements.blue_motion.state.start_ori in [IN, OUT]
        ) or (
            self.pictograph.elements.red_motion.state.start_ori in [CLOCK, COUNTER]
            and self.pictograph.elements.blue_motion.state.start_ori in [CLOCK, COUNTER]
        )

    def starts_from_radial_orientation(self) -> bool:
        return self.pictograph.elements.red_motion.state.start_ori in [
            IN,
            OUT,
        ] and self.pictograph.elements.blue_motion.state.start_ori in [IN, OUT]

    def starts_from_nonradial_orientation(self) -> bool:
        return self.pictograph.elements.red_motion.state.start_ori in [
            CLOCK,
            COUNTER,
        ] and self.pictograph.elements.blue_motion.state.start_ori in [CLOCK, COUNTER]

    def has_hybrid_motions(self) -> bool:
        return (
            self.pictograph.elements.red_motion.state.motion_type
            != self.pictograph.elements.blue_motion.state.motion_type
        )

    def has_all_props_of_type(self, prop_type: PropType) -> bool:
        return all(
            prop.prop_type_str == prop_type
            for prop in self.pictograph.elements.props.values()
        )

    def has_strict_placed_props(self) -> bool:
        strict_props = [
            PropType.Bigdoublestar,
            PropType.Bighoop,
            PropType.Bigbuugeng,
        ]
        return any(self.has_all_props_of_type(prop_type) for prop_type in strict_props)

    def has_one_float(self) -> bool:
        return any(
            motion.state.motion_type == FLOAT
            for motion in self.pictograph.elements.motion_set.values()
        )

    def has_two_floats(self) -> bool:
        return all(
            motion.state.motion_type == FLOAT
            for motion in self.pictograph.elements.motion_set.values()
        )
