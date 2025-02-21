import json
import codecs
from typing import TYPE_CHECKING, Dict, Any

from Enums.letters import LetterConditions
from data.constants import (
    ANTI,
    BOX,
    DIAMOND,
    FLOAT,
    NONRADIAL,
    CLOCK,
    COUNTER,
    DASH,
    IN,
    OUT,
    PRO,
    RADIAL,
    STATIC,
)
from objects.arrow.arrow import Arrow
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:  # Replace with: if TYPE_CHECKING:
    from .arrow_placement_manager import ArrowPlacementManager


class DefaultArrowPositioner:
    """
    A refactored version that loads BOTH diamond and box defaults up front,
    preserves the exact `_get_adjustment_key` logic, and gracefully handles
    pictographs that may lack `grid_mode`.
    """

    def __init__(self, placement_manager: "ArrowPlacementManager"):
        self.placement_manager = placement_manager
        self.pictograph = placement_manager.pictograph

        self.all_defaults: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = {
            "diamond": {},
            "box": {},
        }

        self.diamond_placements_files = {
            PRO: "default_diamond_pro_placements.json",
            ANTI: "default_diamond_anti_placements.json",
            FLOAT: "default_diamond_float_placements.json",
            DASH: "default_diamond_dash_placements.json",
            STATIC: "default_diamond_static_placements.json",
        }
        self.box_placement_files = {
            PRO: "default_box_pro_placements.json",
            ANTI: "default_box_anti_placements.json",
            FLOAT: "default_box_float_placements.json",
            DASH: "default_box_dash_placements.json",
            STATIC: "default_box_static_placements.json",
        }

        # Load everything for diamond/box so we can handle any pictograph
        self._load_all_default_placements()

    def _load_all_default_placements(self) -> None:
        """
        Load diamond AND box data for each motion type, so we never rely on
        'pictograph.state.grid_mode' at init (avoiding 'Beat' object has no attribute grid_mode').
        """
        motion_types = [PRO, ANTI, FLOAT, DASH, STATIC]

        for motion_type in motion_types:
            # Load diamond JSON
            diamond_file = self.diamond_placements_files[motion_type]
            diamond_path = get_images_and_data_path(
                f"data/arrow_placement/diamond/default/{diamond_file}"
            )
            diamond_data = self._load_json(diamond_path)

            # Load box JSON
            box_file = self.box_placement_files[motion_type]
            box_path = get_images_and_data_path(
                f"data/arrow_placement/box/default/{box_file}"
            )
            box_data = self._load_json(box_path)

            # Store them
            self.all_defaults["diamond"][motion_type] = diamond_data
            self.all_defaults["box"][motion_type] = box_data

    def _load_json(self, path: str) -> dict:
        """
        Safely load a JSON file. Returns an empty dict on error.
        """
        try:
            with codecs.open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading default placements from {path}: {e}")
            return {}

    # ------------------------------------------------------------------------
    #         *** EXACT `_get_adjustment_key` LOGIC FROM YOUR ORIGINAL CODE ***
    # ------------------------------------------------------------------------
    def _get_adjustment_key(self, arrow: Arrow, default_placements: dict) -> str:
        """
        Identical logic to your original code. This method is unmodified
        except for removing the forced `_load_all_default_placements` call
        (we already do that at init).
        """
        # Not reloading anything here, to avoid infinite recursion
        # self._load_all_default_placements()  # removed

        has_beta_props = arrow.pictograph.managers.check.ends_with_beta()
        has_alpha_props = arrow.pictograph.managers.check.ends_with_alpha()
        has_gamma_props = arrow.pictograph.managers.check.ends_with_gamma()
        has_hybrid_orientation = arrow.pictograph.managers.check.ends_with_layer3()
        has_radial_props = arrow.pictograph.managers.check.ends_with_radial_ori()
        has_nonradial_props = arrow.pictograph.managers.check.ends_with_nonradial_ori()
        motion_end_ori = arrow.motion.end_ori

        key_suffix = "_to_"
        motion_end_ori_key = ""
        if has_hybrid_orientation:
            if motion_end_ori in [IN, OUT]:
                motion_end_ori_key = f"{RADIAL}_"
            elif motion_end_ori in [CLOCK, COUNTER]:
                motion_end_ori_key = f"{NONRADIAL}_"

        letter_suffix = ""
        if (
            arrow.pictograph.state.letter.value
            and (
                arrow.pictograph.state.letter
                in arrow.pictograph.state.letter.get_letters_by_condition(
                    LetterConditions.TYPE3
                )
            )
            or (
                arrow.pictograph.state.letter
                in arrow.pictograph.state.letter.get_letters_by_condition(
                    LetterConditions.TYPE5
                )
            )
        ):
            char = arrow.pictograph.state.letter.value[:-1]
            letter_suffix = f"_{char}_dash"
        elif arrow.pictograph.state.letter:
            letter_suffix = f"_{arrow.pictograph.state.letter.value}"

        if has_radial_props:
            key_middle = "layer1"
        elif has_nonradial_props:
            key_middle = "layer2"
        elif has_hybrid_orientation:
            key_middle = "layer3"
        else:
            key_middle = ""

        if has_alpha_props:
            key_middle += "_alpha"
        elif has_beta_props:
            key_middle += "_beta"
        elif has_gamma_props:
            key_middle += "_gamma"

        # Build the final keys
        key = arrow.motion.motion_type + (
            key_suffix + motion_end_ori_key + key_middle if key_middle else ""
        )
        key_with_letter = f"{key}{letter_suffix}"

        # Check in the default_placements dictionary
        if key_with_letter in default_placements:
            return key_with_letter
        elif key in default_placements:
            return key
        else:
            return arrow.motion.motion_type

    def get_default_adjustment(self, arrow: Arrow) -> tuple[int, int]:
        """
        Use the arrow's motion_type and pictograph's grid_mode (fallback to 'diamond')
        to find the correct dictionary in self.all_defaults. Then build the exact same
        key via _get_adjustment_key, and look up offset data for arrow.motion.turns.
        """
        # 1) Figure out motion type
        motion_type = arrow.motion.motion_type

        # 2) Fallback to 'diamond' if no grid_mode or attribute
        grid_mode = getattr(arrow.pictograph, "grid_mode", DIAMOND)
        if grid_mode not in ["diamond", "box"]:
            grid_mode = DIAMOND

        # 3) Retrieve data from the loaded defaults
        if (
            grid_mode in self.all_defaults
            and motion_type in self.all_defaults[grid_mode]
        ):
            default_placements = self.all_defaults[grid_mode][motion_type]
        else:
            default_placements = {}

        # 4) Build the EXACT same key using original method
        adjustment_key = self._get_adjustment_key(arrow, default_placements)

        # 5) Look up "turns" sub-dictionary
        if (
            adjustment_key in default_placements
            and str(arrow.motion.turns) in default_placements[adjustment_key]
        ):
            return default_placements[adjustment_key][str(arrow.motion.turns)]
        else:
            # Fallback: no match for key or turns => (0, 0)
            return default_placements.get(motion_type, {}).get(
                str(arrow.motion.turns),
                (0, 0),
            )
