import logging
from functools import lru_cache
from math import pi
from typing import TYPE_CHECKING

from enums.letter.letter import Letter
from data.constants import (
    END_LOC,
    FLOAT,
    LEADING,
    MOTION_TYPE,
    NO_ROT,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PROP_ROT_DIR,
    RED,
    BLUE,
    START_LOC,
    START_ORI,
    TRAILING,
    TURNS,
)
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from ...legacy_pictograph import LegacyPictograph

logger = logging.getLogger(__name__)


class MotionDataUpdater:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph
        self.getter = pictograph.managers.get

    def update_motions(self, pictograph_data: dict) -> None:
        """
        Updates motion objects based on the provided pictograph data.
        """
        if pictograph_data:
            try:
                motion_dataset = self._extract_motion_dataset(pictograph_data)
            except Exception as e:
                logger.error(f"Failed to extract motion dataset: {e}", exc_info=True)
                return
        else:
            motion_dataset = {}

        for motion in self.pictograph.elements.motion_set.values():
            try:
                # Show graphics if we have data for this color
                if motion_dataset.get(motion.state.color):
                    self._show_motion_graphics(motion.state.color)

                # CRITICAL: Handle float turns FIRST - before any other updates
                turns_value = motion_dataset.get(motion.state.color, {}).get(TURNS)
                if turns_value == "fl":
                    # Ensure motion type is set to FLOAT when turns are "fl"
                    motion.state.turns = "fl"
                    motion.state.motion_type = FLOAT
                    motion.state.prop_rot_dir = NO_ROT

                    # Also update the dataset to ensure consistency during update_motion
                    if motion.state.color in motion_dataset:
                        motion_dataset[motion.state.color][MOTION_TYPE] = FLOAT
                        motion_dataset[motion.state.color][PROP_ROT_DIR] = NO_ROT

                # Update the motion with the dataset (which now has consistent motion type)
                if motion_dataset:
                    motion.updater.update_motion(
                        motion_dataset.get(motion.state.color, {})
                    )

                # Initialize arrow if needed
                if not motion.arrow.state.initialized:
                    motion.arrow.setup_components()

                # Set turns value from dataset (should be redundant but just in case)
                if turns_value is not None:
                    motion.state.turns = turns_value
                    # Double-check consistency between turns and motion type
                    if turns_value == "fl" and motion.state.motion_type != FLOAT:
                        motion.state.motion_type = FLOAT
                        motion.state.prop_rot_dir = NO_ROT

            except Exception as e:
                logger.error(
                    f"Error updating motion for {motion.state.color}: {e}",
                    exc_info=True,
                )

        # Handle lead states for specific letters
        for motion in self.pictograph.elements.motion_set.values():
            try:
                if motion.pictograph.state.letter in [
                    Letter.S,
                    Letter.T,
                    Letter.U,
                    Letter.V,
                ]:
                    self.assign_lead_states(motion)
            except Exception as e:
                logger.error(
                    f"Error assigning lead state for {motion.state.color}: {e}",
                    exc_info=True,
                )

    def assign_lead_states(self, motion: "Motion") -> None:
        leading_motion = motion.pictograph.managers.get.leading_motion()
        trailing_motion = motion.pictograph.managers.get.trailing_motion()
        if motion.pictograph.managers.get.leading_motion():
            leading_motion.state.lead_state = LEADING
            trailing_motion.state.lead_state = TRAILING

    def _override_motion_type_if_needed(
        self, pictograph_data: dict, motion: Motion
    ) -> None:
        motion_type = motion.state.motion_type
        turns_key = f"{motion_type}_turns"
        if turns_key in pictograph_data:
            motion.state.turns = pictograph_data[turns_key]
            logger.debug(
                f"Overriding motion type for {motion.state.color} using key {turns_key}."
            )

    def _show_motion_graphics(self, color: str) -> None:
        try:
            self.pictograph.elements.props[color].show()
            self.pictograph.elements.arrows[color].show()
        except Exception as e:
            logger.warning(f"Could not show graphics for {color} motion: {e}")

    def _extract_motion_dataset(self, data: dict) -> dict:
        hashable_tuple = self._dict_to_tuple(data)
        return self._get_motion_dataset_from_tuple(hashable_tuple)

    @lru_cache(maxsize=None)
    def _get_motion_dataset_from_tuple(self, hashable_tuple: tuple) -> dict:
        data = self._tuple_to_dict(hashable_tuple)
        motion_attributes = [
            MOTION_TYPE,
            START_LOC,
            END_LOC,
            TURNS,
            START_ORI,
            PROP_ROT_DIR,
        ]
        motion_dataset = {}
        for color in [RED, BLUE]:
            motion_data = data.get(f"{color}_attributes", {})
            dataset_for_color = {
                attr: motion_data.get(attr)
                for attr in motion_attributes
                if attr in motion_data
            }

            # Handle prefloat motion type
            prefloat_motion = motion_data.get(PREFLOAT_MOTION_TYPE)
            dataset_for_color[PREFLOAT_MOTION_TYPE] = (
                None
                if prefloat_motion == FLOAT
                else motion_data.get(
                    PREFLOAT_MOTION_TYPE, dataset_for_color.get(MOTION_TYPE)
                )
            )

            # Handle prefloat prop rotation direction
            prefloat_prop_rot = motion_data.get(PREFLOAT_PROP_ROT_DIR)
            dataset_for_color[PREFLOAT_PROP_ROT_DIR] = (
                None
                if prefloat_prop_rot == NO_ROT
                else motion_data.get(
                    PREFLOAT_PROP_ROT_DIR, dataset_for_color.get(PROP_ROT_DIR)
                )
            )

            # Ensure motion type is FLOAT if turns is "fl"
            if (
                dataset_for_color.get(TURNS) == "fl"
                and dataset_for_color.get(MOTION_TYPE) != FLOAT
            ):
                dataset_for_color[MOTION_TYPE] = FLOAT
                dataset_for_color[PROP_ROT_DIR] = NO_ROT

            motion_dataset[color] = dataset_for_color
        return motion_dataset

    def _dict_to_tuple(self, d: dict) -> tuple:
        def make_hashable(value):
            if isinstance(value, dict):
                return self._dict_to_tuple(value)
            elif isinstance(value, list):
                return tuple(make_hashable(v) for v in value)  # Convert lists to tuples
            return value

        return tuple(
            (k, make_hashable(v))
            for k, v in sorted(d.items())
            if k != self.pictograph.state.letter.value
        )

    def _tuple_to_dict(self, t: tuple) -> dict:
        return {
            k: self._tuple_to_dict(v) if isinstance(v, tuple) else v
            for k, v in t
            if k != self.pictograph.state.letter.value
        }

    def clear_cache(self) -> None:
        """
        Clears the LRU cache for the motion dataset extraction.
        """
        self._get_motion_dataset_from_tuple.cache_clear()
