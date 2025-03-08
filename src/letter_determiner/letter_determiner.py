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
from letter_determiner.non_hybrid_shift_letter_determiner import (
    NonHybridShiftLetterDeterminer,
)
from letter_determiner.motion_comparator import MotionComparator
from letter_determiner.prefloat_attribute_updater import PrefloatAttributeUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LetterDeterminer:
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
        blue_attrs = pictograph_data[BLUE_ATTRS]
        red_attrs = pictograph_data[RED_ATTRS]

        if self._is_dual_float_case(blue_attrs, red_attrs):
            letter = self._handle_dual_float_case(pictograph_data)
        else:
            letter = self._handle_hybrid_case(pictograph_data, swap_prop_rot_dir)

        # if letter == None:
        #     raise ValueError("Letter not found")

        return letter

    def _is_dual_float_case(self, blue: dict, red: dict) -> bool:
        return blue[MOTION_TYPE] == FLOAT and red[MOTION_TYPE] == FLOAT

    def _handle_dual_float_case(self, pictograph_data: dict) -> Optional[Letter]:
        self.prefloat_updater.update_prefloat_attributes(pictograph_data, BLUE, RED)
        blue_attrs = pictograph_data[BLUE_ATTRS]
        red_attrs = pictograph_data[RED_ATTRS]
        return self._find_matching_letter(blue_attrs, red_attrs)

    def _handle_hybrid_case(
        self, pictograph_data: dict, swap_prop_rot_dir: bool
    ) -> Optional[Letter]:
        blue_attrs = pictograph_data[BLUE_ATTRS]
        red_attrs = pictograph_data[RED_ATTRS]

        if (
            blue_attrs[MOTION_TYPE] in [PRO, ANTI] and red_attrs[MOTION_TYPE] == FLOAT
        ) or (
            red_attrs[MOTION_TYPE] in [PRO, ANTI] and blue_attrs[MOTION_TYPE] == FLOAT
        ):

            return self.non_hybrid_letter_determiner.determine_letter(pictograph_data)
        return self._find_matching_letter(blue_attrs, red_attrs)

    def _find_matching_letter(
        self, blue_attrs: dict, red_attrs: dict
    ) -> Optional[Letter]:
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_to_example(
                    blue_attrs, red_attrs, example
                ):
                    return letter
        return None
