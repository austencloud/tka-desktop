from math import pi
from tkinter import NO
from typing import TYPE_CHECKING, Optional
from enums.letter.letter import Letter

from data.constants import (
    ANTI,
    BLUE,
    BLUE_ATTRS,
    COLOR,
    COUNTER_CLOCKWISE,
    CLOCKWISE,
    DIRECTION,
    FLOAT,
    LETTER,
    NO_ROT,
    OPP,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
    MOTION_TYPE,
)
from letter_determiner.dual_float_letter_determiner import MotionComparator
from letter_determiner.prefloat_attribute_updater import PrefloatAttributeUpdater

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from .letter_determiner import LetterDeterminer


class NonHybridShiftLetterDeterminer:
    """
    This is for when there is one float and one shift,
    ensuring that hybrid letters (like C, F, I, or L) are not used
    when there is one float and one Pro/Anti.
    """

    def __init__(
        self, letter_determiner: "LetterDeterminer", comparator: MotionComparator
    ):
        self.main_widget = letter_determiner.main_widget
        self.letters = letter_determiner.letters
        self.comparator = comparator
        self.prefloat_updater = PrefloatAttributeUpdater(self.main_widget)

    def determine_letter(self, pictograph_data: dict) -> Optional[Letter]:
        """Determine the letter while handling pre-float attributes."""
        blue_attrs, red_attrs = pictograph_data[BLUE_ATTRS], pictograph_data[RED_ATTRS]
        print(pictograph_data[LETTER])
        if blue_attrs[MOTION_TYPE] == FLOAT and red_attrs[MOTION_TYPE] in [PRO, ANTI]:
            self._update_prefloat_attributes(
                pictograph_data, blue_attrs, red_attrs, BLUE
            )
            return self._find_matching_letter(blue_attrs, red_attrs)
        elif red_attrs[MOTION_TYPE] == FLOAT and blue_attrs[MOTION_TYPE] in [PRO, ANTI]:
            self._update_prefloat_attributes(
                pictograph_data, red_attrs, blue_attrs, RED
            )
            return self._find_matching_letter(red_attrs, blue_attrs)
        return None

    def _update_prefloat_attributes(
        self,
        pictograph_data: dict,
        float_attrs: dict,
        non_float_attrs: dict,
        float_color: str,
    ) -> None:
        """Update pre-float attributes in both pictograph data and JSON."""
        non_float_color = RED if float_color == BLUE else BLUE
        json_index = self._get_json_index_for_current_beat()

        float_attrs[PREFLOAT_MOTION_TYPE] = non_float_attrs[MOTION_TYPE]
        self.prefloat_updater.update_json_prefloat_motion_type(
            json_index, float_color, non_float_attrs[MOTION_TYPE]
        )

        if PROP_ROT_DIR in float_attrs or non_float_attrs[MOTION_TYPE] in [PRO, ANTI]:
            prop_rot_dir = self._get_prop_rot_dir(
                float_attrs, non_float_attrs, non_float_color, pictograph_data
            )


            float_attrs[PREFLOAT_PROP_ROT_DIR] = prop_rot_dir
            self.prefloat_updater.update_prefloat_prop_rot_dir_in_json(
                json_index, float_color, prop_rot_dir
            )

    def _find_matching_letter(
        self, float_attrs: dict, shift_attrs: dict
    ) -> Optional[Letter]:
        """Find a matching letter with pre-float aware comparison."""
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_with_prefloat(
                    float_attrs, shift_attrs, example
                ):
                    return letter
        return None

    def _get_json_index_for_current_beat(self) -> int:
        """Calculate the JSON index for the currently selected beat."""
        return (
            self.main_widget.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
            + 2
        )

    def _get_opposite_rotation_direction(self, rotation_direction: str) -> str:
        """Return the opposite prop rotation direction."""
        # return COUNTER_CLOCKWISE if rotation_direction == CLOCKWISE else CLOCKWISE
        if rotation_direction == CLOCKWISE:
            return COUNTER_CLOCKWISE
        elif rotation_direction == COUNTER_CLOCKWISE:
            return CLOCKWISE
        else:
            raise ValueError(f"Invalid rotation direction: {rotation_direction}")

    def _get_prop_rot_dir(
        self,
        float_attrs: dict,
        non_float_attrs: dict,
        non_float_color: str,
        pictograph_data,
    ) -> str:
        """Retrieve the prop rotation direction from JSON."""
        prop_rot_dir = float_attrs[PROP_ROT_DIR]

        if prop_rot_dir == NO_ROT:
            prefloat_prop_rot_dir = float_attrs.get(PREFLOAT_PROP_ROT_DIR)
            if prefloat_prop_rot_dir:
                prop_rot_dir = self._get_opposite_rotation_direction(prefloat_prop_rot_dir)
            else:
                raise ValueError(
                    f"Prop Rot Dir not found in {non_float_color} attributes"
                )

        elif pictograph_data.get(DIRECTION) == OPP:
            prop_rot_dir = self._get_opposite_rotation_direction(prop_rot_dir)

        elif non_float_attrs[MOTION_TYPE] in [PRO, ANTI]:
            prop_rot_dir = non_float_attrs.get(PROP_ROT_DIR)
            if not prop_rot_dir:
                raise ValueError(
                    f"Prop Rot Dir not found in {non_float_color} attributes"
                )
            if pictograph_data.get(DIRECTION) == OPP:
                prop_rot_dir = self._get_opposite_rotation_direction(prop_rot_dir)
        return prop_rot_dir
