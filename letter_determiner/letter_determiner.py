from typing import TYPE_CHECKING
from Enums.letters import Letter, LetterConditions, LetterType
from data.constants import ANTI, COUNTER_CLOCKWISE, DASH, FLOAT, PRO, CLOCKWISE, STATIC
from .dual_float_letter_determiner import DualFloatLetterDeterminer
from .non_hybrid_letter_determiner import NonHybridShiftLetterDeterminer
from objects.motion.motion_ori_calculator import MotionOriCalculator
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LetterDeterminer:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.letters = self.main_widget.pictograph_dataset
        self.non_hybrid_shift_letter_determiner = NonHybridShiftLetterDeterminer(self)
        self.dual_float_letter_determiner = DualFloatLetterDeterminer(self)
        self.beat_frame = None

    def determine_letter(
        self, motion: "Motion", swap_prop_rot_dir: bool = False
    ) -> Letter:
        """Update the motion attributes based on the change in prop_rot_dir."""
        if not self.beat_frame:
            self.beat_frame = self.main_widget.sequence_workbench.sequence_beat_frame
        other_motion = motion.pictograph.managers.get.other_motion(motion)
        motion_type = motion.state.motion_type

        if motion_type == FLOAT and other_motion.state.motion_type == FLOAT:
            return self.dual_float_letter_determiner.determine_letter(motion)
        elif motion_type in [PRO, ANTI] and other_motion.state.motion_type == FLOAT:
            return self.non_hybrid_shift_letter_determiner.determine_letter(
                motion, motion.state.motion_type, swap_prop_rot_dir
            )
        elif motion_type in [DASH, STATIC]:
            new_motion_type = motion_type
        if (
            swap_prop_rot_dir
            and other_motion.state.motion_type == FLOAT
            and other_motion.pictograph.state.letter.get_letter_type()
            == LetterType.Type1
        ):
            return self.non_hybrid_shift_letter_determiner.determine_letter(
                motion, new_motion_type, swap_prop_rot_dir
            )
        if motion.state.motion_type == FLOAT and other_motion.state.motion_type in [
            PRO,
            ANTI,
        ]:
            return self.non_hybrid_shift_letter_determiner.determine_letter(
                motion, other_motion.state.motion_type, swap_prop_rot_dir
            )
        motion.state.end_ori = MotionOriCalculator(motion).get_end_ori()

        new_letter = self.find_letter_based_on_attributes(motion)
        return new_letter

    def find_letter_based_on_attributes(self, motion: "Motion") -> str:
        other_motion = motion.pictograph.managers.get.other_motion(motion)
        letter_type = motion.pictograph.state.letter.get_letter_type()
        original_letter = motion.pictograph.state.letter
        for letter, examples in self.letters.items():

            if letter_type == LetterType.Type1:
                for example in examples:
                    if self.compare_motion_attributes_for_type1(
                        motion, other_motion, example
                    ):
                        return letter
            elif letter_type in [LetterType.Type2, LetterType.Type3]:
                for example in examples:
                    if self.compare_motion_attributes_for_type2_3(motion, example):
                        return letter
            else:
                return original_letter
        return None

    def compare_motion_attributes_for_type1(
        self, motion: "Motion", other_motion: "Motion", example
    ):
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(motion, example)
            and example[f"{motion.state.color}_attributes"]["start_loc"]
            == motion.state.start_loc
            and example[f"{motion.state.color}_attributes"]["end_loc"]
            == motion.state.end_loc
            and self._is_shift_prop_rot_dir_matching(motion, example)
            and self.is_shift_motion_type_matching(other_motion, example)
            and example[f"{other_motion.state.color}_attributes"]["start_loc"]
            == other_motion.state.start_loc
            and example[f"{other_motion.state.color}_attributes"]["end_loc"]
            == other_motion.state.end_loc
            and self._is_shift_prop_rot_dir_matching(other_motion, example)
        )

        return motion_attributes_match_example

    def _is_shift_prop_rot_dir_matching(self, motion: "Motion", example):
        is_rot_dir_matching = (
            example[f"{motion.state.color}_attributes"]["prop_rot_dir"]
            == self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                self.beat_frame.get.index_of_currently_selected_beat() + 2,
                motion.state.color,
            )
            or example[f"{motion.state.color}_attributes"]["prop_rot_dir"]
            == motion.state.prop_rot_dir
        )

        return is_rot_dir_matching

    def compare_motion_attributes_for_type1_hybrids_with_one_float(
        self, motion: "Motion", example
    ):
        float_motion = motion.pictograph.managers.get.float_motion()
        non_float_motion = float_motion.pictograph.managers.get.other_motion(
            float_motion
        )
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(float_motion, example)
            and example[f"{float_motion.state.color}_attributes"]["start_loc"]
            == float_motion.state.start_loc
            and example[f"{float_motion.state.color}_attributes"]["end_loc"]
            == float_motion.state.end_loc
            and example[f"{float_motion.state.color}_attributes"]["prop_rot_dir"]
            == self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                self.beat_frame.get.index_of_currently_selected_beat() + 2,
                float_motion.state.color,
            )
            and self.is_shift_motion_type_matching(non_float_motion, example)
            and example[f"{non_float_motion.state.color}_attributes"]["start_loc"]
            == non_float_motion.state.start_loc
            and example[f"{non_float_motion.state.color}_attributes"]["end_loc"]
            == non_float_motion.state.end_loc
            and example[f"{non_float_motion.state.color}_attributes"]["prop_rot_dir"]
            == non_float_motion.state.prop_rot_dir
        )

        return motion_attributes_match_example

    def compare_motion_attributes_for_type1_nonhybrids_with_one_float(
        self, float_motion: "Motion", example
    ):
        non_float_motion = float_motion.pictograph.managers.get.other_motion(
            float_motion
        )
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(float_motion, example)
            and example[f"{float_motion.state.color}_attributes"]["start_loc"]
            == float_motion.state.start_loc
            and example[f"{float_motion.state.color}_attributes"]["end_loc"]
            == float_motion.state.end_loc
            and example[f"{float_motion.state.color}_attributes"]["prop_rot_dir"]
            == self.main_widget.json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                self.beat_frame.get.index_of_currently_selected_beat() + 2,
                float_motion.state.color,
            )
            and self.is_shift_motion_type_matching(non_float_motion, example)
            and example[f"{non_float_motion.state.color}_attributes"]["start_loc"]
            == non_float_motion.state.start_loc
            and example[f"{non_float_motion.state.color}_attributes"]["end_loc"]
            == non_float_motion.state.end_loc
            and example[f"{non_float_motion.state.color}_attributes"]["prop_rot_dir"]
            == non_float_motion.state.prop_rot_dir
        )

        return motion_attributes_match_example

    def compare_motion_attributes_for_type2_3(self, motion: "Motion", example):
        shift = motion.pictograph.managers.get.shift()
        non_shift = motion.pictograph.managers.get.other_motion(shift)
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(shift, example)
            and example[f"{shift.state.color}_attributes"]["start_loc"]
            == shift.state.start_loc
            and example[f"{shift.state.color}_attributes"]["end_loc"] == shift.end_loc
            and self._is_shift_prop_rot_dir_matching(shift, example)
            and example[f"{non_shift.state.color}_attributes"]["motion_type"]
            == non_shift.state.motion_type
            and example[f"{non_shift.state.color}_attributes"]["start_loc"]
            == non_shift.state.start_loc
            and example[f"{non_shift.state.color}_attributes"]["end_loc"]
            == non_shift.state.end_loc
        )

        return motion_attributes_match_example

    def is_shift_motion_type_matching(self, motion: "Motion", example):
        is_matching_motion_type = (
            example[f"{motion.state.color}_attributes"]["motion_type"]
            == motion.state.motion_type
            or example[f"{motion.state.color}_attributes"]["motion_type"]
            == motion.state.prefloat_motion_type
        )

        return is_matching_motion_type
