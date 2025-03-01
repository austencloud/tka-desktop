from enums.letter.letter import Letter, LetterCondition

from data.constants import CLOCK, COUNTER, IN, NONRADIAL, OUT, RADIAL
from objects.arrow.arrow import Arrow


class PlacementKeyGenerator:
    def _get_motion_end_ori_key(
        self, has_hybrid_orientation: bool, motion_end_ori: str
    ) -> str:
        if has_hybrid_orientation and motion_end_ori in [IN, OUT]:
            return f"{RADIAL}_"
        elif has_hybrid_orientation and motion_end_ori in [CLOCK, COUNTER]:
            return f"{NONRADIAL}_"
        else:
            return ""

    def _get_letter_suffix(self, arrow: Arrow) -> str:
        letter = arrow.pictograph.state.letter
        if not letter:
            return ""

        if letter in letter.get_letters_by_condition(
            LetterCondition.TYPE3
        ) or letter in letter.get_letters_by_condition(LetterCondition.TYPE5):
            return f"_{letter.value[:-1]}_dash"
        else:
            return f"_{letter.value}"

    def _get_key_middle(
        self,
        has_radial_props: bool,
        has_nonradial_props: bool,
        has_hybrid_orientation: bool,
        has_alpha_props: bool,
        has_beta_props: bool,
        has_gamma_props: bool,
    ) -> str:
        if has_radial_props:
            key_middle = "layer1"
        elif has_nonradial_props:
            key_middle = "layer2"
        elif has_hybrid_orientation:
            key_middle = "layer3"
        else:
            return ""

        if has_alpha_props:
            key_middle += "_alpha"
        elif has_beta_props:
            key_middle += "_beta"
        elif has_gamma_props:
            key_middle += "_gamma"
        return key_middle

    def generate_key(self, arrow: Arrow, default_placements: dict) -> str:
        check_manager = arrow.pictograph.managers.check
        has_beta_props = check_manager.ends_with_beta()
        has_alpha_props = check_manager.ends_with_alpha()
        has_gamma_props = check_manager.ends_with_gamma()
        has_hybrid_orientation = check_manager.ends_with_layer3()
        has_radial_props = check_manager.ends_with_radial_ori()
        has_nonradial_props = check_manager.ends_with_nonradial_ori()
        motion_end_ori = arrow.motion.state.end_ori

        key_suffix = "_to_"

        motion_end_ori_key = self._get_motion_end_ori_key(
            has_hybrid_orientation, motion_end_ori
        )

        letter_suffix = self._get_letter_suffix(arrow)

        key_middle = self._get_key_middle(
            has_radial_props,
            has_nonradial_props,
            has_hybrid_orientation,
            has_alpha_props,
            has_beta_props,
            has_gamma_props,
        )

        key = arrow.motion.state.motion_type + (
            key_suffix + motion_end_ori_key + key_middle if key_middle else ""
        )
        key_with_letter = f"{key}{letter_suffix}"

        return self._select_key(
            key_with_letter, key, arrow.motion.state.motion_type, default_placements
        )

    def _select_key(
        self, key_with_letter: str, key: str, motion_type: str, default_placements: dict
    ) -> str:
        if key_with_letter in default_placements:
            return key_with_letter
        elif key in default_placements:
            return key
        else:
            return motion_type
