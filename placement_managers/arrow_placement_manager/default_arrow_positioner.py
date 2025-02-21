import json
import codecs
from typing import TYPE_CHECKING, Any

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


if TYPE_CHECKING:
    from .arrow_placement_manager import ArrowPlacementManager


class DefaultArrowPositioner:
    def __init__(self, placement_manager: "ArrowPlacementManager"):
        self.placement_manager = placement_manager
        self.pictograph = placement_manager.pictograph
        self.all_defaults: dict[str, dict[str, dict[str, Any]]] = {
            "diamond": {},
            "box": {},
        }
        self.diamond_placements_files: dict[str, str] = {
            PRO: "default_diamond_pro_placements.json",
            ANTI: "default_diamond_anti_placements.json",
            FLOAT: "default_diamond_float_placements.json",
            DASH: "default_diamond_dash_placements.json",
            STATIC: "default_diamond_static_placements.json",
        }
        self.box_placement_files: dict[str, str] = {
            PRO: "default_box_pro_placements.json",
            ANTI: "default_box_anti_placements.json",
            FLOAT: "default_box_float_placements.json",
            DASH: "default_box_dash_placements.json",
            STATIC: "default_box_static_placements.json",
        }
        self._load_all_default_placements()

    def _load_all_default_placements(self) -> None:
        motion_types = [PRO, ANTI, FLOAT, DASH, STATIC]
        for motion_type in motion_types:
            self._load_placements(motion_type, DIAMOND)
            self._load_placements(motion_type, BOX)

    def _load_placements(self, motion_type: str, grid_mode: str) -> None:
        if grid_mode == DIAMOND:
            filename = self.diamond_placements_files[motion_type]
        elif grid_mode == BOX:
            filename = self.box_placement_files[motion_type]
        else:
            raise ValueError(f"Invalid grid mode: {grid_mode}")

        filepath = get_images_and_data_path(
            f"data/arrow_placement/{grid_mode}/default/{filename}"
        )
        self.all_defaults[grid_mode][motion_type] = self._load_json(filepath)

    def _load_json(self, path: str) -> dict[str, Any]:
        try:
            with codecs.open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading default placements from {path}: {e}")
            return {}

    def _get_adjustment_key(self, arrow: Arrow, default_placements: dict) -> str:
        check_manager = arrow.pictograph.managers.check
        has_beta_props = check_manager.ends_with_beta()
        has_alpha_props = check_manager.ends_with_alpha()
        has_gamma_props = check_manager.ends_with_gamma()
        has_hybrid_orientation = check_manager.ends_with_layer3()
        has_radial_props = check_manager.ends_with_radial_ori()
        has_nonradial_props = check_manager.ends_with_nonradial_ori()
        motion_end_ori = arrow.motion.end_ori

        key_suffix = "_to_"

        motion_end_ori_key = self._get_motion_end_ori_key(
            has_hybrid_orientation, motion_end_ori
        )

        letter_suffix = self._get_letter_suffix(arrow)

        key_middle = self._get_key_middle(
            has_radial_props,
            has_nonradial_props,
            has_hybrid_orientation,
            has_alpha_props,
            has_beta_props,
            has_gamma_props,
        )

        key = arrow.motion.motion_type + (
            key_suffix + motion_end_ori_key + key_middle if key_middle else ""
        )
        key_with_letter = f"{key}{letter_suffix}"

        return self._select_key(
            key_with_letter, key, arrow.motion.motion_type, default_placements
        )

    def _get_motion_end_ori_key(
        self, has_hybrid_orientation: bool, motion_end_ori: str
    ) -> str:
        if has_hybrid_orientation and motion_end_ori in [IN, OUT]:
            return f"{RADIAL}_"
        elif has_hybrid_orientation and motion_end_ori in [CLOCK, COUNTER]:
            return f"{NONRADIAL}_"
        else:
            return ""

    def _get_letter_suffix(self, arrow: Arrow) -> str:
        letter = arrow.pictograph.state.letter
        if not letter:
            return ""

        if letter in letter.get_letters_by_condition(
            LetterConditions.TYPE3
        ) or letter in letter.get_letters_by_condition(LetterConditions.TYPE5):
            return f"_{letter.value[:-1]}_dash"
        else:
            return f"_{letter.value}"

    def _get_key_middle(
        self,
        has_radial_props: bool,
        has_nonradial_props: bool,
        has_hybrid_orientation: bool,
        has_alpha_props: bool,
        has_beta_props: bool,
        has_gamma_props: bool,
    ) -> str:
        if has_radial_props:
            key_middle = "layer1"
        elif has_nonradial_props:
            key_middle = "layer2"
        elif has_hybrid_orientation:
            key_middle = "layer3"
        else:
            return ""

        if has_alpha_props:
            key_middle += "_alpha"
        elif has_beta_props:
            key_middle += "_beta"
        elif has_gamma_props:
            key_middle += "_gamma"
        return key_middle

    def _select_key(
        self, key_with_letter: str, key: str, motion_type: str, default_placements: dict
    ) -> str:
        if key_with_letter in default_placements:
            return key_with_letter
        elif key in default_placements:
            return key
        else:
            return motion_type

    def get_default_adjustment(self, arrow: Arrow) -> tuple[int, int]:
        motion_type = arrow.motion.motion_type
        grid_mode = arrow.pictograph.state.grid_mode
        if grid_mode not in [DIAMOND, BOX]:
            grid_mode = DIAMOND

        default_placements = self.all_defaults.get(grid_mode, {}).get(motion_type, {})
        adjustment_key = self._get_adjustment_key(arrow, default_placements)
        return default_placements.get(adjustment_key, {}).get(
            str(arrow.motion.turns), (0, 0)
        )
