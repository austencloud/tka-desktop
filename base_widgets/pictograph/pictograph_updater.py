from typing import TYPE_CHECKING
from Enums.Enums import LetterType
from Enums.letters import Letter
from data.constants import LEADING, TRAILING, RED, BLUE
from main_window.main_widget.grid_mode_checker import GridModeChecker
from objects.motion.motion import Motion
from functools import lru_cache

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene


class PictographUpdater:
    def __init__(self, pictograph: "PictographScene") -> None:
        self.pictograph = pictograph

    def update_pictograph(self, pictograph_data: dict = None) -> None:
        """
        Updates the pictograph with the given pictograph_data.
        If the dict is complete, it will be assigned to the pictograph's pictograph_data attribute.
        If the dict is incomplete, it will be used to update the pictograph's attributes.
        If there is no dict, the pictograph will update its children without reference to a dict.
        """
        if not self.pictograph.get.is_initialized:
            self.pictograph.get.initiallize_getter()

        if pictograph_data:
            if pictograph_data.get("is_placeholder", False):
                return

            if self.pictograph.check.is_pictograph_data_complete(pictograph_data):
                self.pictograph.pictograph_data = pictograph_data
                self.pictograph.grid_mode = GridModeChecker.get_grid_mode(
                    self.pictograph.pictograph_data
                )
                self.pictograph.grid.update_grid_mode()

                self._update_from_pictograph_data(pictograph_data)
                self.pictograph.turns_tuple = self.pictograph.get.turns_tuple()
                self.pictograph.vtg_glyph.set_vtg_mode()
                self.pictograph.elemental_glyph.set_elemental_glyph()
                self.pictograph.start_to_end_pos_glyph.set_start_to_end_pos_glyph()
            else:
                self._update_from_pictograph_data(pictograph_data)
                self.pictograph.turns_tuple = self.pictograph.get.turns_tuple()

        self.pictograph.tka_glyph.update_tka_glyph()
        self.pictograph.elemental_glyph.update_elemental_glyph()
        self.pictograph.reversal_glyph.update_reversal_symbols()

        self._position_objects()

    def get_end_pos(self) -> str:
        return self.pictograph.end_pos[:-1]

    def _update_from_pictograph_data(self, pictograph_data: dict) -> None:
        self.pictograph.attr_manager.update_data(pictograph_data)
        motion_dataset = self._get_motion_dataset(pictograph_data)
        self.pictograph.letter_type = LetterType.get_letter_type(self.pictograph.letter)
        red_arrow_data, blue_arrow_data = self.get_arrow_dataset(pictograph_data)
        self._update_motions(pictograph_data, motion_dataset)
        self._update_arrows(red_arrow_data, blue_arrow_data)
        self._set_lead_states()

    def _update_motions(
        self, pictograph_data: dict, motion_dataset: dict[str, dict]
    ) -> None:
        for motion in self.pictograph.motions.values():
            self.override_motion_type_if_necessary(pictograph_data, motion)
            if motion_dataset.get(motion.color) is not None:
                self.show_graphical_objects(motion.color)
            if motion_dataset[motion.color].get("turns", "") == "fl":
                motion.turns = "fl"
            motion.updater.update_motion(motion_dataset[motion.color])
            turns_value = motion_dataset[motion.color].get("turns", None)
            if turns_value is not None:
                motion.turns = turns_value
        for motion in self.pictograph.motions.values():
            if motion.pictograph.letter in [
                Letter.S,
                Letter.T,
                Letter.U,
                Letter.V,
            ]:
                motion.attr_manager.assign_lead_states()

    def _set_lead_states(self):
        if self.pictograph.letter.value in ["S", "T", "U", "V"]:
            self.pictograph.get.leading_motion().lead_state = LEADING
            self.pictograph.get.trailing_motion().lead_state = TRAILING
        else:
            for motion in self.pictograph.motions.values():
                motion.lead_state = None

    def _update_arrows(self, red_arrow_data, blue_arrow_data):
        if self.pictograph.letter_type == LetterType.Type3:
            self.pictograph.get.shift().arrow.updater.update_arrow()
            self.pictograph.get.dash().arrow.updater.update_arrow()
        else:
            self.pictograph.arrows.get(RED).updater.update_arrow(red_arrow_data)
            self.pictograph.arrows.get(BLUE).updater.update_arrow(blue_arrow_data)

    def get_arrow_dataset(self, pictograph_data):
        if pictograph_data.get("red_attributes") and not pictograph_data.get(
            "blue_attributes"
        ):
            red_arrow_data = self.get_arrow_data_from_pictograph_data(
                pictograph_data, RED
            )
            blue_arrow_data = None
        elif pictograph_data.get("blue_attributes") and not pictograph_data.get(
            "red_attributes"
        ):
            blue_arrow_data = self.get_arrow_data_from_pictograph_data(
                pictograph_data, BLUE
            )
            red_arrow_data = None
        elif pictograph_data.get("red_attributes") and pictograph_data.get(
            "blue_attributes"
        ):
            red_arrow_data = self.get_arrow_data_from_pictograph_data(
                pictograph_data, RED
            )
            blue_arrow_data = self.get_arrow_data_from_pictograph_data(
                pictograph_data, BLUE
            )
        return red_arrow_data, blue_arrow_data

    def get_arrow_data_from_pictograph_data(
        self, pictograph_data: dict, color: str
    ) -> dict:
        turns = pictograph_data[f"{color}_attributes"].get("turns", None)
        prop_rot_dir = pictograph_data[f"{color}_attributes"].get("prop_rot_dir", None)
        loc = pictograph_data[f"{color}_attributes"].get("loc", None)

        if turns or turns == 0:
            arrow_data = {"turns": turns}
        elif prop_rot_dir:
            arrow_data = {"prop_rot_dir": prop_rot_dir}
        else:
            arrow_data = None
        if loc:
            arrow_data["loc"] = loc
        return arrow_data

    def show_graphical_objects(self, color: str) -> None:
        self.pictograph.props[color].show()
        self.pictograph.arrows[color].show()

    def override_motion_type_if_necessary(
        self, pictograph_data: dict, motion: Motion
    ) -> None:
        motion_type = motion.motion_type
        turns_key = f"{motion_type}_turns"
        if turns_key in pictograph_data:
            motion.turns = pictograph_data[turns_key]

    def _get_motion_dataset(self, pictograph_data: dict) -> dict:
        # Convert the dict to a hashable type (tuple of tuples)
        hashable_dict = self._dict_to_tuple(pictograph_data)
        return self._get_motion_dataset_from_pictograph_data(hashable_dict)

    @lru_cache(maxsize=None)
    def _get_motion_dataset_from_pictograph_data(self, hashable_dict: tuple) -> dict:
        # Convert the hashable dict back to a normal dict
        pictograph_data = self._tuple_to_dict(hashable_dict)

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
            motion_data: dict = pictograph_data.get(f"{color}_attributes", {})
            motion_dataset[color] = {
                attr: motion_data.get(attr)
                for attr in motion_attributes
                if attr in motion_data
            }

            # Ensure prefloat_motion_type is not "float"
            prefloat_motion_type = motion_data.get("prefloat_motion_type")
            if prefloat_motion_type == "float":
                prefloat_motion_type = None  # Prevent it from being set to "float"

            if prefloat_motion_type:
                motion_dataset[color]["prefloat_motion_type"] = prefloat_motion_type
            else:
                motion_dataset[color]["prefloat_motion_type"] = motion_dataset[
                    color
                ].get("motion_type")

            # Ensure prefloat_prop_rot_dir is not "no_rot"
            prefloat_prop_rot_dir = motion_data.get("prefloat_prop_rot_dir")
            if prefloat_prop_rot_dir == "no_rot":
                prefloat_prop_rot_dir = None  # Prevent it from being set to "no_rot"

            if prefloat_prop_rot_dir:
                motion_dataset[color]["prefloat_prop_rot_dir"] = prefloat_prop_rot_dir
            else:
                motion_dataset[color]["prefloat_prop_rot_dir"] = motion_dataset[
                    color
                ].get("prop_rot_dir")

        return motion_dataset

    def _dict_to_tuple(self, d: dict) -> tuple:  # Changed parameter name from dict->d
        """Recursively convert a dictionary to a hashable tuple of tuples, handling circular references."""
        return tuple(
            (
                k,
                self._dict_to_tuple(v) if isinstance(v, dict) else v,
            )  # Now using actual dict type
            for k, v in sorted(d.items())  # Changed dict->d
            if k != self.pictograph.letter.value
        )

    def _tuple_to_dict(self, t: tuple) -> dict:  # Changed parameter name from tuple->t
        """Recursively convert a hashable tuple of tuples back to a dictionary."""
        return {
            k: self._tuple_to_dict(v) if isinstance(v, tuple) else v
            for k, v in t  # Changed tuple->t
            if k != self.pictograph.letter.value
        }

    def _position_objects(self) -> None:
        self.pictograph.prop_placement_manager.update_prop_positions()
        self.pictograph.arrow_placement_manager.update_arrow_placements()
        self.pictograph.update()  # Add this line

    def update_dict_from_attributes(self) -> dict:
        pictograph_data = self.pictograph.get.pictograph_data()
        self.pictograph.pictograph_data = pictograph_data
        return pictograph_data
