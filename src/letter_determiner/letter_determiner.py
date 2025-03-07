from typing import TYPE_CHECKING
from enums.letter.letter import Letter
from data.constants import ANTI, DASH, FLOAT, PRO, STATIC, MOTION_TYPE
from enums.letter.letter_type import LetterType
from .dual_float_letter_determiner import DualFloatLetterDeterminer
from .non_hybrid_letter_determiner import NonHybridShiftLetterDeterminer
from .motion_comparator import MotionComparator
from objects.motion.motion_ori_calculator import MotionOriCalculator

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from objects.motion.motion import Motion


class LetterDeterminer:
    """Determines the correct letter based on motion attributes."""

    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.letters = self.main_widget.pictograph_dataset
        self.non_hybrid_shift_letter_determiner = NonHybridShiftLetterDeterminer(self)
        self.dual_float_letter_determiner = DualFloatLetterDeterminer(self)
        self.comparator = MotionComparator(self.main_widget)
        self.beat_frame = None

    def determine_letter(
        self, motion: "Motion", swap_prop_rot_dir: bool = False
    ) -> Letter:
        """Determine the letter based on motion attributes."""
        if not self.beat_frame:
            self.beat_frame = self.main_widget.sequence_workbench.beat_frame
        other_motion = motion.pictograph.managers.get.other_motion(motion)

        if (
            motion.state.motion_type == FLOAT
            and other_motion.state.motion_type == FLOAT
        ):
            return self.dual_float_letter_determiner.determine_letter(motion)

        elif (
            motion.state.motion_type in [PRO, ANTI]
            and other_motion.state.motion_type == FLOAT
        ):
            return self.non_hybrid_shift_letter_determiner.determine_letter(
                motion, motion.state.motion_type, swap_prop_rot_dir
            )

        elif motion.state.motion_type in [DASH, STATIC]:
            return None  # No letter for dash/static motions

        # Handle swaps in motion types
        if (
            swap_prop_rot_dir
            and other_motion.state.motion_type == FLOAT
            and other_motion.pictograph.state.letter.get_letter_type()
            == LetterType.Type1
        ):
            return self.non_hybrid_shift_letter_determiner.determine_letter(
                motion, motion.state.motion_type, swap_prop_rot_dir
            )

        # Handle non-hybrid letters
        if motion.state.motion_type == FLOAT and other_motion.state.motion_type in [
            PRO,
            ANTI,
        ]:
            return self.non_hybrid_shift_letter_determiner.determine_letter(
                motion, other_motion.state.motion_type, swap_prop_rot_dir
            )

        motion.state.end_ori = MotionOriCalculator(motion).get_end_ori()
        return self.find_letter_based_on_attributes(motion)

    def find_letter_based_on_attributes(self, motion: "Motion") -> Letter:
        """Find the correct letter based on attributes."""
        other_motion = motion.pictograph.managers.get.other_motion(motion)
        letter_type = motion.pictograph.state.letter.get_letter_type()
        original_letter = motion.pictograph.state.letter

        if letter_type == LetterType.Type1:
            return self._find_letter_for_type1(motion, other_motion) or original_letter

        elif letter_type in [LetterType.Type2, LetterType.Type3]:
            return self._find_letter_for_type2_3(motion) or original_letter

        return original_letter

    def _find_letter_for_type1(
        self, motion: "Motion", other_motion: "Motion"
    ) -> Letter:
        """Find a matching letter for Type 1 motion attributes."""
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_to_example(
                    motion, other_motion, example
                ):
                    return letter
        return None

    def _find_letter_for_type2_3(self, motion: "Motion") -> Letter:
        """Find a matching letter for Type 2 & 3 motion attributes."""
        shift = motion.pictograph.managers.get.shift()
        non_shift = motion.pictograph.managers.get.other_motion(shift)

        for letter, examples in self.letters.items():
            for example in examples:
                if self._compare_motion_attributes_for_type2_3(
                    shift, non_shift, example
                ):
                    return letter
        return None

    def _compare_motion_attributes_for_type2_3(
        self, shift: "Motion", non_shift: "Motion", example: dict
    ) -> bool:
        """Compare motion attributes for Type 2 and Type 3 letters."""
        return (
            self.comparator.compare_motion_to_example(shift, example)
            and example[f"{non_shift.state.color}_attributes"][MOTION_TYPE]
            == non_shift.state.motion_type
            and example[f"{non_shift.state.color}_attributes"]["start_loc"]
            == non_shift.state.start_loc
            and example[f"{non_shift.state.color}_attributes"]["end_loc"]
            == non_shift.state.end_loc
        )

