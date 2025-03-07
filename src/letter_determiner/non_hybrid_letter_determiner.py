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
    OPP,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
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
    It ensures that we don't use hybrid letters (like C, F, I, or L)
    to describe letters that have one float and one Pro/Anti.
    """

    def __init__(
        self, letter_determiner: "LetterDeterminer", comparator: MotionComparator
    ):
        self.main_widget = letter_determiner.main_widget
        self.letters = letter_determiner.letters
        self.comparator = comparator  # Use the passed comparator
        self.prefloat_updater = PrefloatAttributeUpdater(self.main_widget)

    def determine_letter(
        self, pictograph_data: dict, color: str, swap_prop_rot_dir: bool = False
    ) -> Optional[Letter]:
        """Determine letter while handling pre-float attributes."""
        blue_attrs = pictograph_data[BLUE_ATTRS]
        red_attrs = pictograph_data[RED_ATTRS]

        # Update pre-float attributes before comparison
        if blue_attrs[MOTION_TYPE] == FLOAT and red_attrs[MOTION_TYPE] in [PRO, ANTI]:
            self._update_prefloat_attributes(pictograph_data, BLUE, RED)
            return self._find_matching_letter(blue_attrs, red_attrs)
        elif red_attrs[MOTION_TYPE] == FLOAT and blue_attrs[MOTION_TYPE] in [PRO, ANTI]:
            self._update_prefloat_attributes(pictograph_data, RED, BLUE)
            return self._find_matching_letter(red_attrs, blue_attrs)
        return None

    def _update_prefloat_attributes(
        self, pictograph_data: dict, float_color: str, non_float_color: str
    ) -> None:
        """Update pre-float attributes in both pictograph data and JSON."""
        json_index = self._get_json_index_for_current_beat()
        non_float_attrs = pictograph_data[f"{non_float_color}_attributes"]
        float_attrs = pictograph_data[f"{float_color}_attributes"]
        float_attrs[COLOR]  = float_color
        non_float_attrs[COLOR] = non_float_color
        # Store pre-float motion type
        pictograph_data[f"{float_color}_attributes"][PREFLOAT_MOTION_TYPE] = (
            non_float_attrs[MOTION_TYPE]
        )
        self.prefloat_updater.update_json_prefloat_motion_type(
            json_index, float_color, non_float_attrs[MOTION_TYPE]
        )

        # Store pre-float prop rotation direction
        prop_rot_dir = self._get_prop_rot_dir(
            json_index, float_attrs, non_float_attrs, pictograph_data
        )
        if pictograph_data.get("direction") == OPP:
            prop_rot_dir = self._get_opposite_rotation_direction(prop_rot_dir)

        pictograph_data[f"{float_color}_attributes"][
            PREFLOAT_PROP_ROT_DIR
        ] = prop_rot_dir
        self.prefloat_updater.update_prefloat_prop_rot_dir_in_json(
            json_index, float_color, prop_rot_dir
        )

    def _find_matching_letter(
        self, float_attrs: dict, shift_attrs: dict
    ) -> Optional[Letter]:
        """Find matching letter with pre-float aware comparison."""
        for letter, examples in self.letters.items():
            for example in examples:
                if self.comparator.compare_dual_motion_with_prefloat(
                    float_attrs, shift_attrs, example
                ):
                    return letter
        return None

    def _update_motion_attributes(
        self, motion: "Motion", new_motion_type: str, other_motion: "Motion"
    ) -> None:
        """Update the attributes of the other motion."""
        motion.state.prefloat_motion_type = new_motion_type
        if motion.state.motion_type == FLOAT:
            json_index = self._get_json_index_for_current_beat()
            self._update_json_with_prefloat_attributes(
                json_index, motion, new_motion_type
            )
            motion.state.prefloat_prop_rot_dir = self._get_prop_rot_dir(
                json_index, other_motion
            )

            self.main_widget.json_manager.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
                json_index,
                motion.state.color,
                motion.state.prefloat_prop_rot_dir,
            )

    def _update_json_with_prefloat_attributes(
        self, json_index: int, other_motion: "Motion", motion_type: str
    ) -> None:
        """Update JSON with pre-float motion type and rotation direction."""
        self.main_widget.json_manager.updater.motion_type_updater.update_json_prefloat_motion_type(
            json_index,
            other_motion.state.color,
            motion_type,
        )

    def _get_json_index_for_current_beat(self) -> int:
        """Calculate the JSON index for the currently selected beat."""
        return (
            self.main_widget.sequence_workbench.beat_frame.get.index_of_currently_selected_beat()
            + 2
        )

    def _get_opposite_rotation_direction(self, rotation_direction: str) -> str:
        """Return the opposite prop rotation direction."""
        return COUNTER_CLOCKWISE if rotation_direction == CLOCKWISE else CLOCKWISE

    def _get_prop_rot_dir(
        self, json_index: int, float_attrs, non_float_attrs, pictograph_data
    ) -> str:
        """Retrieve the prop rotation direction from JSON."""
        if non_float_attrs[COLOR] == RED:
            float_color = BLUE
        else:
            float_color = RED
        prop_rot_dir = self.main_widget.json_manager.loader_saver.get_json_prop_rot_dir(
            json_index,
            float_color,
        )
        if pictograph_data[DIRECTION] == OPP:
            prop_rot_dir = self._get_opposite_rotation_direction(prop_rot_dir)
        elif non_float_attrs[MOTION_TYPE] in [PRO, ANTI]:
            prop_rot_dir = (
                self.main_widget.json_manager.loader_saver.get_json_prop_rot_dir(
                    json_index,
                    non_float_attrs[COLOR],
                )
            )
            if pictograph_data[DIRECTION] == OPP:
                prop_rot_dir = self._get_opposite_rotation_direction(prop_rot_dir)

        return prop_rot_dir
