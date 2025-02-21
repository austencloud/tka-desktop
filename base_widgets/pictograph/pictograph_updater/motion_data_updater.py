import logging
from functools import lru_cache
from typing import TYPE_CHECKING

from Enums.letters import Letter
from data.constants import RED, BLUE
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from ..pictograph_scene import PictographScene

logger = logging.getLogger(__name__)


class MotionDataUpdater:
    def __init__(self, pictograph: "PictographScene") -> None:
        """
        The 'getter' dependency is injected for accessing related motion data
        (instead of referencing self.pictograph.managers.get directly).
        """
        self.pictograph = pictograph
        self.getter = pictograph.managers.get

    def update(self, data: dict) -> None:
        """
        Updates motion objects based on the provided data.
        """
        try:
            motion_dataset = self._extract_motion_dataset(data)
        except Exception as e:
            logger.error(f"Failed to extract motion dataset: {e}", exc_info=True)
            return

        for motion in self.pictograph.elements.motions.values():
            try:
                self._override_motion_type_if_needed(data, motion)
                if motion_dataset.get(motion.color):
                    self._show_motion_graphics(motion.color)
                if motion_dataset[motion.color].get("turns", "") == "fl":
                    motion.turns = "fl"
                motion.updater.update_motion(motion_dataset[motion.color])
                turns_value = motion_dataset[motion.color].get("turns")
                if turns_value is not None:
                    motion.turns = turns_value
            except Exception as e:
                logger.error(
                    f"Error updating motion for {motion.color}: {e}", exc_info=True
                )

        for motion in self.pictograph.elements.motions.values():
            try:
                if motion.pictograph.state.letter in [
                    Letter.S,
                    Letter.T,
                    Letter.U,
                    Letter.V,
                ]:
                    motion.attr_manager.assign_lead_states()
            except Exception as e:
                logger.error(
                    f"Error assigning lead state for {motion.color}: {e}", exc_info=True
                )

    def _override_motion_type_if_needed(self, data: dict, motion: Motion) -> None:
        motion_type = motion.motion_type
        turns_key = f"{motion_type}_turns"
        if turns_key in data:
            motion.turns = data[turns_key]
            logger.debug(
                f"Overriding motion type for {motion.color} using key {turns_key}."
            )

    def _show_motion_graphics(self, color: str) -> None:
        try:
            self.pictograph.elements.props[color].show()
            self.pictograph.elements.arrows[color].show()
        except Exception as e:
            logger.warning(f"Could not show graphics for {color} motion: {e}")

    def _extract_motion_dataset(self, data: dict) -> dict:
        hashable_dict = self._dict_to_tuple(data)
        return self._get_motion_dataset_from_tuple(hashable_dict)

    @lru_cache(maxsize=None)
    def _get_motion_dataset_from_tuple(self, hashable_dict: tuple) -> dict:
        data = self._tuple_to_dict(hashable_dict)
        motion_attributes = [
            "motion_type",
            "start_loc",
            "end_loc",
            "turns",
            "start_ori",
            "prop_rot_dir",
        ]
        motion_dataset = {}
        for color in [RED, BLUE]:
            motion_data = data.get(f"{color}_attributes", {})
            dataset_for_color = {
                attr: motion_data.get(attr)
                for attr in motion_attributes
                if attr in motion_data
            }
            prefloat_motion = motion_data.get("prefloat_motion_type")
            dataset_for_color["prefloat_motion_type"] = (
                None
                if prefloat_motion == "float"
                else motion_data.get(
                    "prefloat_motion_type", dataset_for_color.get("motion_type")
                )
            )
            prefloat_prop_rot = motion_data.get("prefloat_prop_rot_dir")
            dataset_for_color["prefloat_prop_rot_dir"] = (
                None
                if prefloat_prop_rot == "no_rot"
                else motion_data.get(
                    "prefloat_prop_rot_dir", dataset_for_color.get("prop_rot_dir")
                )
            )
            motion_dataset[color] = dataset_for_color
        return motion_dataset

    def _dict_to_tuple(self, d: dict) -> tuple:
        return tuple(
            (k, self._dict_to_tuple(v) if isinstance(v, dict) else v)
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
