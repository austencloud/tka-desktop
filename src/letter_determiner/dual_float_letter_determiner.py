from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from .motion_comparator import MotionComparator
from .prefloat_attribute_updater import PrefloatAttributeUpdater

if TYPE_CHECKING:
    from .letter_determiner import LetterDeterminer
    from objects.motion.motion import Motion


class DualFloatLetterDeterminer:
    """Determines the letter for dual float motions."""

    def __init__(self, letter_engine: "LetterDeterminer"):
        self.main_widget = letter_engine.main_widget
        self.letters = letter_engine.letters
        self.prefloat_updater = PrefloatAttributeUpdater(self.main_widget)
        self.comparator = MotionComparator(self.main_widget)

    def determine_letter(self, motion: "Motion") -> Letter:
        """Determine the letter for dual float motions."""
        other_motion = motion.pictograph.managers.get.other_motion(motion)

        # Update pre-float attributes
        self.prefloat_updater.update_prefloat_attributes(motion, other_motion)

        # Find and return the correct letter
        return self._find_matching_letter(motion, other_motion)

    def _find_matching_letter(self, motion: "Motion", other_motion: "Motion") -> Letter:
        """Compare motion attributes to find the correct letter."""
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_to_example(
                    motion, other_motion, example
                ):
                    return letter
        return None
