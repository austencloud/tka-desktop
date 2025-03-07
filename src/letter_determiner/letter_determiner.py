from typing import TYPE_CHECKING, Optional
from enums.letter.letter import Letter
from data.constants import (
    BLUE,
    BLUE_ATTRS,
    RED,
    RED_ATTRS,
    MOTION_TYPE,
    FLOAT,
    PRO,
    ANTI,
)
from letter_determiner.non_hybrid_letter_determiner import (
    NonHybridShiftLetterDeterminer,
)
from letter_determiner.motion_comparator import MotionComparator
from letter_determiner.prefloat_attribute_updater import PrefloatAttributeUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LetterDeterminer:
    """Determines the correct letter based on pictograph attributes."""

    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.letters = self.main_widget.pictograph_dataset
        self.comparator = MotionComparator(self.main_widget)
        self.prefloat_updater = PrefloatAttributeUpdater(self.main_widget)
        self.non_hybrid_letter_determiner = NonHybridShiftLetterDeterminer(
            self, self.comparator
        )

    def determine_letter(
        self, pictograph_data: dict, swap_prop_rot_dir: bool = False
    ) -> Optional[Letter]:
        """Determine the letter based on pictograph attributes."""
        blue_attrs = pictograph_data[BLUE_ATTRS]
        red_attrs = pictograph_data[RED_ATTRS]

        # Check for dual float case
        if blue_attrs[MOTION_TYPE] == FLOAT and red_attrs[MOTION_TYPE] == FLOAT:
            self.prefloat_updater.update_prefloat_attributes(pictograph_data, BLUE, RED)
            return self._find_matching_letter(blue_attrs, red_attrs)

        # Check for non-hybrid cases
        if blue_attrs[MOTION_TYPE] in [PRO, ANTI] and red_attrs[MOTION_TYPE] == FLOAT:
            return self.non_hybrid_letter_determiner.determine_letter(
                pictograph_data, BLUE, swap_prop_rot_dir
            )
        if red_attrs[MOTION_TYPE] in [PRO, ANTI] and blue_attrs[MOTION_TYPE] == FLOAT:
            return self.non_hybrid_letter_determiner.determine_letter(
                pictograph_data, RED, swap_prop_rot_dir
            )

        # Default case
        return self._find_matching_letter(blue_attrs, red_attrs)

    def _find_matching_letter(
        self, blue_attrs: dict, red_attrs: dict
    ) -> Optional[Letter]:
        """Find the matching letter by comparing attributes to the dataset."""
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_to_example(
                    blue_attrs, red_attrs, example
                ):
                    return letter
        return None
